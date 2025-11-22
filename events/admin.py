from django.contrib import admin
from .models import Evento, Inscricao, Comment

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data', 'local', 'organizador')
    list_filter = ('data', 'local', 'organizador')
    search_fields = ('titulo', 'descricao', 'local')
    prepopulated_fields = {"slug": ("titulo",)}
    date_hierarchy = 'data'
    ordering = ('-data',)

@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    list_display = ('evento', 'usuario', 'data_inscricao')
    list_filter = ('evento', 'usuario', 'data_inscricao')
    search_fields = ('evento__titulo', 'usuario__username')
    ordering = ('evento', '-data_inscricao',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('evento', 'name', 'email', 'comment', 'created', 'active')
    list_filter = ('name', 'created', 'active')
    ordering = ('active', '-created',)

# Register your models here.
