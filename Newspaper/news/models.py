from django.contrib.auth.models import User
from django.db import models
from django.forms import IntegerField


class Author(models.Model):
    name = models.CharField(max_length=144)
    rating: IntegerField = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        total_rating = 0
        # Получаем все статьи автора
        posts = Post.objects.filter(author=self)
        # Проходим по всем статьям и суммируем рейтинг
        for post in posts:
            total_rating += post.rating * 3
        # Получаем все комментарии автора
        comments = Comment.objects.filter(user=self.user)
        # Проходим по всем комментариям и суммируем рейтинг
        for comment in comments:
            total_rating += comment.rating
        # Получаем все комментарии к статьям автора
        comments = Comment.objects.filter(post__author=self)
        # Проходим по всем комментариям и суммируем рейтинг
        for comment in comments:
           total_rating += comment.rating
        # Обновляем рейтинг автора
        self.rating = total_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=144, unique=True)


OPTION_SELECT = [
    ('news', "Новость"),
    ('post', "Публикация"),
]


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    option = models.CharField(max_length=4, choices=OPTION_SELECT)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through="PostCategory")
    header = models.CharField(max_length=144)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def preview(self):
        return self.text[:124] + '...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
