import drest

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase

from backend.models import Article, Genre


class MyTest(LiveServerTestCase):


    fixtures=['users.json']

    def test_api_articles_get(self):
        api = drest.api.TastyPieAPI(self.live_server_url + '/api/v1/', auth_mech='basic')
        api.auth('admin', 'admin')

        #create genre
        genre_data = dict(title='SF', id=1)
        api.genre.post(genre_data)
        genre = Genre.objects.all()[0]
        assert 'SF' in genre.title
        genre_uri = api.genre.get().data['objects'][0]['resource_uri']

        #create author
        user_uri = api.user.get().data['objects'][0]['resource_uri']
        assert api.author.get().data['objects'] == []
        author_data = dict(pseudo='addy', user=user_uri)
        api.author.post(author_data)
        author_objects = api.author.get().data['objects']
        assert author_objects[0]['pseudo'] == author_data['pseudo']
        author_uri = api.author.get().data['objects'][0]['resource_uri']

        #create article
        assert api.article.get().data['objects'] == []
        article_data = dict(title='1',
                            text='2',
                            genre=genre_uri,
                            authors=[author_uri])
        api.article.post(article_data)
        article_objects = api.article.get().data['objects']
        assert article_objects[0]['title'] == article_data['title']

        #patch article
        ##create one more author
        user_uri = api.user.get().data['objects'][1]['resource_uri']
        api.author.post(dict(pseudo='mimi', user=user_uri))
        author2_data = api.author.get(2).data
        assert author2_data['pseudo'] == 'mimi'
        author2_data['pseudo'] = 'mimi2'
        ##test put author in parallel
        api.author.put(2, author2_data)
        author2_data = api.author.get(2).data
        assert author2_data['pseudo'] == 'mimi2'

        #really patch article
        ##get old authors
        old_authors = api.article.get(1).data['authors']
        old_authors.append(author2_data['resource_uri'])
        ##patch
        api.article.patch(1, dict(authors=old_authors))
        assert api.article.get(1).data['authors'] == old_authors