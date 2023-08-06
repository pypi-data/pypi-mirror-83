import requests, time
from pythontools.core import logger

def uploadToHastebin(content):
    url = 'https://hastebin.com'
    data = ""
    if type(content) == str:
        data = content
    elif type(content) == list:
        for i in content:
            data += str(i) + "\n"
    else:
        logger.log("§cError: Please insert string or list!")
        return
    response = requests.post(url + '/documents', data=data.encode('utf-8'))
    return url + '/' + response.json()['key']

logTimes = {}

def startLogTime(name):
    logTimes[name] = time.time()

def endLogTime(name, log=True):
    if name in logTimes:
        convertedTime = convertTime(time.time() - logTimes[name], millis=True)
        if log:
            logger.log("§8[§bTIME§8] §e" + str(name) + " finished in §6" + convertedTime)
        logTimes.pop(name)
        return convertedTime
    else:
        logger.log("§cError: " + str(name) + " not exist!")

def convertTime(seconds, millis=False, millisDecimalPlaces=10):
    sec = seconds
    min = 0
    h = 0
    days = 0
    while sec >= 60:
        min += 1
        sec -= 60
    while min >= 60:
        h += 1
        min -= 60
    while h >= 24:
        days += 1
        h -= 24
    if days > 0:
        return str(days) + "d " + str(h) + "h"
    if h > 0:
        return str(h) + "h " + str(min) + "m"
    if min > 0:
        if millis:
            return str(min) + "m " + str(round(sec, millisDecimalPlaces)) + "s"
        return str(min) + "m " + str(int(sec)) + "s"
    if millis:
        return str(round(sec, millisDecimalPlaces)) + "s"
    return str(int(sec)) + "s"

round_robin_indices = {}

def getRoundRobinValue(list):
    if id(list) not in round_robin_indices:
        round_robin_indices[id(list)] = 0
    if len(list) >= 0:
        if round_robin_indices[id(list)] >= len(list):
            round_robin_indices[id(list)] = 0
        round_robin_indices[id(list)] += 1
        return list[round_robin_indices[id(list)]-1]
    return None