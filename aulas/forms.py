from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re

class CadastroSeguroForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        help_text='Obrigatório e ÚNICO. Usado para recuperação segura da conta.'
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['username'].help_text = 'Padrão obrigatório: NOME_PALAVRA (use o underline). Ex: maria_aluna'
        self.fields['username'].label = 'Nome de Usuário'

        self.fields['password1'].help_text = (
            "Crie uma senha forte (mínimo de 8 caracteres). "
            "Proibido sequências (ex: 1234, abcd) ou repetições (ex: aaa, 111). "
            "OBRIGATÓRIO: Pelo menos um caractere especial (@, $, !, %, *, ?, &, #, _, ., -)."
        )

    # --- DEFESA: NOME DE USUÁRIO ---
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Validar inputs ativamente 
        if not re.match(r'^[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)+$', username):
            raise forms.ValidationError("O nome de usuário DEVE conter um underline (_) separando os nomes. Exemplo: maria_aluna")
        return username
# --- DEFESA CRÍTICA: E-MAIL ÚNICO, FORMATO E ANTI-ERROS ---
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # 1. Defesa Sintática Estrita (Apenas caracteres válidos)
        padrao_estrito = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(padrao_estrito, email):
            raise forms.ValidationError("ALERTA: Formato de e-mail inválido. Verifique se digitou corretamente.")

        if '..' in email:
            raise forms.ValidationError("ALERTA: O e-mail não pode conter pontos seguidos.")

        # Fatiamos o e-mail para analisar os pedaços separadamente
        partes_dominio = email.split('@')[1].lower()
        provedor = partes_dominio.split('.')[0] # Pega a palavra antes do ponto (ex: gmail)
        terminacao = email.split('.')[-1].lower() # Pega a última palavra (ex: com, br)

        # 2. Dicionário de Defesa: Provedores (Erros de digitação comuns)
        erros_gmail = ['gmaol', 'gamil', 'gmai', 'gmeil', 'gemail', 'gimal', 'gmil']
        erros_hotmail = ['hotmal', 'hotmai', 'hotimail', 'hormail', 'rotmail', 'hotmaio', 'hotmial']
        erros_outlook = ['outlok', 'otlook', 'outluk', 'outloo', 'outlooc']
        erros_yahoo = ['yahho', 'yaho', 'yhoo', 'yahu', 'yaoo', 'yaho']
        
        if provedor in erros_gmail:
            raise forms.ValidationError(f"ALERTA: Verifique o e-mail. Você digitou '{provedor}', você quis dizer 'gmail'?")
        if provedor in erros_hotmail:
            raise forms.ValidationError(f"ALERTA: Verifique o e-mail. Você digitou '{provedor}', você quis dizer 'hotmail'?")
        if provedor in erros_outlook:
            raise forms.ValidationError(f"ALERTA: Verifique o e-mail. Você digitou '{provedor}', você quis dizer 'outlook'?")
        if provedor in erros_yahoo:
            raise forms.ValidationError(f"ALERTA: Verifique o e-mail. Você digitou '{provedor}', você quis dizer 'yahoo'?")

        # 3. Dicionário de Defesa: Terminações (.com, .br)
        erros_terminacao = ['con', 'cmo', 'xom', 'comn']
        if terminacao in erros_terminacao:
            raise forms.ValidationError(f"ALERTA: O final do e-mail parece errado. Você digitou '.{terminacao}', você quis dizer '.com'?")
            
        # Pega erros clássicos de brasileiros no ".com.br"
        if partes_dominio.endswith('.com.b') or partes_dominio.endswith('.com.brr') or partes_dominio.endswith('.con.br'):
            raise forms.ValidationError("ALERTA: O final do e-mail parece errado. Você quis dizer '.com.br'?")

        # 4. Defesa contra domínios de teste ou falsos
        dominios_proibidos = ['teste.com', 'exemplo.com', 'email.com', 'fake.com']
        if partes_dominio in dominios_proibidos or partes_dominio.startswith('teste.'):
            raise forms.ValidationError("ALERTA: E-mails falsos ou de teste não são permitidos. Use seu e-mail real.")

        # 5. Defesa Final: E-mail Duplicado no Banco de Dados
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("ALERTA: Este e-mail já está cadastrado no sistema. Por favor, faça o login.")
        
        return email

    # --- DEFESA MELHORADA: SENHA MILITAR ---
    def clean(self):
        cleaned_data = super().clean()
        senha = self.data.get('password1') 
        
        if senha:
            senha_lower = senha.lower() # Transforma tudo em minúscula para pegar 'Abcd' e 'abcd'
            
            # 1. Trava de Tamanho Mínimo
            if len(senha) < 8:
                self.add_error('password1', "A senha deve ter no mínimo 8 caracteres.")
            
            # 2. Trava do Caractere Especial
            if not re.search(r'[@$!%*?&#_.-]', senha):
                self.add_error('password1', "A senha precisa ter pelo menos um caractere especial (@, $, !, %, *, ?, &, #, _, ., -).")
            
            # 3. Trava de Repetições (Reduzido para 3: bloqueia 'aaa', '111')
            if re.search(r'(.)\1{2,}', senha_lower):
                self.add_error('password1', "Por segurança, não repita o mesmo caractere 3 vezes seguidas (ex: aaa, 111).")
            
            # 4. Trava de Sequências (Agora pega Números E Letras)
            seq_num = "01234567890 09876543210"
            seq_alfa = "abcdefghijklmnopqrstuvwxyz zyxwvutsrqponmlkjihgfedcba"
            
            # Analisa a senha em blocos de 4 caracteres
            for i in range(len(senha_lower) - 3):
                trecho = senha_lower[i:i+4]
                if trecho in seq_num:
                    self.add_error('password1', "A senha não pode conter números em sequência (ex: 1234, 8765).")
                    break 
                if trecho.isalpha() and trecho in seq_alfa:
                    self.add_error('password1', "A senha não pode conter letras em sequência do alfabeto (ex: abcd, dcba).")
                    break 
        
        return cleaned_data