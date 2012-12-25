
import json
from tastypie import fields
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.authentication import BasicAuthentication
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.paginator import Paginator
from tastypie.resources import ModelResource

from django.db.models import Q
from django.contrib.auth.models import User
from django.http import HttpResponse

from backend.models import Article, Author, Genre


class GenreResource(ModelResource):

    class Meta:
        queryset = Genre.objects.all()
        resource_name = 'genre'
        filtering = {'title': ALL}
        authorization = Authorization()


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']


class AuthorResource(ModelResource):
    class Meta:
        queryset = Author.objects.all()
        resource_name = 'author'
        fields=['pseudo']
        filtering = {'pseudo': ALL}
        authorization = DjangoAuthorization()
        authentication = BasicAuthentication()

    user = fields.OneToOneField(UserResource, 'user')

    # def dehydrate(self, bundle):
    #     """custom field for all objects"""
    #     obj = self.obj_get(id=bundle.data['id'])
    #     bundle.data['some_field'] = Author.objects.get(id=1).some_fun()
    #     return bundle


class ArticleResource(ModelResource):

    genre = fields.ForeignKey(GenreResource, 'genre')
    authors = fields.ManyToManyField(AuthorResource, 'authors')

    class Meta:
        queryset = Article.objects.all()
        resource_name = 'article'
        authorization = DjangoAuthorization()
        authentication = BasicAuthentication()
        filtering = {'authors': ALL_WITH_RELATIONS,
                     'title': ALL,
                     'genre': ALL_WITH_RELATIONS,
                     'text': ALL,
                     'q': ALL
                     }
        paginator_class = Paginator

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(ArticleResource, self).build_filters(filters)
        if 'q' in filters:
            query = filters['q']
            qset = Q(authors__pseudo__startswith=query)
            orm_filters.update({'custom': qset})

        if 'g' in filters:
            query = filters['g']
            qset = Q(genre__title=query)
            orm_filters.update({'custom': qset})

        return orm_filters

    def apply_filters(self, request, applicable_filters):
        custom = None
        if 'custom' in applicable_filters:
            custom = applicable_filters.pop('custom')

        semi_filtered = super(ArticleResource, self).apply_filters(request, applicable_filters)

        return semi_filtered.filter(custom) if custom else semi_filtered

    def dehydrate(self, bundle):
        if self.get_resource_uri(bundle) == bundle.request.path:
            #detail view. all fields are available
            print "Detail"

        if self.get_resource_uri(bundle) != bundle.request.path:
            #delete some fields if we show all articles in a time
            del(bundle.data['genre'])
            del(bundle.data['authors'])
            del(bundle.data['text'])
            del(bundle.data['id'])

        return bundle



#         0. Basic query
#         http://localhost:8000/api/v1/article/?format=json
#         1. Simple queries (exact)
#         http://localhost:8000/api/v1/article/?format=json&title=third
#         2. Simple filtering (startswith)
#         http://localhost:8000/api/v1/article/?format=json&title__startswith=t
#         3. relations
#         http://localhost:8000/api/v1/article/?format=json&authors__pseudo__startswith=a
#         http://localhost:8000/api/v1/article/?genre__title=NF&format=json
#         4. custom filter:
#         authors__pseudo__startswith converts to q thanks to the build_filters and apply_filters

# misc:
# full=True in ForeignKey, ToMAnyField shows full data, not just links
# limit/offset - http://localhost:8000/api/v1/article/?format=json&limit=1&offset=1
# autheticated GET:
# curl --user admin:admin --dump-header -H "Content-Type: application/json" -X GET http://localhost:8000/api/v1/article/
# funny that official dox for testing don't work with pip installed tastypie
