from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='publish')


class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)  # <-- ADICIONE ESTA LINHA!
    descricao = models.TextField()
    data = models.DateTimeField()
    local = models.CharField(max_length=200)
    organizador = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'is_superuser': True},
        related_name='eventos_organizados',
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

class Inscricao(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_inscricao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.evento.titulo}"

class Comment(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='comments')
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