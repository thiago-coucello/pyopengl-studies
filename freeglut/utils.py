from OpenGL.GL import * # type: ignore
from PIL import Image
from typing import List

def point(x: float, y: float, z: float = 0):
  glVertex3f(x, y, z)

def color(r: float, g: float, b: float, alpha: float = 1.0):  # type: ignore
	if(r > 1): r = r / 255
	if(g > 1): g = g / 255
	if(b > 1): b = b / 255
	if(alpha > 1): alpha = alpha / 255
	glColor4f(r, g, b, alpha)
     
def getPreviousColor(prev: List[float]):
    glGetFloatv(GL_CURRENT_COLOR, prev)
    
def setColor(rgba: List[float]):
    color(rgba[0], rgba[1], rgba[2], rgba[3])
     
def load_tga_texture(filename: str):
    image = Image.open(filename)
    image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGBA").tobytes()

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)