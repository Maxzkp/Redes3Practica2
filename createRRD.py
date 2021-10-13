#!/usr/bin/env python
import sys
import rrdtool

def create():
    ret = rrdtool.create(f'rrd/usage.rrd',
                         "--start",'N',
                         "--step",'5',
                         "DS:CPU:GAUGE:600:U:U",
                         "DS:RAM:GAUGE:600:U:U",
                         "DS:STG:GAUGE:600:U:U",
                         "RRA:AVERAGE:0.5:1:720")

    if ret:
        print (rrdtool.error())

def graph(var, umbrales):
    last_read = int(rrdtool.last('rrd/usage.rrd'))
    tf = last_read
    t0 = tf - 600

    ret = rrdtool.graphv(f'rrd/{var}usage.png',
                     "--start",str(t0),
                     "--end",str(tf),
                     f"--vertical-label={var} load",
                     "--lower-limit", "0",
                     "--upper-limit", "100",
                     f"--title=Uso de {var} del agente usando SNMP y RRDtools\n Deteccion de umbrales",
                     f"DEF:{var}load=rrd/usage.rrd:{var}:AVERAGE",
                     
                     f"VDEF:cargaMAX={var}load,MAXIMUM",
                     f"VDEF:cargaMIN={var}load,MINIMUM",
                     f"VDEF:cargaSTDEV={var}load,STDEV",
                     f"VDEF:cargaLAST={var}load,LAST",

                     f"CDEF:Normal={var}load,{umbrales[0]},LE,{var}load,0,IF",
                     f"CDEF:Ready={var}load,{umbrales[0]},LE,0,{var}load,IF",
                     f"CDEF:Set={var}load,{umbrales[1]},LE,0,{var}load,IF",
                     f"CDEF:Go={var}load,{umbrales[2]},LE,0,{var}load,IF",

                     f"HRULE:{umbrales[0]}#0000FF:Umbral Ready",
                     f"HRULE:{umbrales[1]}#CFCF30:Umbral Set",
                     f"HRULE:{umbrales[2]}#FF0000:Umbral Go",

                     f"AREA:Normal#00FF00:Carga de {var} normal",
                     f"AREA:Ready#0000FF:Carga de {var} mayor a {umbrales[0]}%",
                     f"AREA:Set#CFCF30:Carga de {var} mayor a {umbrales[1]}%",
                     f"AREA:Go#FF0000:Carga de {var} mayor a {umbrales[2]}%",
                     
                     "PRINT:cargaLAST:%6.2lf",
                     "GPRINT:cargaMIN:%6.2lf %SMIN",
                     "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                     "GPRINT:cargaLAST:%6.2lf %SLAST")