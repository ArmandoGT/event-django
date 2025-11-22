from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='publish')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('publish', 'Publish'),
    )
    objects = models.Manager() # Gerenciador Padrão
    published = PublishedManager() # Gerenciador Personalizado


    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def get_absolute_url(self):
        return reverse('blog:detail_post', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

    class Meta:
        ordering = ['-publish']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField('Nome', max_length=250)
    email = models.EmailField('Email')
    comment = models.TextField('Comentário')
    created = models.DateTimeField('Data da Criação', auto_now_add=True)
    active = models.BooleanField('Ativo', default=False)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentarios'
        ordering = ['-created']

    def __str__(self):
        return 'Comentário de: ' + self.name