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


def data_parse(raw_adddress):
    with Dadata(token) as dadata:
        autosuggested_data = dadata.suggest(name="address", query=raw_adddress)
    if not autosuggested_data:
        logger.warning("Dadata returns null result because of bad query. Query: " + str(raw_adddress))
    else:
        address_array = [autosuggested_data[0]['data']['postal_code'], autosuggested_data[0]['data']['federal_district'], autosuggested_data[0]['data']['region'],
                     autosuggested_data[0]['data']['city'], autosuggested_data[0]['data']['settlement'], autosuggested_data[0]['data']['street'], autosuggested_data[0]['data']['house'],
                     autosuggested_data[0]['data']['block'], autosuggested_data[0]['data']['flat']]

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
    logger.warning("No addresses in arguments which should contains address. XML doesn't generated")

print("--- %s seconds ---" % (time.time() - start_time))
