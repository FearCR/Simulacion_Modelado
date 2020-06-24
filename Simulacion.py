from random import random
from random import randrange
import math

MAX_VALUE = 999999999
TIME_TO_FINISH = 500
clock = 0
queue_s1 = 0
queue_s2 = 0
s1_server1 = False
s2_server1 = False
s2_server2 = False

tiempoTrabajador1=0
tiempoTrabajador2=0
tiempoTrabajador3=0

paquetesListos=0
mascarillasDesechadas=0
events = [[MAX_VALUE],[],[],[MAX_VALUE],[],[MAX_VALUE],[MAX_VALUE]]
distributions = [-1,-1,-1,-1]


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



#distribuciones
def uniforme(a,b):
    r=random()
    x=(b-a)*r+a
    return x

def normal(Mu,vari):
    r1 = random()
    r2 = random()
    Z=(-2*math.log(r1))
    Z=pow(Z,1/2)
    pi=math.pi
    Z=Z*(math.cos(2*pi*r2))
    x=(vari*Z)+Mu
    if x<0:
        x=-1*x
    return x+1

def exponencial(lamb):
    r = random()
    x=(-math.log(1-r))/lamb
    return x

def convolucion(Mu,vari):
    Z=0
    for i in range(1,13):
        r = random()
        Z=Z+r
    x = (vari * Z) + Mu
    return x

def funcionDensidad(funcion,a,b):
    print("por implementar")


def generate_distribution(index_distribution):
	if distributions[index_distribution] == 1:
		return uniforme(uniform_param_1[index_distribution],uniform_param_2[index_distribution])
	else:
		if distributions[index_distribution] == 2:
			return normal(normal_param_1[index_distribution],normal_param_2[index_distribution])
		else:
			if distributions[index_distribution] == 3:
				return exponencial(exponential_param[index_distribution])
			else:
				return convolucion(convolution_param_1[index_distribution],convolution_param_2[index_distribution])
	return


#llega mascarilla del exterior a Seccion 1
def event_one():
    global clock
    global s1_server1
    global tiempoTrabajador1
    global events
    global queue_s1
    clock = events[0][0]
    print("e1",events,clock)
    if s1_server1 == False:

        tiempoTrabajador1=tiempoTrabajador1+1
        s1_server1 = True
        d2 = generate_distribution(2)
        events[3][0] = clock + d2
        print(s1_server1)
    else:
        queue_s1 = queue_s1 + 1
        d1 = generate_distribution(1)
        events[0][0] = clock + d1
        print(s1_server1)
        return

#llegan 2 mascarillas de la seccion 2 servidor1
def event_two():
    global clock
    global s1_server1
    global events
    global tiempoTrabajador2
    global queue_s1
    clock=events[1].pop(0)
    print("e2",events,clock)
    if s1_server1 == False:
        queue_s1 = queue_s1 + 1
        tiempoTrabajador2=tiempoTrabajador2+1
        s1_server1==True
        d2 = generate_distribution(2)
        events[3][0] = clock + d2
        print(s1_server1)
    else:
        queue_s1 = queue_s1 + 2
        print(s1_server1)
    return

#llegan 2 mascarillas de la seccion 2 servidor2
def event_three():
    global s1_server1
    global events
    global queue_s1
    global tiempoTrabajador3
    global clock
    clock = events[2].pop(0)
    print("e3",events,clock)
    if s1_server1 == False:
        tiempoTrabajador3=tiempoTrabajador3+1
        s1_server1 = True
        queue_s1 = queue_s1 + 1
        d2 = generate_distribution(2)
        events[3][0] = clock + d2
        print(s1_server1)
    else:
        queue_s1 = queue_s1 + 2
    return

#se desocupa la seccion 1
def event_four():
    global clock
    global mascarillasDesechadas
    global queue_s1
    global events
    global MAX_VALUE
    global s1_server
    clock = events[3][0]
    print("e4",events,clock)
    if queue_s1 > 0:
        queue_s1 = queue_s1 - 1
        d2 = generate_distribution(2)
        events[3][0] = clock + d2
    else:
        events[3][0] = MAX_VALUE
        s1_server1 = False
    random_value = randrange(100)
    if random_value > 10:			#el 90% de las veces no se desecha y se programa el evento 5
        events[4].append(clock + 1)
    else:
        mascarillasDesechadas=mascarillasDesechadas+1
    return

#llega una mascarilla a la seccion 2
def event_five():
    global clock
    global events
    global s2_server1
    global s2_server2
    global queue_s2
    clock = events[4].pop(0)
    print("e5",events,clock)
    if queue_s2 >= 1:
        if s2_server1 == False | s2_server2 == False:
            if s2_server1 == False:
                queue_s2 = queue_s2 - 1
                d3 =generate_distribution(3)
                events[5][0] = clock + d3
                s2_server1 = True
            else:
				#if s2_server2 == False:
                queue_s2 = queue_s2 - 1
                d4 = generate_distribution(4)
                events[6][0] = clock + d4
                s2_server2 = True
        else:
            queue_s2 = queue_s2 + 1
    else:
        queue_s2 = queue_s2 + 1
    return

#se desocupa el servidor 1 de la seccion 2
def event_six():
    global events
    global MAX_VALUE
    global s2_server1
    global queue_s2
    global paquetesListos
    global mascarillasDesechadas
    global clock
    s2_server1 = False
    clock = events[5][0]
    print("e6",events,clock)
    if queue_s2 >= 2:
        queue_s2 = queue_s2 - 2
        d3 = generate_distribution(3)
        events[5][0] = clock + d3
    else:
        events[5][0] = MAX_VALUE
        s2_server1 = False
    random_value = randrange(100)
    if random_value >= 20 and random_value<75:
        events[1].append(clock + 2)
    elif random_value >= 5 and random_value<20:
        mascarillasDesechadas=mascarillasDesechadas+2
    elif random_value >= 75:
        paquetesListos=paquetesListos+1
    return


#se desocupa el servidor 2 de la seccion 2
def event_seven():
    global clock
    global queue_s2
    global s2_server2
    global paquetesListos
    global mascarillasDesechadas
    clock = events[6][0]
    print("e7",events,clock)
    if queue_s2 >= 2:
        queue_s2 = queue_s2 - 2
        d4 = generate_distribution(4)
        events[6][0] = clock + d4
    else:
        events[6][0] = MAX_VALUE
        s2_server2 = False
    random_value = randrange(100)
    if random_value >= 15 and random_value < 40:
        events[3].append(clock + 2)
    elif random_value >= 15 and random_value < 25:
        mascarillasDesechadas=mascarillasDesechadas+2
    elif random_value>=40:
        paquetesListos=paquetesListos+1
    return

#metodo para inicializar datos para iniciar la simulacion
def data_init(e1):
	events[0][0]=e1

#metodo para buscar el evento mas proximo
def get_next_event(events):
    next_event=0
    for i in range (len(events)):
        if len(events[i])>0:
            if events[i][0]<events[next_event][0]:
                next_event=i
    return next_event

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
    data_init(3)


    distribution = 0
    d=1
    while distribution < 4:
        print("seleccione cada una de las distribuciones que desea utilizar para d"+str(d))
        distributions[distribution] = int(input("1 : Uniforme - 2: Normal  - 3 : Exponencial - 4 : Convolucion  : \n"))
        if distributions[distribution] == 1:
            uniform_param_1[distribution] = int(input("ingrese el primer parametro para la distribucion uniforme : "))
            uniform_param_2[distribution] = int(input("ingrese el segundo parametro para la distrubicion uniforme : "))
        else:
            if distributions[distribution] == 2:
                normal_param_1[distribution] = int(input("ingrese el primer parametro para la distribucion normal : "))
                normal_param_2[distribution] = int(input("ingrese el segundo parametro para la distrubicion normal : "))
            else:
                if distributions[distribution] == 3:
                    exponential_param[distribution] = int(input("ingrese el parametro para la distrubucion exponencial : "))
                else:
                    convolution_param_1[distribution] = int(input(
                        "ingrese el primer parametro para la distribucion convolucion"))
                    convolution_param_2[distribution] = int(input(
                        "ingrese el segundo parametro para la distribucion convolucion"))
        distribution = distribution + 1
        d=d+1

    while clock < TIME_TO_FINISH:
        event = get_next_event(events)
        switcher = {
			0:event_one,
			1:event_two,
			2:event_three,
			3:event_four,
			4:event_five,
			5:event_six,
			6:event_seven
		}
        func = switcher.get(event, "invalid event")
        func()
        #clock=TIME_TO_FINISH
        #print(normal(2,10))
        #print(randrange(100))
    #lista=[1,2,3]

    print("Mascarillas desechadas ",mascarillasDesechadas)
    print("Paquetes listos ", paquetesListos)
    #print("Tiempo ocuado Trabajador 1: ",(tiempoTrabajador1/TIME_TO_FINISH))
    #print("Tiempo ocuado Trabajador 2: ",(tiempoTrabajador2/TIME_TO_FINISH))
    #print("Tiempo ocuado Trabajador 3: ",(tiempoTrabajador3/TIME_TO_FINISH))





if __name__ == "__main__":
    main()