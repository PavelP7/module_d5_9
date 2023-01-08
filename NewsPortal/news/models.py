from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        self.rating = Post.objects.filter(author__user=self.user).aggregate(Sum('rating'))['rating__sum'] * 3 + \
                      Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum'] + \
                      Comment.objects.filter(post__author__user=self.user).aggregate(Sum('rating'))['rating__sum']
        self.save()

class Category(models.Model):
    topic = models.TextField(unique=True)

class Post(models.Model):
    news = 'NW'
    article = 'AR'

    TYPES = [
        (news, 'новость'),
        (article, 'статья'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TYPES, default=news)
    datetime_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.TextField()
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating = self.rating + 1
        self.save()

    def dislike(self):
        self.rating = self.rating - 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    datetime_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating = self.rating + 1
        self.save()

    def dislike(self):
        self.rating = self.rating - 1
        self.save()
