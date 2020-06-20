
from random import random
from random import randrange
import math

MAX_VALUE = 999999999
clock = 0
time_to_finish = 5000
queue_s1 = 0
queue_s2 = 0
s1_server1 = False
s2_server1 = False
s2_server2 = False
events = [MAX_VALUE,MAX_VALUE,MAX_VALUE,MAX_VALUE,MAX_VALUE,MAX_VALUE,MAX_VALUE]

def uniforme(a,b):
    r=random()
    x=(b-a)*r+a
    return int(x)

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
    return int(x)

def convolucion(Mu,vari):
    Z=0
    for i in range(1,13):
        r = random()
        Z=Z+r
    x = (vari * Z) + Mu
    return int(x)

def funcionDensidad(funcion,a,b):
    print("por implementar")




def generate_d1():
	return 0

def generate_d2():
	return 0

def generate_d3():
	return 0

def generate_d4():
	return 0



def event_one():
	global s1_server1
	global events
	global queue_s1
	clock = events[0]
	if s1_server1 == False:
		s1_server1 = True
		d2 = generate_d2()
		events[3] = int(clock) + int(d2)
		print(s1_server1)
	else:
		queue_s1 = queue_s1 + 1
		d1 = generate_d1()
		events[0] = int(clock) + int(d1)
		print(s1_server1)
	return
def event_two():
    global clock
	global s1_server1
	global events
	global queue_s1
    clock=events[1]
    if s1_server1 == False:
        queue_s1 = queue_s1 + 1
        s1_server1==True
        d2 = generate_d2()
		events[3] = int(clock) + int(d2)
        print(s1_server1)
    else:
    	queue_s1 = queue_s1 + 2
    	print(s1_server1)

	return
def event_three():
	return
def event_four():
	global queue_s1
	global events
	global MAX_VALUE
	global s1_server1
	clock = events[3]
	if queue_s1 > 0:
		queue_s1 = queue_s1 - 1
		d2 = generate_d2()
		events[3] = int(clock) + int(d2)
	else:
		events[3] = MAX_VALUE
		s1_server1 = False
	random_value = randrange(100)
	if random_value > 10:			#el 90% de las veces no se desecha y se programa el evento 5
		events[4] = clock + 1
	return
def event_five():
	return
def event_six():
	return
def event_seven():
	return

def data_init(e1):
	events[0]=e1

def get_next_event(events):
	next_event=0
	for i in range (len(events)):
		if events[i]<events[next_event]:
			next_event=i
	return next_event
def main():
	global clock
	data_init(3)
	while clock < time_to_finish:
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
		clock=time_to_finish
		print(normal(2,10))
		print(randrange(100))

if __name__ == "__main__":
    main()
