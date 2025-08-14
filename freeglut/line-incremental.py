from textwrap import fill
from typing import Literal, NamedTuple, Tuple, List
#import matplotlib.pyplot as plt
import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as Glut
import math
import numpy as np
from glut import writeText


mode: Literal["line", "circle"] = "line"
technique: Literal["implicit", "midpoint"] = "implicit"
filled: bool = False

Point = Tuple[int, int]
Color = Tuple[int, int, int, int]
X = 0
Y = 1
start: Point | None = None
end: Point | None = None

class Element(NamedTuple):
    start: Point
    end: Point
    shape: Literal["line", "circle"]
    technique: Literal["implicit", "midpoint"]
    filled: bool

elements: List[Element] = []

orthoWidth = 25
orthoHeight = 25

gridStart = (1, 1)
gridEnd = (16, 16)
textColor: Color = (1, 1, 1, 1)  # Cor do texto
textFont = Glut.GLUT_BITMAP_HELVETICA_12  # Fonte do texto # type: ignore

def add_element(start: Point, end: Point, shape: Literal["line", "circle"], technique: Literal["implicit", "midpoint"] = technique, filled: bool = filled):
    global elements
    if start is None or end is None:
        return
    
    new_element = Element(start, end, shape, technique, filled)
    if new_element not in elements:
        elements.append(new_element)

def write_pixel(x: int, y: int, color: Color = (0, 0, 0, 1)):
    #plt.plot(x, y, marker='o', color=color)
    r, g, b, a = color

    if r > 1:
        r /= 255
    if g > 1:
        g /= 255
    if b > 1:
        b /= 255
        
    gl.glColor4f(r, g, b, a)
    gl.glVertex2i(x, y)

def circle_point_symmetry(x: int, y: int, cx: int, cy: int, color: Color = (1, 1, 0, 1)):
    return [
        (cx + x, cy + y),  # 2º octante
        (cx + y, cy + x),  # 1º octante
        (cx - y, cy + x),  # 8º octante
        (cx - x, cy + y),  # 7º octante
        (cx - x, cy - y),  # 6º octante
        (cx - y, cy - x),  # 5º octante
        (cx + y, cy - x),  # 4º octante
        (cx + x, cy - y),  # 3º octante
    ]

def draw_circle(center: Point, radius: int, color: Color):
    xo, yo = center

    angles = np.linspace(45, 90, 1000, endpoint=False)
    points = []
    for angle in angles:
        rad = math.radians(angle)
        x = round(radius * math.cos(rad))
        y = round(radius * math.sin(rad))
        points.extend(circle_point_symmetry(x, y, xo, yo, color))
    
     # Remover duplicatas e ordenar
    points = list(set(points))  # evita repetição
    points.sort(key=lambda p: math.atan2(p[1] - yo, p[0] - xo))  # ordena pelo ângulo

    # Desenhar em ordem
    for px, py in points:
        write_pixel(px, py, color)

def midpoint_circle(center: Point, radius: int, color: Color):
    center_x, center_y = center
    d = 1 - radius
    x, y = 0, radius
    delta_x = lambda x: 2 * x + 3
    delta_y = lambda x, y: 2 * (x - y) + 5

    points = []
    points.extend(circle_point_symmetry(x, y, center_x, center_y, color))

    while x < y:
        if d < 0:
            d += delta_x(x)
        else:
            d += delta_y(x, y)
            y -= 1
        x += 1
        points.extend(circle_point_symmetry(x, y, center_x, center_y, color))

    # Remover duplicatas e ordenar
    points = list(set(points))  # evita repetição
    points.sort(key=lambda p: math.atan2(p[1] - center_y, p[0] - center_x))  # ordena pelo ângulo

    # Desenhar em ordem
    for px, py in points:
        write_pixel(px, py, color)

def midpoint_line(start: Point, end: Point, color: Color):
    x0, y0 = start[X], start[Y]
    x1, y1 = end[X], end[Y]

    if x0 == x1:
        # Apenas itera no eixo Y
        start_y = min(y0, y1)
        end_y = max(y0, y1)
        for y in range(start_y, end_y + 1):
            write_pixel(x0, y, color)
        return
    
    # Trata linhas horizontais
    if y0 == y1:
        # Apenas itera no eixo X
        start_x = min(x0, x1)
        end_x = max(x0, x1)
        for x in range(start_x, end_x + 1):
            write_pixel(x, y0, color)
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
            write_pixel(x, y, color)
            if d > 0:
                y += sy
                d -= 2*dx
            d += 2*dy
    else:
        # Inclinação > 1, itera em y
        d = 2*dx - dy
        x = x0
        
        for y in range(y0, y1 + sy, sy):
            write_pixel(x, y, color)
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
    for x in range(gridStart[X], gridEnd[X] + 1):
        for y in range(gridStart[Y], gridEnd[Y] + 1):
            gl.glVertex2i(x, y)
    gl.glEnd()

    gl.glBegin(gl.GL_LINES)
    # Linhas verticais
    for x in range(gridStart[X], gridEnd[X] + 1):
        gl.glVertex2f(x, gridStart[Y])
        gl.glVertex2f(x, gridEnd[Y])
    # Linhas horizontais
    for y in range(gridStart[Y], gridEnd[Y] + 1):
        gl.glVertex2f(gridStart[X], y)
        gl.glVertex2f(gridEnd[X], y)
    gl.glEnd()

def draw_shape(start: Point, end: Point, mode: Literal["line", "circle"], technique: Literal["implicit", "midpoint"], filled: bool):
    if mode == "line":
            gl.glBegin(gl.GL_POINTS)
            if technique == "implicit":
                draw_inc_line(start, end, color=(0, 1, 0, 1))
            elif technique == "midpoint":
                midpoint_line(start, end, color=(0, 1, 0, 1))
            gl.glEnd()
    elif mode == "circle":
        radius = int(math.sqrt((end[X] - start[X])**2 + (end[Y] - start[Y])**2))
        
        if filled:
            gl.glBegin(gl.GL_TRIANGLE_FAN)
        else:
            gl.glBegin(gl.GL_POINTS)
        
        if technique == "implicit":
            draw_circle(start, radius, color=(1, 1, 0, 1))
        elif technique == "midpoint":
            midpoint_circle(start, radius, color=(1, 1, 0, 1))
        
        gl.glEnd()

def display():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    draw_grid()

    gl.glPointSize(12)

    writeText(1, 24, "Pressione 'c' para circulo, 'l' para linha", clr=textColor, font=textFont) # type: ignore
    writeText(1, 23, "Pressione 'i' para implicita, 'm' para ponto medio", clr=textColor, font=textFont) # type: ignore
    writeText(1, 22, "Pressione 'r' para reiniciar", clr=textColor, font=textFont) # type: ignore
    writeText(1, 21, "Pressione ESC para sair", clr=textColor, font=textFont) # type: ignore
    writeText(1, 18, f"Modo: {mode}, Tecnica: {technique}", clr=textColor, font=textFont) # type: ignore

    if start is not None and end is not None:
        draw_shape(start, end, mode, technique=technique, filled=filled)

        gl.glBegin(gl.GL_LINES)
        gl.glVertex2i(start[X], start[Y])
        gl.glVertex2i(end[X], end[Y])
        gl.glEnd()

    if start is not None:
        gl.glBegin(gl.GL_POINTS)
        write_pixel(start[X], start[Y], color=(0, 0, 1, 1))
        gl.glEnd()

    if end is not None:
        gl.glBegin(gl.GL_POINTS)
        write_pixel(end[X], end[Y], color=(1, 0, 0, 1))
        gl.glEnd()

    if len(elements) > 0:
        for element in elements:
            draw_shape(element.start, element.end, element.shape, element.technique, element.filled)

    Glut.glutSwapBuffers()

def mouse(button: int, state: int, x: int, y: int):
    global start, end
    width = Glut.glutGet(Glut.GLUT_WINDOW_WIDTH)
    height = Glut.glutGet(Glut.GLUT_WINDOW_HEIGHT)

    width = Glut.glutGet(Glut.GLUT_WINDOW_WIDTH)
    height = Glut.glutGet(Glut.GLUT_WINDOW_HEIGHT)

    if width == 0 or height == 0:
        raise ValueError("Erro: largura ou altura da janela são zero.")
    
    y = height - y  # Corrige a coordenada Y

    grid_x = (x / width) * orthoWidth
    grid_y = (y / height) * orthoHeight

    grid_x, grid_y = round(grid_x), round(grid_y)

    if state == Glut.GLUT_DOWN:
        if grid_x < gridStart[X] or grid_x > gridEnd[X] or grid_y < gridStart[Y] or grid_y > gridEnd[Y]:
            start = None
            end = None
            return
        
        match button:
            case Glut.GLUT_LEFT_BUTTON:
                start = (grid_x, grid_y)
            case Glut.GLUT_RIGHT_BUTTON:
                end = (grid_x, grid_y)
    Glut.glutPostRedisplay()  


def keyboard(key, x: int, y: int):
    global start, end, mode, technique, filled
    key = key.lower()  # Normaliza a tecla para minúscula
    match key:
        case b'\x1b':
            # Encerra no ESC
            Glut.glutLeaveMainLoop()
        case b'r':
            start = None
            end = None
            elements.clear()
            print("Reiniciando...")
        case b'c':
            mode = "circle"
        case b'l':
            mode = "line"
        case b'm':
            technique = "midpoint"
        case b'i':
            technique = "implicit"
        case b'f':
            filled = not filled
        case b'a':
            if start is not None and end is not None:
                add_element(start, end, mode, technique, filled)
                print(f"Elemento adicionado: {start} -> {end} como {mode}")
        case _:
            print(f"Tecla desconhecida: {key}")
    Glut.glutPostRedisplay()


def initScreen():
    gl.glClearColor(0, 0, 0, 1) # Clean screen with black background
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()

    # Defining the coordinates system 
    glu.gluOrtho2D(0, orthoWidth, 0, orthoHeight)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()

if __name__ == "__main__":
    Glut.glutInit()
    Glut.glutInitDisplayMode(Glut.GLUT_DOUBLE | Glut.GLUT_RGBA) # type: ignore
    Glut.glutInitWindowSize(800, 800)
    Glut.glutInitWindowPosition(100, 100)
    Glut.glutCreateWindow(b"implicit Line Drawing - PyOpenGL")

    initScreen()
    Glut.glutDisplayFunc(display)
    Glut.glutIdleFunc(display)
    Glut.glutKeyboardFunc(keyboard)
    Glut.glutMouseFunc(mouse)
    Glut.glutMainLoop()