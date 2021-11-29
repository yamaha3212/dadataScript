from dadata import Dadata
import xml.etree.cElementTree as ET
from xml.dom import minidom
import sys
import threading
from loguru import logger
import os
import inspect

logger.add("dadatascrypt.log", format="{time:DD.MM.YYYY HH:mm:ss Z} {level} {message}", level="DEBUG", encoding='utf-8')


def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False):
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)


try:
    os.mkdir(get_script_dir() + os.path.sep + 'xml')
except FileExistsError:
    pass

arguments = sys.argv
root = ET.Element("root")
creationFlag = []

logger.info("================================================ STARTED")

try:
    filename = str(arguments[1]) + ".xml"
except IndexError:
    logger.critical("There is no uid in arguments")
    logger.info("============================================ with error")
    sys.exit()

token = "b25c5e62f5bf23de40e1c61791284509d35a000f"


def data_parse(raw_adddress):
    with Dadata(token) as dadata:
        autosuggested_data = dadata.suggest(name="address", query=raw_adddress)
    if not autosuggested_data:
        logger.warning("Dadata returns null result because of bad query. Query: " + str(raw_adddress))
        address_string = ",,,,,,,,,"
        return address_string
    else:
        address_array = [
            autosuggested_data[0]['data']['postal_code'],
            autosuggested_data[0]['data']['region_kladr_id'][0:2],
            autosuggested_data[0]['data']['federal_district'],
            autosuggested_data[0]['data']['area'],
            autosuggested_data[0]['data']['city'],
            autosuggested_data[0]['data']['street_with_type'],
            autosuggested_data[0]['data']['house'],
            autosuggested_data[0]['data']['block'],
            autosuggested_data[0]['data']['flat']
        ]

        address_string = ""
        i = 0
        for element in address_array:
            if element is None:
                address_array[i] = ","
                address_string = address_string + address_array[i]
            else:
                address_string = address_string + address_array[i] + ","
            i = i + 1

        if address_string[-2] != ",":
            address_string = address_string[0:-1]

        return address_string


def multithread_generation(argument):
    try:
        exhaust_address = data_parse(arguments[argument])
        creationFlag.append(exhaust_address)
        ET.SubElement(root, "Addr" + str(argument - 1), name="Addr" + str(argument - 1)).text = exhaust_address
    except Exception as ex:
        logger.critical("Query error (dadata), query uid is " + arguments[1] + " " + str(ex))
        logger.info("============================================ with error")


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


if len(creationFlag) == len(arguments) - 2 and creationFlag:
    with open(get_script_dir() + os.path.sep + 'xml' + os.path.sep + filename, "w", encoding='utf-8') as xmlFile:
        xmlFile.write(minidom.parseString(ET.tostring(root)).toprettyxml())
    logger.info("Created xml document with id " + arguments[1])
    logger.info("============================================ " + str(arguments[1]))
if len(arguments) < 3:
    logger.warning("No addresses in arguments which should contains address. XML doesn't generated")
    logger.info("============================================ with error")
