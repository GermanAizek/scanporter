# by GermanAizek

from threading import Thread
import socket, sys, time

counting_open = []
counting_close = []
threads = []

def testConnect():
	s = socket.socket()
	
	if not s.connect_ex(('216.58.207.78',80)) == 0: # google.com
		return True
	else:
		return False
		
	s.close()
	
def createRange(from_ip, to_ip): # 23.111.248.0 - 23.249.231.255
	range_ip = []
	
	range_ip.append(from_ip)

	unpart_from = from_ip.split('.')
	print(unpart_from)
	unpart_to = to_ip.split('.')
	for i in unpart_to:
		for i in unpart_from:
			if not unpart_from[i] == unpart_to[i]:
				unpart_from[i] = int(i) + 1
				for i in unpart_from:
					unpart_from[i] = i + '.'
				range_ip.append(unpart_from)
						
	print(range_ip)

def scan(port):
	s = socket.socket()
	
	if testConnect():
		print(' -> No connection to server. Retrying...')
		s.close()
		scan(port)
	
	result = s.connect_ex((host,port))
	if result == 0:
		counting_open.append(port)
		print((str(port))+' -> open')
		s.close()
	else:
		counting_close.append(port)
		#print((str(port))+' -> close')
		s.close()
	
#key = input('key -> ')

#if key != '0451':
if testConnect():
	print(' -> No connection to server.')
	sys.exit(1)

host = input('host > ')

if '-' in host:
	range_ip = host.split('-')
	createRange(range_ip[0], range_ip[1])
	print('Range IP: {0}'.format(range_ip))



menu = input('1. range ports\n2. popular ports\n3. ports UNIX\n4. Kerberos ports\n5. Register ports\n6. Unregister ports\n > ')

if menu is '1':
	from_port = int(input('start scan from port > '))
	to_port = int(input('finish scan to port > '))
	
	#for ip in range(range_ip):
	for i in range(from_port, to_port+1):
		t = Thread(target=scan, args=(i,))
		threads.append(t)
		t.start()
elif menu is '2':
	from ports import *
	
	for i in popular_ports:
		t = Thread(target=scan, args=(i,))
		threads.append(t)
		t.start()
elif menu is '3':
	from ports import *
	
	for i in unix_ports:
		t = Thread(target=scan, args=(i,))
		threads.append(t)
		t.start()
elif menu is '4':
	from ports import *
	
	for i in kerberos_ports:
		t = Thread(target=scan, args=(i,))
		threads.append(t)
		t.start()
elif menu is '5':
	from ports import *
	
	for i in register_ports:
		t = Thread(target=scan, args=(i,))
		threads.append(t)
		t.start()
elif menu is '6':
	from ports import *
	
	for i in unregister_ports:
		t = Thread(target=scan, args=(i,))
		threads.append(t)
		t.start()
else:
	print('Error!')
	
[x.join() for x in threads]

print('Open ports: {0}'.format(counting_open))
#print('Close ports: {0}'.format(counting_close))

f = open('result.log', 'a')
f.write('HOST: {0}\nOPEN PORTS: {1}\n'.format(host, counting_open))
f.close()