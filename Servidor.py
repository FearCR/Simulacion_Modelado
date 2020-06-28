from queue import Queue

class servidor:
    # Inicializador, hay que agregar una variable para cada parte
    def __init__(self):
        self.TiempoOcupado=0
        self.TiempoDesocupado = 0
        self.ocupado=False
        self.colaMascarilla=Queue()
        self.mascarillaSiendoAtendida = None

    def setMascarillaSiendoAtendida(self, mascarilla):
        self.mascarillaSiendoAntendida = mascarilla

    def getMascarillaSiendoAtendida(self):
        return self.mascarillaSiendoAtendida

    def setTiempoOcupado(self,tiempo):
        self.TiempoOcupado= self.TiempoOcupado+tiempo

    def getTiempoOcupado(self):
        return self.TiempoOcupado

    def setTiempoDesocupado(self,tiempo):
        self.TiempoDesocupado=self.TiempoDesocupado+tiempo

    def getTiempoOcupado(self):
        return self.TiempoDesocupado

    def setOcupado(self,ocupado):
        self.ocupado=ocupado

    def getOcupado(self):
        return self.ocupado

    def encolarMascarrilla(self,mascarilla):
        self.colaMascarilla.put(mascarilla)

    def desencolarMascarrilla(self):
        return self.colaMascarilla.get()
