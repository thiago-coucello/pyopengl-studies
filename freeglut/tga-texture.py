from OpenGL.GLUT import * # type: ignore
from OpenGL.GLU import * # type: ignore
from OpenGL.GL import * # type: ignore
from typing import Tuple
from glut import load_tga_texture, point, color, getPreviousColor, setColor, writeText
from math import cos, sin
import numpy as np

PI = 3.1415926535897    # Valor de PI para desenho de círculos
NO_TEXTURES = 3	        # Numero de texturas utilizadas

texture_id: Tuple

textureNumber = 0
stopAnimation = 1

angle: float = 0 
fAspect: float = 0 
rotationAngle: float = 0
    
	
'''
# **********************************************************************
#  void initTexture(void)
#		Define a textura a ser usada 
#
# **********************************************************************
'''
def initTexture():
    global texture_id
    # Habilita o uso de textura 
    glEnable ( GL_TEXTURE_2D )

    # Define a forma de armazenamento dos pixels na textura (1= alihamento por byte)
    glPixelStorei ( GL_UNPACK_ALIGNMENT, 1 )

    # Define quantas texturas serao usadas no programa 
    texture_id = glGenTextures (NO_TEXTURES)  # 1 = uma textura
                                    # texture_id = vetor que guardas os numeros das texturas

    # Define que tipo de textura será usada
    # GL_TEXTURE_2D ==> define que será usada uma textura 2D (bitmaps)
    # texture_id[CUBE_TEXTURE]  ==> define o número da textura 
    glBindTexture( GL_TEXTURE_2D, texture_id[0])

    # carrega a uma imagem TGA 
    load_tga_texture("earth.tga")

    glBindTexture( GL_TEXTURE_2D, texture_id[1])
    load_tga_texture("tartaruga.tga")

    glBindTexture( GL_TEXTURE_2D, texture_id[2])
    load_tga_texture("Tree.tga")

    glDisable(GL_TEXTURE_2D)

def drawCircle(radius: float):
    glBegin(GL_TRIANGLE_FAN)
    angles = np.linspace(0, 2 * PI, 1000)
    for angle in angles:
      point(cos(angle) * radius, sin(angle) * radius)
    glEnd()

def drawWireSquare(size: float, lineWidth: float):
  squareSize: float = size/2
  glLineWidth(lineWidth)
  glBegin(GL_LINE_LOOP)
  
  point(-squareSize, squareSize)
  point(squareSize, squareSize)
  point(squareSize, -squareSize)
  point(-squareSize, -squareSize)

  glEnd()
  glLineWidth(1.0)

def drawSquare(size: float, withBorder: bool):
  squareSize: float = size/2
  glBegin(GL_QUADS)

  point(-squareSize, squareSize)
  point(squareSize, squareSize)
  point(squareSize, -squareSize)
  point(-squareSize, -squareSize)

  glEnd()

  if withBorder:
    prev = getPreviousColor()
    color(0,0,0, 1)
    drawWireSquare(size, 10)
    setColor(prev)

def drawTexturedSquare(size: float, textureNumber: int, withBorder: bool):
    global texture_id
    squareSize: float = size/2
    glBindTexture ( GL_TEXTURE_2D, texture_id[textureNumber] )
    glEnable(GL_TEXTURE_2D)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0)
    point(-squareSize, squareSize, 0)
    glTexCoord2f(1.0, 1.0)
    point(squareSize, squareSize, 0)
    glTexCoord2f(1.0, 0.0)
    point(squareSize, -squareSize, 0)
    glTexCoord2f(0.0, 0.0)
    point(-squareSize, -squareSize, 0)
    glEnd()
    glDisable(GL_TEXTURE_2D)
	
    if withBorder:
        prev = getPreviousColor()
        color(0,0,0)
        drawWireSquare(size, 7.5)
        setColor(prev)

def drawTexturedCircle(radius: float, textureNumber: int):
    global texture_id
    glBindTexture ( GL_TEXTURE_2D, texture_id[textureNumber] )
    glEnable(GL_TEXTURE_2D)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glBegin(GL_TRIANGLE_FAN)
    glTexCoord2f(0, 0)
    angles = np.linspace(0, 2 * PI, 1000)
    for angle in angles:
        glTexCoord2f(cos(angle) * radius, sin(angle) * radius)
        point(cos(angle) * radius, sin(angle) * radius, 0)
    glEnd()
    glDisable(GL_TEXTURE_2D)

		        
# Função callback chamada para fazer o desenho
def draw():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
	# Limpa a janela e o depth buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # type: ignore

    glColor3f(0.0, 0.0, 1.0)

    glPushMatrix()
    glLoadIdentity()
    writeText(-15, 25, "Aplicacao de Texturas com PyOpenGL", font=GLUT_BITMAP_TIMES_ROMAN_24) # type: ignore
    glPopMatrix()

    glPushMatrix()
    # Tela
    glPushMatrix()
    color(1, 1, 1)
    glTranslatef(0, 15, 1.0)
    # Borda
    drawSquare(15, True)
        
    # Quadro com Textura
    glPushMatrix()
    color(0, 1, 0)
    glTranslatef(0, 0, 0.5)
    drawTexturedSquare(13, textureNumber, True)
    #drawTexturedCircle(8, textureNumber)
    glPopMatrix()
    glPopMatrix()
		
    # Armário
    glPushMatrix()
    color(0.6, 0.4, 0)
    glTranslatef(0, -10, 0)
	#Parte central
    drawSquare(20, True)
			
    # Parte de cima
    glPushMatrix()
    glScalef(2.2, 0.2, 1)
    glTranslatef(0, 50, 1.0)
    drawSquare(10, True)
    # Fim parte de cima
    glPopMatrix()
			
    # Porta da direita
    glPushMatrix()
    color(0, 0, 0)
    glTranslatef(-5, -1, 1.0)
    glScalef(0.9, 1.7, 1)
    drawWireSquare(10, 5)
				
    # Maçaneta
    glPushMatrix()
    color(0.9, 0.1, 0.1)
    glTranslatef(3, 0, 0)
    drawCircle(0.75)
    # Fim maçaneta
    glPopMatrix()

    # Fim porta da direita		
    glPopMatrix()
			
    # Porta da esquerda
    glPushMatrix()
    color(0, 0, 0)
    glTranslatef(5, -1, 1.0)
    glScalef(0.9, 1.7, 1)
    drawWireSquare(10, 5)
				
    # Maçaneta
    glPushMatrix()
    color(0.9, 0.1, 0.1)
    glTranslatef(-3, 0, 0)
    drawCircle(0.75)
    # Fim maçaneta
    glPopMatrix()

    # Fim porta da esquerda				
    glPopMatrix()
			
    # Pé direito
    glPushMatrix()
    color(0.6, 0.4, 0)
    glTranslatef(-8, -12.5, 0)
    glScalef(0.2, 0.4, 1)
    drawSquare(10, True)
    glPopMatrix()
			
    # Pé esquerdo
    glPushMatrix()
    color(0.6, 0.4, 0)
    glTranslatef(8, -12.5, 0)
    glScalef(0.2, 0.4, 1)
    drawSquare(10, True)
    glPopMatrix()
			
    glPopMatrix()
		
    color(0.8, 0.8, 0.3)
    glScalef(1, 2, 1)
    drawSquare(30, True)
    glPopMatrix()
	
    glutSwapBuffers()

# Inicializa par?metros de rendering
def init(): 
    # Especifica que a cor de fundo da janela é branca
    glClearColor(1.0, 1.0, 1.0, 1.0)

    # Habilita o depth-buffering
    glEnable(GL_DEPTH_TEST)
    # Habilida o blend
    glEnable(GL_BLEND)

    # Colorização Gouraund
    glShadeModel(GL_SMOOTH)	

# Função usada para especificar o volume de visualização
def defineVisualizationParams():
	# Especifica sistema de coordenadas de projeção
	glMatrixMode(GL_PROJECTION)
	# Carrega a matriz identidade
	glLoadIdentity()
	# Utiliza projeção ortogonal
	glOrtho(-50, 50, -50, 50, -20, 20)
	
	# Limpa os buffers
	glClear(GL_COLOR_BUFFER_BIT)

# Função callback chamada quando o tamanho da janela é alterado 
def resizeWindow(w: int, h: int):
	# Para previnir uma divisão por zero
	if ( h == 0 ): h = 1

	# Especifica o tamanho da viewport
	glViewport(0, 0, w, h)

	defineVisualizationParams()

def keyboard(key, x: int, y: int):
    global textureNumber

    match key:
        case b'\x1b':
            print("ESC pressed! Terminating...")
            glutLeaveMainLoop()

        case b'1':
            textureNumber = 0
        case b'2':
            textureNumber = 1
        case b'3':
            textureNumber = 2

    glutPostRedisplay()

if __name__ == "__main__":
	#Inicia a Telinha
    glutInit()

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH) # type: ignore
    glutInitWindowSize(1280, 900)
    glutCreateWindow("Atividade Textura")
	
    init()
    initTexture()
	
    glutDisplayFunc(draw)
    glutKeyboardFunc(keyboard)
    glutReshapeFunc(resizeWindow)
    glutMainLoop()

    exit(0)