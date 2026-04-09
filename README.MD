# 💛 UEMS Acolhe - Portal de Integração

O **UEMS Acolhe** é uma plataforma web desenvolvida para facilitar a integração e o acolhimento de estudantes imigrantes e refugiados na Universidade Estadual de Mato Grosso do Sul (UEMS) e na comunidade local.

## 🎯 O Propósito
A barreira do idioma e a falta de informação clara são os maiores obstáculos para a população imigrante. Este portal centraliza:
- **Aulas de Português como Língua de Acolhimento:** Lições estruturadas, com vídeos, materiais em PDF e liberação programada por data.
- **Tutor IA em Tempo Real:** Um mascote com Inteligência Artificial rodando na nuvem para tirar dúvidas de português de forma imediata e didática.
- **Guia de Serviços Essenciais:** Informações traduzidas e acessíveis sobre Saúde (SUS), Documentação (CPF, RNE), Educação e Transporte.

## 🛠️ Tecnologias Utilizadas
- **Backend:** Python 3.11, Django 5.x
- **Inteligência Artificial:** Integração via API REST com o Groq Cloud (Modelo Llama 3).
- **Frontend:** HTML5, CSS3, Bootstrap 5, FontAwesome
- **Banco de Dados:** SQLite (Desenvolvimento/Produção inicial)
- **Hospedagem:** PythonAnywhere
- **Segurança:** Django-Axes (Proteção contra força bruta) e gestão de variáveis de ambiente.

## ✨ Principais Funcionalidades
- **Mascote IA Educacional:** Chatbot integrado às lições. Utiliza engenharia de prompt ultra-estruturada e o processamento ultrarrápido da API do Groq para atuar estritamente como um tutor de português, garantindo respostas curtas, precisas e contextualizadas ao idioma do aluno.
- **Aulas Multimídia:** Suporte a incorporação automática de vídeos do YouTube nativos no conteúdo da aula, adaptando links comuns ou *Shorts* automaticamente.
- **Busca Inteligente (Fuzzy Search):** Sistema de pesquisa tolerante a erros, que ignora acentos e letras maiúsculas/minúsculas, essencial para usuários não-nativos (ex: buscar por "cartao" encontra "Cartão").
- **Agendamento de Aulas:** Sistema de bloqueio automático de lições que só ficam disponíveis na data programada pelo professor.
- **Rich Text Editor:** Integração com CKEditor para que coordenadores formatem textos, tabelas e imagens sem precisar de código.
- **Painel Administrativo com Auditoria:** Registro detalhado (Logs) de tentativas de acesso e ações no sistema, garantindo rastreabilidade e segurança contra invasões.

## 🚀 Como rodar o projeto localmente

### 1. Preparando o Ambiente Django
Clone o repositório e acesse a pasta do projeto:
```bash
git clone [https://github.com/geysa-stanislav/projeto_acolhimento.git](https://github.com/geysa-stanislav/projeto_acolhimento.git)
cd projeto_acolhimento
