from django import forms
from .models import Episodio, Review

class EpisodioForm(forms.ModelForm):
    class Meta:
        model = Episodio
        fields = ['id_api', 'nome', 'data_lancamento', 'codigo_episodio']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comentario']