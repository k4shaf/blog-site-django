from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import Http404
from .models import Post, Category, Tag, Comment, UserActivity
from .forms import PostForm, CommentForm, SearchForm
from accounts.models import UserProfile


class HomeView(ListView):
    """Home page with list of published posts"""
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(status='published').prefetch_related('author', 'category', 'tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['popular_tags'] = Tag.objects.annotate(
            count=Count('posts')
        ).order_by('-count')[:10]
        context['popular_posts'] = Post.objects.filter(
            status='published'
        ).order_by('-views_count')[:5]
        return context


class PostDetailView(DetailView):
    """Detailed view of a single post"""
    model = Post
    template_name = 'blog/post_detail.html'
    slug_field = 'slug'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.prefetch_related('comments', 'tags', 'author')

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        post = self.get_object()
        
        # Check if user is authorized to view draft posts
        if post.status == 'draft':
            if not request.user.is_authenticated or (request.user != post.author and not request.user.is_staff):
                raise Http404("This post is not published.")
        
        # Increment view count and record activity
        post.increment_views()
        if request.user.is_authenticated:
            UserActivity.objects.create(
                user=request.user,
                activity_type='view_post',
                post=post,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
        
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # Get approved comments
        context['comments'] = post.comments.filter(status='approved')
        
        # Initialize comment form
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
        
        # Get related posts (same category)
        context['related_posts'] = Post.objects.filter(
            status='published',
            category=post.category
        ).exclude(pk=post.pk)[:3]
        
        return context

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class PostSearchView(ListView):
    """Search and filter posts"""
    model = Post
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(status='published')
        
        query = self.request.GET.get('query', '')
        category_id = self.request.GET.get('category', '')
        tag_id = self.request.GET.get('tag', '')
        
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(excerpt__icontains=query)
            )
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)
        
        return queryset.prefetch_related('author', 'category', 'tags').distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(self.request.GET)
        context['query'] = self.request.GET.get('query', '')
        return context


class CategoryPostsView(ListView):
    """Posts filtered by category"""
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(
            category=self.category,
            status='published'
        ).prefetch_related('author', 'tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class TagPostsView(ListView):
    """Posts filtered by tag"""
    model = Post
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return self.tag.posts.filter(status='published').prefetch_related('author', 'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    """Create a new blog post"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        form.save_m2m()  # Save many-to-many relationships
        
        # Record user activity
        UserActivity.objects.create(
            user=self.request.user,
            activity_type='create_post',
            post=post
        )
        
        messages.success(self.request, 'Post created successfully!')
        return redirect(post.get_absolute_url())

    def dispatch(self, request, *args, **kwargs):
        # Check if user has author role
        if not request.user.profile.is_author():
            if request.user.profile.author_request_pending:
                messages.warning(request, 'Your author role request is pending. An admin will review it soon!')
            else:
                messages.error(request, 'You need author privileges to create posts.')
            return redirect('accounts:request_author')
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    """Update an existing blog post"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    slug_field = 'slug'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def form_valid(self, form):
        post = form.save()
        
        # Record user activity
        UserActivity.objects.create(
            user=self.request.user,
            activity_type='edit_post',
            post=post
        )
        
        messages.success(self.request, 'Post updated successfully!')
        return redirect(post.get_absolute_url())

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user and not request.user.is_staff:
            messages.error(request, 'You can only edit your own posts.')
            return redirect('blog:home')
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class PostDeleteView(DeleteView):
    """Delete a blog post"""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('accounts:dashboard')
    slug_field = 'slug'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        
        # Record user activity
        UserActivity.objects.create(
            user=request.user,
            activity_type='delete_post',
            post=post
        )
        
        messages.success(request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user and not request.user.is_staff:
            messages.error(request, 'You can only delete your own posts.')
            return redirect('blog:home')
        return super().dispatch(request, *args, **kwargs)


@login_required
def add_comment(request, slug):
    """Add a comment to a post"""
    post = get_object_or_404(Post, slug=slug, status='published')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            
            # Record user activity
            UserActivity.objects.create(
                user=request.user,
                activity_type='comment_post',
                post=post
            )
            
            messages.success(request, 'Your comment has been submitted for moderation.')
            return redirect(post.get_absolute_url())
    
    return redirect(post.get_absolute_url())


@login_required
def approve_comment(request, comment_id):
    """Approve a comment (moderator only)"""
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if user is the post author or staff
    if comment.post.author != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to moderate comments.')
        return redirect('blog:home')
    
    comment.status = 'approved'
    comment.save()
    messages.success(request, 'Comment approved!')
    return redirect(comment.post.get_absolute_url())


@login_required
def reject_comment(request, comment_id):
    """Reject a comment (moderator only)"""
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if user is the post author or staff
    if comment.post.author != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to moderate comments.')
        return redirect('blog:home')
    
    comment.status = 'rejected'
    comment.save()
    messages.success(request, 'Comment rejected!')
    return redirect(comment.post.get_absolute_url())


@login_required
def delete_comment(request, comment_id):
    """Delete a comment (author or moderator only)"""
    comment = get_object_or_404(Comment, id=comment_id)
    post = comment.post
    
    # Check permissions
    if comment.user != request.user and post.author != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this comment.')
        return redirect(post.get_absolute_url())
    
    comment.delete()
    messages.success(request, 'Comment deleted!')
    return redirect(post.get_absolute_url())
