from django.urls import path

from articles.views import ArticleListView

app_name = "articles"
urlpatterns = [
    path("", ArticleListView.as_view(), name="article_list"),
]
