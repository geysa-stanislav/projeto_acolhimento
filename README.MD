# Projeto Acolhimento 🤝

Sistema em Django desenvolvido para gerenciar e facilitar a criação de guias e tutoriais pelos professores.

## ⚙️ Tecnologias Utilizadas
* Python 3.10+
* Django 5.x
* Banco de Dados: SQLite (Ambiente de Desenvolvimento)
* Editor Rich Text: django-ckeditor

## 🚀 Como rodar o projeto localmente

1. Clone o repositório: `git clone [URL_DO_SEU_GITHUB]`
2. Ative o seu ambiente virtual.
3. Instale as dependências: `pip install -r requirements.txt`
4. Crie as tabelas: `python manage.py migrate`
5. Colete os estáticos: `python manage.py collectstatic`
6. Inicie o servidor: `python manage.py runserver`

## 📝 Manual do Usuário (Professores)
1. Acesse a rota `/admin` e faça login.
2. Navegue até a seção de "Guias" ou "Aulas".
3. Utilize a caixa de texto do editor para formatar o conteúdo (negrito, imagens, links) antes de salvar. O sistema já renderiza o HTML automaticamente em tela.