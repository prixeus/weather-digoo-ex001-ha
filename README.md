# weather-pi
UDP server for "Digoo DG-EX001" and MQTT integration

Based on reverse engineering done by Mr Łukasz Kalamłacki: http://kalamlacki.eu/sp73.php and further detailed by @matjon https://github.com/matjon/em3371-controller/blob/main/Documentation/device_protocol.md

Should work with any EMAX EM3371 rebranded weasther station

## Current status

* Listens for UDP packets from the Digoo unit (Sent via DNS override of the default SMARTSERVER.EMAXTIME.CN server address)
    * it can be overridden in the Digoo unit's web settings as well
* Deciphers data and displays to screen via terminal
* Dockerfile to build the service that transfers data from the Digoo to the (HAs) MQTT
* Removed all files that weren't necessary to run the translator

## Useful commands:

docker build . -t digoo

docker run -v <settingsfile>:/settings.yaml -p 17000:17000 digoo

Note: update the settings.yaml before usage
