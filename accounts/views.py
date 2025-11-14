from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from .models import UserProfile
from blog.models import Post, UserActivity


class RegisterView(View):
    """User registration view"""
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user, role='reader')
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('accounts:login')
        return render(request, 'accounts/register.html', {'form': form})


class LoginView(View):
    """User login view"""
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Try to authenticate with username first, then email
            user = authenticate(request, username=username, password=password)
            if not user:
                user = User.objects.filter(email=username).first()
                if user:
                    user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                login(request, user)
                # Record user activity
                UserActivity.objects.create(
                    user=user,
                    activity_type='login',
                    ip_address=self.get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
                
                next_page = request.GET.get('next', 'blog:home')
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username/email or password.')
        
        return render(request, 'accounts/login.html', {'form': form})

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class LogoutView(View):
    """User logout view"""
    def get(self, request):
        if request.user.is_authenticated:
            UserActivity.objects.create(
                user=request.user,
                activity_type='logout',
                ip_address=LoginView.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('blog:home')


@method_decorator(login_required, name='dispatch')
class ProfileDetailView(DetailView):
    """User profile detail view"""
    model = UserProfile
    template_name = 'accounts/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_posts'] = user.blog_posts.all()
        context['user_comments'] = user.comments.all()
        context['user_activity'] = user.activities.all()[:10]
        return context


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    """User profile update view"""
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user.profile

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class AuthorDashboardView(ListView):
    """Dashboard for authors to manage their posts"""
    model = Post
    template_name = 'accounts/dashboard.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if not user.profile.is_author():
            messages.error(self.request, 'You do not have permission to access the dashboard.')
            return Post.objects.none()
        return user.blog_posts.all().prefetch_related('comments', 'tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['stats'] = {
            'total_posts': user.blog_posts.count(),
            'published_posts': user.blog_posts.filter(status='published').count(),
            'draft_posts': user.blog_posts.filter(status='draft').count(),
            'total_comments': user.blog_posts.values_list('comments', flat=True).count(),
            'total_views': sum(post.views_count for post in user.blog_posts.all()),
        }
        return context


@login_required
def request_author_role(request):
    """Request author role upgrade"""
    user_profile = request.user.profile
    
    if user_profile.is_author():
        messages.info(request, 'You already have author privileges!')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        user_profile.author_request_pending = True
        user_profile.save()
        messages.success(request, 'Your author role request has been submitted! An admin will review it soon.')
        return redirect('blog:home')
    
    context = {'user_profile': user_profile}
    return render(request, 'accounts/request_author.html', context)


@login_required
def request_status(request):
    """Check status of author role request"""
    user_profile = request.user.profile
    
    if user_profile.is_author():
        context = {'status': 'approved', 'message': 'You are now an author!'}
    elif user_profile.author_request_pending:
        context = {'status': 'pending', 'message': 'Your author role request is pending admin approval.'}
    else:
        context = {'status': 'none', 'message': 'You have not requested author privileges yet.'}
    
    return render(request, 'accounts/request_status.html', context)
