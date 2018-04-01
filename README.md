# Waveshare_e_paper_display
Python library for Waveshare 2.13" e-paper display for use on Raspberry Pi

See www.waveshare.com/wiki/2.13inch_e-Paper_HAT for details of the screen hardware

## Dependencies

* SPI interface on R-Pi should be enabled
* Python libraries spidev and PIL (think both come with R-Pi now)


## Connections

The following table shows the connections assumed by the code:

| Display PIN  | R-Pi GPIO  |
| --- | --- |
| 3.3V | 3.3V |
| GND | GND |
| DIN | MOSI (GPIO10) |
| CLK | SCLK (GPIO11) |
| CS | CE0 (GPIO8) or CE1 (GPIO7) |
| DC | GPIO19 |
| RST | GPIO13 |
| Busy | GPIO6 |


GPIO numbering is BCM, NOT the physical pin number/position on R-Pi.
Note these pin numbers can be changed when initialising the EDP() class (see below).


## Example usage


Create the e-paper display object

	from waveshare_epd_lib import EPD
	epd = EPD()

Draw shapes on screen

	epd.rect((10,10,40,40),fill=0)
	epd.ellipse((10,10,40,40),fill=0)
	epd.line((80,80,140,140),fill=0,width=5)
	epd.text((50,130),'Hello')
	epd.text((10,120),'Hello',fontsize=20)

Update screen with new shapes
	
	epd.update()
	
Clear screen completely. Note the screen flashes during this.

	epd.clear_screen()
	
	
## Setting Pins

The pins used to control the screen can be changed when creating the
EPD() class:

	epd=EPD(reset_pin=13,dc_pin=19,busy_pin=6,spi_dev=1)
                 
                 
The *spi_dev* parameter can be 0 or 1 corresponding to GPIO pins CE0 and CE1                 

