class mascarrilla:
    def __init__(self):
        self.tiempoEncola=0
        self.tiempoDeSalida=0

    def setTiempoEncola(self,tiempo):
        self.tiempoEncola=  self.tiempoEncola+tiempo

    def getTiempoEncola(self):
        return self.tiempoEncola


    def setTiempoDeSalida(self,tiempo):
        self.tiempoDeSalida=  self.tiempoDeSalida+tiempo

    def getTiempoDeSalida(self):
        return self.tiempoDeSalida