from django.views.generic import ListView

from .models import Article


class ArticlesListView(ListView):
    queryset = (
        Article.objects
        .select_related(
            "author",
            "category",
        )
        .prefetch_related(
            "tags",
        )
        .defer(
            "content",
        )
    )