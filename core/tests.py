from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Operation
from datetime import datetime, timezone
from time import sleep
import json


class OperacaoModelTest(TestCase):

    def setUp(self):
        # Cria um user de testes para associar operações
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_operacao_creation(self):
        # Testa a criação de uma OP de somar
        operacao = Operation.objects.create(

            default_user=self.user,
            number1=10,
            number2=5,
            operation_type='soma',
            result=15
        )

        self.assertEqual(operacao.default_user, self.user)
        self.assertEqual(operacao.number1, 10)
        self.assertEqual(operacao.number2, 5)
        self.assertEqual(operacao.operation_type, 'soma')
        self.assertEqual(operacao.result, 15)

    def test_operacao_ordering(self):
        # Testa se as operações são ordenadas corretamente(mais recente primeiro)

        op1 = Operation.objects.create(
            default_user=self.user,
            number1=10,
            number2=5,
            operation_type='soma',
            result=15
        )
        sleep(1)

        op2 = Operation.objects.create(
            default_user=self.user,
            number1=20,
            number2=10,
            operation_type='subtracao',
            result=10
        )

        sleep(1)

        op3 = Operation.objects.create(
            default_user=self.user,
            number1=30,
            number2=15,
            operation_type='multiplicacao',
            result=450
        )

        all_op = Operation.objects.all()
        self.assertEqual(list(all_op), [op3, op2, op1])

    def test_operacao_fk_on_delete(self):
        Operation.objects.create(
            default_user=self.user,
            number1=10,
            number2=5,
            operation_type='soma',
            result=15
        )

        self.assertEqual(Operation.objects.count(), 1)
        self.user.delete()
        self.assertEqual(Operation.objects.count(), 0)


class ViewTest(TestCase):

    def setUp(self):
        self.client = Client()  # Cliente de teste para fazer requisições HTTP
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )

    def testar_login(self):
        # Testa o login de um usuário válido
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        # Redirecionamento após login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('calculadora'))

    def test_salvar_operacao_ajax(self):
        # Testa o salvamento de operação via AJAX
        self.client.login(username='testuser', password='testpassword')
        data = {
            'number1': 10,
            'number2': 5,
            'operation_type': 'soma',
            'result': 15
        }
        response = self.client.post(
            reverse('save_operation'),
            json.dumps(data),
            content_type='application/json',
            HTTP_X_CSRFTOKEN='dummytoken'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Operation.objects.count(), 1)
        self.assertEqual(Operation.objects.first().result, 15)
        self.assertTrue(json.loads(response.content)['success'])

    def testar_limpar_historico(self):
        # Testa o limpar histórico
        self.client.login(username='testuser', password='testpassword')
        Operation.objects.create(
            default_user=self.user,
            number1=10,
            number2=5,
            operation_type='soma',
            result=15
        )

        self.assertEqual(Operation.objects.count(), 1)

        response = self.client.post(
            reverse('clear_history'),
            HTTP_X_CSRFTOKEN='dummytoken'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Operation.objects.count(), 0)
        self.assertTrue(json.loads(response.content)['success'])
