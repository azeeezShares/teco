from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from .models import Post
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
    
class AdminPostEdit(LoginRequiredMixin, generic.View):
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

# View for creating a new post
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
            messages.success(request, 'Post created successfully.')
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})