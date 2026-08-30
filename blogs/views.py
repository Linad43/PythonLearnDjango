from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView

from blogs.models import Blog


# Create your views here.

class BlogsListView(ListView):
    model = Blog
    template_name = 'blogs.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        return Blog.objects.filter(is_published=True)


class BlogDetailsView(DetailView):
    model = Blog
    template_name = 'blog_details.html'
    context_object_name = 'blog'
    pk_url_kwarg = 'id_blog'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.increase_views()
        return obj


class BlogUpdateView(UpdateView):
    model = Blog
    template_name = 'blog_form.html'
    fields = ['title', 'content', "image", "is_published"]

    def get_success_url(self) -> str:
        return reverse("blogs:blog_details",
                       kwargs={'id_blog': self.object.id})
