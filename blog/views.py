from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from .models import Post
from .forms import PageForm

# Froala Editor
class PageEdit(generic.View):
    template_name = 'blog/editor.html'
    success_url = 'blog_homeview'
    
    def get(self, request, *args, **kwargs):
        post_id = request.GET.get('post_id')  # Get post_id from query params
        if post_id:
            page = get_object_or_404(Post, id=post_id)  # Fetch the page if post_id is provided
            form = PageForm(instance=page)  # Pre-populate the form
        else:
            form = PageForm()  # Create a blank form for a new page
        return render(request, self.template_name, {'form': form, 'post_id': post_id})
    
    def post(self, request, *args, **kwargs):
        post_id = request.GET.get('post_id')  # Check if post_id is provided
        if post_id:
            page = get_object_or_404(Post, id=post_id)  # Fetch the page
            form = PageForm(request.POST, instance=page)  # Bind the form with POST data
        else:
            form = PageForm(request.POST)  # Create a new form instance for a new page
        
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form, 'post_id': post_id})


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/list.html'

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog/post.html'

    def get(self, request, slug, *args, **kwargs):  # Add slug as a parameter
        post = get_object_or_404(Post, slug=slug, status=1)  # Fetch by slug;status 0 means draft, 1 means published;
        return render(request, self.template_name, {'post': post})