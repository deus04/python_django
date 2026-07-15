from django.urls import path

from .views import ArticlesListView

app_name = "blogapp"

urlpatterns = [
    path("articles/", ArticlesListView.as_view(), name="article-list"),

]