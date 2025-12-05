# Em pages/models.py
from django.db import models

class Curso(models.Model):
    # 'Back-end com Django', 'PowerBI', etc.
    nome = models.CharField(max_length=200) 
    
    # 'Gustavo'
    instrutor = models.CharField(max_length=100)
    
    # Armazenamos o NÚMERO (40), não o texto "40 horas".
    # O texto "horas" será colocado no template.
    carga_horaria = models.IntegerField()
    
    # 'Iniciante'
    # Usar 'choices' é uma boa prática para campos com valores fixos
    NIVEL_CHOICES = [
        ('Iniciante', 'Iniciante'),
        ('Intermediário', 'Intermediário'),
        ('Avançado', 'Avançado'),
    ]
    nivel = models.CharField(max_length=50, choices=NIVEL_CHOICES, default='Iniciante')

    descricao = models.CharField(max_length=1000, default ='')

    def __str__(self):
        # Isso ajuda a ver o nome do curso no painel Admin
        return self.nome
    
class Plano(models.Model):
    nome = models.CharField(max_length=20)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    beneficios = models.TextField()
    destaque = models.BooleanField(default=False)

    def __str__(self):
        # Isso ajuda a ver o nome do curso no painel Admin
        return f'{self.nome}- R${self.preco}'