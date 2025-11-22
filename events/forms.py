from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Comment
from django.core.mail import EmailMessage



class EmailEventoForm(forms.Form):
    email = forms.EmailField(
        label="Seu e-mail",
    )
    name = forms.CharField(
        label="Seu nome",
        max_length=100,
    )
    destination = forms.EmailField(
        label="E-mail do destinatário",
    )
    comment = forms.CharField(
        label="Mensagem (opcional)",
        required=False,
        widget=forms.Textarea,
    )

    def send_email(self, myevent):
        email = self.cleaned_data['email']
        name = self.cleaned_data['name']
        destination = self.cleaned_data['destination']
        comment = self.cleaned_data['comment']

        content = (
            f"Recomendo o evento: {myevent.titulo}\n"
            f"Descrição: {myevent.descricao}\n\n"
            f"Comentário de {name}: {comment}"
        )

        msg = EmailMessage(
            subject=f"{name} recomendou o evento: {myevent.titulo}",
            body=content,
            from_email='contato@mysite.com.br',
            to=[destination],
            headers={'Reply-To': email}
        )
        msg.send()



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'comment')

    def save_comment(self, evento):
        new_comment = self.save(commit=False)
        new_comment.evento = evento
        new_comment.save()
        return new_comment



class CadUserForm(UserCreationForm):
    email = forms.EmailField(
        label="E-mail",
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        # remove os help_text padrão do Django
        help_texts = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Usuário
        self.fields["username"].label = "Usuário"
        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["username"].help_text = (
            '<br>'
            'Use apenas letras, números e @ . + - _.'
        )

        # E-mail
        self.fields["email"].help_text = (
            '<br>'
            'Informe um e-mail válido.'
        )

        # Senha
        self.fields["password1"].label = "Senha"
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password1"].help_text = (
            '<br>'
            'Use pelo menos 8 caracteres, misturando letras e números.'
        )

        # Confirmação de senha
        self.fields["password2"].label = "Confirmação de senha"
        self.fields["password2"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].help_text = (
            '<br>'
            'Repita a mesma senha digitada acima.'
        )



class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
