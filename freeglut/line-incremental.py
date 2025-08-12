from typing import Tuple
import matplotlib.pyplot as plt
import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut

Point = Tuple[int, int]
Color = Tuple[int, int, int, int]
X = 0
Y = 1

def write_pixel(x: int, y: int, color: Color):
    #plt.plot(x, y, marker='o', color=color)
    gl.glVertex2i(x, y)

def draw_inc_line(start: Point, end: Point, color: Color):
    dx = end[X] - start[X]
    dy = end[Y] - start[Y]
    d = 2 * dy - dx # Starting value of 'd'
    incE = 2 * dy   # E increment
    incNE = 2 * (dy - dx) # NE increment

    x = start[X]
    y = start[Y]

    #plt.figure()
    write_pixel(x, y, color)
    while (x < end[X]):
        if d <= 0:
            # Pick E
            d += incE
            x += 1
        else:
            # Pick NE
            d += incNE
            x += 1
            y += 1
        write_pixel(x, y, color)
    #plt.grid(True)
    #plt.show()

def draw_grid():
    gl.glColor3f(0.5, 0.5, 0.5)  # cinza claro
    gl.glLineWidth(1)

    gl.glBegin(gl.GL_LINES)
    # Linhas verticais
    for x in range(0, 16):
        gl.glVertex2f(x, 0)
        gl.glVertex2f(x, 15)
    # Linhas horizontais
    for y in range(0, 16):
        gl.glVertex2f(0, y)
        gl.glVertex2f(15, y)
    gl.glEnd()

def displayPoints():
    start: Point = (5, 8)
    end: Point = (9, 11)
    color: Color = (255, 0, 0, 0) # RGBA

    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    draw_grid()

    gl.glColor3f(color[0]/255, color[1]/255, color[2]/255)   # Cor branca
    gl.glPointSize(20)

    gl.glBegin(gl.GL_POINTS)
    draw_inc_line(start, end, color)
    gl.glEnd()

    glut.glutSwapBuffers()

def initScreen():
    gl.glClearColor(0, 0, 0, 1) # Clean screen with black background
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()

    # Defining the coordinates system 
    glu.gluOrtho2D(0, 15, 0, 15)

if __name__ == "__main__":
    glut.glutInit()
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA) # type: ignore
    glut.glutInitWindowSize(500, 500)
    glut.glutInitWindowPosition(100, 100)
    glut.glutCreateWindow(b"Incremental Line Drawing - PyOpenGL")

    initScreen()
    glut.glutDisplayFunc(displayPoints)
    glut.glutIdleFunc(displayPoints)
    glut.glutMainLoop()