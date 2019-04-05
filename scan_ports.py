from threading import Thread, Timer
import socket, sys, time
import itertools

counting_open = []
counting_close = []

host_open = []
host_close = []
threads = []

ip_list = []

def testConnect(socket):
	if not socket.connect_ex(('216.58.207.78',80)) == 0: # google.com
		return True
	else:
		return False
		
	s.close()
	
def ipRange(string):
	octets = string.split('.')
	chunks = [list(map(int, octet.split('-'))) for octet in octets]
	ranges = [range(c[0], c[1] + 1) if len(c) == 2 else c for c in chunks]
	
	for address in itertools.product(*ranges):
		ip_list.append('.'.join(list(map(str, address))))
		

def scanTarget(host, port):
	#print('scanning ' + host + ' an port ' + str(port))
	socket = socket.socket()
	
	if testConnect(socket):
		print(' -> No connection to server. Retrying...')
		socket.close()
		scanTarget(port)
	
	result = socket.connect_ex((host,port))
	if result == 0:
		counting_open.append(host)
		host_open.append(port)
		print('{0}:{1} -> open'.format(host, str(port)))
	else:
		counting_open.append(host)
		host_close.append(port)
		#print((str(port))+' -> close')

	socket.close()
		
def scanRange(range_ip, ports, interval):
	progress = 0
	for ip in range_ip:
		progress += 1
		progress_m = (progress / len(ip_list)) * 100
		print("Scanned {0}/{1} - {2}% : IP -> {3}".format(progress, len(ip_list), round(progress_m, 2), ip))
		print('\r', end='')
		#print('{0} scaning...'.format(ip))
		time.sleep(interval/1000)
		for port in ports:
			thread = Thread(target=scanTarget, args=(ip, port,))
			threads.append(thread)
			time.sleep(interval/100000)
			thread.start()

#if testConnect():
#	print(' -> No connection to server.')
#	sys.exit(1)

host = input('host > ')

if host.find('-'):
	ipRange(host)
	print('Range IP: {0}'.format(ip_list))

menu = input('1. range ports\n2. popular ports\n3. ports UNIX\n4. Kerberos ports\n5. Register ports\n6. Unregister ports\n > ')

interval = int(input('interval scan > '))

if menu is '1':
	from_port = int(input('start scan from port > '))
	to_port = int(input('finish scan to port > '))
	
	for ip in ip_list:
		#print('{0} scaning...'.format(ip))
		time.sleep(interval/1000)
		for port in range(from_port, to_port+1):
			thread = Thread(target=scanTarget, args=(ip, port,))
			threads.append(thread)
			time.sleep(interval/100000)
			thread.start()
			
elif menu is '2':
	from ports import *
	
	scanRange(ip_list, popular_ports, interval)
elif menu is '3':
	from ports import *
	
	scanRange(ip_list, unix_ports, interval)
elif menu is '4':
	from ports import *
	
	scanRange(ip_list, kerberos_ports, interval)
elif menu is '5':
	from ports import *
	
	scanRange(ip_list, register_ports, interval)
elif menu is '6':
	from ports import *
	
	scanRange(ip_list, unregister_ports, interval)
else:
	print('Error!')
	
[x.join() for x in threads]

print('Open ports: {0}'.format(counting_open))
#print('Close ports: {0}'.format(counting_close))

f = open('result.log', 'a')
if ip_list:
	for ip in ip_list:
		f.write('HOST: {0}\nOPEN PORTS: {1}\n'.format(ip, counting_open))
else:
	f.write('HOST: {0}\nOPEN PORTS: {1}\n'.format(host, counting_open))
f.close()
