from random import random
from random import randrange
import math
from Servidor import servidor
from Mascarilla import mascarilla
from queue import Queue


MAX_VALUE = 999999999
TIME_TO_FINISH = 5000
clock = 0
queue_s1 = 0
queue_s2 = 0

#servidor de la sección 1
s1_server1 = servidor()
#servidor 1 de la sección 2 
s2_server1 = servidor()
#servidor 2 de la sección 2
s2_server2 = servidor()

#total de veces que se desea ejecutar la simulación antes de generar estadisticas. 
runs = 0

#tiempo que trabajan los servidores de ambas secciones. 
tiempoTrabajador1=0
tiempoTrabajador2=0
tiempoTrabajador3=0

paquetesListos=0
mascarillasDesechadas=0

#vector de eventos, como se puede observar corresponde a 7 campos, los cuales corresponde a los 7 eventos posibles. 
#cada posición corresponde a un evento, y se una lista, puesto que existen eventos en los que pueden haber más de un mismo evento del mismo tipo
events = [[MAX_VALUE],[],[],[MAX_VALUE],[],[MAX_VALUE],[MAX_VALUE]]
distributions = [-1,-1,-1,-1]

# se utilizan para simular el envio de mascarillas de la seccion 1 a la seccion 2 y viseversa. 
seccionUnoAseccionDos = Queue()
seccionDosAseccionUno = Queue()

#cola de mascarillas compartida por los 2 servidores de la sección 2. 
seccion2Queue = Queue()

#tiempo total que pasan las mascarillas en el sistema antes de salir del sistema con exito
time_masks = 0

#tiempo total que pasan las mascarillas en el sistema antes de ser desechadas. 
time_masks_Desechadas = 0


#parametros uniforme
uniform_param_1 = [0,0,0,0]
uniform_param_2 = [0,0,0,0]

#parametros normal
normal_param_1 = [0,0,0,0]
normal_param_2 = [0,0,0,0]

#parametros exponencial
exponential_param = [0,0,0,0]

#parametros convolucion
convolution_param_1 = [0,0,0,0]
convolution_param_2 = [0,0,0,0]
#parametros funcionDensidad
constanteK = [0,0,0,0]
a = [0,0,0,0]
b = [0,0,0,0]

totalMascarillasIngresan=0

#Estadisticas
'''
Descripción: este vector se utiliza para ir guardando los resultados correspondientes
a las estadisticas finales, cada posición corresponde a una estadistica concreta : 
0 : tiempo promedio que dura una mascarilla en el sistema antes de desecharse
1 : tiempo promedio que dura una mascarilla en el sistema antes de estar lista 
2 : tiempo que dura una mascarilla en el sistema 
3 : Eficiencia del sistema
4 : Equilibro del sistema
5[0] : tota de mascarillas desechadas 
5[1] : porcentaje equivalente a las mascarillas desechadas de 5[0]
5[2] : total de mascarillas listas 
5[3] : porcentaje equivalente a las mascarillas listas de 5[2]
5[4] : total de mascarillas que ingresaron al sistema
6[0] : porcentaje que pasa ocupado el servidor de la sección 1 durante toda la simulación 
6[1] : porcentaje que pasa ocupado el servidor1 de la seccion 2 durante toda la simulación
6[2] : porcentaje que pasa ocupado el servidor2 de la seccion 2 durante toda la simulación 
 
'''
Estadisticas = [0,0,0,0,0,[0,0,0,0,0],[0,0,0]]

#Para cacular la varianza
varianza=[]

#Para calcular la eficiencia del sistema
d2_accumulated = 0
d3_accumulated = 0
d4_accumulated = 0
counter_s1 = 0
counter_s2 = 0


#distribuciones

'''
@Descripción: Se encarga de calcular la distribución uniforme con el "a" 
y "b" que ingresa el usuario y retorna el resultado.
Para esto generamos un valor aleatorio con la funcion random()

@utiliza: Los parametros "a" y "b" que da el usuario
@modifica: Nada
'''
def uniforme(a,b):
    r=random()
    x=(b-a)*r+a
    return x
'''
@Descripción: Se encarga de calcular la distribución normal con el método directo
con el miu y la varianza que ingresa el usuario y retorna el resultado.
Para esto generamos dos valores aleatorios con la funcion random()
@utiliza: Los parametros "miu" y "varianza" que da el usuario
@modifica: Nada
'''
def directo(Mu,vari):
    r1 = random()
    r2 = random()
    Z=(-2*math.log(r1))
    Z=pow(Z,1/2)
    pi=math.pi
    Z=Z*(math.cos(2*pi*r2))
    SD = math.sqrt(vari)
    x = (SD * Z) + Mu
    if x<0:
        x=-1*x
    return x
'''
@Descripción: Se encarga de calcular la distribución exponencial con el
lambda que ingresa el usuario y retorna el resultado.
Para esto generamos un valor aleatorio con la funcion random().
@utiliza: El lambda que ingresa el usuario
@modifica:Nada
'''
def exponencial(lamb):
    r = random()
    x=(-math.log(1-r))/lamb
    return x
'''
@Descripción: Se encarga de calcular la distribución normal 
con el método de convolucióncon el miu y la varianza que 
ingresa el usuario y retorna el resultado.
Para esto generamos dos valores aleatorios con la funcion random()
@utiliza: Los parametros "miu" y "varianza" que da el usuario
@modifica: Nada
'''
def convolucion(Mu,vari):
    Z=0
    for i in range(1,13):
        r = random()
        Z=Z+(r-6)

    SD=math.sqrt(vari)
    x = (SD * Z) + Mu
    return x
'''
@Descripción: Se encarga de calcular la distribución con la funcion densidad
con la "constanteK" y "a", que da el usuario y retorna el resultado.
Para esto generamos un valor aleatorio con la funcion random().
@utiliza: La "constanteK" y "a", que da el usuario
@modifica: Nada 
'''
def funcionDensidad(constanteK,a,b):
    r = random()
    r=2*r

    a=math.pow(a,2)

    x=math.sqrt((r/constanteK)+a)

    return x


'''
@Descripción: Se encarga de generar el valor de la distribuciones que ha elegido
el usuario. 
@utiliza:
La variable ¨distributions¨, que es un arreglo de 4 posiciones, el cual almacena
las 4 distribuciones que eligió el usuario.
La variable  ¨index_distribution¨, se utiliza para conecer el valor de las
4 posiciones del arreglo y saber cuales distribuciones generar, como para
acceder a los parametros que digitó el usuario para dichas distribuciones,
como es el caso de las varibles que terminan en "_param".

@modifica:Nada
'''
def generate_distribution(index_distribution):
        if distributions[index_distribution] == 1:
            return uniforme(uniform_param_1[index_distribution],uniform_param_2[index_distribution])
        elif distributions[index_distribution] == 2:
            return directo(normal_param_1[index_distribution],normal_param_2[index_distribution])
        elif distributions[index_distribution] == 3:
            return exponencial(exponential_param[index_distribution])
        elif distributions[index_distribution] == 4:
            return convolucion(convolution_param_1[index_distribution],convolution_param_2[index_distribution])
        elif distributions[index_distribution] == 5:
            return funcionDensidad(constanteK[index_distribution],a[index_distribution],b[index_distribution])

'''
@Descripción: Se encarga de ejecutar y programar posteriormente el evento 1:
llega mascarilla del exterior a Seccion 1
@utiliza: 
events, para adelantar el reloj al tiempo en que ocurre el evento
s1_server1, pra saber si el servidor esta ocupado
@modifica: 
clock, cuando llega una mascarilla adelanta el reloj al momento de su llegada.
queue_s1, si el servidor esta ocupado, envia la mascarilla a la cola.
s1_server1, si esta desocupado, se ocupa.
totalMascarillasIngresan, aumenta el numero de mascarillas que ingresan al sistema.
d2_accumulated, acumula la distribucion d2 para calcular el Ws promedio de esta seccion.
counter_s1, aumenta la cantidad de veces que una mascarilla paso por esta seccion.
events, programa el evento 1 y el evento 4,
'''
#llega mascarilla del exterior a Seccion 1
def event_one():
    global clock
    global s1_server1
    global events
    global queue_s1
    global totalMascarillasIngresan
    global d2_accumulated
    global counter_s1
    clock = events[0][0]
    #print("e1",events,clock)
    if clock > 120:
        totalMascarillasIngresan=totalMascarillasIngresan+1

    if s1_server1.getOcupado() == False:
        s1_server1.setOcupado(True)
        #s1_server1 = True
        mask = mascarilla()					#creo la mascarilla.
        mask.set_initial_clock(clock)
        s1_server1.setMascarillaSiendoAtendida(mask)
        d2 = generate_distribution(1)
        d2_accumulated = d2_accumulated + d2
        counter_s1 = counter_s1 + 1
        #print("se esta imprimiendo d2 : ", d2)
        if clock > 120:
            s1_server1.setTiempoOcupado((d2))
        #print("se suma",d2)
        events[3][0] = clock + d2
        #print(s1_server1.getOcupado())
    else:
        #print("se encola")
        mask = mascarilla()
        mask.set_initial_clock(clock)
        s1_server1.encolarMascarrilla(mask)
        queue_s1 = queue_s1 + 1
    d1 = generate_distribution(0)
    events[0][0] = clock + d1
    #print(s1_server1.getOcupado())
    return
'''
@Descripción:Se encarga de ejecutar el evento 2: llegan 2 mascarillas de la seccion 2 servidor1 a la seccion 1
@utiliza:
s1_server1, para saber si el servidor esta ocupado
events, para adelantar el reloj al tiempo en que ocurre el evento
@modifica:
clock, cuando llega una mascarilla adelanta el reloj al momento de su llegada.
queue_s1, si el servidor esta ocupado, envia la mascarilla a la cola.
s1_server1, si esta desocupado, se ocupa.
d2_accumulated, acumula la distribucion d2 para calcular el Ws promedio de esta seccion.
counter_s1, aumenta la cantidad de veces que una mascarilla paso por esta seccion.
events, programa el evento 4.
seccionDosAseccionUno, elimina las mascarillas del sistema de colas implementado para controlar
las mascarillas que son enviadas de vuelta de la seccion 2.
'''
#llegan 2 mascarillas de la seccion 2 al servidor1
def event_two():
    global clock
    global s1_server1
    global events
    global queue_s1
    global seccionUnoAseccionDos
    global seccionDosAseccionUno
    global seccion2Queue
    global d2_accumulated
    global counter_s1
    clock=events[1].pop(0)
    #print("e2",events,clock)
    mask_one = seccionDosAseccionUno.get()
    mask_two = seccionDosAseccionUno.get()
    if s1_server1.getOcupado() == False:
        queue_s1 = queue_s1 + 1
        s1_server1.encolarMascarrilla(mask_one)
        s1_server1.setMascarillaSiendoAtendida(mask_two)
        s1_server1.setOcupado(True)
        d2 = generate_distribution(1)
        d2_accumulated = d2_accumulated + d2
        counter_s1 = counter_s1 + 1
        events[3][0] = clock + d2
        if clock > 120:
            s1_server1.setTiempoOcupado((d2))
        #print("se suma", d2)
        #print(s1_server1)
    else:
        s1_server1.encolarMascarrilla(mask_one)
        s1_server1.encolarMascarrilla(mask_two)
        queue_s1 = queue_s1 + 2
        #print(s1_server1)
    return
'''
@Descripción:Se encarga de ejecutar el evento 3:llegan 2 mascarillas de la seccion 2 servidor2 a la seccion 1
@utiliza:
s1_server1, para saber si el servidor esta ocupado
events, para adelantar el reloj al tiempo en que ocurre el evento
@modifica:
clock, cuando llega una mascarilla adelanta el reloj al momento de su llegada.
queue_s1, si el servidor esta ocupado, envia la mascarilla a la cola.
s1_server1, si esta desocupado, se ocupa.
d2_accumulated, acumula la distribucion d2 para calcular el Ws promedio de esta seccion.
counter_s1, aumenta la cantidad de veces que una mascarilla paso por esta seccion.
events, programa el evento 4.
seccionDosAseccionUno, elimina las mascarillas del sistema de colas implementado para controlar
las mascarillas que son enviadas de vuelta de la seccion 2.
'''
#llegan 2 mascarillas de la seccion 2 servidor2
def event_three():
    global s1_server1
    global events
    global queue_s1
    global clock
    global seccionUnoAseccionDos
    global seccionDosAseccionUno
    global seccion2Queue
    global d2_accumulated
    global counter_s1
    clock = events[2].pop(0)
    #print("e3",events,clock)
    mask_one = seccionDosAseccionUno.get()
    mask_two = seccionDosAseccionUno.get()
    if s1_server1.getOcupado() == False:
        s1_server1.encolarMascarrilla(mask_one)
        s1_server1.setMascarillaSiendoAtendida(mask_two)
        s1_server1.setOcupado(True)
        queue_s1 = queue_s1 + 1
        d2 = generate_distribution(1)
        d2_accumulated = d2_accumulated + d2
        counter_s1 = counter_s1 + 1
        events[3][0] = clock + d2
        if clock > 120:
            s1_server1.setTiempoOcupado((d2))
        #print("se suma", d2)
        #print(s1_server1)
    else:
        s1_server1.encolarMascarrilla(mask_one)
        s1_server1.encolarMascarrilla(mask_two)
        queue_s1 = queue_s1 + 2
    return
'''
@Descripción:Se encarga de ejecutar el evento 4:Se desocupa la seccion 1
@utiliza:
queue_s1, revisa si la cola esta vacia
@modifica
clock, adelanta el reloj
s1_server1, desocupa el servidor si no hay mas mascarillas en cola
events, programa el evento 4, y el evento 5.
queue_s1, reduce la cola de la seccion 1.
'''
#se desocupa la seccion 1
def event_four():
    global clock
    global mascarillasDesechadas
    global queue_s1
    global events
    global MAX_VALUE
    global s1_server1
    global seccionUnoAseccionDos
    global seccionDosAseccionUno
    global seccion2Queue
    global time_masks_Desechadas
    global d2_accumulated
    global counter_s1
    clock = events[3][0]
    mask = s1_server1.getMascarillaSiendoAtendida()
    if queue_s1 > 0:
        queue_s1 = queue_s1 - 1
        new_mask = s1_server1.desencolarMascarrilla()
        s1_server1.setMascarillaSiendoAtendida(new_mask)
        d2 = generate_distribution(1)
        d2_accumulated = d2_accumulated + d2
        counter_s1 = counter_s1 + 1
        if clock > 120:
            s1_server1.setTiempoOcupado(( d2))
        events[3][0] = clock + d2
    else:
        events[3][0] = MAX_VALUE
        s1_server1.setOcupado(False)
    random_value = randrange(100)
    if random_value > 10:			#el 90% de las veces no se desecha y se programa el evento 5
        events[4].append(clock + 1)
        seccionUnoAseccionDos.put(mask)
    else:
        if clock>120:
            mascarillasDesechadas=mascarillasDesechadas+1
            time_masks_Desechadas=time_masks_Desechadas+(clock - mask.get_initial_clock())
    return
'''
@Descripción:Se encarga de ejecutar el evento 5:llega una mascarilla a la seccion 2
@utiliza:
s2_server1, revisa si el encargado 1 de la secccion 2 esta ocupado
s2_server2,revisa si el encargado 1 de la secccion 2 esta ocupado
queue_s2, revisa si en la cola hay suficientes mascarillas para procesar
@modifica
clock, adelanta el reloj
events, programa los eventos 6 y 7
queue_s2, aumenta la cola de s2 si los servidores estan ocupados o si 
no hay suficientes mascarillas para procesar
d3 y d4_accumulated, acumula el tiempo que duran procesando mascarillas los encargados de esta seccion
counter_s2, aumenta la cantidad de mascarillas que se procesan en la seccion 2.
'''
#llega una mascarilla a la seccion 2
def event_five():
    global clock
    global events
    global s2_server1
    global s2_server2
    global queue_s2
    global d3_accumulated
    global d4_accumulated
    global counter_s2
    clock = events[4].pop(0)
    #print("e5",events,clock)
    if queue_s2 >= 1:
			#mascarilla 2
        #print("---------------------------OCUPADO S2S1?",s2_server1.getOcupado())
        if s2_server1.getOcupado() == False:
            #print("entra a s2.server1")
            mask = seccionUnoAseccionDos.get()				#no puedo tomar esta, porque puede que en la cola esten esperando ya otras antes.
            seccion2Queue.put(mask)							#se mete a la cola.
            new_mask = seccion2Queue.get()				#mascarilla 1
            new_mask2 = seccion2Queue.get()				#mascarilla 2
            s2_server1.encolarMascarrilla(new_mask)		#se usa la cola del server para los que esta atendiendo.
            s2_server1.encolarMascarrilla(new_mask2)	#Lo mismo
            queue_s2 = queue_s2 - 1
            d3 =generate_distribution(2)
            d3_accumulated = d3_accumulated + d3
            counter_s2 = counter_s2 + 1
            events[5][0] = clock + d3
            s2_server1.setOcupado(True)
            if clock > 120:
                s2_server1.setTiempoOcupado((d3))

        elif s2_server2.getOcupado() == False:
            mask = seccionUnoAseccionDos.get()				#no puedo tomar esta, porque puede que en la cola esten esperando ya otras antes.
            seccion2Queue.put(mask)							#se mete a la cola.
            new_mask = seccion2Queue.get()				#mascarilla 1
            new_mask2 = seccion2Queue.get()				#mascarilla 2
			#
            s2_server2.encolarMascarrilla(new_mask)
            s2_server2.encolarMascarrilla(new_mask2)
            queue_s2 = queue_s2 - 1
            d4 = generate_distribution(3)
            d4_accumulated = d4_accumulated + d4
            counter_s2 = counter_s2 + 1
            events[6][0] = clock + d4
            if clock > 120:
                s2_server2.setTiempoOcupado((d4))
            s2_server2.setOcupado(True)
        else:
            mask = seccionUnoAseccionDos.get()
            seccion2Queue.put(mask)
            queue_s2 = queue_s2 + 1
            #print("se encola S2")
    else:
        mask = seccionUnoAseccionDos.get()
        seccion2Queue.put(mask)
        queue_s2 = queue_s2 + 1
        #print("se encola S2")
    return

'''
@Descripción:Se encarga de ejecutar el evento 6:se desocupa el servidor 1 de la seccion 2
@utiliza
queue_s2, para ver si hay suficientes mascarillas para seguir procesando
MAX_VALUE, se utiliza para representar infinito en caso de que no se procesen mas mascarillas
@modifica:
clock, adelanta el reloj
events, programa el evento 6, y el evento 2.
queue_s2, si hay suficientes mascarillas para procesar las saca de la cola
paquetesListos, aumenta la cantidad de paquetes listos
mascarillasDesechadas, aumenta la cantidad de mascarillas desechadas
time_masks, y time_masks_Desechadas, establece el tiempo que paso una mascarilla en el sitema
antes de salir.
seccionDosAseccionUno, aumenta la cola de mascarillas que se devuelven a la seccion 1
'''
#se desocupa el servidor 1 de la seccion 2
def event_six():
    global events
    global MAX_VALUE
    global s2_server1
    global queue_s2
    global paquetesListos
    global mascarillasDesechadas
    global clock
    global time_masks
    global time_masks_Desechadas
    global seccionUnoAseccionDos
    global seccionDosAseccionUno
    global seccion2Queue
    global counter_s2
    global d3_accumulated
    #s2_server1 = False
    clock = events[5][0]
    #print("e6",events,clock)
    mask_ready1 = s2_server1.desencolarMascarrilla()		#mascarillas que acaba de terminar de trabajar.
    mask_ready2 = s2_server1.desencolarMascarrilla()
    if queue_s2 >= 2:
        new_mask = seccion2Queue.get()						#hay suficientes para seguir trabajando.
        new_mask2 = seccion2Queue.get()
        s2_server1.encolarMascarrilla(new_mask)				#se las vuelve a poner como las mascarillas que va a trabajar.
        s2_server1.encolarMascarrilla(new_mask2)
        queue_s2 = queue_s2 - 2
        d3 = generate_distribution(2)
        d3_accumulated = d3_accumulated + d3
        counter_s2 = counter_s2 + 1
        events[5][0] = clock + d3
        #s2_server1.setTiempoOcupado((d3))
    else:
        events[5][0] = MAX_VALUE
        s2_server1.setOcupado(False)
        #s2_server1 = False
    random_value = randrange(100)
    if random_value >= 20 and random_value<75:
        events[1].append(clock + 2)
        seccionDosAseccionUno.put(mask_ready1)				#las meto en esa lista, para que el evento 2 las pueda sacar.
        seccionDosAseccionUno.put(mask_ready2)
    elif random_value >= 5 and random_value<20:
        if clock > 120:
            mascarillasDesechadas=mascarillasDesechadas+2
            time_masks_Desechadas=time_masks_Desechadas+ (clock - mask_ready1.get_initial_clock())
            time_masks_Desechadas=time_masks_Desechadas+ (clock - mask_ready2.get_initial_clock())

    elif random_value >= 75:
        if clock > 120:
            paquetesListos=paquetesListos+1
            time_masks = time_masks + (clock - mask_ready1.get_initial_clock())
            time_masks = time_masks + (clock - mask_ready2.get_initial_clock())
    return

'''
@Descripción:Se encarga de ejecutar el evento 7:se desocupa el servidor 2 de la seccion 2
@utiliza
queue_s2, para ver si hay suficientes mascarillas para seguir procesando
MAX_VALUE, se utiliza para representar infinito en caso de que no se procesen mas mascarillas
@modifica:
clock, adelanta el reloj
events, programa el evento 6, y el evento 2.
queue_s2, si hay suficientes mascarillas para procesar las saca de la cola
paquetesListos, aumenta la cantidad de paquetes listos
mascarillasDesechadas, aumenta la cantidad de mascarillas desechadas
time_masks, y time_masks_Desechadas, establece el tiempo que paso una mascarilla en el sitema
antes de salir.
seccionDosAseccionUno, aumenta la cola de mascarillas que se devuelven a la seccion 1
'''
#se desocupa el servidor 2 de la seccion 2
def event_seven():
    global clock
    global queue_s2
    global s2_server2
    global paquetesListos
    global mascarillasDesechadas
    global time_masks
    global seccionUnoAseccionDos
    global seccionDosAseccionUno
    global seccion2Queue
    global time_masks_Desechadas
    global counter_s2
    global d4_accumulated
    clock = events[6][0]
    #print("e7",events,clock)
    mask_ready1 = s2_server2.desencolarMascarrilla()
    mask_ready2 = s2_server2.desencolarMascarrilla()
    if queue_s2 >= 2:
        new_mask = seccion2Queue.get()
        new_mask2 = seccion2Queue.get()
        s2_server2.encolarMascarrilla(new_mask)
        s2_server2.encolarMascarrilla(new_mask2)
        queue_s2 = queue_s2 - 2
        d4 = generate_distribution(3)
        d4_accumulated = d4_accumulated + d4
        counter_s2 = counter_s2 + 1
        events[6][0] = clock + d4
        #s2_server2.setTiempoOcupado((d4))
    else:
        events[6][0] = MAX_VALUE
        s2_server2.setOcupado(False)
        #s2_server2 = False
    random_value = randrange(100)
    if random_value > 15 and random_value < 40:
        events[2].append(clock + 2)
        seccionDosAseccionUno.put(mask_ready1)
        seccionDosAseccionUno.put(mask_ready2)
    elif random_value <= 15:
        if clock > 120:
            mascarillasDesechadas=mascarillasDesechadas+2
            time_masks_Desechadas = time_masks_Desechadas + (clock - mask_ready1.get_initial_clock())
            time_masks_Desechadas = time_masks_Desechadas + (clock - mask_ready2.get_initial_clock())
    elif random_value>=40:
        if clock > 120:
            paquetesListos=paquetesListos+1
            time_masks = time_masks + (clock - mask_ready1.get_initial_clock())
            time_masks = time_masks + (clock - mask_ready2.get_initial_clock())
    return


'''
@Descripción: Inicia la simulacion, programa la llegada de la primera
mascarilla al sistema
@utiliza: events
@modifica: events
'''
#metodo para inicializar datos para iniciar la simulacion
def data_init(e1):
	events[0][0]=e1


'''
@Descripción: Se encarga de retornar el evento próximoa ocurrir que se encuentra
en ¨events¨
@utiliza: events
@modifica: Nada
'''
#metodo para buscar el evento mas proximo
def get_next_event(events):
    next_event=0
    for i in range (len(events)):
        if len(events[i])>0:
            if events[i][0]<events[next_event][0]:
                next_event=i
    return next_event



'''
@Descripción: calcula el promedio de todas las corridas establecidas por el usuario y las despliega en consola.
@utiliza:Estadisticas, en esta variable se acumularon las estadisticas de todas las corridas
@modifica:Estadistica, promedia las estadisticas acumuladas
'''
def calcularEstadisticasFinales():
    global runs
    global Estadisticas
    for i in range(len(Estadisticas)):
        if i != 5 and i != 6:
            Estadisticas[i] = Estadisticas[i]/runs
        else:
            for j in range(len(Estadisticas[i])):
                Estadisticas[i][j] = Estadisticas[i][j]/runs
	#print("Las estadisticas finales son : ", Estadisticas)
    print("tiempo promedio que dura una mascarilla en el sistema antes de desecharse : ", Estadisticas[0])
    print("tiempo promedio que dura una mascarilla en el sistema antes de estar lista : ", Estadisticas[1])
    print("tiempo que dura una mascarilla en el sistema : ", Estadisticas[2])
    print("Eficiencia del sistema : ", Estadisticas[3])
    print("Equilibro del sistema: ", Estadisticas[4])
    print("Total de mascarillas que ingresaron:",Estadisticas[5][4])
    print("Mascarillas listas : ", Estadisticas[5][2], " y representan : ", Estadisticas[5][3], "% de las que ingresaron")
    print("Mascarillas desechadas : ", Estadisticas[5][0], " y representan : ", Estadisticas[5][1], "% de las que ingresaron")
    print("Porcentaje ocupado s1_server1 : ", Estadisticas[6][0], "%")
    print("Porcentaje ocupado s2_server1 : ", Estadisticas[6][1], "%")
    print("Porcentaje ocupado s2_server2 : ", Estadisticas[6][2], "%")


'''
@Descripción: Se encarga de calcular el intervalo de confianza
cuanto la cantidad de corridas que digita el usuario es de 10
@utiliza:
La varible global varianza la cual almacena los resultados individuales 
de el tiempo que dura una mascarilla en el sistema, y se utliza para
calcular la varianza muestral.

La varible global Estadisticas que es un vector, el cual almacena en sumatoria
los resultados de las diferentes estadisticas, en este caso en la posición 2
del vector almacena la sumatoria del tiempo que dura una mascarilla en el sistema
para las 10 corridas, con dicho valor se divide entre 10 y obtenemos la media muestral.
@modifica: Nada
'''
def calcularIntervalo():
    global varianza
    global Estadisticas
    mediaMuestral=(Estadisticas[2]/10)

    # Para calcular la varianza muestral
    sumatoria=0

    for i in varianza:
        sumatoria=sumatoria+(pow((i-mediaMuestral),2))

    varianzaMuestral= sumatoria/9

    final=math.sqrt((varianzaMuestral/10))

    limiteInferior=mediaMuestral-(2.26*final)
    limiteSuperior = mediaMuestral + (2.26 * final)


    print("El intervalo de confianza para el tiempo que dura una mascarilla en el sistema :[",limiteInferior,",",limiteSuperior,"]")

    print("Diferencia es de:", limiteSuperior-limiteInferior)

def main():
    global clock
    global events
    global MAX_VALUE
    global s1_server1
    global s2_server1
    global s2_server2
    global queue_s1
    global queue_s2
    global distributions
    global paquetesListos
    global mascarillasDesechadas
    global distributions
    global uniform_param_1
    global uniform_param_2
    global normal_param_1
    global normal_param_2
    global exponential_param
    global convolution_param_1
    global convolution_param_2
    global totalMascarillasIngresan
    global constanteK
    global a
    global b
    global time_masks
    global time_masks_Desechadas
    global Estadisticas
    global varianza
    global runs
    global d2_accumulated
    global counter_s1
    global d3_accumulated
    global d4_accumulated
    global counter_s2

    distribution = 0
    d = 1
    runs = int(input("ingrese la cantidad de veces que desea correr la simulacion:  "))
    max_Time = int(input("ingrese el tiempo maximo que desea correr la simulacion:  "))
    #pide al usuario las distribuciones deseadas y sus parametros correspondientes.
    while distribution < 4:
        try:
            print("seleccione cada una de las distribuciones que desea utilizar para d" + str(d))
            distributions[distribution] = int(input(
                "1 : Uniforme - 2: Normal directo  - 3 : Exponencial - 4 : Normal convolucion  : - 5 : Funcion Densidad  :\n"))
            if distributions[distribution] == 1:
                uniform_param_1[distribution] = float(input(
                    "ingrese el valor de a "))
                uniform_param_2[distribution] = float(input(
                    "ingrese el valor de b "))
                distribution = distribution + 1
                d = d + 1
            elif distributions[distribution] == 2:
                normal_param_1[distribution] = float(input("ingrese el valor de miu : "))
                normal_param_2[distribution] = float(input("ingrese el valor de la varianza  : "))
                distribution = distribution + 1
                d = d + 1
            elif distributions[distribution] == 3:
                exponential_param[distribution] = float(input("ingrese el valor de lambda : "))
                distribution = distribution + 1
                d = d + 1
            elif distributions[distribution] == 4:
                convolution_param_1[distribution] = float(input("ingrese el valor de miu : "))
                convolution_param_2[distribution] = float(input("ingrese el valor de la varianza  : "))
                distribution = distribution + 1
                d = d + 1
            elif distributions[distribution] == 5:
                constanteK[distribution] = float(input(
                    "ingrese la constante "))
                a[distribution] = float(input(
                    "ingrese el valor de a "))

                b[distribution] = float(input(
                    "ingrese el valor de b "))
                distribution = distribution + 1
                d = d + 1
            else:
                print("entrada invalida")
        except ValueError:
            print("entrada invalida")
    TIME_TO_FINISH = max_Time
    
    #corre la simulacion la cantidad de veces especificada por el usuario y almacena sus estadisticas 
    for i in range(runs):
        data_init(1)
        while clock < (TIME_TO_FINISH+120):
            event = get_next_event(events)
            switcher = {
                0: event_one,
                1: event_two,
                2: event_three,
                3: event_four,
                4: event_five,
                5: event_six,
                6: event_seven
            }
            func = switcher.get(event, "invalid event")
            func()
            # clock=TIME_TO_FINISH
            # print(normal(2,10))
            # print(randrange(100))
            # lista=[1,2,3]
        print("\n\n\n\n\nEstadisticas de la corrida", i + 1, "\n")

        # Estadistica 1
        print("tiempo promedio que dura una mascarilla en el sistema antes de desecharse :",
              (time_masks_Desechadas / mascarillasDesechadas))

        Estadisticas[0] = Estadisticas[0] + (time_masks_Desechadas / mascarillasDesechadas)

        # Estadistica 2
        print("tiempo promedio que dura una mascarilla en el sistema antes de estar lista :",
              time_masks / (paquetesListos * 2))
        Estadisticas[1] = Estadisticas[1] + (time_masks / (paquetesListos * 2))

        # Estadistica 3
        print("tiempo que dura una mascarilla en el sistema : ",
              (time_masks + time_masks_Desechadas) / ((paquetesListos * 2) + mascarillasDesechadas))
        Estadisticas[2] = Estadisticas[2] + (
                    (time_masks + time_masks_Desechadas) / ((paquetesListos * 2) + mascarillasDesechadas))
        # Para la varianza
        if runs == 10:
            varianza.append((time_masks + time_masks_Desechadas) / ((paquetesListos * 2) + mascarillasDesechadas))

        # Estadistica 4
        print("Eficiencia del sistema : ",
              ((d2_accumulated / counter_s1) + ((d3_accumulated + d4_accumulated) / counter_s2)/((time_masks + time_masks_Desechadas) / ((paquetesListos * 2) + mascarillasDesechadas))))

        Estadisticas[3]=Estadisticas[3]+((d2_accumulated / counter_s1) + ((d3_accumulated + d4_accumulated) / counter_s2)/((time_masks + time_masks_Desechadas) / ((paquetesListos * 2) + mascarillasDesechadas)))


        # Estadistica 5
        equi1 = totalMascarillasIngresan / (TIME_TO_FINISH - 120)
        equi2 = ((paquetesListos * 2) + mascarillasDesechadas) / (TIME_TO_FINISH - 120)
        print("Equilibrio del sistema", (equi1 / equi2))
        Estadisticas[4] = Estadisticas[4] + (equi1 / equi2)

        # Estadistica 6
        print("Total de mascarillas que llegaron:", totalMascarillasIngresan)
        Estadisticas[5][4] = Estadisticas[5][4]+ totalMascarillasIngresan
        print("Mascarillas desechadas ", mascarillasDesechadas, " y representan: ",
              100 * (mascarillasDesechadas / totalMascarillasIngresan), "% de las que ingresaron")
        Estadisticas[5][0] = Estadisticas[5][0] + mascarillasDesechadas
        # Porcentaje
        Estadisticas[5][1] = Estadisticas[5][1] + 100 * (mascarillasDesechadas / totalMascarillasIngresan)

        print("Mascarillas listas ", (paquetesListos * 2), " y representan: "
              , 100 * ((paquetesListos * 2) / totalMascarillasIngresan), "% de las que ingresaron")

        Estadisticas[5][2] = Estadisticas[5][2] + (paquetesListos * 2)

        # Porcentaje
        Estadisticas[5][3] = Estadisticas[5][3] + 100 * ((paquetesListos * 2) / totalMascarillasIngresan)

        # Estadistica 7
        print("Tiempo ocupado s1_server1", float(s1_server1.getTiempoOcupado()))
        print("Tiempo ocupado s2_server1", float(s2_server1.getTiempoOcupado()))
        print("Tiempo ocupado s2_server2", float(s2_server2.getTiempoOcupado()))

        print("Porcentaje ocupado s1_server1", 100 * (float(s1_server1.getTiempoOcupado() / (TIME_TO_FINISH - 120))),
              "%")

        Estadisticas[6][0] = Estadisticas[6][0] + (
                    100 * (float(s1_server1.getTiempoOcupado() / (TIME_TO_FINISH - 120))))

        print("Porcentaje ocupado s2_server1", 100 * (float(s2_server1.getTiempoOcupado() / (TIME_TO_FINISH - 120))),
              "%")

        Estadisticas[6][1] = Estadisticas[6][1] + (
                    100 * (float(s2_server1.getTiempoOcupado() / (TIME_TO_FINISH - 120))))

        print("Porcentaje ocupado s2_server2", 100 * (float(s2_server2.getTiempoOcupado() / (TIME_TO_FINISH - 120))),
              "%")

        Estadisticas[6][2] = Estadisticas[6][2] + (
                    100 * (float(s2_server2.getTiempoOcupado() / (TIME_TO_FINISH - 120))))

        print("Longitud de la cola seccion 1:", s1_server1.getLongitudCola())
        print("Longitud de la cola seccion 2:", seccion2Queue.qsize())

        # print("las estadisticas son : ", Estadisticas)
        input("\n\npresione la tecla Enter para continuar...\n\n")





        #reinicio de las variables globales

        clock = 0
        queue_s1 = 0
        queue_s2 = 0
        s1_server1 = servidor()
        s2_server1 = servidor()
        s2_server2 = servidor()

        d2_accumulated =0
        counter_s1 =0
        d3_accumulated =0
        d4_accumulated =0
        counter_s2 =0

        paquetesListos=0
        mascarillasDesechadas=0
        events = [[MAX_VALUE],[],[],[MAX_VALUE],[],[MAX_VALUE],[MAX_VALUE]]
        while not seccionUnoAseccionDos.empty():
            seccionUnoAseccionDos.get()
        while not seccionDosAseccionUno.empty():
            seccionDosAseccionUno.get()
        while not seccion2Queue.empty():
            seccion2Queue.get()

        time_masks = 0
        time_masks_Desechadas = 0
        totalMascarillasIngresan=0



    print("\n\n\n\nESTADISTICAS FINALES DE LAS : ", runs, "  SIMULACIONES")
    print("-------------------------------------------------------------------------")
    #se despliega el intervalo de confianza y las estadisticas finales
    if runs==10:
        calcularIntervalo()
    calcularEstadisticasFinales()
    print("-------------------------------------------------------------------------")
    input("\nPresione Enter para finalizar...")


if __name__ == "__main__":
    main()
