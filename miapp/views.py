from django.shortcuts import render
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
import os
import numpy as np
from PIL import Image

@csrf_exempt
def prueba(request):
    if request.method == 'POST':
        # RECOLECCION DE DATOS
        imagen = request.FILES.get('imagen')
        operador = request.POST.get('operador')
        canny = request.POST.get('canny')
        umbral1 = int(request.POST.get('umbral1'))
        umbral2 = int(request.POST.get('umbral2'))

        # ALMACENAMIENTO DE LA IMAGEN
        ruta_carpeta = os.path.join("miapp", "static", "image")
        ruta_archivo = os.path.join(ruta_carpeta, "imagen.tif")
        ruta_archivo2 = os.path.join(ruta_carpeta, "resultado.jpg")

        with open(ruta_archivo, 'wb') as archivo_destino:
            for chunk in imagen.chunks():
                archivo_destino.write(chunk)

        # PROCESAMIENTO DE IMAGENES

        # Función para aplicar el operador de identidad
        def identidad(P):
            Q = P
            return Q

        # Función para aplicar el operador inverso
        def inverso(P):
            Q = 255 - P
            return Q

        # Función para aplicar el operador binarizado
        def binarizado(P):
            Q = (P >= umbral1).astype(int)
            return Q
        
        def binarizado_inv(P):
            Q = (P<umbral1).astype(int)
            return Q
        imgGray = Image.open(ruta_archivo).convert('L')
        imgNP = np.array(imgGray)

        print(operador)
        if operador == 'identidad':
            resultado = identidad(imgNP)
        elif operador == 'inverso':
            resultado = inverso(imgNP)
        elif operador == 'umbral':
            resultado = binarizado(imgNP)
        elif operador == 'invUmbral':
            resultado = binarizado_inv(imgNP)
        else:
            resultado = imgNP  # Si no se selecciona ningún operador, se mantiene la imagen original

        img = Image.fromarray(resultado*255)
        img = img.convert('RGB')  # Convierte la imagen a RGB
        img.save(ruta_archivo2)
        img.close()

        resultado = f"Imagen recibida y procesada con el operador {operador}"
        return JsonResponse({'resultado': resultado})
    
def home(request):
    return render(request, "index.html")

@csrf_exempt
def eliminar(request):
    if request.method == 'POST':
        nombre_imagen = "imagen.jpg"  
        ruta_carpeta = "miapp\static\image"  
        ruta_archivo = os.path.join(ruta_carpeta, nombre_imagen)

        try:
            os.remove(ruta_archivo)
            resultado = f"Imagen {nombre_imagen} eliminada correctamente"
        except FileNotFoundError:
            resultado = f"La imagen {nombre_imagen} no fue encontrada"

        return JsonResponse({'resultado': resultado})
