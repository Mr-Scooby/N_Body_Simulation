# -*- coding: utf-8 -*-
"""
Created on Sat May 21 23:40:37 2022

@author: Radek
"""
import numpy as np
import body_class as body

class PB_NC():
    ''' Evolucion temporal del problema de N cuerpos.  Mínimo requerido 2.
            t_0 = 0  float   Instante incial de la simulación. 
            t_fin    float   Tiempo final de la simulación [s]
            N = 3    int     Número de cuerpos a simular --> Generados de forma aleatoria.
            
        *crear tantos objetos de tipo Body() como se desee para relizar la simulación 
        de la evolvución en el tiempo con cuerpos determinados.
        
        Cuando se calcule la trayectoria con el inntegrador, el vector resultante 
        tendra la siguente forma:
                                y[num, curpo, vect, axis]
        siendo num = numero de iteración; cuerpo = cuerpo al que corresponda (0,...,N)
        vect = vector que se desee (0 = posición, 1 = velocidad); axis= eje de coordenada (0 =x, 1=y, 2 = z)
        '''
            
    def __init__(self, t_fin=1000, t_0 = 0, N = 3):
        
        # if  N is not None or len(Body.instances)< 2: 
        #     print('body.instances = ', len(Body.instances)< 2)
        #     r = np.random.rand(1,3)*4
        #     r = r.tolist()
        #     v = np.random.rand(1,3)
        #     v = v.tolist()
        #     _ = [Body(r,v, M= np.random.rand()) for _ in range(N)]
            
        self.x_0 = t_0
        self.y_0 = np.array([bd.y_0 for bd in Body.instances])
        self.x_fin = t_fin
   
            
    def __call__(self, _, y):

        x = []
        # LLamamos a cada insatncia de un cuerpo para calcular sus nuevos vectores
        for idx,bd in enumerate(Body.instances): 
            x.append(bd(_,y[idx]))
        return np.array(x)

    def __repr__(self):
      txt = f'PVI de los N cuerpos. Simulación de tiempo comprendida entre {self.x_0} y {self.x_fin} s.\n \
      Datos iniciales: (r_vect, v_vect) \n{self.y_0}'  
      return txt