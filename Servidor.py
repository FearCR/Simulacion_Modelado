from queue import Queue
from Mascarilla import mascarilla

class servidor:

    def __init__(self):
        self.TiempoOcupado=0
        self.TiempoDesocupado = 0
        self.ocupado=False
        self.colaMascarilla=Queue()
        self.mascarillaSiendoAtendida = mascarilla()

    '''
    @Descripcion: Se encarga de colocar en  self.mascarillaSiendoAtendida
    la mascarilla que esta haciendo atendida
    @utiliza: self.mascarillaSiendoAtendida
    @modifica: self.mascarillaSiendoAtendida
    '''
    def setMascarillaSiendoAtendida(self, mascarilla):
        self.mascarillaSiendoAtendida = mascarilla

    '''
    @Descripcion: Se encarga de retornar la mascarilla que está haciendo
    atendida por el servidor
    @utiliza:self.mascarillaSiendoAtendida
    @modifica: Nada
    '''
    def getMascarillaSiendoAtendida(self):
        return self.mascarillaSiendoAtendida

    '''
    @Descripcion:Se encarga de sumar los tiempos que el servidor ha estado
    ocupado en la variable self.TiempoOcupado
    @utiliza: self.TiempoOcupado
    @modifica:Nada
    '''
    def setTiempoOcupado(self,tiempo):
        self.TiempoOcupado= self.TiempoOcupado+tiempo

    '''
    @Descripcion:Retorna el tiempo que el servidor ha estado ocupado
    @utiliza: self.TiempoOcupado
    @modifica: Nada
    '''
    def getTiempoOcupado(self):
        return self.TiempoOcupado

    '''
    @Descripcion: Se modificar el valor self.ocupado, ya sea
    True para cuando esta ocupado o False cuando esta desocupado
    @utiliza:self.ocupado
    @modifica:self.ocupado
    '''
    def setOcupado(self,ocupado):
        self.ocupado=ocupado

    '''
    @Descripcion: Se encarga de retornar la longitud de la cola
    @utiliza: self.colaMascarilla
    @modifica: Nada
    '''
    def getLongitudCola(self):
        return self.colaMascarilla.qsize()

    '''
    @Descripcion: Se encarga de retornar si el servidor se encuentra 
    ocupado
    @utiliza:self.ocupado, que es un valor booleano
    @modifica:Nada
    '''
    def getOcupado(self):
        return self.ocupado

    '''
    @Descripcion:Se encarga de encolar la mascarilla 
    @utiliza: colaMascarilla
    @modifica: colaMascarilla
    '''
    def encolarMascarrilla(self,mascarilla):
        self.colaMascarilla.put(mascarilla)

    '''
    @Descripcion: Se encarga de desencolar la mascarilla y retornarla
    @utiliza: colaMascarilla
    @modifica:Nada
    '''
    def desencolarMascarrilla(self):
        return self.colaMascarilla.get()