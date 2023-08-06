import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import time
import math

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

cs = digitalio.DigitalInOut(board.D5)

mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P1)

B = 4275
R0 = 10000

while True:
	R = 1023.0/chan.value - 1.0
	R = R0 * R
	temp = 1.0 / (math.log(abs(R/R0))/B + 1 / 289.15) - 273.15
	print("Temp: ", temp)
	print("Raw ADC Value: ", (chan.value*3.3)/1024.0)
	print("ADC Voltage: " + str((chan.voltage*3.3)/1024.0) + "V")
	time.sleep(2)
