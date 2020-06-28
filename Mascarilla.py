class mask:
	def __init__(self):
		self.initial_clock = 0.0
		self.clock_next_event = 0.0 
		self.time_on_system = 0.0 
	
	def set_initial_clock(self, clock):
		self.initial_clock = clock
	
	def set_time_on_system(self, clock):
		self.time_on_system  = clock - self.initial_clock
	
	def get_time_on_system(self):
		return self.time_on_system
	
	def set_clock_next_event(self, clock):
		self.clock_next_event = clock
	
	def print_m(self):
		print("reloj inicial : ", self.initial_clock, " siguiente evento : ", self.clock_next_event, " tiempo en el sistema : ", self.time_on_system)


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
