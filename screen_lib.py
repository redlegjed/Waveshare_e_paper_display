"""
PIL based screen classes
---------------------------------

Defines the Screen() class which can be used to make
black and white images for e-paper displays.


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

from collections import OrderedDict

from PIL import Image,ImageDraw,ImageFont


class Screen():
    """
    Screen for use with e-ink displays

    Example usage
    --------------

    Create a Screen object
    >>> scr = Screen()
    
    Draw shapes on screen
    >>> scr.rect((10,10,40,40),fill=0)
    >>> scr.ellipse((10,10,40,40),fill=0)
    >>> scr.line((80,80,140,140),fill=0,width=5)

    Return a PIL image object
    >>> my_image = scr.image

    """

    def __init__(self,width=128,height=250):
        """

        """

        self.width = width
        self.height = height

        self._image = Image.new('1', (self.width, self.height), 255)
        self._draw = ImageDraw.Draw(self._image)

        # Shape list
        # 
        self.shapes = OrderedDict()
        self.shape_counter = 0

    @property
    def image(self):
        self.blank_screen()
        for name,shape in self.shapes.items():
            #shape.function(*shape.args,**shape.kwargs)
            shape.draw()

        return self._image

    def __getitem__(self,key):
        """
        Return shape from self.shapes

        Input
        ------
        key: str
            key in self.shapes
        """

        assert key in self.shapes, "No shape called %s in screen" % key

        return self.shapes[key]


    def reset_screen(self):
        """
        Clear all shapes from memory
        """

        self._image = Image.new('1', (self.width, self.height), 255)
        self._draw = ImageDraw.Draw(self._image)

        self.shapes = OrderedDict()
        self.shape_counter = 0
        

    def blank_screen(self):
        """
        Blank the screen
        """

        self._draw.rectangle((0,0,self.width,self.height),fill=255)

        

    # ------------------------------------------------------
    # Shape classes
    # ------------------------------------------------------
    # Wrapper classes for the shapes supported by ImageDraw

    def rect(self,xy,outline=0,fill=255,name=None):
        """
        Draw rectangle

        Inputs
        -----------
        xy: list of int
            x,y coordinates of two corners of the rectangle
            [x1,y1,x2,y2]

        outline : int
            Outline colour [default=0 (black)]

        fill : int
            fill colour [default=255 (white)]

        """
        if name is None:
            name = 'rect%i' % self.shape_counter
            
        args = [xy]
        kwargs = {'outline':outline,'fill':fill}

        self.shapes[name] = Shape(name,self._draw.rectangle,args,kwargs)
        self.shape_counter +=1



    def line(self,xy,width=1,fill=0,name=None):
        """
        Draw line

        Inputs
        -----------
        xy: list of int
            x,y coordinates of two ends
            [x1,y1,x2,y2]

        width : int
            width of line in pixels [default=1 ]

        fill : int
            line colour [default=0 (black)]

        """
        if name is None:
            name = 'line%i' % self.shape_counter
            
        args = [xy]
        kwargs = {'width':width,'fill':fill}

        self.shapes[name] = Shape(name,self._draw.line,args,kwargs)
        self.shape_counter +=1


    def ellipse(self,xy,outline=0,fill=255,name=None):
        """
        Draw ellipse

        Inputs
        -----------
        xy: list of int
            x,y coordinates of two corners of the bounding box of ellipse
            [x1,y1,x2,y2]

        outline : int
            Outline colour [default=0 (black)]

        fill : int
            fill colour [default=255 (white)]

        """
        if name is None:
            name = 'ellipse%i' % self.shape_counter
            
        args = [xy]
        kwargs = {'outline':outline,'fill':fill}

        
        self.shapes[name] = Shape(name,self._draw.ellipse,args,kwargs)
        self.shape_counter +=1


    def polygon(self,xy,outline=0,fill=255,name=None):
        """
        Draw polygon

        Inputs
        -----------
        xy: list of int
            x,y coordinates of vertices of polygon
            [x1,y1,x2,y2]

        outline : int
            Outline colour [default=0 (black)]

        fill : int
            fill colour [default=255 (white)]

        """
        if name is None:
            name = 'polygon%i' % self.shape_counter
            
        args = [xy]
        kwargs = {'outline':outline,'fill':fill}

        
        self.shapes[name] = Shape(name,self._draw.polygon,args,kwargs)
        self.shape_counter +=1


    def text(self,xy,text_str,fill=0,font=None,name=None):
        """
        Draw text

        Inputs
        -----------
        xy: list of int
            x,y coordinates of where text starts
            [x,y]


        fill : int
            text colour [default=0 (black)]

        """
        if name is None:
            name = 'text%i' % self.shape_counter
            
        args = [xy,text_str]
        kwargs = {'font':font,'fill':fill}

        
        self.shapes[name] = Shape(name,self._draw.text,args,kwargs)
        self.shape_counter +=1




class Shape():
    """
    Structure for a shape 
    """

    def __init__(self,name,function,args,kwargs):
        
        self.name = name
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        return 'Shape(%s)' % self.name

    def draw(self):
        """
        Draw the shape using function
        """

        self.function(*self.args,**self.kwargs)



def make_test_image(scr1):
    """
    Return a test image
    
    """
    scr1.rect([30,30,70,70])
    scr1.ellipse([50,50,90,90])
    scr1.line([1,1,45,65])
    return scr1.image


    
