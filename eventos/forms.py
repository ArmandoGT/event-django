from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from blog.models import Comment


class EmailPostForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField(max_length=100)
    destination = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea)

    def send_email(self, mypost):
        email = self.cleaned_data['email']
        name = self.cleaned_data['name']
        destination = self.cleaned_data['destination']
        comment = self.cleaned_data['comment']
        content = f"Recomendo Ler o post: {mypost.title}\n" \
                  f"Comentários: {comment}"
        msg = EmailMessage(
            subject=f"{name} Recomendo este post",
            body=content,
            from_email='contato@mysite.com.br',
            to=[destination],
            headers={'Reply-To': email}
        )

        msg.send()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('post', 'name', 'email', 'comment')

    def save_comment(self, post):
        new_comment = self.save(commit=False)
        new_comment.post = post # Vinculando Comentário ao Post
        new_comment.name = self.cleaned_data['name']
        new_comment.email = self.cleaned_data['email']
        new_comment.comment = self.cleaned_data['comment']
        new_comment.save()
        return new_comment


class CadUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username','password', 'email')
