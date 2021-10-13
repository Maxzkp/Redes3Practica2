from SNMPdata import MonitorInfo
from time import sleep
import MailControl
import createRRD
import rrdtool
import os

monitor = MonitorInfo(hosts = ['192.168.1.82'])

#CPU use 		1.3.6.1.2.1.25.3.3.1.2.196608
#RAM total		1.3.6.1.2.1.25.2.3.1.5.1
#RAM use		1.3.6.1.2.1.25.2.3.1.6.1
#STG total		1.3.6.1.2.1.25.2.3.1.5.36
#STG use		1.3.6.1.2.1.25.2.3.1.6.36
#Cache use		1.3.6.1.2.1.25.2.3.1.6.7

SOIDs = ['1.3.6.1.2.1.25.2.3.1.5.36',
		'1.3.6.1.2.1.25.2.3.1.5.1']

OIDs = ['1.3.6.1.2.1.25.3.3.1.2.196608',
		'1.3.6.1.2.1.25.2.3.1.6.36',
		'1.3.6.1.2.1.25.2.3.1.6.1',
		'1.3.6.1.2.1.25.2.3.1.6.7']

umbral = [[40, 70, 85],
		  [68, 75, 90],
		  [50, 70, 80]]

msgcooldown = [0, 0, 0]

stdcd = 3600/5

sinfo = [int(monitor.snmpConsult(monitor.hosts[0], oid)) for oid in SOIDs]

#CPU	0
#STG	1
#RAM	2
watching = 0
names = ['CPU', 'STG', 'RAM']
while 1:

	for host in monitor.hosts:
		info = [int(monitor.snmpConsult(host, oid)) for oid in OIDs]
		info = [info[0], 
				int((info[1]*100)/sinfo[0]), 
				int(((info[2]-info[3])*100)/sinfo[1])]
		rrdinfo = 'N:' + ':'.join([str(e) for e in info])
		if os.path.exists(f'rrd/usage.rrd'):
			rrdtool.update(f'rrd/usage.rrd', rrdinfo)
			rrdtool.dump(f'rrd/usage.rrd', f'rrd/usage.xml')
			print(info)
		else:
			createRRD.create()
	print(info[watching])

	if info[watching] > umbral[watching][2] and msgcooldown[2] == 0:
		print('Go')
		createRRD.graph(names[watching], umbral[watching])
		MailControl.sendWarning(2, names[watching])
		msgcooldown[2] = stdcd
	elif info[watching] > umbral[watching][1] and info[watching] < umbral[watching][2] and msgcooldown[1] == 0:
		print('Set')
		createRRD.graph(names[watching], umbral[watching])
		MailControl.sendWarning(1, names[watching])
		msgcooldown[1] = stdcd
	elif info[watching] > umbral[watching][0] and info[watching] < umbral[watching][1] and msgcooldown[0] == 0:
		print('Ready')
		createRRD.graph(names[watching], umbral[watching])
		MailControl.sendWarning(0, names[watching])
		msgcooldown[0] = stdcd

	if msgcooldown[0] > 0:
		msgcooldown[0] -= 1
	if msgcooldown[1] > 0:
		msgcooldown[1] -= 1
	if msgcooldown[2] > 0:
		msgcooldown[2] -= 1
	sleep(5)