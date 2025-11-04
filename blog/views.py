from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView, LoginView
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, CreateView

from .forms import EmailPostForm, CommentForm, CadUserForm, LoginForm
from .models import Post

class ListPostsView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post/list_posts.html'

class DetailPostView(DetailView):
    template_name = 'blog/post/detail_post.html'
    context_object_name = 'post'
    model = Post

    def _get_comments(self, id_post):
        try:
            post = Post.objects.get(pk=id_post)
            return post.comments.all()
        except Post.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(DetailPostView, self).get_context_data(**kwargs)
        context['comments'] = self._get_comments(self.object.id)
        return context


class FormPostView(FormView):
    template_name = 'blog/post/sharepost.html'
    form_class = EmailPostForm
    success_url = reverse_lazy('blog:list_posts')

    def get_post(self, id_post):
        try:
            return Post.objects.get(pk=id_post)
        except Post.DoesNotExist:
            messages.error(self.request, 'Post not found')
            return None

    def get_context_data(self, **kwargs):
        context = super(FormPostView, self).get_context_data(**kwargs)
        context['post'] = self.get_post(self.kwargs['pk'])
        return context

    def form_valid(self, form, *args, **kwargs):
        mypost = self.get_context_data()['post']
        form.send_email(mypost)
        messages.success(self.request, f'Post {mypost.title} ' f'enviado com sucesso')
        return super(FormPostView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        mypost = self.get_context_data()['post']
        messages.error(self.request, f'Post {mypost.title} ' f'não foi enviado')
        return super(FormPostView, self).form_invalid(form, *args, **kwargs)


class comment_views(CreateView):
    template_name = 'blog/post/comment.html'
    form_class = CommentForm

    def _get_post(self, id_post):
        try:
            post = Post.objects.get(pk=id_post)
            return post
        except Post.DoesNotExist:
            messages.error(self.request, 'Post not found')

    def get_context_data(self, **kwargs):
        context = super(comment_views, self).get_context_data(**kwargs)
        context['post'] = self._get_post(self.kwargs['pk'])
        return context

    def form_valid(self, form, *args, **kwargs):
        post = self._get_post(self.kwargs['pk'])
        form.save_comment(post)
        return redirect('blog:detail_post', slug=post.slug)

    def form_invalid(self, form, *args, **kwargs):
        post = self._get_post(self.kwargs['pk'])

class CadUserView(CreateView):
    template_name = 'blog/users/caduser.html'
    form_class = CadUserForm
    success_url = reverse_lazy('blog:loginuser')

    def form_valid(self, form, *args, **kwargs):
        form.cleaned_data
        form.save()
        messages.success(self.request, f"Your account has been created")
        return super(CadUserView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Account not created')
        return super(CadUserView, self).form_invalid(form, *args, **kwargs)

class LoginUserView(LoginView):
    template_name = 'blog/users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('blog:list_posts')

    def form_valid(self, form, *args, **kwargs):
        user = authenticate(self.request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"Login successful {user.username}")
            return redirect('blog:list_posts')
        else:
            messages.error(self.request, 'Login failed')
            return redirect('blog:loginuser')
        
    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Login failed')
        return redirect('blog:loginuser')


class LogoutUserView(LogoutView):
    next_page = reverse_lazy('blog:list_posts')