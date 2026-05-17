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
from .models import Licao, Recado # Importando o Recado
from .forms import CadastroSeguroForm
from guia.models import Publicacao
from groq import Groq

def remover_acentos(texto):
    if not texto: return ""
    return unicodedata.normalize('NFKD', str(texto)).encode('ASCII', 'ignore').decode('utf-8').lower()

def home(request):
    busca = request.GET.get('busca')
    hoje = timezone.now().date()
    
    recados = Recado.objects.filter(ativo=True).order_by('-data_publicacao') 
    
    if busca:
        busca_limpa = remover_acentos(busca)
        licoes = [l for l in Licao.objects.all() if busca_limpa in remover_acentos(l.titulo) or busca_limpa in remover_acentos(l.conteudo)]
        publicacoes = [p for p in Publicacao.objects.all() if busca_limpa in remover_acentos(p.titulo) or busca_limpa in remover_acentos(p.conteudo)]
    else:
        licoes = Licao.objects.all()
        publicacoes = None
        
    return render(request, 'home.html', {'licoes': licoes, 'publicacoes': publicacoes, 'hoje': hoje, 'recados': recados})

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

            # REFINAMENTO DO PROMPT PARA SUPORTE MULTILINGUE E GRAMATICAL
            sistema = f"""Você é o Tutor IA do UEMS Acolhe, um assistente pedagógico poliglota e empático para imigrantes.

AULA ATUAL: {titulo_aula}
CONTEÚDO BASE (PDF):
{conteudo_aula[:12000]}

DIRETRIZES DE IDIOMA E APOIO:
1. IDIOMA: Responda SEMPRE no idioma em que o aluno falar com você (Português, Inglês, Espanhol, Francês ou Crioulo Haitiano). Se ele pedir para mudar de idioma, mude imediatamente.
2. ZERO INGLÊS NÃO SOLICITADO: NUNCA adicione traduções entre parênteses em inglês. NUNCA use avisos em inglês como "Note:". Se o aluno pedir em Árabe, responda APENAS em Árabe. Se pedir em Japonês, APENAS em Japonês (sem explicações em inglês ao lado).
3. SUPORTE LINGUÍSTICO: Traduzir termos, explicar gramática básica (como o que é um verbo, substantivo, etc.) ou praticar pronúncia NÃO são considerados dúvidas "fora do conteúdo". Isso é suporte necessário ao letramento.
4. CONTEÚDO: Sua base principal é o conteúdo do PDF acima. Use-o para dar exemplos.
5. RESTRIÇÃO: Recuse apenas perguntas totalmente irrelevantes ao ambiente escolar ou à vida no Brasil (ex: futebol, fofocas, política externa). Para estas, responda: "Essa dúvida está fora do conteúdo desta aula."
6. ESTILO: Respostas curtas (máximo 3-4 linhas), português simples e tom acolhedor.
7. CONTEXTO: Mantenha o fio da conversa através do histórico."""

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