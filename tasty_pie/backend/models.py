from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):

    user = models.OneToOneField(User, related_name='team_member')
    pseudo = models.CharField(max_length=50)

    def __unicode__(self):
        return self.pseudo

    def some_fun(self):
        return 'just for test'


class Genre(models.Model):

    GENRE_CHOICES = (
        ('SF', 'Science Fiction'),
        ('FA', 'Fantasy'),
        ('NF', 'Non-fiction'),
        ('SH', 'Shit')
    )

    title = models.CharField(choices=GENRE_CHOICES, max_length=2)

    def __unicode__(self):
        return self.title

class Follow(models.Model):
    article = models.ForeignKey('Article')
    author = models.ForeignKey(Author)


class Article(models.Model):

    title = models.CharField(max_length=100)
    text = models.TextField()
    authors = models.ManyToManyField(Author, throught=Follow)
    genre = models.ForeignKey(Genre)

    def __unicode__(self):
        return self.title
