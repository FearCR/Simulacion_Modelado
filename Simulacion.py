MAX_VALUE = 999999999
clock = 0
time_to_finish = 5000
queue_s1 = 0
queue_s2 = 0
s1_server1 = False
s2_server1 = False
s2_server2 = False
events = [MAX_VALUE,MAX_VALUE,MAX_VALUE,MAX_VALUE,MAX_VALUE,MAX_VALUE,MAX_VALUE]


def get_next_event(events):
	return 0


def generate_d2():
	return 0

def generate_d1():
	return 0

def generate_random():
	return 0

#llega una mascarilla del exterior a la seccion 1
def event_one():
	global s1_server1
	global events
	global queue_s1
	clock = events[0]
	if s1_server1 == False:
		s1_server1 = True
		d2 = generate_d2()
		events[3] = int(clock) + int(d2)
	else:
		queue_s1 = queue_s1 + 1
		d1 = generate_d1()
		events[0] = int(clock) + int(d1)
	return
	
def event_two():
	return
def event_three():
	return

#Se desocupa el servidor de la seccion 1
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
	random_value = int(generate_random())
	if random_value > 10:			#el 90% de las veces no se desecha y se programa el evento 5
		events[4] = clock + 1
	return
	
def event_five():
	return
def event_six():
	return
def event_seven():
	return


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
	clock = time_to_finish
	uy = func()
