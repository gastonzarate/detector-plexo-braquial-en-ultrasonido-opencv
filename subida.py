import os
import cv2
import shutil

rutaCarpeta = "subida"
ruta = os.path.join(rutaCarpeta, "submission.csv")
rutaImg = os.path.join("DatosNormalizados", "test")
clasificador = os.path.join("Clasificadores",'cascade2.xml')
ancho = 580
alto = 420
margen = 5

# Si existe el directorio carpeta la elimina
if os.path.exists(rutaCarpeta):
    shutil.rmtree(rutaCarpeta, ignore_errors=True)
else:
    os.makedirs(rutaCarpeta)
# Crea el archivo de subida
archivo = open(ruta, 'w')
archivo.close()
# Abre el archivo de subida
archivo = open(ruta, 'a')
archivo.write("img,pixels")

numImg = 1

#Carga el clasificador
cascade = cv2.CascadeClassifier(clasificador)

#Recorre las imagenes, las clasifica y guarda su solucion
for base, dirs, files in os.walk(rutaImg):
    for name in files:
        if not 'mask' in name:
            print numImg

            #Carla la imagen
            img = cv2.imread(os.path.join(base, name))

            #cv2.imshow("imagen",img)
            #cv2.waitKey(0)

            #Detecta las imagenes
            pa = cascade.detectMultiScale(
                img,
                scaleFactor=1.1,
                minNeighbors=9,
                minSize=(10, 10),
                maxSize=(200, 200),
                flags=0)
            #Guarda en el archivo su numero
            archivo.write("%d," % numImg)
            #Guarda en el archivo la primera deteccion
            for (x, y, w, h) in pa:
                x = x + margen
                y = y + margen
                h = h - margen*2
                w = w - margen*2
                com = (x - 1) * ancho + y
                fin = ((x - 1) + w) * ancho + y
                for i in range(com, fin, alto):
                    archivo.write('%d %d ' % (i,h))
                break
            archivo.write(" \n")
            numImg = numImg + 1
archivo.close()





