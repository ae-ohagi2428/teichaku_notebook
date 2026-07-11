from django import forms

from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'タイトルを入力してください'
                }),
            'content': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows' : 10,
                'placeholder': 'ノートの内容を入力してください', 
            })
        }
        labels = {
            'title': 'タイトル',
            'content': '内容'
        }