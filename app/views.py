from django.shortcuts import render, get_object_or_404, redirect
from .models import *  # 1. Importar
from .forms import CursoForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import Group # <-- Importação para cadastro usuario do grupo Cliente
import requests # A biblioteca padrão de mercado para APIs
from django.contrib import messages # Para dar feedback ao usuário


def home_view(request):
    # 2. PEDIR AO BANCO:
    todos_os_cursos = Curso.objects.all()
    
    context = {
        'instrutor': 'Gustavo',
        'logado': request.user.is_authenticated,
        'cursos': todos_os_cursos  # 3. Passar dados reais
    }
    
    # 4. Chamar o template
    return render(request, 'home.html', context)

def metodologia_view(request):
    return render(request, 'metodologia.html')

def assinaturas_view(request):
    todas_as_assinaturas=Plano.objects.all()

    context = {
        "planos" : todas_as_assinaturas
    }

    return render(request, 'assinaturas.html', context)

def curso_detalhe_view(request, pk):
    # Busca o curso com o ID específico
    curso = get_object_or_404(Curso, pk=pk)
    
    # Renderiza o template passando o curso
    return render(request, 'curso_detalhe.html', {'curso': curso})

def curso_form_view(request):
    if request.method == 'POST':
        # Usuário enviou dados preenchidos
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()  # Salva no banco de dados
            return redirect('home')  # Redireciona para a página inicial
    else:
        # Usuário quer ver o formulário vazio
        form = CursoForm()
    
    return render(request, 'curso_form.html', {'form': form})

# Use 'pk' em vez de 'id' para manter o padrão do urls.py (<int:pk>)
def editar_curso_view(request, pk):
    # 1. Busca o curso com segurança (se não achar, dá erro 404)
    curso = get_object_or_404(Curso, pk=pk)
 
    # 2. Preenche o formulário com os dados existentes (instance=curso)
    #    O "request.POST or None" é um atalho inteligente:
    #    Se tem dados (POST), usa eles. Se não tem (GET), usa None.
    form = CursoForm(request.POST or None, instance=curso)
 
    if form.is_valid():
        form.save()
        return redirect('home') # Redireciona para a lista (nome da sua rota home)
 
    # 3. CORREÇÃO: Renderiza o MESMO template de criação
    return render(request, 'curso_form.html', {'form': form})

def deletar_curso_view(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    
    if request.method == 'POST':
        # Só apaga se vier do form
        curso.delete()
        return redirect('home')
    
    # GET mostra confirmação
    return render(request,'confirmar_exclusao.html',{'curso': curso})

def cadastro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # --- LÓGICA DE GRUPO ---
            # Pega o grupo "Client". 
            # Nota: O grupo PRECISA existir no Admin antes de rodar isso.
            grupo_client = Group.objects.get(name='Client')
            user.groups.add(grupo_client)

            # Login automático
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    
    return render(request,'registration/cadastro.html',{'form': form})

def contato_view(request):
    if request.method == 'POST':
        # 1. Pegar os dados do formulário
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # 2. Configurar a API do EmailJS (Backend)
        # Na vida real, estas chaves ficariam no .env!
        service_id = 'service_cmc47cz'
        template_id = 'template_doa9i9d'
        user_id = 'u8BgNyrmh9VGjmfgf' # No backend eles chamam de User ID muitas vezes
        
        # 3. Montar o pacote de dados (Payload)
        payload = {
            'service_id': service_id,
            'template_id': template_id,
            'user_id': user_id,
            'template_params': {
                'from_name': name,
                'reply_to': email,
                'message': message
            }
        }
        
        # 4. Consumir a API (Fazer o Request)
        try:
            response = requests.post(
                'https://api.emailjs.com/api/v1.0/email/send',
                json=payload # O requests converte ditado para JSON automaticamente
            )
            
            # 5. Verificar se deu certo (Status 200 = OK)
            if response.status_code == 200:
                messages.success(request, 'E-mail enviado com sucesso!')
            else:
                messages.error(request, 'Erro ao enviar e-mail. Tente novamente.')
                
        except Exception as e:
            messages.error(request, f'Erro de conexão: {e}')
            
    return render(request, 'contato.html')