import paho.mqtt.client as mqtt
import json
from settings import Settings
import getmac
import logging



class MQTT:
  def createClient(self):
    client = mqtt.Client()
    client.username_pw_set(self.__settings['username'],self.__settings['password'])
    return client

  def createOnlineDict(self, topic):
    client = self.createClient()
    client.will_set(topic,"offline",retain=True)
    return {
      "topic": topic,
      "client": client
    }

  def __init__(self):
    self.__settings = Settings()['mqtt']
    self.__client = self.createClient()
    self.__statetopic = self.__settings['basetopic'] + '/state'
    self.__weatherstationOnline = self.createOnlineDict(self.__settings['basetopic'] + '/online/weatherstation')

  def __startAClient(self,client):
    client.connect(self.__settings['host'])
    client.loop_start()

  def __registerHA(self):
    if self.__settings['hatopic'] != None:
      Payload = {
        "unique_id": getmac.get_mac_address() + ":digoo:pressure",
        "name": "Digoo Pressure",
        "availability_topic": self.__weatherstationOnline["topic"],
        "device": {
          "manufacturer":"Digoo",
          "model":"DG-EX001",
          "name":"Digoo Weather Station",
          "identifiers":[getmac.get_mac_address() + ":digoo"],
          "via_device": getmac.get_mac_address()
        },
        "device_class": "pressure",
        "state_class": "measurement",
        "state_topic": self.__settings['basetopic'] + '/state',
        "value_template": "{{ value_json.Digoo.Pressure }}",
        "unit_of_measurement": "hPa"
      }
      self.__client.publish(self.__settings['hatopic'] + "/sensor/digoo/pressure/config", json.dumps(Payload), retain=True)
      Payload = {
        "unique_id": getmac.get_mac_address() + ":digoo:forecast",
        "name": "Digoo Forecast",
        "availability_topic": self.__weatherstationOnline["topic"],
        "device": {
          "manufacturer":"Digoo",
          "model":"DG-EX001",
          "name":"Digoo Weather Station",
          "identifiers":[getmac.get_mac_address() + ":digoo"],
          "via_device": getmac.get_mac_address()
        },
        "state_topic": self.__settings['basetopic'] + '/state',
        "value_template": "{{ value_json.Digoo.Forecast }}"
      }
      self.__client.publish(self.__settings['hatopic'] + "/sensor/digoo/forecast/config", json.dumps(Payload), retain=True)
      Payload = {
        "unique_id": getmac.get_mac_address() + ":digoo:inside:temperature",
        "name": "Digoo Inside Temperature",
        "availability_topic": self.__weatherstationOnline["topic"],
        "device": {
          "manufacturer":"Digoo",
          "model":"DG-EX001",
          "name":"Digoo Weather Station",
          "identifiers":[getmac.get_mac_address() + ":digoo"],
          "via_device": getmac.get_mac_address()
        },
        "device_class": "temperature",
        "state_class": "measurement",
        "state_topic": self.__settings['basetopic'] + '/state',
        "value_template": "{{ value_json.Digoo.MainSensor.Temperature }}",
        "unit_of_measurement": "°C"
      }
      self.__client.publish(self.__settings['hatopic'] + "/sensor/digoo/insidetemperature/config", json.dumps(Payload), retain=True)
      Payload = {
        "unique_id": getmac.get_mac_address() + ":digoo:inside:humidity",
        "name": "Digoo Inside Humidity",
        "availability_topic": self.__weatherstationOnline["topic"],
        "device": {
          "manufacturer":"Digoo",
          "model":"DG-EX001",
          "name":"Digoo Weather Station",
          "identifiers":[getmac.get_mac_address() + ":digoo"],
          "via_device": getmac.get_mac_address()
        },
        "device_class": "humidity",
        "state_class": "measurement",
        "state_topic": self.__settings['basetopic'] + '/state',
        "value_template": "{{ value_json.Digoo.MainSensor.Humidity }}",
        "unit_of_measurement": "%"
      }
      self.__client.publish(self.__settings['hatopic'] + "/sensor/digoo/insidehumidity/config", json.dumps(Payload), retain=True)
      for i in range(3):
        Payload = {
          "unique_id": getmac.get_mac_address() + ":digoo:outside:temperature" + str(i),
          "name": "Digoo Outside Temperature Sensor " + str(i),
          "availability_topic": self.__weatherstationOnline["topic"],
          "device": {
            "manufacturer":"Digoo",
            "model":"DG-EX001",
            "name":"Digoo Weather Station",
            "identifiers":[getmac.get_mac_address() + ":digoo"],
            "via_device": getmac.get_mac_address()
          },
          "device_class": "temperature",
          "state_class": "measurement",
          "state_topic": self.__settings['basetopic'] + '/state',
          "value_template": "{{ value_json.Digoo.RemoteSensor" + str(i) + ".Temperature }}",
          "unit_of_measurement": "°C"
        }
        self.__client.publish(self.__settings['hatopic'] + "/sensor/digoo/outsidetemperature" + str(i) + "/config", json.dumps(Payload), retain=True)
        Payload = {
          "unique_id": getmac.get_mac_address() + ":digoo:outside:humidity" + str(i),
          "name": "Digoo Outside Humidity Sensor " + str(i),
          "availability_topic": self.__weatherstationOnline["topic"],
          "device": {
            "manufacturer":"Digoo",
            "model":"DG-EX001",
            "name":"Digoo Weather Station",
            "identifiers":[getmac.get_mac_address() + ":digoo"],
            "via_device": getmac.get_mac_address()
          },
          "device_class": "humidity",
          "state_class": "measurement",
          "state_topic": self.__settings['basetopic'] + '/state',
          "value_template": "{{ value_json.Digoo.RemoteSensor" + str(i) + ".Humidity }}",
          "unit_of_measurement": "%"
        }
        self.__client.publish(self.__settings['hatopic'] + "/sensor/digoo/outsidehumidity" + str(i) + "/config", json.dumps(Payload), retain=True)


  def StartClient(self):
    try:
      self.__startAClient(self.__client)
      self.__startAClient(self.__weatherstationOnline['client'])
      self.__registerHA()
    except Exception as e:
      logging.error(e)

    logging.info('MQTT Running')


  def SendState(self, data):
    self.CheckSetOnline(data['Digoo']['TimeStamp'],self.__weatherstationOnline)

    del data['Digoo']['TimeStamp']

    packet = json.dumps(data)

    self.__client.publish(self.__statetopic,packet,0)


  def CheckSetOnline(self, payloadTimeStamp, onlineDict):
    onlineDict["client"].publish(onlineDict["topic"],"online" if payloadTimeStamp != None else "offline",retain=True)
