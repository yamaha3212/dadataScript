from dadata import Dadata
import xml.etree.cElementTree as ET
from xml.dom import minidom
import sys
import threading
import time
from loguru import logger

logger.add("dadatascrypt.log", format="{time} {level} {message}", level="DEBUG")

start_time = time.time()
arguments = sys.argv

try:
    str(arguments[1])
except IndexError:
    logger.critical("There is no uid in arguments")

token = "b25c5e62f5bf23de40e1c61791284509d35a000f"
secret = "c8d18a173c1f13bdb57212e72dfc3685fe91f92a"


def data_parse(raw_adddress):
    with Dadata(token, secret) as dadata:
        autosuggested_data = dadata.suggest(name="address", query=raw_adddress)
        clean_data = dadata.clean(name="address", source=autosuggested_data[1]['value'])

    address_array = [clean_data['postal_code'], clean_data['federal_district'], clean_data['region'],
                     clean_data['city_area'], clean_data['city_district'], clean_data['street'], clean_data['house'],
                     clean_data['block'], clean_data['flat']]

    address_string = ""
    i = 0
    for element in address_array:
        if element is None:
            address_array[i] = ","
            address_string = address_string + address_array[i]
        else:
            address_string = " " + address_string + address_array[i] + ","
        i = i + 1

    if address_string[-2] != ",":
        address_string = address_string[0:-1]
    return address_string


root = ET.Element("root")

creationFlag = []

def multithread_generation(argument):
    try:
        exhaust_address = data_parse(arguments[argument])
        creationFlag.append(exhaust_address)
        ET.SubElement(root, "Addr" + str(argument - 1), name="Addr" + str(argument - 1)).text = exhaust_address
    except Exception as ex:
        logger.critical("Query error (dadata), query uid is " + arguments[1] + " " + str(ex))


threads = list()
for n in range(len(arguments)):
    if n == 0 or n == 1:
        continue
    else:
        x = threading.Thread(target=multithread_generation, args=(n,))
        threads.append(x)
        x.start()
for index, thread in enumerate(threads):
    thread.join()

filename = str(arguments[1]) + ".xml"

xml_string = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
if len(creationFlag) == len(arguments) - 2 and creationFlag:
    with open(filename, "w", encoding='utf-8') as f:
        f.write(xml_string)
    logger.info("Created xml document with id " + arguments[1])
if len(arguments) < 3:
    logger.warning("No addresses in arguments which should contains address, query uid is " + arguments[1] + ". XML doesn't generated")

print("--- %s seconds ---" % (time.time() - start_time))
