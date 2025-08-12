from typing import Tuple
#import matplotlib.pyplot as plt
import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut
import math

Point = Tuple[int, int]
Color = Tuple[int, int, int, int]
X = 0
Y = 1
start: Point | None = None
end: Point | None = None

def write_pixel(x: int, y: int, color: Color = (0, 0, 0, 1)):
    #plt.plot(x, y, marker='o', color=color)
    gl.glVertex2i(x, y)

def midpoint_line(start: Point, end: Point, color: Color):
    x0, y0 = start[X], start[Y]
    x1, y1 = end[X], end[Y]

    if x0 == x1:
        # Apenas itera no eixo Y
        start_y = min(y0, y1)
        end_y = max(y0, y1)
        for y in range(start_y, end_y + 1):
            write_pixel(x0, y)
        return
    
    # Trata linhas horizontais
    if y0 == y1:
        # Apenas itera no eixo X
        start_x = min(x0, x1)
        end_x = max(x0, x1)
        for x in range(start_x, end_x + 1):
            write_pixel(x, y0)
        return

    # Calcula as diferenças
    dx = x1 - x0
    dy = y1 - y0
    
    # Decide o sentido da variação para x e y
    sx = 1 if dx > 0 else -1
    sy = 1 if dy > 0 else -1
    
    dx = abs(dx)
    dy = abs(dy)
    
    # Caso inclinação <= 1, itera em x
    if dx >= dy:
        d = 2*dy - dx
        y = y0
        
        for x in range(x0, x1 + sx, sx):
            write_pixel(x, y)
            if d > 0:
                y += sy
                d -= 2*dx
            d += 2*dy
    else:
        # Inclinação > 1, itera em y
        d = 2*dx - dy
        x = x0
        
        for y in range(y0, y1 + sy, sy):
            write_pixel(x, y)
            if d > 0:
                x += sx
                d -= 2*dy
            d += 2*dx

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

    gl.glPointSize(10)

    gl.glBegin(gl.GL_POINTS)
    for x in range(0, 16):
        for y in range(0, 16):
            gl.glVertex2i(x, y)
    gl.glEnd()

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
    color: Color = (0, 255, 0, 0) # RGBA

    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    draw_grid()

    gl.glPointSize(12)
    gl.glColor3f(color[0]/255, color[1]/255, color[2]/255)

    if start is not None and end is not None:
        gl.glBegin(gl.GL_POINTS)
        #draw_inc_line(start, end, color)
        midpoint_line(start, end, color)
        gl.glEnd()

        gl.glBegin(gl.GL_LINES)
        gl.glVertex2i(start[X], start[Y])
        gl.glVertex2i(end[X], end[Y])
        gl.glEnd()

    if start is not None:
        gl.glBegin(gl.GL_POINTS)
        gl.glColor4f(0, 0, 1, 1)
        write_pixel(start[X], start[Y])
        gl.glEnd()

    if end is not None:
        gl.glBegin(gl.GL_POINTS)
        gl.glColor4f(1, 0, 0, 1)
        write_pixel(end[X], end[Y])
        gl.glEnd()

    glut.glutSwapBuffers()

def mouse(button: int, state: int, x: int, y: int):
    global start, end
    width = glut.glutGet(glut.GLUT_WINDOW_WIDTH)
    height = glut.glutGet(glut.GLUT_WINDOW_HEIGHT)

    width = glut.glutGet(glut.GLUT_WINDOW_WIDTH)
    height = glut.glutGet(glut.GLUT_WINDOW_HEIGHT)

    print(f"Window size: width={width}, height={height}")
    print(f"Raw mouse pos: x={x}, y={y}")

    if width == 0 or height == 0:
        raise ValueError("Erro: largura ou altura da janela são zero.")
    
    y = height - y  # Corrige a coordenada Y

    grid_x = (x / width) * 15
    grid_y = (y / height) * 15

    grid_x, grid_y = round(grid_x), round(grid_y)

    print(f"Button {'left' if button == glut.GLUT_LEFT_BUTTON else 'right'} was {'pressed' if state == glut.GLUT_DOWN else 'released'}")
    if state == glut.GLUT_DOWN:
        match button:
            case glut.GLUT_LEFT_BUTTON:
                start = (grid_x, grid_y)
                print(f"New start point: {start}")
            case glut.GLUT_RIGHT_BUTTON:
                end = (grid_x, grid_y)
                print(f"New end point point: {end}")
    glut.glutPostRedisplay()  


def keyboard(key, x: int, y: int):
    global start, end
    match key:
        case b'\x1b':
            # Encerra no ESC
            glut.glutLeaveMainLoop()
        case b'r':
            start = None
            end = None


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
    glut.glutKeyboardFunc(keyboard)
    glut.glutMouseFunc(mouse)
    glut.glutMainLoop()