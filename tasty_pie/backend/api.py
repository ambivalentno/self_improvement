from tastypie.resources import ModelResource
from backend.models import Article


class ArticleResource(ModelResource):
    class Meta:
        queryset = Article.objects.all()
        resource_name = 'article'