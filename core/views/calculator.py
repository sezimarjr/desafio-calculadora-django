from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from core.models import Operation
from django.http import JsonResponse
import json


@login_required(login_url='login')
def calculator(request):
    result = None
    operation_history = []

    if request.method == 'POST':
        try:
            number1 = float(request.POST.get('number1'))
            number2 = float(request.POST.get('number2'))
            operation_type = request.POST.get('operation_type')

            if operation_type == 'soma':
                result = number1 + number2
            elif operation_type == 'subtracao':
                result = number1 - number2
            elif operation_type == 'multiplicacao':
                result = number1 * number2
            elif operation_type == 'divisao':
                if number2 != 0:
                    raise ValueError('Divisão por zero.')
                result = number1 / number2
            else:
                raise ValueError('Operação inválida.')

             # Salva a operação no banco de dados
            Operation.objects.create(
                default_user=request.user,
                number1=number1,
                number2=number2,
                operation_type=operation_type,
                result=result
            )

        except ValueError as e:
            result = f"Erro: {e}"
        except Exception as e:
            result = f"Ocorreu um erro inesperado: {e}"

    # Recupera o histórico de operações do usuário logado
    # ordered by -data_operacao (mais recente primeiro) já está no Meta do model
    operation_history = Operation.objects.filter(
        default_user=request.user).order_by('-operation_date')[:10]

    context = {
        'result': result,
        'operation_history': operation_history,
    }
    return render(request, 'calculator.html', context)


@login_required()
def save_operation(request):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            number1 = data.get("number1")
            number2 = data.get("number2")
            operation_type = data.get("operation_type")
            result = data.get("result")

            # Verifica se todos os campos necessários estão presentes
            if None in [number1, number2, operation_type, result]:
                return JsonResponse({"success": False, "error": "Dados inválidos"}, status=400)

            # Valida os tipos de operação permitidos
            valid_operations = ['soma', 'subtracao',
                                'multiplicacao', 'divisao']
            if operation_type not in valid_operations:
                return JsonResponse({"success": False, "error": "Tipo de operação inválido"}, status=400)

            # Salva a operação no banco de dados
            operation = Operation.objects.create(
                default_user=request.user,
                number1=number1,
                number2=number2,
                operation_type=operation_type,
                result=result
            )

            return JsonResponse({
                "success": True,
                "new_operation": {
                    "number1": operation.number1,
                    "number2": operation.number2,
                    "operation_type": operation.operation_type,
                    "result": operation.result,
                    "operation_date": operation.operation_date.isoformat()

                }
            })

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "JSON inválido"}, status=400)
        except ValueError as e:
            return JsonResponse({"success": False, "error": f"Erro: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": f"Ocorreu um erro inesperado: {e}"}, status=500)

    return JsonResponse({"success": False, "error": "Método não permitido"}, status=400)


@login_required()
def clear_history(request):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            Operation.objects.filter(default_user=request.user).delete()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": f"Ocorreu um erro inesperado: {e}"}, status=500)

    return JsonResponse({"success": False, "error": "Método não permitido"}, status=400)
