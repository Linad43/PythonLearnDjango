from django.urls import path

from blogs.apps import BlogsConfig
from blogs.views import BlogsListView, BlogDetailsView, BlogUpdateView


app_name = BlogsConfig.name


urlpatterns = [
    path("", BlogsListView.as_view(), name="blogs"),
    path("<int:id_blog>/", BlogDetailsView.as_view(), name="blog_details"),
    path("<int:id_blog>/edit/", BlogUpdateView.as_view(), name="blog_update"),
]