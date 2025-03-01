# wsBackend-Fabrica25.1
  O projeto consite em um crud onde é possivel buscar um episodio na api do RickandMorty atraves do 
id do episodio e com isso ele ira puxar informaçoes como nome do episodio e data de lançamento alem 
do numero do episodio e temporada e com isso o crud reviews voce podera adicionar reviews e pode 
manipulados como editar, criar novos e excluir.

O Models foi separado em duas entidades

Sendo a primeira o episodio que sera puxado da api:

    class Episodio(models.Model):
        id_api = models.CharField(max_length=10, unique=True)  # ID do episódio na API
        nome = models.CharField(max_length=200)  # Nome do episódio
        data_lancamento = models.DateField()  # Data de lançamento
        codigo_episodio = models.CharField(max_length=50)  # Código do episódio (ex: S01E01)
    
        def __str__(self):
            return f"{self.nome} ({self.codigo_episodio})"

Logo em seguida temos a classe Review que esta sendo relacionada com a Classe Episodio atraves de uma chave estrageira:

    class Review(models.Model):
      episodio = models.ForeignKey(Episodio, on_delete=models.CASCADE, related_name='reviews')  
      comentario = models.TextField()  
      criado_em = models.DateTimeField(auto_now_add=True)
  
      def __str__(self):
          return f"Review de {self.episodio.nome}"


A primeira funçao da views foi criada para buscar os dados da api apos inserir o id:

      def buscar_episodio_api(episodio_id):
          url = f"https://rickandmortyapi.com/api/episode/{episodio_id}"
          response = requests.get(url)
          if response.status_code == 200:
              dados_api = response.json()
              data_lancamento = datetime.strptime(dados_api['air_date'], "%B %d, %Y").strftime("%Y-%m-%d")
              dados_api['air_date'] = data_lancamento 
              return dados_api
          return None

A segunda funçao ira listar os episodios que estao sendo puxados da api:

    def listar_episodios(request):
        episodios = Episodio.objects.all()
        return render(request, 'listar_episodios.html', {'episodios': episodios})

A terceira funçao pega os dados do episodio caso seja encontrado na api e a informação guardada sera listada na lista de episodios:

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

A quarta funçao ira mostrar o episodio e suas reviews associadas a ele, caso encontrado e caso nao seja retorna o erro 404:

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

A quinta funçao é possivel editar as reviews:

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

a sexta e ultima função permite excluir reviews:

    def excluir_review(request, review_id):
        review = get_object_or_404(Review, id=review_id)
        if request.method == 'POST':
            episodio_id = review.episodio.id
            review.delete()
            return redirect('detalhes_episodio', episodio_id=episodio_id)
        return render(request, 'excluir_review.html', {'review': review})






