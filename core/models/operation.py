
from django.db import models
from django.contrib.auth.models import User


class Operation(models.Model):
    number1 = models.FloatField(verbose_name='Número 1')
    number2 = models.FloatField(verbose_name='Número 2')

    # Campo para armazenar o tipo de operação (soma, subtracao, multiplicacao, divisao)
    OPERATION_CHOICES = [
        ('soma', 'Soma'),
        ('subtracao', 'Subtração'),
        ('multiplicacao', 'Multiplicação'),
        ('divisao', 'Divisão'),
    ]

    operation_type = models.CharField(
        max_length=20,
        choices=OPERATION_CHOICES,
        verbose_name='Tipo de Operação',
    )

    # Campo para armazenar o resultado da operação
    result = models.FloatField(verbose_name='Resultado')

    # Chave estrangeira para o modelo User do Django
    # Isso associa cada operação a um usuário específico

    default_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='operacoes',
        verbose_name='Usuário',

    )

    # Campo para registrar a data e hora da operação
    operation_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Data da Operação')

    class Meta:
        verbose_name = 'Operação'
        verbose_name_plural = 'Operações'
        ordering = ['-operation_date']

    def __str__(self):
        # Representação em string do objeto, útil para o Django Admin
        return f"{self.default_user} - {self.number1} {self.operation_type} {self.number2} = {self.result}"
