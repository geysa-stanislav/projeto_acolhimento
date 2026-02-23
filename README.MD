# 💛 UEMS Acolhe - Portal de Integração

O **UEMS Acolhe** é uma plataforma web desenvolvida para facilitar a integração e o acolhimento de estudantes imigrantes e refugiados na Universidade Estadual de Mato Grosso do Sul (UEMS) e na comunidade local.

## 🎯 O Propósito
A barreira do idioma e a falta de informação clara são os maiores obstáculos para a população imigrante. Este portal centraliza:
- **Aulas de Português como Língua de Acolhimento:** Lições estruturadas, com materiais em PDF e liberação programada por data.
- **Guia de Serviços Essenciais:** Informações traduzidas e acessíveis sobre Saúde (SUS), Documentação (CPF, RNE), Educação e Transporte.

## 🛠️ Tecnologias Utilizadas
- **Backend:** Python 3.11, Django 5.x
- **Frontend:** HTML5, CSS3, Bootstrap 5, FontAwesome
- **Banco de Dados:** SQLite (Desenvolvimento/Produção inicial)
- **Hospedagem:** PythonAnywhere
- **Segurança:** Django-Axes (Proteção contra força bruta)

## ✨ Principais Funcionalidades
- **Busca Inteligente (Fuzzy Search):** Sistema de pesquisa tolerante a erros, que ignora acentos e letras maiúsculas/minúsculas, essencial para usuários não-nativos (ex: buscar por "cartao" encontra "Cartão").
- **Agendamento de Aulas:** Sistema de bloqueio automático de lições que só ficam disponíveis na data programada pelo professor.
- **Rich Text Editor:** Integração com CKEditor para que coordenadores formatem textos, tabelas e imagens sem precisar de código.
- **Painel Administrativo com Auditoria:** Registro detalhado (Logs) de todas as ações de usuários, garantindo controle e rastreabilidade para os gestores do projeto.

## 🚀 Como rodar o projeto localmente

1. Clone o repositório:
```bash
git clone [https://github.com/geysa-stanislav/projeto_acolhimento.git](https://github.com/geysa-stanislav/projeto_acolhimento.git)