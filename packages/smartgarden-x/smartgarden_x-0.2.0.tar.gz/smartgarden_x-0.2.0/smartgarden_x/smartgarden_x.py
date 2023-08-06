"""Main module."""

import Adafruit_DHT

class SmartGardenX:

	def dht11_sensor(self, condition):
		pin = 17
		dht11 = Adafruit_DHT.DHT11
		humidity, temperature = Adafruit_DHT.read_retry(dht11, pin)
		if condition == "temperature":
			return temperature
		elif condition == "humidity":
			return humidity
		else:
			pass

	def temperature(self):
		return self.dht11_sensor("temperature")

	def humidity(self):
		return self.dht11_sensor("humidity")
