#!/usr/bin/python
"""Example file for class DAC8552 in module dac8552:
Grading LED luminosity
Hardware: Waveshare High Precision AD/DA board interfaced to the Raspberry Pi 3
Narcisse Assogba, 2018-07-17
Mods by Mitch Kahn Quantinapril-2020
Dual card mods by Jason Morgan Oct-2020
"""
import sys
from time import sleep
import pigpio as io

from waveshare.DAC8552.pigpio import DAC8552, DAC_A, DAC_B, MODE_POWER_DOWN_100K
from waveshare.DAC8552.default_config import DefaultConfig

# Change this to the local DNS name of your Pi (often raspberrypi.local, if you have changed it) or
# make it blank to connect to localhost.
PI_HOST = 'localhost'

card1 = DefaultConfig()
card2 = DefaultConfig()

card2.CS_PIN = 25

# STEP 1: Initialise DAC object:
dac1 = DAC8552(pi=io.pi(PI_HOST), conf=card1)
dac2 = DAC8552(pi=io.pi(PI_HOST), conf=card2)

try:
    print("\033[2J\033[H")  # Clear screen
    print(__doc__)
    print("\nPress CTRL-C to exit.")

    steps = 50

    dac1.__step = int(dac1.v_ref * dac1.digit_per_v / steps)
    dac2.__step = int(dac2.v_ref * dac2.digit_per_v / steps)

    direction = True
    i = 0
    while True:
        for n, dac in enumerate((dac1, dac2)):
            if direction:
                # STEP 2: Write to DAC:
                dac.write_dac(DAC_A, i * dac.__step)
                dac.write_dac(DAC_B, (steps - i) * dac.__step)
            else:
                dac.write_dac(DAC_A, (steps - i) * dac.__step)
                dac.write_dac(DAC_B, i * dac.__step)

        sleep(0.025)
        i += 1
        if i > steps:
            i = 0
            direction = not direction
except KeyboardInterrupt:
    print("\nUser exit.\n")
    # STEP 3: Put DAC to Power Down Mode:
    for n, dac in enumerate((dac1, dac2)):
        dac.power_down(DAC_A, MODE_POWER_DOWN_100K)
        dac.power_down(DAC_B, MODE_POWER_DOWN_100K)
    sys.exit(0)
