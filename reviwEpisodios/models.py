from django.db import models

class Episodio(models.Model):
    id_api = models.CharField(max_length=10, unique=True) 
    nome = models.CharField(max_length=200)  
    data_lancamento = models.DateField()  
    codigo_episodio = models.CharField(max_length=50)  

    def __str__(self):
        return f"{self.nome} ({self.codigo_episodio})"

class Review(models.Model):
    episodio = models.ForeignKey(Episodio, on_delete=models.CASCADE, related_name='reviews')  
    comentario = models.TextField()  
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review de {self.episodio.nome}"