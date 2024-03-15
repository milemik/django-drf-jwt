from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated

from articles.models import Article


class ArticleListView(generics.ListAPIView):
    class ArticleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = ("id", "title", "body", "published", "created_at", "updated_at")

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticated,)
