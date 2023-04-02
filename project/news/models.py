from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.IntegerField(default=0)

    def update_rating(self):
        postRate = self.post_set.aggregate(rPost=Sum('ratingPost'))
        pRate = 0
        pRate += postRate.get('rPost')

        commentRate = self.authorUser.comment_set.aggregate(rComment=Sum('ratingComment'))
        cRate = 0
        cRate += commentRate.get('rComment')

        self.ratingAuthor = pRate * 3 + cRate
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)


class Post(models.Model):
    authorPost = models.ForeignKey(Author, on_delete=models.CASCADE)

    ARTICLE='AT'
    NEWS='NW'
    CATEGORY_CHOICES = (
        (NEWS,'Новость'),
        (ARTICLE,'Статья')
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=NEWS)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    ratingPost = models. IntegerField(default=0)

    def like(self):
        self.ratingPost += 1
        self.save()

    def dislike(self):
        self.ratingPost -= 1
        self.save()

    def preview(self):
        preview_text = self.text[0:123]
        return preview_text + '...'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    ratingComment = models. IntegerField(default=0)

    def like(self):
        self.ratingComment += 1
        self.save()

    def dislike(self):
        self.ratingComment -= 1
        self.save()