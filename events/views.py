from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView, LoginView
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, CreateView

from .forms import EmailEventoForm, CommentForm, CadUserForm, LoginForm
from .models import Evento

class EventoListView(ListView):
    context_object_name = 'Eventos'
    model = Evento
    template_name = 'eventos/myevent/list_eventos.html'

class EventoDetailView(DetailView):
    context_object_name = 'evento'
    model = Evento
    template_name = 'eventos/myevent/detail_event.html'

    def _get_comments(self, id_post):
        try:
            post = Evento.objects.get(pk=id_post)
            return post.comments.all()
        except Evento.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(EventoDetailView, self).get_context_data(**kwargs)
        context['comments'] = self._get_comments(self.object.id)
        return context


class FormEventoView(FormView):
    template_name = 'eventos/myevent/eventshare.html'
    form_class = EmailEventoForm
    success_url = reverse_lazy('events:list_eventos')

    def get_post(self, pk):
        try:
            return Evento.objects.get(pk=pk)
        except Evento.DoesNotExist:
            messages.error(self.request, 'Evento não encontrado')
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myevent'] = self.get_post(self.kwargs['pk'])
        return context

    def form_valid(self, form, *args, **kwargs):
        mypost = self.get_context_data()['myevent']
        form.send_email(mypost)
        messages.success(self.request, f'Evento \"{mypost.titulo}\" enviado com sucesso')
        return super().form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        mypost = self.get_context_data().get('myevent')
        messages.error(self.request, f'Evento \"{mypost.titulo if mypost else ""}\" não foi enviado')
        return super().form_invalid(form, *args, **kwargs)



class comment_views(CreateView):
    template_name = 'eventos/myevent/comment.html'
    form_class = CommentForm

    def _get_post(self, pk):
        try:
            evento = Evento.objects.get(pk=pk)
            return evento
        except Evento.DoesNotExist:
            messages.error(self.request, 'Evento não encontrado')

    def get_context_data(self, **kwargs):
        context = super(comment_views, self).get_context_data(**kwargs)
        context['myevent'] = self._get_post(self.kwargs['pk'])
        return context

    def form_valid(self, form, *args, **kwargs):
        post = self._get_post(self.kwargs['pk'])
        form.save_comment(post)
        return redirect('events:detail_event', slug=post.slug)

    def form_invalid(self, form, *args, **kwargs):
        post = self._get_post(self.kwargs['pk'])
        messages.error(self.request, 'Comentário não enviado. Corrija os erros do formulário.')
        context = self.get_context_data(form=form, **kwargs)
        return self.render_to_response(context)


class CadUserView(CreateView):
    template_name = "eventos/users/caduser.html"
    form_class = CadUserForm
    success_url = reverse_lazy('events:loginuser')

    def form_valid(self, form, *args, **kwargs):
        form.cleaned_data
        form.save()
        messages.success(self.request, f"Your account has been created")
        return super(CadUserView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Account not created')
        return super(CadUserView, self).form_invalid(form, *args, **kwargs)

class LoginUserView(LoginView):
    template_name = 'eventos/users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('events:list_eventos')

    def form_valid(self, form, *args, **kwargs):
        user = authenticate(self.request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
            return redirect('events:list_eventos')
        else:
            messages.error(self.request, 'Login failed')
            return redirect('events:loginuser')
        
    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Login failed')
        return redirect('events:loginuser')


class LogoutUserView(LogoutView):
    next_page = reverse_lazy('events:list_eventos')