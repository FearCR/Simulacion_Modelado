
	return 0

def event_one():
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

MAX_VALUE = 999999999
clock = 0
time_to_finish = 5000
queue_s1 = []
queue_s2 = []
s1_server1 = False
s2_server1 = False
s2_server2 = False
events = [MAX_VALUE,MAX_VALUE,MAX_VALUE,MAX_VALUE,MAX_VALUE,MAX_VALUE,MAX_VALUE]

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
