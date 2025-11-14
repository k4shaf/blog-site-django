from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit, Button
from .models import Post, Comment, Category, Tag


class PostForm(forms.ModelForm):
    """Form for creating and editing blog posts"""
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text="Select one or more tags"
    )

    class Meta:
        model = Post
        fields = ('title', 'slug', 'excerpt', 'content', 'category', 'tags', 
                  'featured_image', 'status')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Leave empty to auto-generate'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Brief summary of your post'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Write your post content here'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                'Create/Edit Post',
                'title',
                'slug',
                'excerpt',
                'content',
                Row(
                    Column('category', css_class='form-group col-md-6 mb-0'),
                    Column('status', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                'featured_image',
                'tags',
            ),
            Row(
                Column(Submit('submit', 'Save Post', css_class='btn btn-primary'), 
                       css_class='form-group col-md-6'),
                Column(Button('cancel', 'Cancel', css_class='btn btn-secondary',
                             onclick="window.history.back()"),
                       css_class='form-group col-md-6'),
                css_class='form-row mt-3'
            )
        )

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 3:
            raise forms.ValidationError('Title must be at least 3 characters long.')
        return title


class CommentForm(forms.ModelForm):
    """Form for posting comments on blog posts"""
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Share your thoughts...',
                'required': True
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Add a Comment',
                'content',
            ),
            Submit('submit', 'Post Comment', css_class='btn btn-primary mt-2')
        )


class SearchForm(forms.Form):
    """Form for searching blog posts"""
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search posts by title or content...'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='All Categories',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    tag = forms.ModelChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        empty_label='All Tags',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class = 'form-inline'
        self.helper.layout = Layout(
            Row(
                Column('query', css_class='form-group col-md-4 mb-2'),
                Column('category', css_class='form-group col-md-4 mb-2'),
                Column('tag', css_class='form-group col-md-3 mb-2'),
                Column(Submit('search', 'Search', css_class='btn btn-primary mb-2'),
                       css_class='form-group col-md-1 mb-2'),
                css_class='form-row'
            )
        )


class CategoryForm(forms.ModelForm):
    """Form for creating/editing categories"""
    class Meta:
        model = Category
        fields = ('name', 'slug', 'description')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Category name'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Leave empty to auto-generate'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Category description'
            }),
        }


class TagForm(forms.ModelForm):
    """Form for creating/editing tags"""
    class Meta:
        model = Tag
        fields = ('name', 'slug')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tag name'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Leave empty to auto-generate'
            }),
        }
