#!/usr/bin/env python3
from .basic import _Basic_class
# import RPi.GPIO as GPIO
from periphery import GPIO

'''
Robot Hat Library adapted for Google Dev Board
TODO: finish IRQ alternative

'''

class Pin(_Basic_class):

    OUT = "out"
    IN = "in"
    IRQ_FALLING = "falling"
    IRQ_RISING = "rising"
    IRQ_RISING_FALLING = "both"
    PULL_UP = "pull_up"
    PULL_DOWN = "pull_down"
    PULL_NONE = "disable"

    _dict = {
        "BOARD_TYPE": 12,
    }
    _dict_3 = {
        "D0": ["/dev/ttymxc2",None], #UART 11
        "D1": ["/dev/gpiochip4",10], #UART or SAI
        "D2": ["/dev/gpiochip0",0],
        "D3": [2, 0], #PWM
        "D4": ["/dev/gpiochip2", 9],
        "D5": ["/dev/gpiochip4", 10],
        "D6": ["/dev/gpiochip4", 12],
        "D7": [""], #UART 7
        "D8": ["/dev/gpiochip0", 7],
        "D9": ["/dev/gpiochip0", 8],
        "D10": [""], #PWM 32
        "D11": [""], #PWM 33
        "D12": [""], ##SAI 35 Synchronous audio interface
        "D13": ["/dev/gpiochip4", 13], #GPIO on 36
        "D14": ["/dev/gpiochip2", 13], #37
        "D15": [], ## SAI 38
        "D16": [] #SAI 40
    }
    _dict_1 = {
        "D0":  17,
        "D1":  18,
        "D2":  27,
        "D3":  22,
        "D4":  23,
        "D5":  24,
        "D6":  25,
        "D7":  4,
        "D8":  5,
        "D9":  6,
        "D10": 12,
        "D11": 13,
        "D12": 19,
        "D13": 16,
        "D14": 26,
        "D15": 20,
        "D16": 21, 
        "SW":  19,
        "USER": 19,        
        "LED": 26,
        "BOARD_TYPE": 12,
        "RST": 16,
        "BLEINT": 13,
        "BLERST": 20,
        "MCURST": 21,

    }

    _dict_2 = {
        "D0":  17,
        "D1":   4, # Changed
        "D2":  27,
        "D3":  22,
        "D4":  23,
        "D5":  24,
        "D6":  25, # Removed
        "D7":   4, # Removed
        "D8":   5, # Removed
        "D9":   6,
        "D10": 12,
        "D11": 13,
        "D12": 19,
        "D13": 16,
        "D14": 26,
        "D15": 20,
        "D16": 21,     
        "SW":  25, # Changed
        "USER": 25,
        "LED": 26,
        "BOARD_TYPE": 12,
        "RST": 16,
        "BLEINT": 13,
        "BLERST": 20,
        "MCURST":  5, # Changed
    }
    #value is a str type e.g. D2 and will be converted using dict
    def __init__(self, *value):
        super().__init__()
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setwarnings(False)
        self.gpio = None
        self.check_board_type()
        print(value)
        if len(value) > 0:
            pin = value[0]
            print("Pin: ",pin)
        if len(value) > 1:
            mode = value[1]
            print("mode: ",mode)
        else:
            mode = None
        if len(value) > 2:
            setup = value[2]
        else:
            setup = None
        if isinstance(pin, str):
            try:
                self._board_name = pin
                self._pin = self.dict()[pin]
            except Exception as e:
                print(e)
                self._error('Pin should be in %s, not %s' % (self._dict.keys(), pin))
        elif isinstance(pin, int):
            self._pin = pin
        else:
            self._error('Pin should be in %s, not %s' % (self._dict.keys(), pin))
        self._value = 0
        self.init(mode, pull=setup)
        self._info("Pin init finished.")
        
    def check_board_type(self):
        self._dict = self._dict_3

    def init(self, mode, pull=None):
        self._pull = pull
        self._mode = mode
        if mode != None:
            if pull != None:
                self.gpio = GPIO(self._pin[0], self._pin[1], bias = pull)
                # GPIO.setup(self._pin, mode, pull_up_down=pull)
            else:
                self.gpio = GPIO(self._pin[0], self._pin[1], mode)
                # GPIO.setup(self._pin, mode)

    def dict(self, *_dict):
        if len(_dict) == 0:
            return self._dict
        else:
            if isinstance(_dict, dict):
                self._dict = _dict
            else:
                self._error(
                    'argument should be a pin dictionary like {"my pin": ezblock.Pin.cpu.GPIO17}, not %s' % _dict)

    def __call__(self, value):
        return self.value(value)

    def value(self, *value):
        if len(value) == 0:
            if self._mode in [None, self.OUT]:
                #assure that mode is set to reading when value() without arguments in the constructor is called
                self.mode(self.IN)
            result = self.gpio.read()
            # result = GPIO.input(self._pin)
            self._debug("read pin %s: %s" % (self._pin, result))
            return result
        else:
            value = value[0]
            if self._mode in [None, self.IN]:
                self.mode(self.OUT)
            self.gpio.write(value)
            # GPIO.output(self._pin, value)
            return value

    def on(self):
        return self.value(1)

    def off(self):
        return self.value(0)

    def high(self):
        return self.on()

    def low(self):
        return self.off()

    def mode(self, *value):
        if len(value) == 0:
            return (self._mode, self._pull)
        else:
            self._mode = value[0]
            if len(value) == 1:
                self.gpio = GPIO(self._pin[0], self._pin[1], self._mode)
                # GPIO.setup(self._pin, self._mode)
            elif len(value) == 2:
                self._pull = value[1]
                self.gpio = GPIO(self._pin[0], self._pin[1], self._mode, bias = self._pull) #pull functionality not implemented yet
                # GPIO.setup(self._pin, self._mode, self._pull)

    def pull(self, *value):
        return self._pull

    def irq(self, handler=None, trigger=None, bouncetime=200):
        self.mode(self.IN)
        #not implemented yet, periphery has not an out-of-the-box working alternative for creating callbacks on events
        # GPIO.add_event_detect(self._pin, trigger, callback=handler, bouncetime=bouncetime)

    def name(self):
        return "GPIO%s"%self._pin

    def names(self):
        return [self.name, self._board_name]

    class cpu(object):
        GPIO17 = 17
        GPIO18 = 18
        GPIO27 = 27
        GPIO22 = 22
        GPIO23 = 23
        GPIO24 = 24
        GPIO25 = 25
        GPIO26 = 26
        GPIO4  = 4
        GPIO5  = 5
        GPIO6  = 6
        GPIO12 = 12
        GPIO13 = 13
        GPIO19 = 19
        GPIO16 = 16
        GPIO26 = 26
        GPIO20 = 20
        GPIO21 = 21

        def __init__(self):
            pass
