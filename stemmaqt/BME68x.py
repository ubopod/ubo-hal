# Adafruit BME680 library used for connectivity to BME680 & BME688
# Sensor Data Sheet for Bosch BME 688:
# https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme688-ds000.pdf

# TODO: IAQ conversion

# BSEC  3.4 MB Zip, 13 MB uncompressed
# https://www.bosch-sensortec.com/media/boschsensortec/software_tools/software/bme688/08_02_2023/bsec2-4-0-0_generic_release_23012023.zip

# BME AI Studio (licensed blob from Bosch) 652 MB Zip, 1.4 GB extracted, for linux, NOT Raspberry Pi compatible
# https://www.bosch-sensortec.com/media/boschsensortec/software_tools/software/bme688/08_02_2023/bme_ai-studio-v2-0-0-linux.zip


import adafruit_bme680
import time
import board

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()   # uses board.SCL and board.SDA
bme68x = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 995.26  # OAK @ 08:45 20230321


"""
Table 6: Index for Air Quality (IAQ) classification and color-coding12

  IAQ Index Air Quality Impact (long-term exposure) Suggested action

    0 – 50	Excellent Pure air; best for well-being No measures needed.
    51 – 100	Good No irritation or impact on well-being No measures needed.
    101 – 150	Lightly polluted Reduction of well-being possible Ventilation suggested.
    151 – 200	Moderately polluted More significant irritation possible Increase ventilation with clean air.
    201 – 250	Heavily polluted Exposition might lead to effects like
		headache depending on type of VOCs optimize ventilation.
    251 – 350	Severely polluted More severe health issue possible if harmful VOC present.
		Contamination should be identified if level is reached even
		w/o presence of people; maximize ventilation & reduce attendance.
    > 351	Extremely polluted Headaches, additional neurotoxic effects possible.
		Contamination needs to be identified; avoid presence in room and maximize ventilation.

  * These are calculated values, not to be confused with the raw "ohm" value returned from the sensor.
"""

while True:
    print("\nTemperature: %0.1f C" % bme68x.temperature)
    print("Gas: %d ohm" % bme68x.gas)
    print("Humidity: %0.1f %%" % bme68x.relative_humidity)
    print("Pressure: %0.3f hPa" % bme68x.pressure)
    print("Altitude = %0.2f meters" % bme68x.altitude)

    time.sleep(2)
