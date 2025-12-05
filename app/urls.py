from django.urls import path
from . import views  # O '.' significa 'importe da pasta atual'

urlpatterns = [
    # Quando alguém visitar a URL raiz deste app (ex: /), 
    # chame a função 'app_view' que está em 'views.py'.
    # O 'name' é um apelido opcional que usaremos mais tarde.
    path('', views.home_view, name='home'),
    path('metodologia/', views.metodologia_view, name='metodologia'),
    path('contato/', views.contato_view, name='contato'),
    path('assinaturas/', views.assinaturas_view, name='assinaturas'),
    path('curso/<int:pk>/', views.curso_detalhe_view, name='curso_detalhe'),
    path('curso/criar/', views.curso_form_view, name='curso_form'),
    path('curso/editar/<int:pk>/', views.editar_curso_view, name='curso_editar'),
    path('curso/deletar/<int:pk>/', views.deletar_curso_view, name='curso_deletar'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    # Se você tivesse outras páginas neste app, você as adicionaria aqui:
    # ex: path('sobre/', views.sobre_view, name='sobre'),
    # ex: path('contato/', views.contato_view, name='contato'),
]