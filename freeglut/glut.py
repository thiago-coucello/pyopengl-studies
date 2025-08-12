from OpenGL.GL import * # type: ignore
from OpenGL.GLUT import * # type: ignore
from OpenGL.GLU import * # type: ignore
from typing import Tuple
from PIL import Image
import ctypes

Point = Tuple[float, float]
Color = Tuple[float, float, float, float]

def point(x: float, y: float, z: float = 0):
    glVertex3f(x, y, z)

def color(r: float, g: float, b: float, alpha: float = 1):
    if(r > 1): r = r / 255
    if(g > 1): g = g / 255
    if(b > 1): b = b / 255
    if(alpha > 1): alpha = alpha / 255
    glColor4f(r, g, b, alpha)

def setColor(rgba: Color):
    color(rgba[0], rgba[1], rgba[2], rgba[3])

def getPreviousColor() -> Tuple[float, float, float, float]:
    data = (ctypes.c_float * 4)()
    glGetFloatv(GL_CURRENT_COLOR, data)
    return tuple(data)

def load_tga_texture(filename: str):
    image = Image.open(filename)
    image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGBA").tobytes()

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

'''
/************************
*				FONTS LIST			*
*************************

* GLUT_BITMAP_8_BY_13 - A variable-width font with every character fitting in a rectangle of 13 pixels high by at most 8 pixels wide.
* GLUT_BITMAP_9_BY_15 - A variable-width font with every character fitting in a rectangle of 15 pixels high by at most 9 pixels wide.
* GLUT_BITMAP_TIMES_ROMAN_10 - A 10-point variable-width Times Roman font.
* GLUT_BITMAP_TIMES_ROMAN_24 - A 24-point variable-width Times Roman font.
* GLUT_BITMAP_HELVETICA_10 - A 10-point variable-width Helvetica font.
* GLUT_BITMAP_HELVETICA_12 - A 12-point variable-width Helvetica font.
* GLUT_BITMAP_HELVETICA_18 - A 18-point variable-width Helvetica font.
* GLUT_STROKE_ROMAN - A proportionally-spaced Roman Simplex font
* GLUT_STROKE_MONO_ROMAN - A fixed-width Roman Simplex font

*************************/
'''

def writeText(x: float, y: float, text: str, clr: Color = (0, 0, 0, 1), font: int = GLUT_BITMAP_TIMES_ROMAN_24): # type: ignore
    previousColors = getPreviousColor()
    color(clr[0], clr[1], clr[2], clr[3])
    glRasterPos2f(x, y)

    encoded_text = text.encode("utf-8")
    text_pointer = ctypes.c_char_p(encoded_text)
    glutBitmapString(font, text_pointer)
    
    setColor(previousColors)