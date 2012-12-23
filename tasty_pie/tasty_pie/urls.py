from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

#api import
from backend.api import ArticleResource

article_resource = ArticleResource()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tasty_pie.views.home', name='home'),
    # url(r'^tasty_pie/', include('tasty_pie.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(article_resource.urls)),
)
