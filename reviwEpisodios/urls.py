from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_episodios, name='listar_episodios'),
    path('buscar/', views.buscar_episodio, name='buscar_episodio'),
    path('detalhes/<int:episodio_id>/', views.detalhes_episodio, name='detalhes_episodio'),
    path('adicionar-review/<int:episodio_id>/', views.adicionar_review, name='adicionar_review'),
    path('editar-review/<int:review_id>/', views.editar_review, name='editar_review'),
    path('excluir-review/<int:review_id>/', views.excluir_review, name='excluir_review'),
]