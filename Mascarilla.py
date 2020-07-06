class mascarilla:
    def __init__(self):
        self.tiempoEncola = 0
        self.tiempoDeSalida = 0
        self.initial_clock = 0

    def set_initial_clock(self, clock):
        self.set_initial_clock = clock

    def get_initial_clock(self):
        return self.initial_clock

    def setTiempoEncola(self, tiempo):
        self.tiempoEncola = self.tiempoEncola + tiempo

    def getTiempoEncola(self):
        return self.tiempoEncola

    def setTiempoDeSalida(self, tiempo):
        self.tiempoDeSalida = self.tiempoDeSalida + tiempo

    def getTiempoDeSalida(self):
        return self.tiempoDeSalidaalida