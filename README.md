# Waveshare_e_paper_display
Python library for Waveshare 2.13" e-paper display for use on Raspberry Pi

See www.waveshare.com/wiki/2.13inch_e-Paper_HAT for details of the screen hardware

## Dependencies

* SPI interface on R-Pi should be enabled
* Python libraries spidev and PIL (think both come with R-Pi now)

## Example usage


Create the e-paper display object

	from waveshare_epd_lib import EPD
	epd = EPD()

Draw shapes on screen

	epd.screen.rect((10,10,40,40),fill=0)
	epd.screen.ellipse((10,10,40,40),fill=0)
	epd.screen.line((80,80,140,140),fill=0,width=5)
	epd.screen.text((50,130),'Hello')

Update screen with new shapes
	
	epd.update()
	
Clear screen completely. Note the screen flashes during this.

	epd.clear_screen()
