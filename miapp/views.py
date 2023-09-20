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
        cannyvalue = request.POST.get('canny')
        umbral1 = int(request.POST.get('umbral1'))
        umbral2 = int(request.POST.get('umbral2'))
        cannyMin = int(request.POST.get('cannyMin'))
        cannyMax = int(request.POST.get('cannyMax'))
        # ALMACENAMIENTO DE LA IMAGEN
        ruta_carpeta = os.path.join("miapp", "static", "image")
        ruta_archivo = os.path.join(ruta_carpeta, "imagen.tif")
        ruta_archivo2 = os.path.join(ruta_carpeta, "resultado.jpg")

        with open(ruta_archivo, 'wb') as archivo_destino:
            for chunk in imagen.chunks():
                archivo_destino.write(chunk)

        # PROCESAMIENTO DE IMAGENES
        n,m = 0,0

        #OPERADORES PUNTUALES
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
        
        # Función para aplicar el operador binarizado inverso
        def binarizado_inv(P):
            Q = (P<umbral1).astype(int)
            return Q
        
        def binarizado2Umbral(P):
            Q =((P >= umbral1) & (P<=umbral2)).astype(int)
            return Q

        def binarizado2Umbral_inv(P):
            Q = ((P < umbral1) | (P > umbral2)).astype(int)
            return Q

        def filtrar3x3(I, M):
            Q = np.zeros((m, n))
            for i in range(1, m - 1):
                for j in range(1, n - 1):
                    P = I[i - 1:i + 2, j - 1:j + 2]
                    Q[i, j] = (P * M).sum()
            return Q
        
        def resaltarborde(I,Mh,Mv):
            Q = np.zeros((m,n))
            for i in range(1,m-1):
                for j in range(1,n-1):
                    P = I[i-1:i+2,j-1:j+2]
                    Gx = (P*Mh).sum()
                    Gy = (P*Mv).sum()
                    Q[i,j] = (Gx*Gx + Gy*Gy)**0.5       
            return Q
        
        def canny(imgNP):
            gradiente_x = np.gradient(imgNP, axis=1)
            gradiente_y = np.gradient(imgNP, axis=0)
            gradiente_x_abs = np.abs(gradiente_x)
            gradiente_y_abs = np.abs(gradiente_y)
            gradiente_magnitud = np.sqrt(gradiente_x_abs**2 + gradiente_y_abs**2)
            umbral_min = cannyMin
            umbral_max = cannyMax
            bordes = ((gradiente_magnitud >= umbral_min) & (gradiente_magnitud <= umbral_max)).astype(int)
            imagen_bordes = Image.fromarray(np.uint8(bordes) * 255)  
            return imagen_bordes




        #OPERADORES CON VECINDAD:
        promedio = (1.0/9.0) * np.ones((3, 3))
        gaussiano = np.array([[1.0/16.0, 2.0/16.0, 1.0/16.0],
                            [2.0/16.0, 4.0/16.0, 2.0/16.0],
                            [1.0/16.0, 2.0/16.0, 1.0/16.0]])

        prewittH = np.array([[1.0,0.0,-1.0],
                     [1.0,0.0,-1.0],
                     [1.0,0.0,-1.0]])
        
        prewittV = np.array([[-1.0,-1.0,-1.0],
                            [0.0,0.0,0.0],
                            [1.0,1.0,1.0]])
        
        sobelH = np.array([[1.0,0.0,-1.0],
                        [2.0,0.0,-2.0],
                        [1.0,0.0,-1.0]])
        
        sobelV = np.array([[-1.0,-2.0,-1.0],
                            [0.0,0.0,0.0],
                            [1.0,2.0,1.0]])
        
        robertH = np.array([[0.0,0.0,0.0],
                        [0.0,1.0,0.0],
                        [0.0,0.0,-1.0]])

        robertV = np.array([[0.0,0.0,0.0],
                            [0.0,0.0,1.0],
                            [0.0,-1.0,0.0]])


        imgGray = Image.open(ruta_archivo).convert('L')
        imgNP = np.array(imgGray)

        print(operador,"canny:",cannyvalue)
        if operador == 'identidad':
            resultado = identidad(imgNP)
            img = Image.fromarray(resultado)
            if cannyvalue == "1":
                print("se aplico canny")
                img = canny(resultado)
            img = img.convert('RGB')
            img.save(ruta_archivo2)
            img.close()

        elif operador == 'invNegativo':
            resultado = inverso(imgNP)
            img = Image.fromarray(resultado)
            if cannyvalue == "1":
                print("se aplico canny")
                img = canny(resultado)
            img = img.convert('RGB')
            img.save(ruta_archivo2)
            img.close()

        elif operador == 'umbral':
            resultado = binarizado(imgNP)
            img = Image.fromarray(resultado*255)
            if cannyvalue == "1":
                print("se aplico canny")
                img = canny(resultado)
            img = img.convert('RGB')
            img.save(ruta_archivo2)
            img.close()

        elif operador == 'invUmbral':
            resultado = binarizado_inv(imgNP)
            img = Image.fromarray(resultado*255)
            if cannyvalue == "1":
                print("se aplico canny")
                img = canny(resultado)
            img = img.convert('RGB')
            img.save(ruta_archivo2)
            img.close()

        elif operador == 'umbrales':
            resultado = binarizado2Umbral(imgNP)
            img = Image.fromarray(resultado*255)
            if cannyvalue == "1":
                print("se aplico canny")
                img = canny(resultado)
            img = img.convert('RGB')
            img.save(ruta_archivo2)
            img.close()

        elif operador == 'umbralesInv':
            resultado = binarizado2Umbral_inv(imgNP)
            img = Image.fromarray(resultado*255)
            if cannyvalue == "1":
                print("se aplico canny")
                img = canny(resultado)
            img = img.convert('RGB')
            img.save(ruta_archivo2)
            img.close()

        elif operador == "filtroPromedio":
            n,m = imgGray.size
            resultado = filtrar3x3(imgNP, promedio)
            img = Image.fromarray(resultado)
            if cannyvalue == "1":
                print("se aplico canny")
                img = canny(resultado)
            img = img.convert('RGB')
            img.save(ruta_archivo2)
            img.close()

        elif operador == "filtroGaussiano":
            n,m = imgGray.size
            resultado = filtrar3x3(imgNP, gaussiano)
            img = Image.fromarray(resultado)
            if cannyvalue == "1":
                print("se aplico canny")
                img = canny(resultado)
            img = img.convert('RGB')
            img.save(ruta_archivo2)
            img.close()

        elif operador == "prewitt":
            n,m = imgGray.size
            resultado = resaltarborde(imgNP,prewittH,prewittV)
            img = Image.fromarray(resultado)
            if cannyvalue == "1":
                print("se aplico canny")
                img = canny(resultado)
            img = img.convert('RGB')
            img.save(ruta_archivo2)
            img.close()

        elif operador == "sobel":
            n,m = imgGray.size
            resultado = resaltarborde(imgNP,sobelH,sobelV)
            img = Image.fromarray(resultado)
            if cannyvalue == "1":
                print("se aplico canny")
                img = canny(resultado)
            img = img.convert('RGB')
            img.save(ruta_archivo2)
            img.close()

        elif operador == "roberts":
            n,m = imgGray.size
            resultado = resaltarborde(imgNP,robertH,robertV)
            img = Image.fromarray(resultado)
            if cannyvalue == "1":
                print("se aplico canny")
                img = canny(resultado)
            img = img.convert('RGB')
            img.save(ruta_archivo2)
            img.close()
        else:
            resultado = identidad(imgNP)
            img = Image.fromarray(resultado)
            if cannyvalue == "1":
                print("se aplico canny")
                img = canny(resultado)
            img = img.convert('RGB')
            img.save(ruta_archivo2)
            img.close()

     

        resultado = f"Imagen recibida y procesada con el operador {operador}"
        return JsonResponse({'resultado': resultado})
    
def home(request):
    return render(request, "index.html")

@csrf_exempt
def eliminar(request):
    print("eliminacion")
    if request.method == 'POST':
        nombre_imagen = "resultado.jpg"  
        ruta_carpeta = "miapp\static\image"  
        ruta_archivo = os.path.join(ruta_carpeta, nombre_imagen)

        try:
            os.remove(ruta_archivo)
            resultado = f"Imagen {nombre_imagen} eliminada correctamente"
        except FileNotFoundError:
            resultado = f"La imagen {nombre_imagen} no fue encontrada"

        return JsonResponse({'resultado': resultado})
