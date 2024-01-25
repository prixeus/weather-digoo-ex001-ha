import yaml
import logging
import sys

class Settings:
  __instance = None
  def __new__(cls):
    if Settings.__instance == None:
      logging.info("Grabbing settings")
      with open("settings.yaml","r") as stream:
        try:
          Settings.__instance = yaml.load(stream, Loader=yaml.SafeLoader)
        except:
          logging.error("malformed settings file")
          sys.exit()
    return Settings.__instance



