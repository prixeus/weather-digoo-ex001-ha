#!/usr/bin/python3

import asyncio
from udphandler import UDPHandler
from digoodata import DigooData
from mqtt import MQTT
import sys
import logging


logging.basicConfig(level=logging.INFO)
logging.info("Digoo translator Starting")
#shared weather instance
curWeather = DigooData()
#udp handler - for getting updates from the real weather station
udphandler = UDPHandler(curWeather)
#MQTT For reporting
mqtt = MQTT()

def dispatchUpdate():
  mqtt.SendState({"Digoo": curWeather.DataList})

def sbUpdate():
  dispatchUpdate()

curWeather.OnUpdate = dispatchUpdate

#main loop
async def main():
  mqtt.StartClient()
  await udphandler.startListening()

  logging.info("Initialization complete")

  #keep on chugging forever
  await asyncio.Event().wait()

asyncio.run(main())