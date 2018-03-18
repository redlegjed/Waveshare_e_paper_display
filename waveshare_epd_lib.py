"""
Consolidated Screen driver for Waveshare 2.13" e-paper screen
==============================================================

Taken from Waveshare code:
* epdif.py
* ep2in13.py


Example usage
================

Create the e-paper display object
>>> epd = EPD()

Draw shapes on screen
>>> epd.screen.rect((10,10,40,40),fill=0)
>>> epd.screen.ellipse((10,10,40,40),fill=0)
>>> epd.screen.line((80,80,140,140),fill=0,width=5)
Update screen with new shapes
>>> epd.update()


"""

#  Copyright 2018  Redlegjed <rlj_github@nym.hush.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

# ===================================
# Imports
# ===================================
import spidev
import RPi.GPIO as GPIO
import time
from PIL import Image
import screen_lib as scr

# ===================================
# Setup
# ===================================

# Pin definition
RST_PIN         = 13 #17
DC_PIN          = 19 #25
CS_PIN          = {0:8,1:7} #8
BUSY_PIN        = 6 #24

# Display resolution
EPD_WIDTH       = 128
EPD_HEIGHT      = 250

# EPD2IN13 commands
DRIVER_OUTPUT_CONTROL                       = 0x01
BOOSTER_SOFT_START_CONTROL                  = 0x0C
GATE_SCAN_START_POSITION                    = 0x0F
DEEP_SLEEP_MODE                             = 0x10
DATA_ENTRY_MODE_SETTING                     = 0x11
SW_RESET                                    = 0x12
TEMPERATURE_SENSOR_CONTROL                  = 0x1A
MASTER_ACTIVATION                           = 0x20
DISPLAY_UPDATE_CONTROL_1                    = 0x21
DISPLAY_UPDATE_CONTROL_2                    = 0x22
WRITE_RAM                                   = 0x24
WRITE_VCOM_REGISTER                         = 0x2C
WRITE_LUT_REGISTER                          = 0x32
SET_DUMMY_LINE_PERIOD                       = 0x3A
SET_GATE_TIME                               = 0x3B
BORDER_WAVEFORM_CONTROL                     = 0x3C
SET_RAM_X_ADDRESS_START_END_POSITION        = 0x44
SET_RAM_Y_ADDRESS_START_END_POSITION        = 0x45
SET_RAM_X_ADDRESS_COUNTER                   = 0x4E
SET_RAM_Y_ADDRESS_COUNTER                   = 0x4F
TERMINATE_FRAME_READ_WRITE                  = 0xFF

# Full update - flickers
LUT_FULL_UPDATE = [
    0x22, 0x55, 0xAA, 0x55, 0xAA, 0x55, 0xAA, 0x11,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E,
    0x01, 0x00, 0x00, 0x00, 0x00, 0x00
]

# Partial update - smoother
LUT_PARTIAL_UPDATE  = [
    0x18, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x0F, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00
]

# SPI device, bus = 0, device = 0
#SPI = spidev.SpiDev(0, 0)
#SPI = spidev.SpiDev(0, 1)




# ===================================
# e-paper screen class
# ===================================

class EPD(scr.Screen):
    """
    e-paper display class

    Example usage
    -------------

    Create e-paper object
    >>> epd = EPD()
    
    
    """

    # Look up tables for screen refresh mode

    
    
    def __init__(self,reset_pin=RST_PIN,dc_pin=DC_PIN,busy_pin=BUSY_PIN,
                 spi_bus=0,spi_dev=1,
                 width=128,height=250,
                 lut_full_update=LUT_FULL_UPDATE,
                 lut_partial_update=LUT_PARTIAL_UPDATE):
        """
        Initialise class
        * Setup pins
        * Connect to screen SPI interface
        * Initialise screen

        Inputs
        -------
        Default pins
        
        reset_pin : int
        dc_pin : int
        busy_pin : int

        SPI bus

        spi_bus : int
            0 or 1 [Default 0]

        spi_device: int
            0 or 1 [Default 1]

        width : int
            width of screen in pixels

        height : int
            height of screen in pixels

        lut_full_update: list
            Lookup table for full update of screen
            Supplied by manufacturer

        lut_partial_update : list
            Lookup table for partial update of screen
            Supplied by manufacturer
        
        """
        super().__init__(width,height)
        
        # Setup pins
        self.reset_pin = reset_pin
        self.dc_pin = dc_pin
        self.busy_pin = busy_pin
        self.cs_pin = CS_PIN[spi_dev]
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self.lut_partial_update = lut_partial_update
        self.lut_full_update = lut_full_update
        self.lut = self.lut_full_update

        # Screen management
        #self.screen = scr.Screen(width=self.width,height=self.height)
        
        

        # Connect to screen over SPI
        self.SPI = spidev.SpiDev(spi_bus, spi_dev)

        # Initialise screen
        self.init(self.lut_partial_update)
        #self.set_to_partial_update()


    


    def update(self):
        """
        Update screen.
        Run this after making changes to a screen
        """

        self.set_frame_memory(self.image,0,0)
        self.display_frame()
        

        # Toggle screen between 0 and 1
        #self.current_screen = not self.current_screen 
    

    def epd_init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.reset_pin, GPIO.OUT)
        GPIO.setup(self.dc_pin, GPIO.OUT)
        GPIO.setup(self.cs_pin, GPIO.OUT)
        GPIO.setup(self.busy_pin, GPIO.IN)
        self.SPI.max_speed_hz = 2000000
        self.SPI.mode = 0b00
        return 0;

    def digital_write(self, pin, value):
        GPIO.output(pin, value)

    def digital_read(self, pin):
        return GPIO.input(BUSY_PIN)

    def delay_ms(self, delaytime):
        time.sleep(delaytime / 1000.0)

    def spi_transfer(self,data):
        self.SPI.writebytes(data)

    def send_command(self, command):
        self.digital_write(self.dc_pin, GPIO.LOW)
        # the parameter type is list but not int
        # so use [command] instead of command
        self.spi_transfer([command])

    def send_data(self, data):
        self.digital_write(self.dc_pin, GPIO.HIGH)
        # the parameter type is list but not int
        # so use [data] instead of data
        self.spi_transfer([data])

    def init(self, lut):
        if (self.epd_init() != 0):
            return -1
        # EPD hardware init start
        self.lut = lut
        self.reset()
        self.send_command(DRIVER_OUTPUT_CONTROL)
        self.send_data((EPD_HEIGHT - 1) & 0xFF)
        self.send_data(((EPD_HEIGHT - 1) >> 8) & 0xFF)
        self.send_data(0x00)                     # GD = 0 SM = 0 TB = 0
        self.send_command(BOOSTER_SOFT_START_CONTROL)
        self.send_data(0xD7)
        self.send_data(0xD6)
        self.send_data(0x9D)
        self.send_command(WRITE_VCOM_REGISTER)
        self.send_data(0xA8)                     # VCOM 7C
        self.send_command(SET_DUMMY_LINE_PERIOD)
        self.send_data(0x1A)                     # 4 dummy lines per gate
        self.send_command(SET_GATE_TIME)
        self.send_data(0x08)                     # 2us per line
        self.send_command(DATA_ENTRY_MODE_SETTING)
        self.send_data(0x03)                     # X increment Y increment
        self.set_lut(self.lut)
        # EPD hardware init end
        return 0

    def set_to_full_update(self):
        self.init(self.lut_full_update)

    def set_to_partial_update(self):
        self.init(self.lut_partial_update)

    def wait_until_idle(self):
        while(self.digital_read(self.busy_pin) == 1):      # 0: idle, 1: busy
            self.delay_ms(100)
##
 #  @brief: module reset.
 #          often used to awaken the module in deep sleep,
 ##
    def reset(self):
        self.digital_write(self.reset_pin, GPIO.LOW)         # module reset
        self.delay_ms(200)
        self.digital_write(self.reset_pin, GPIO.HIGH)
        self.delay_ms(200)    

##
 #  @brief: set the look-up table register
 ##
    def set_lut(self, lut):
        self.lut = lut
        self.send_command(WRITE_LUT_REGISTER)
        # the length of look-up table is 30 bytes
        for i in range(0, len(lut)):
            self.send_data(self.lut[i])

##
 #  @brief: convert an image to a buffer
 ##
    def get_frame_buffer(self, image):
        buf = [0x00] * (self.width * self.height / 8)
        # Set buffer to value of Python Imaging Library image.
        # Image must be in mode 1.
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size
        if imwidth != self.width or imheight != self.height:
            raise ValueError('Image must be same dimensions as display \
                ({0}x{1}).' .format(self.width, self.height))

        pixels = image_monocolor.load()
        for y in range(self.height):
            for x in range(self.width):
                # Set the bits for the column of pixels at the current position.
                if pixels[x, y] != 0:
                    buf[(x + y * self.width) / 8] |= 0x80 >> (x % 8)
        return buf

##
 #  @brief: put an image to the frame memory.
 #          this won't update the display.
 ##
    def set_frame_memory(self, image, x, y):
        if (image == None or x < 0 or y < 0):
            return
        image_monocolor = image.convert('1')
        image_width, image_height  = image_monocolor.size
        # x point must be the multiple of 8 or the last 3 bits will be ignored
        x = x & 0xF8
        image_width = image_width & 0xF8
        if (x + image_width >= self.width):
            x_end = self.width - 1
        else:
            x_end = x + image_width - 1
        if (y + image_height >= self.height):
            y_end = self.height - 1
        else:
            y_end = y + image_height - 1
        self.set_memory_area(x, y, x_end, y_end)
        # send the image data
        pixels = image_monocolor.load()
        byte_to_send = 0x00
        for j in range(y, y_end + 1):
            self.set_memory_pointer(x, j)
            self.send_command(WRITE_RAM)
            # 1 byte = 8 pixels, steps of i = 8
            for i in range(x, x_end + 1):
                # Set the bits for the column of pixels at the current position.
                if pixels[i - x, j - y] != 0:
                    byte_to_send |= 0x80 >> (i % 8)
                if (i % 8 == 7):
                    self.send_data(byte_to_send)
                    byte_to_send = 0x00

##
 #  @brief: clear the frame memory with the specified color.
 #          this won't update the display.
 ##
    def clear_frame_memory(self, color):
        self.set_memory_area(0, 0, self.width - 1, self.height - 1)
        self.set_memory_pointer(0, 0)
        self.send_command(WRITE_RAM)
        # send the color data
        for i in range(0, int(self.width / 8 * self.height)): # added int() [JDB]
            self.send_data(color)

##
 #  @brief: update the display
 #          there are 2 memory areas embedded in the e-paper display
 #          but once this function is called,
 #          the the next action of SetFrameMemory or ClearFrame will 
 #          set the other memory area.
 ##
    def display_frame(self):
        self.send_command(DISPLAY_UPDATE_CONTROL_2)
        self.send_data(0xC4)
        self.send_command(MASTER_ACTIVATION)
        self.send_command(TERMINATE_FRAME_READ_WRITE)
        self.wait_until_idle()

##
 #  @brief: specify the memory area for data R/W
 ##
    def set_memory_area(self, x_start, y_start, x_end, y_end):
        self.send_command(SET_RAM_X_ADDRESS_START_END_POSITION)
        # x point must be the multiple of 8 or the last 3 bits will be ignored
        self.send_data((x_start >> 3) & 0xFF)
        self.send_data((x_end >> 3) & 0xFF)
        self.send_command(SET_RAM_Y_ADDRESS_START_END_POSITION)
        self.send_data(y_start & 0xFF)
        self.send_data((y_start >> 8) & 0xFF)
        self.send_data(y_end & 0xFF)
        self.send_data((y_end >> 8) & 0xFF)

##
 #  @brief: specify the start point for data R/W
 ##
    def set_memory_pointer(self, x, y):
        self.send_command(SET_RAM_X_ADDRESS_COUNTER)
        # x point must be the multiple of 8 or the last 3 bits will be ignored
        self.send_data((x >> 3) & 0xFF)
        self.send_command(SET_RAM_Y_ADDRESS_COUNTER)
        self.send_data(y & 0xFF)
        self.send_data((y >> 8) & 0xFF)
        self.wait_until_idle()

##
 #  @brief: After this command is transmitted, the chip would enter the
 #          deep-sleep mode to save power.
 #          The deep sleep mode would return to standby by hardware reset.
 #          You can use reset() to awaken or init() to initialize
 ##
    def sleep(self):
        self.send_command(DEEP_SLEEP_MODE)
        self.wait_until_idle()


    def clear_screen(self):
        """
        Clear screen using full update method.
        This makes the screen flash, but cleans off all the pixels.
        
        """
        
        # Set to full update mode and clear memory
        self.set_to_full_update()
        self.clear_frame_memory(255)
        self.display_frame()

        # Return to partial update mode
        self.set_to_partial_update()
        
        

# =====================================================
# Demo functions
# =====================================================

def moving_box(epd):
    """
    Box moving across the screen

    """

    epd.screen.rect((20,20,30,30),fill=0,name='box')
    epd.update()

    for offset in range(0,100,10):
        epd.screen['box'].args = [(20,20+offset,30,30+offset)]
        epd.update()

        

    

