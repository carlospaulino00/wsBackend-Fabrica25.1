import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Episodio, Review
from .forms import ReviewForm
from datetime import datetime

def buscar_episodio_api(episodio_id):
    url = f"https://rickandmortyapi.com/api/episode/{episodio_id}"
    response = requests.get(url)
    if response.status_code == 200:
        dados_api = response.json()
        data_lancamento = datetime.strptime(dados_api['air_date'], "%B %d, %Y").strftime("%Y-%m-%d")
        dados_api['air_date'] = data_lancamento 
        return dados_api
    return None

def listar_episodios(request):
    episodios = Episodio.objects.all()
    return render(request, 'listar_episodios.html', {'episodios': episodios})

def buscar_episodio(request):
    if request.method == 'POST':
        episodio_id = request.POST.get('episodio_id')
        dados_api = buscar_episodio_api(episodio_id)
        if dados_api:
            Episodio.objects.update_or_create(
                id_api=episodio_id,
                defaults={
                    'nome': dados_api['name'],
                    'data_lancamento': dados_api['air_date'],
                    'codigo_episodio': dados_api['episode'],
                }
            )
            return redirect('listar_episodios')
        else:
            return render(request, 'buscar_episodio.html', {'erro': 'Episódio não encontrado!'})
    return render(request, 'buscar_episodio.html')

def detalhes_episodio(request, episodio_id):
    episodio = get_object_or_404(Episodio, id=episodio_id)
    reviews = episodio.reviews.all()
    return render(request, 'detalhes_episodio.html', {'episodio': episodio, 'reviews': reviews})

def adicionar_review(request, episodio_id):
    episodio = get_object_or_404(Episodio, id=episodio_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.episodio = episodio
            review.save()
            return redirect('detalhes_episodio', episodio_id=episodio.id)
    else:
        form = ReviewForm()
    return render(request, 'adicionar_review.html', {'form': form, 'episodio': episodio})

def editar_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('detalhes_episodio', episodio_id=review.episodio.id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'editar_review.html', {'form': form, 'review': review})

def excluir_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        episodio_id = review.episodio.id
        review.delete()
        return redirect('detalhes_episodio', episodio_id=episodio_id)
    return render(request, 'excluir_review.html', {'review': review})