"""
Get measurement values from mess-pc Ethernetbox via snmp protocol.

Also see https://www.messpc.de/snmp.php

By Dennis Spicker, 2025
"""

import time
import csv
import os.path
import asyncio
import pysnmp.hlapi.v1arch.asyncio as psnmp

SNMP_HOST = "141.2.243.203"
SNMP_OID_TEMPSENSOR  = '.1.3.6.1.4.1.14848.2.1.2.1.5.3'
SNMP_OID_HUMIDSENSOR = '.1.3.6.1.4.1.14848.2.1.2.1.5.7'


async def run_snmp_request(requested_oid: str):
    """ Executes one snmp get request and returns the sensor value as float. """
    value = 0.0

    error_indication, error_status, error_index, var_binds = await psnmp.get_cmd(
        psnmp.SnmpDispatcher(),
        psnmp.CommunityData('public', 0),  # mpModel: SNMP version - 0 for SNMPv1 and 1 for SNMPv2c.
        await psnmp.UdpTransportTarget.create((SNMP_HOST, 161)),
        psnmp.ObjectType(psnmp.ObjectIdentity(requested_oid)),
        lookupMib=False
    )

    # Check if there was an error querying the device
    if error_indication is not None  or error_status is True:
        print (f"Error: {error_index} {error_status} {error_indication}")
        for oid, val in var_binds:
            print(oid.prettyPrint(), val.prettyPrint())
        print(time.strftime("%Y-%m-%d %H:%M", time.localtime()))
    else:
        for oid, val in var_binds:
            #print(oid.prettyPrint(), val.prettyPrint())
            value = float(val.prettyPrint()) / 10.0

    return value


async def main():
    """ Main function of this script. """
    current_temp = await run_snmp_request(SNMP_OID_TEMPSENSOR)
    current_humidity = await run_snmp_request(SNMP_OID_HUMIDSENSOR)

    time_str = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    epoch = time.mktime(time.localtime())

    csv_filename = "env_data.csv"
    csv_fullpath = os.getcwd() + "/" + csv_filename

    if not os.path.isfile(csv_fullpath) :
        file = open(csv_fullpath, "w", newline='', encoding='utf-8')
        file.write("Epoch,Time,Humidity %RH,Temperature C\n")
        file.close()

    with open(csv_fullpath, 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow([epoch, time_str, current_humidity, current_temp ])

    #print( "Epoch       , Time            , Humidity %RH, Temperature C")
    #print(f"{epoch}, {time_str}, {current_humidity}        , {current_temp} ")


if __name__ == "__main__":
    asyncio.run(main())
