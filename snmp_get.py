import sys
import time
import csv
import os.path
from pysnmp.entity.rfc3413.oneliner import cmdgen

csv_filename = "/home/dspicker/environment_monitoring/env_data.csv"
sysname_temp = '.1.3.6.1.4.1.14848.2.1.2.1.5.3'
sysname_humi = '.1.3.6.1.4.1.14848.2.1.2.1.5.7'
host = '141.2.243.203'

current_temp = 0.0
current_humidity = 0.0

time_str = time.strftime("%Y-%m-%d %H:%M", time.localtime())
epoch = time.mktime(time.localtime())

#print("{} Start of Script".format(time_str))

# Define a PySNMP CommunityData object named auth, by providing the SNMP community string
auth = cmdgen.CommunityData('public', None, 0)

# Define the CommandGenerator, which will be used to send SNMP queries
cmdGen = cmdgen.CommandGenerator()

# Query a network device using the getCmd() function, providing the auth object, a UDP transport
# our OID for SYSNAME, and don't lookup the OID in PySNMP's MIB's
errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    auth,
    cmdgen.UdpTransportTarget((host, 161)),
    cmdgen.MibVariable(sysname_temp),
    lookupMib=False,
)
# Check if there was an error querying the device
if errorIndication is not None  or errorStatus is True:
    print ('Error: {} {} {}'.format(errorIndex, errorStatus, errorIndication))
else:
    for oid, val in varBinds:
        #print(oid.prettyPrint(), val.prettyPrint())
        current_temp = float(val.prettyPrint()) / 10.0


errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    auth,
    cmdgen.UdpTransportTarget((host, 161)),
    cmdgen.MibVariable(sysname_humi),
    lookupMib=False,
)
if errorIndication is not None  or errorStatus is True: 
    print ('Error: {} {} {}'.format(errorIndex, errorStatus, errorIndication))
    sys.exit()
else:
    for oid, val in varBinds:
        #print(oid.prettyPrint(), val.prettyPrint())
        current_humidity = float(val.prettyPrint()) / 10.0

#degree_sign = u'\N{DEGREE SIGN}'
#print("Epoch       ,Time            ,Humidity %RH ,Temperature C")
#print('{}, {}, {}        , {} '.format(epoch, time_str, current_humidity, current_temp))

if not os.path.isfile(csv_filename) :
    file = open(csv_filename, "w", newline='', encoding='utf-8')
    file.write("Epoch,Time,Humidity %RH,Temperature C\n")
    file.close()

with open(csv_filename, 'a', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow([epoch, time_str, current_humidity, current_temp ])

#print("finish.")
