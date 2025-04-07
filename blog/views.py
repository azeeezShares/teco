from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from .models import Post, Tag
from .forms import PageForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/list.html'

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get(self, request, slug, *args, **kwargs):  # Add slug as a parameter
        post = get_object_or_404(Post, slug=slug, status=1)  # Fetch by slug;status 0 means draft, 1 means published;
        return render(request, self.template_name, {'post': post})

class TagList(generic.ListView):
    model = Post
    template_name = 'blog/tag_list.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        tag = self.kwargs['tag']
        return Post.objects.filter(tag__name=tag, status=1).order_by('-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs['tag']
        return context
    

# pages for admin
class AdminPostList(LoginRequiredMixin, generic.ListView):
    queryset = Post.objects.all().order_by('-created_on')
    context_object_name = 'posts'
    paginate_by = 10
    template_name = 'admin-temp/blog.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Post.objects.all()
        return context
    
class AdminPostCreate(LoginRequiredMixin, generic.View):
    template_name = 'admin-temp/post_create.html'
    success_url = 'admin_blogview'

    def get(self, request, *args, **kwargs):
        form = PageForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = PageForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # Don't save to the database yet
            post.author = request.user  # Set the author to the currently logged-in user
            post.save()  # Save the post to the database
            form.save_m2m()  # Save many-to-many relationships, including tags
            messages.success(request, 'Post created successfully.')
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})
class AdminPostEdit(LoginRequiredMixin, generic.View):
    """
    A view for handling the creation and editing of blog posts in the admin panel.
    Attributes:
        template_name (str): The template to render for the post edit page.
        success_url (str): The URL to redirect to upon successful form submission.
    Methods:
        get(request, *args, **kwargs):
            Handles GET requests. Renders the post edit form, pre-populated if a post_id is provided.
            Args:
                request (HttpRequest): The HTTP request object.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments.
            Returns:
                HttpResponse: The rendered template with the form and post_id context.
        post(request, *args, **kwargs):
            Handles POST requests. Processes the submitted form data to create or update a post.
            Args:
                request (HttpRequest): The HTTP request object.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments.
            Returns:
                HttpResponseRedirect: Redirects to the success URL if the form is valid.
                HttpResponse: Re-renders the template with the form and post_id context if the form is invalid.
    """
    template_name = 'admin-temp/post_edit.html'
    success_url = 'admin_blogview'
    
    def get(self, request, *args, **kwargs):
        post_id = request.GET.get('post_id')  # Get post_id from query params
        if post_id:
            page = get_object_or_404(Post, id=post_id)  # Fetch the page if post_id is provided
            form = PageForm(instance=page)  # Pre-populate the form
        else:
            form = PageForm()  # Create a blank form for a new page
        return render(request, self.template_name, {'form': form, 'post_id': post_id})

    def post(self, request, *args, **kwargs):
        post_id = request.GET.get('post_id')
        if post_id:
            page = get_object_or_404(Post, id=post_id)
            form = PageForm(request.POST, request.FILES, instance=page)  # Include request.FILES for image upload
        else:
            form = PageForm(request.POST, request.FILES)  # Include request.FILES for image upload
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form, 'post_id': post_id})
    
class AdminPostDelete(LoginRequiredMixin, generic.View):
    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        if post_id:
            post = Post.objects.filter(id=post_id)
            if not post.exists():
                messages.error(request, 'Post not found.')
                return redirect('admin_blogview')
            
            # delete the post if it exists and show success message
            messages.success(request, 'Post deleted successfully.')
            post = post.first().delete()
            return redirect('admin_blogview')
        
        # show error message if post_id is not provided
        messages.error(request, 'Post ID not provided.')
        return redirect('admin_blogview')

# admin create new tag
class AdminTagCreate(LoginRequiredMixin, generic.View):
    """
    A view for creating new tags in the admin panel.

    Attributes:
        template_name (str): The path to the template used for rendering the tag creation form.
        success_url (str): The URL to redirect to upon successful tag creation.

    Methods:
        get(request, *args, **kwargs):
            Handles GET requests and renders the tag creation form.

        post(request, *args, **kwargs):
            Handles POST requests to create a new tag. If the tag name is provided, 
            it creates the tag, displays a success message, and redirects to the 
            success URL. Otherwise, it displays an error message and re-renders 
            the form.
    """
    template_name = 'admin-temp/tag_create.html'
    success_url = 'admin_tag_list'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        tag_name = request.POST.get('tag_name')
        if tag_name:
            tag = Tag.objects.create(name=tag_name)
            messages.success(request, 'Tag created successfully.')
            return redirect(self.success_url)
        messages.error(request, 'Tag name is required.')
        return render(request, self.template_name)

# admin tag list
class AdminTagList(LoginRequiredMixin, generic.ListView):
    """
    AdminTagList is a class-based view that displays a list of tags in the admin interface.

    This view inherits from `LoginRequiredMixin` to ensure that only authenticated users can access it,
    and `generic.ListView` to provide the functionality for listing objects.

    Attributes:
        queryset (QuerySet): A queryset that retrieves all `Tag` objects ordered by their creation date in descending order.
        context_object_name (str): The name of the context variable to use for the list of tags in the template.
        template_name (str): The path to the template used to render the tag list.

    Methods:
        get_context_data(**kwargs):
            Extends the default context data to include all `Tag` objects under the key 'items'.
    """
    queryset = Tag.objects.all().order_by('-created_on')
    context_object_name = 'tags'
    template_name = 'admin-temp/tag_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Tag.objects.all()
        return context

# admin delete tag
class AdminTagDelete(LoginRequiredMixin, generic.View):
    """
    Handles the deletion of a tag in the admin panel.
    This view requires the user to be logged in and processes POST requests
    to delete a tag based on the provided tag ID.
    Methods:
        post(request, *args, **kwargs):
            Handles the POST request to delete a tag. If the tag ID is provided
            and the tag exists, it deletes the tag and displays a success message.
            If the tag ID is missing or the tag does not exist, it displays an
            appropriate error message.
    Attributes:
        None
    Usage:
        - The `tag_id` should be passed in the POST request data.
        - Redirects to 'admin_blogview' after processing the request.
    """
    def post(self, request, *args, **kwargs):
        tag_id = request.POST.get('tag_id')
        if tag_id:
            tag = Tag.objects.filter(id=tag_id)
            if not tag.exists():
                messages.error(request, 'Tag not found.')
                return redirect('admin_blogview')
            
            # delete the tag if it exists and show success message
            messages.success(request, 'Tag deleted successfully.')
            tag = tag.first().delete()
            return redirect('admin_tag_list')
        
        # show error message if tag_id is not provided
        messages.error(request, 'Tag ID not provided.')
        return redirect('admin_tag_list')