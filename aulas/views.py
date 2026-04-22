import json
import os
from dotenv import load_dotenv
load_dotenv()
import unicodedata
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login
from django.utils import timezone
from .models import Licao, Recado # <-- ADICIONADO: Importando o Recado
from .forms import CadastroSeguroForm
from guia.models import Publicacao
from groq import Groq

def remover_acentos(texto):
    if not texto: return ""
    return unicodedata.normalize('NFKD', str(texto)).encode('ASCII', 'ignore').decode('utf-8').lower()

def home(request):
    busca = request.GET.get('busca')
    hoje = timezone.now().date()
    
    # <-- ADICIONADO: Puxando apenas os recados marcados como "ativos"
    recados = Recado.objects.filter(ativo=True).order_by('-data_publicacao') 
    
    if busca:
        busca_limpa = remover_acentos(busca)
        licoes = [l for l in Licao.objects.all() if busca_limpa in remover_acentos(l.titulo) or busca_limpa in remover_acentos(l.conteudo)]
        publicacoes = [p for p in Publicacao.objects.all() if busca_limpa in remover_acentos(p.titulo) or busca_limpa in remover_acentos(p.conteudo)]
    else:
        licoes = Licao.objects.all()
        publicacoes = None
        
    # <-- ADICIONADO: Enviando a variável 'recados' para o HTML
    return render(request, 'home.html', {'licoes': licoes, 'publicacoes': publicacoes, 'hoje': hoje, 'recados': recados})

# ... (MANTENHA O RESTANTE DO CÓDIGO INTACTO A PARTIR DAQUI: def licao_detalhe...)

def licao_detalhe(request, id):
    licao = get_object_or_404(Licao, id=id)
    return render(request, 'licao_detalhe.html', {'licao': licao})

def cadastro(request):
    if request.method == 'POST':
        form = CadastroSeguroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = CadastroSeguroForm()
    return render(request, 'cadastro.html', {'form': form})

def tutor_ia(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            mensagem_usuario = dados.get('mensagem', '')
            licao_id = dados.get('licao_id', None)
            historico = dados.get('historico', [])

            conteudo_aula = ""
            titulo_aula = ""
            if licao_id:
                try:
                    import pypdf, io
                    licao = Licao.objects.get(id=licao_id)
                    titulo_aula = licao.titulo or ""
                    if licao.arquivo_pdf:
                        pdf_bytes = licao.arquivo_pdf.read()
                        leitor = pypdf.PdfReader(io.BytesIO(pdf_bytes))
                        for pagina in leitor.pages:
                            conteudo_aula += pagina.extract_text() or ""
                    if not conteudo_aula:
                        texto_bruto = licao.conteudo or ""
                        conteudo_aula = re.sub(r'<[^>]+>', ' ', texto_bruto).strip()
                except Exception as e:
                    print(f"ERRO: {e}")

            print(f"CONTEUDO AULA: {len(conteudo_aula)} caracteres")

            sistema = f"""Você é o Tutor IA  do UEMS Acolhe, assistente pedagógico de português para imigrantes iniciantes.

AULA ATUAL: {titulo_aula}
CONTEÚDO DA AULA:
{conteudo_aula[:12000]}

REGRAS:
 - Detecte o idioma da mensagem do aluno e responda SEMPRE no mesmo idioma que ele usou.
- Se o aluno escrever em haitiano crioulo, responda em haitiano crioulo.
- Se escrever em espanhol, responda em espanhol.
- Se escrever em português, responda em português.
- Responda SOMENTE perguntas relacionadas ao conteúdo da aula acima. Nunca responda sobre outros temas.
- Se o tema não estiver no conteúdo da aula, responda APENAS: "Essa dúvida está fora do conteúdo desta aula."
- Respostas CURTAS: máximo 3 linhas. Se o aluno quiser saber mais, ele pergunta.
- Use exemplos simples e diretos.
- Mantenha o contexto da conversa — se o aluno perguntou sobre plural, perguntas seguintes são sobre o mesmo tema.
- Quando o aluno perguntar "por que" sobre um tema da aula, explique pedagogicamente de forma simples.
- Responda em português simples para quem está aprendendo.
- Nunca invente regras gramaticais."""

            cliente = Groq(api_key=os.environ.get("GROQ_API_KEY"))

            chat = cliente.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": sistema},
                    *historico,
                    {"role": "user", "content": mensagem_usuario}
                ],
                max_tokens=400,
                temperature=0.3,
            )

            texto_ia = chat.choices[0].message.content.strip()
            return JsonResponse({'resposta': texto_ia})

        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=400)

    return JsonResponse({'erro': 'Método não permitido.'}, status=405)