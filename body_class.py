# -*- coding: utf-8 -*-
"""
Created on Sat May 21 23:36:24 2022

@author: Radek
"""
import numpy as np

class Body ():
    ''' Cuerpo para el problema de los N-cuerpos. Calcula la interacción entre cuerpos 
    por medio de las ecuaciones de gravedad de Newton.
    Datos de inicialización :
        r_vect  list    Vector de posición incial. 
        v_vect  list    Vector de velocidad inicial.
        M       float   Masa del cuerpo.
        
    Se tiene constante de gravedad de Newton como G = 1. 
    Se recomienda reescalar a la unidad datos introducidos. 
    
    NOTA: Todos los objetos creados interactuaran entre sí. Se guarda lista de los 
    objetos creados. 
    '''
    
    G =1  # Tomamos la constante gravitatoria como 1.
    # Guardamos registro de las instancias de la clases para tenerlas en cuenta en  la simulación
    instances = []  
    
    def __init__(self, r_vect : list, v_vect : list , M=1):
        
        self.r = np.array(r_vect)
        self.v = np.array(v_vect) 
        self.m = M 
        
        self.y_0 = np.array([r_vect,v_vect])
        
        # Registramos los objetos creados.
        Body.instances.append(self) 
        self.r0 = np.array(r_vect)
        self.v0 = np.array(v_vect)
        
    def acc(self, r_pos):
        '''
        Calcula la acelaración que sufre el cuerpo debido a la interacción con los 
        demas cuerpos. Realiza los calculos según la ecuación de gravedad de Newton
        '''
        a=0
        # Sumamos todas las interacciones entre los diferentes cuerpos 
        for bd in Body.instances: 
            # evitamos el propio cuerpo en el computo de la aceleración.
            if not bd is self:  
                r = np.linalg.norm(bd.r - r_pos)
                
                # Evitamos que las particulas se acerquen mucho entre ellas
                # para evitar que la función llegue a la asintonta |r| =0 
                if r < 10 : 
                    r = 10
                    
                a += self.G* bd.m * (bd.r - r_pos)/ (r**3)

        return a
    
    def __call__(self, _, y):
        
        # Actualizamos los valores de la posición y de la velocidad. 
        setattr(self, 'r', np.array(y[1]))
        setattr(self, 'v', self.acc(np.array(y[0])))
        
        return np.array([y[1], self.acc(y[0])])  
    
    def __repr__(self):
      return f'Body:\n r_vect = {self.r},\nv_vect = {self.v},\nMass = {self.m}'
  
    
    def add_perturbation_init_Condit(self, sigma= 0.859):
        
        for vect, attr in zip([self.r0, self.v0],['r0','v0']) :
            nvect = []
            for axis in vect:
                if axis == 0:
                    nvect.append (0)
                else:
                    nvect.append ( np.random.normal(axis, sigma) )
            
            setattr(self, attr, np.array(nvect))
            
    def add_mass_perturbation(self, sigma = 0.1):
        setattr(self, 'm', np.random.normal(self.m, sigma))

    @staticmethod
    def random_body_generator(n = 3):
        '''
        Genera N: int cuerpos en posiciones y velocidades aleatorias
        '''
        for i in range(n):
          r = np.random.randint(-15,15,size=(3))
          v = np.random.rand(3)
          _ = Body(r,v,M= 20)
    
    @staticmethod
    def body_generator(vect : list):
        '''
        Genera cuerpos en posiciones y velocidades dadas en el vect.
        vect minimo 2D- list --> [ [r_vect],[v_vect] ]. Para más objetos colocar 
        más listas en el mismo orden --> [([r_vect1],[v_vect1], m),([r_vect2],[v_vect2],m) ...,
        ([r_vectN],[v_vectN], m)] 
        '''
        # if not len(vect)%2 == 0:
        #   print('Tamaño lista no adecuado')
        # else : 
        for r,v,m in vect:
          _ = Body(r, v, M= m)
      
    @classmethod
    def clear_instances(cls):
      cls.instances.clear()

    @staticmethod
    def copy_instances(): 
      ''' realiza una copia de los vectores posicon y velocidad del cuerpo en el 
      instante inicial'''
      vects =  []
      for bd in Body.instances: 
        vects.append((bd.r0.tolist(),bd.v0.tolist(), bd.m))

      return vects