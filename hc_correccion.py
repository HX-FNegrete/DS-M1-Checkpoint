import os
import shutil
from importlib import reload

lista_alumnos = os.listdir('./')
#lista_alumnos = ['lopezdar222', 'lopezdar2220']

i = 0
for alumno in lista_alumnos:
    if (os.path.isdir(alumno)):
        if(os.path.isfile('./'+alumno+'/checkpoint.py')):
            if(os.path.isfile('./'+alumno+'/tests_correccion.py')):
                os.remove(alumno+'/tests.py')
            shutil.copyfile('tests.py', alumno+'/tests.py')
            i += 1

i = 0
for alumno in lista_alumnos:
    if (os.path.isdir(alumno)):
        if(os.path.isfile('./'+alumno+'/checkpoint.py')):
            print('Ejecutando alumno:', alumno)
            os.chdir('./'+alumno)
            os.system('python tests.py')
            os.chdir('../')
            i += 1

resultado_total = open('resultado_test.csv', 'a')
i = 0
for alumno in lista_alumnos:
    if (os.path.isdir(alumno)):
        if(os.path.isfile('./'+alumno+'/resultado_test.csv')):
            resultado_alumno = open('./'+alumno+'/resultado_test.csv', 'r')
            j = 0
            for linea in resultado_alumno:
                if ((j > 0) and (j < 3)):
                    resultado_total.write(alumno+','+linea)
                j+=1
            resultado_alumno.close()
            i += 1
resultado_total.close()
print('Se ejecturaron', i,'tests')