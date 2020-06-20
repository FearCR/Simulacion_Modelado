MAX_VALUE = 999999999
clock = 0
time_to_finish = 5000
queue_s1 = 0
queue_s2 = 0
s1_server1 = False
s2_server1 = False
s2_server2 = False
events = [MAX_VALUE,MAX_VALUE,MAX_VALUE,MAX_VALUE,MAX_VALUE,MAX_VALUE,MAX_VALUE]

def data_init(e1):
	events[0]=e1

def get_next_event(events):
	next_event=0
	for i in range (len(events)):
		if events[i]<events[next_event]:
			next_event=i
	return next_event

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
	return
def event_three():
	return
def event_four():
	return
def event_five():
	return
def event_six():
	return
def event_seven():
	return

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


if __name__ == "__main__":
    main()
