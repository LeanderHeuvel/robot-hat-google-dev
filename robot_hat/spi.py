#!/usr/bin/env python3
import spidev
class SPI(object):
    def __init__(self, bus, device):
        spi = spidev.SpiDev()
        spi.open(bus, device)


