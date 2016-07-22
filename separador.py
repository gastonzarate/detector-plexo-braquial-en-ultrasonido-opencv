import os
import cv2
import re
import ReducirRuido
import numpy as np
from skimage import io

rutaCarpeta = "Entrenamiento"
lista_img = [],[]
rutaPos = os.path.join(rutaCarpeta,"pos")
rutaNeg = os.path.join(rutaCarpeta,"neg")
archPos = os.path.join(rutaCarpeta,"pos.info")
archNeg = os.path.join(rutaCarpeta,"neg.info")
rutaImg = os.path.join("DatosNormalizados","train")
#Margen a agregar a las imagenes ademas de la mascara
margen = 5

def compara(a, b):
    numeros_a = map(int, re.findall("\d+", a))
    numeros_b = map(int, re.findall("\d+", b))

    if len(numeros_a) == 0:
        return 1

    if numeros_a < numeros_b:
        retorno = -1
    elif numeros_a == numeros_b:
        retorno = 0
    else:
        retorno = 1

    return retorno

def listarImagenes():
    for base, dirs, files in os.walk(rutaImg):
        files.sort(cmp=compara)
        for name in files:
            if 'mask' in name:
                lista_img[1].append(name)
            else:
                lista_img[0].append(name)
    return lista_img

def crearDirectorios():
    # Pregunta si existen los directorios o archivos para eliminarlos
    if os.path.exists(rutaCarpeta):
        os.rmdir(rutaPos)

    # Crea las carpetas
    os.makedirs(rutaCarpeta)
    os.makedirs(rutaPos)
    os.makedirs(rutaNeg)
    archivoP = open(archPos, 'w')
    archivoP.close()
    archivoN = open(archNeg, 'w')
    archivoN.close()

def separarPosNeg():
    # Pregunta si existen los directorios o archivos para eliminarlos
    if os.path.exists(rutaImg):

        crearDirectorios()
        # Crea los archivos

        # Abre los archivos para escribir en ellos
        archivoP = open(archPos, 'a')
        archivoN = open(archNeg, 'a')

        lista = listarImagenes()
        iNeg = 1
        iPos = 1

        for mascara in lista[1]:
            #mask = cv2.imread('train/'+mascara,0)
            mask = io.imread(rutaImg+mascara,as_grey=True)
            index = lista[1].index(mascara)
            item = lista[0].__getitem__(index)
            imagen = cv2.imread(rutaImg+item,cv2.IMREAD_GRAYSCALE)
            nomArch = item.split('.')[0]

            if mask.any()!=0:
                mask, thresh = cv2.threshold(mask, 15, 255, cv2.THRESH_BINARY)
                mask, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                # Al encontrarse contorno se busca el de mayor area
                areas = [cv2.contourArea(c) for c in contours]
                max_index = np.argmax(areas)
                cnt = contours[max_index]
                # Se obtiene la recta correspondiente al contorno
                x, y, w, h = cv2.boundingRect(cnt)
                # Se almacena como positiva
                io.imsave(os.path.join(rutaPos, nomArch + ".png"), imagen)
                #Agrega margen a las imagenes
                x = x - margen
                y = y - margen
                h = h + margen*2
                w = w + margen*2

                archivoP.write(os.path.join(rutaPos, nomArch + ".png") + ' 1 %d %d %d %d \n' % (x, y, h, w))

            else:
                io.imsave(os.path.join(rutaNeg, nomArch + ".png"), imagen)
                archivoN.write(os.path.join(rutaNeg, nomArch + ".png") + '\n')

        # Se cierran los archivos
        archivoN.close()
        archivoP.close()

    else:
        print "Debe crear una carpeta DatosNormalizados con las imagenes normalizadas dentro"


separarPosNeg()
