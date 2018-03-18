# Waveshare_e_paper_display
Python library for Waveshare 2.13" e-paper display

## Example usage


Create the e-paper display object
	
	epd = EPD()

Draw shapes on screen

	epd.screen.rect((10,10,40,40),fill=0)
	epd.screen.ellipse((10,10,40,40),fill=0)
	epd.screen.line((80,80,140,140),fill=0,width=5)

Update screen with new shapes
	
	epd.update()
