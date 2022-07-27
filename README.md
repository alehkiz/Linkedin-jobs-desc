# Linkedin-jobs-desc

<!---Esses são exemplos. Veja https://shields.io para outras pessoas ou para personalizar este conjunto de escudos. Você pode querer incluir dependências, status do projeto e informações de licença aqui--->

![GitHub repo size](https://img.shields.io/github/repo-size/alehkiz/Linkedin-jobs-desc?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/alehkiz/Linkedin-jobs-desc?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/alehkiz/Linkedin-jobs-desc?style=for-the-badge)
![Github open issues](https://img.shields.io/github/issues/alehkiz/Linkedin-jobs-desc?style=for-the-badge)


> Scraping de valores de aluguel.

### Melhorias futuras:

- [x] Gerar classe com carregamento por página
- [x] Gerar classe com carregamento por batch
- [x] Gerar main
- [] Gerar pandas.DataFrame
- [] Gerar a geolocalização de cada imóvel

## 💻 Pré-requisitos

* Você instalou a versão mais recente de `python`
* Utilize um ambiente virtual: https://docs.python.org/3/tutorial/venv.html
* No ambiente virtual, instale as bibliotecas necessárias: `pip install -r requirements.txt`

## ☕ Usando Linkedin-jobs-desc

Para usar Linkedin-jobs-desc, siga estas etapas:

na raiz do repositórico, rode:

```
python main.py
```

Todos os dados serão salvos em **data/jobs.pkl** no qual você pode ler com a biblioteca `pickle`. O arquivo conterá um `dict` no qual a chave será a URL de acesso para a vaga e o valor será um objeto `Job` no qual terá os seguintes atributos:
* description: Descrição da vaga, sem nenhum tratamento
* company_url: URL da empresa
* company_name: Nome da empresa
* time_post: Tempo no qual a vaga está aberta
* job_title: Titulo da vaga
* experience_level: Nível de experiência
* type_job: Tipo de emprego: Presencial, remoto ou híbrido
* function: Função que será desempenhada
* sector: Setor
* code: Código, se inativo
* datetime: Data do cadastro

## 📝 Licença

Esse projeto está sob licença. Veja o arquivo [LICENÇA](LICENSE) para mais detalhes.

[⬆ Voltar ao topo](#Linkedin-jobs-desc)<br>
