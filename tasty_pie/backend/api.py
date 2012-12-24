
import json
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication
from tastypie.resources import ModelResource

from django.contrib.auth.models import User
from django.http import HttpResponse

from backend.models import Article, Author, Genre


class GenreResource(ModelResource):
    class Meta:
        queryset = Genre.objects.all()
        resource_name = 'genre'


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']


class AuthorResource(ModelResource):
    class Meta:
        queryset = Author.objects.all()
        resource_name = 'author'
        #fields=['pseudo']
        authentication = BasicAuthentication()

    user = fields.OneToOneField(UserResource, 'user')

    def dehydrate(self, bundle):
        """custom field for all objects"""
        obj = self.obj_get(id=bundle.data['id'])
        bundle.data['some_field'] = Author.objects.get(id=1).some_fun()
        return bundle


class ArticleResource(ModelResource):

    genre = fields.ForeignKey(GenreResource, 'genre')
    authors = fields.ManyToManyField(AuthorResource, 'authors')

    class Meta:
        queryset = Article.objects.all()
        resource_name = 'article'
        authorization= Authorization()
