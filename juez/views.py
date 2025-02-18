from django.shortcuts import render, get_object_or_404
from .models import Problema
import subprocess
import tempfile
import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

STATUS_CODES = {
    200: "OK",
    201: "ACCEPTED",
    400: "WRONG ANSWER",
    401: "COMPILATION ERROR",
    402: "RUNTIME ERROR",
    403: "INVALID FILE",
    404: "FILE NOT FOUND",
    408: "TIME LIMIT EXCEEDED"
}

def lista_problemas(request):
    """ Muestra la lista de problemas disponibles """
    problemas = Problema.objects.all()
    return render(request, 'juez/lista_problemas.html', {'problemas': problemas})

def detalle_problema(request, problema_id):
    """ Muestra los detalles de un problema específico """
    problema = get_object_or_404(Problema, id=problema_id)  # Si no existe, muestra error 404
    return render(request, 'juez/detalle_problema.html', {'problema': problema})

@csrf_exempt
def execute_c_code(request, problema_id):
    """Ejecuta el código sin verificar la salida"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            code = data.get("code", "")

            if not code:
                return JsonResponse({"output": "Error: No code provided"}, status=400)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".c") as temp_source:
                temp_source.write(code.encode())
                temp_source_path = temp_source.name

            executable_path = temp_source_path.replace(".c", "")

            # Compilar código C
            compile_process = subprocess.run(
                ["gcc", temp_source_path, "-o", executable_path],
                capture_output=True, text=True
            )

            if compile_process.returncode != 0:
                return JsonResponse({"output": "Compilation Error:\n" + compile_process.stderr}, status=401)

            # Ejecutar código compilado
            execute_process = subprocess.run(
                [executable_path], capture_output=True, text=True, timeout=5
            )

            return JsonResponse({"output": execute_process.stdout + execute_process.stderr}, status=200)

        except subprocess.TimeoutExpired:
            return JsonResponse({"output": "Execution timed out."}, status=408)

        finally:
            os.remove(temp_source_path)
            if os.path.exists(executable_path):
                os.remove(executable_path)

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def submit_c_code(request, problema_id):
    """Ejecuta y compara la salida del código con múltiples casos de prueba"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            code = data.get("code", "")

            if not code:
                return JsonResponse({"status": 403, "message": "Invalid submission"}, status=403)

            problema = get_object_or_404(Problema, id=problema_id)
            entradas_prueba = problema.entradas_prueba.strip().split("\n")
            salidas_esperadas = problema.salidas_esperadas.strip().split("\n")

            if len(entradas_prueba) != len(salidas_esperadas):
                return JsonResponse({"status": 403, "message": "Mismatch between input and expected output count"}, status=403)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".c") as temp_source:
                temp_source.write(code.encode())
                temp_source_path = temp_source.name

            executable_path = temp_source_path.replace(".c", "")

            # Compilar código C
            compile_process = subprocess.run(
                ["gcc", temp_source_path, "-o", executable_path],
                capture_output=True, text=True
            )

            if compile_process.returncode != 0:
                # Filtrar las rutas del error de compilación
                error_message = compile_process.stderr
                error_message = "\n".join(
                    line for line in error_message.split("\n") if not line.startswith(temp_source_path)
                ).strip()

                return JsonResponse({"status": 401, "message": f"Compilation Error:\n{error_message}"}, status=401)

            resultados = []
            for i, entrada in enumerate(entradas_prueba):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_input:
                    temp_input.write(entrada.encode())
                    temp_input_path = temp_input.name

                # Ejecutar código con entrada estándar
                execute_process = subprocess.run(
                    [executable_path],
                    stdin=open(temp_input_path, "r"),
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                # Normalizar la salida eliminando espacios y saltos de línea extra
                actual_output = execute_process.stdout.strip()
                expected_output = salidas_esperadas[i].strip()

                if actual_output == expected_output:
                    resultados.append(f"Test {i + 1}: ✅ Correcto")
                else:
                    resultados.append(f"Test {i + 1}: ❌ Incorrecto (Esperado: {repr(expected_output)}, Obtenido: {repr(actual_output)})")

                os.remove(temp_input_path)

            return JsonResponse({"status": 201, "message": "\n".join(resultados)}, status=201)

        except subprocess.TimeoutExpired:
            return JsonResponse({"status": 408, "message": "Execution timed out"}, status=408)

        except Problema.DoesNotExist:
            return JsonResponse({"status": 404, "message": "Problem not found"}, status=404)

        finally:
            os.remove(temp_source_path)
            if os.path.exists(executable_path):
                os.remove(executable_path)

    return JsonResponse({"status": 403, "message": "Invalid request"}, status=403)
