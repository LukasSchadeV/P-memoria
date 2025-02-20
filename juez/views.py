from django.shortcuts import render, get_object_or_404
from .models import Problema, Tag
import subprocess
import tempfile
import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


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

def autocomplete_problemas(request):
    """ Retorna sugerencias de problemas según el texto ingresado """
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Solo AJAX
        query = request.GET.get('q', '').strip()
        
        print("🔍 Recibida consulta:", query)  # 📌 Depuración en terminal

        problemas = Problema.objects.filter(titulo__icontains=query)[:5]  # Buscar en títulos
        sugerencias = list(problemas.values_list('titulo', flat=True))

        print("📋 Resultados encontrados:", sugerencias)  # 📌 Depuración en terminal
        
        return JsonResponse({"sugerencias": sugerencias}, safe=False)

    return JsonResponse({"sugerencias": []}, safe=False)



def lista_problemas(request):
    """ Muestra la lista de problemas con opción de búsqueda y filtro por tags """
    query = request.GET.get("q", "").strip()
    tag_filter = request.GET.get("tag", "").strip()

    problemas = Problema.objects.all()
    
    # Filtrar por título si hay búsqueda
    if query:
        problemas = problemas.filter(titulo__icontains=query)

    # Filtrar por tag si se seleccionó uno
    if tag_filter:
        problemas = problemas.filter(tags__nombre__iexact=tag_filter)

    tags = Tag.objects.all()

    return render(request, 'inicio/index.html', {'problemas': problemas, 'tags': tags, 'query': query, 'tag_filter': tag_filter})

def detalle_problema(request, problema_id):
    """ Muestra los detalles de un problema específico """
    problema = get_object_or_404(Problema, id=problema_id)
    return render(request, 'juez/detalle_problema.html', {'problema': problema})

@csrf_exempt
def execute_c_code(request, problema_id):
    """Ejecuta el código con la entrada de ejemplo del problema"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            code = data.get("code", "")

            if not code:
                return JsonResponse({"output": "Error: No code provided"}, status=400)

            problema = get_object_or_404(Problema, id=problema_id)
            entrada_ejemplo = problema.entrada_ejemplo.strip()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".c") as temp_source:
                temp_source.write(code.encode())
                temp_source_path = temp_source.name

            executable_path = temp_source_path.replace(".c", "")

            # ✅ Compilar código C
            compile_process = subprocess.run(
                ["gcc", temp_source_path, "-o", executable_path],
                capture_output=True, text=True
            )

            if compile_process.returncode != 0:
                return JsonResponse({"output": "Compilation Error:\n" + compile_process.stderr}, status=401)

            # ✅ Crear archivo temporal con la entrada de ejemplo
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_input:
                temp_input.write((entrada_ejemplo + "\n").encode())
                temp_input_path = temp_input.name

            # ✅ Ejecutar el código con la entrada de ejemplo
            execute_process = subprocess.run(
                [executable_path],
                stdin=open(temp_input_path, "rb"),
                capture_output=True,
                text=True,
                timeout=5
            )

            # ✅ Capturar la salida normal y de error
            output = execute_process.stdout + execute_process.stderr

            # Limpiar archivos temporales
            os.remove(temp_input_path)

            return JsonResponse({"output": output.strip()}, status=200)

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

            # ✅ Separar los casos de prueba correctamente
            entradas_prueba = [entrada.strip().replace("\r\n", "\n") for entrada in problema.entradas_prueba.split("@@@")]
            salidas_esperadas = [salida.strip().replace("\r\n", "\n") for salida in problema.salidas_esperadas.split("@@@")]

            if len(entradas_prueba) != len(salidas_esperadas):
                return JsonResponse({"status": 403, "message": "Mismatch between input and expected output count"}, status=403)

            # ✅ Crear archivo temporal con el código fuente
            with tempfile.NamedTemporaryFile(delete=False, suffix=".c") as temp_source:
                temp_source.write(code.encode())
                temp_source_path = temp_source.name

            executable_path = temp_source_path.replace(".c", "")

            # ✅ Compilar código C
            compile_process = subprocess.run(
                ["gcc", temp_source_path, "-o", executable_path],
                capture_output=True, text=True
            )

            if compile_process.returncode != 0:
                error_message = "\n".join(
                    line for line in compile_process.stderr.split("\n") if not line.startswith(temp_source_path)
                ).strip()
                return JsonResponse({"status": 401, "message": f"Compilation Error:\n{error_message}"}, status=401)

            resultados = []
            for i, entrada in enumerate(entradas_prueba):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_input:
                    temp_input.write((entrada + "\n").encode())  # Asegurar que la entrada finaliza con un salto de línea
                    temp_input_path = temp_input.name

                # ✅ Ejecutar el código con entrada estándar (`stdin`)
                execute_process = subprocess.run(
                    [executable_path],
                    stdin=open(temp_input_path, "rb"),
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                # ✅ Normalizar la salida obtenida para evitar problemas de formato entre SOs
                actual_output = execute_process.stdout.strip().replace("\r\n", "\n") if execute_process.stdout else "Salida vacía"
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

