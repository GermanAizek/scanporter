from threading import Thread, Timer
import socket, sys, time
import itertools

from ports import *

hostOpen = []
hostClose = []
threads = []

ipList = []

def testConnect(socket):
	if not socket.connect_ex(('216.58.207.78', 80)) == 0: # google.com
		return True
	else:
		return False
		
	socket.close()
	
def ipRange(string):
	octets = string.split('.')
	chunks = [list(map(int, octet.split('-'))) for octet in octets]
	ranges = [range(c[0], c[1] + 1) if len(c) == 2 else c for c in chunks]
	
	for address in itertools.product(*ranges):
		ipList.append('.'.join(list(map(str, address))))
		

def scanTarget(host, port):
	#print('scanning ' + host + ' an port ' + str(port))
	sock = socket.socket()
	
	if testConnect(sock):
		print(' -> No connection to server. Retrying...')
		sock.close()
		scanTarget(port)
	
	result = sock.connect_ex((host,port))
	if result == 0:
		hostOpen.append(host)
		print('{0}:{1} -> open'.format(host, str(port)))
	else:
		hostClose.append(host)
		#print((str(port))+' -> close')

	sock.close()
		
def scanRange(range_ip, ports, interval):
	progress = 0
	for ip in range_ip:
		progress += 1
		progress_m = (progress / len(ipList)) * 100
		time.sleep(interval / 1000)
		for port in ports:
			thread = Thread(target = scanTarget, args = (ip, port,))
			threads.append(thread)
			time.sleep(interval / 1000)
			thread.start()

			print('{0} scaning port {1}'.format(ip, port))

		print("Scanned {0}/{1} - {2}% : IP -> {3}".format(progress, len(ipList), round(progress_m, 2), ip))
		print('\r', end='')

#if testConnect():
#	print(' -> No connection to server.')
#	sys.exit(1)

host = input('host > ')

if host.find('-'):
	ipRange(host)
	print('Range IP: {0}'.format(ipList))

menu = input('1. range ports\n2. popular ports\n3. ports UNIX\n4. Kerberos ports\n5. Register ports\n6. Unregister ports\n > ')

interval = int(input('interval scan (ms) > '))

if menu is '1':
	fromPort = int(input('start scan from port > '))
	toPort = int(input('finish scan to port > '))
	
	for ip in ipList:
		#print('{0} scaning...'.format(ip))
		time.sleep(interval / 1000)
		for port in range(fromPort, toPort + 1):
			thread = Thread(target = scanTarget, args = (ip, port,))
			threads.append(thread)
			time.sleep(interval / 1000)
			thread.start()

elif menu is '2':
	scanRange(ipList, popularPorts, interval)
elif menu is '3':
	scanRange(ipList, unixPorts, interval)
elif menu is '4':
	scanRange(ipList, kerberosPorts, interval)
elif menu is '5':
	scanRange(ipList, registerPorts, interval)
elif menu is '6':
	scanRange(ipList, unregisterPorts, interval)
else:
	print('Error!')
	
[thread.join() for thread in threads]

print('Open ports: {0}'.format(hostOpen))
#print('Close ports: {0}'.format(counting_close))

result = open('result.log', 'a')

if ipList:
	for ip in ipList:
		result.write('HOST: {0}\nOPEN PORTS: {1}\n'.format(ip, hostOpen))
else:
	result.write('HOST: {0}\nOPEN PORTS: {1}\n'.format(host, hostOpen))

result.close()
