from django import forms
from .models import Comments


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comments
		fields = ['name', 'email', 'content']
		widgets = {
			'name': forms.TextInput(attrs={'id': 'name', 'class': "form-control", 'placeholder': 'Name*'}),
			'email': forms.EmailInput(attrs={'id': 'email', 'class': "form-control", 'placeholder': 'Email*'}),
			'content': forms.Textarea(
				attrs={'id': 'content', 'class': "form-control", 'placeholder': 'Messages...', 'cols': 45, 'rows': 4})
		}


class SignInForm(forms.ModelForm):
	pass
