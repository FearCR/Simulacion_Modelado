class mascarilla:
    def __init__(self):

        self.initial_clock = 0

    '''
    @Descripcion: Se encarga de colocar en "self.initial_clock", el tiempo 
    en que la mascarilla entro al sistema.
    @utiliza: self.initial_clock
    @modifica: self.initial_clock
    '''
    def set_initial_clock(self, clock):
        self.initial_clock = clock

    '''
    @Descripcion: Se encarga de retornar el tiempo 
    en que la mascarilla entro al sistema.
    @utiliza: self.initial_clock
    @modifica: Nada
    '''
    def get_initial_clock(self):
        return self.initial_clock

