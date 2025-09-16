from pydoc import text
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from typing import Tuple, List
from glut import writeText  # type: ignore

Point = Tuple[int, int]
Color = Tuple[float, float, float, float]

vertices: List[Point] = []
edge_table: dict[int, List[dict]] = {}
polygon_filled = False
orthoWidth = 25
orthoHeight = 25
textColor = (1, 1, 1, 1)
textFont = GLUT_BITMAP_HELVETICA_12 # type: ignore

# Função para desenhar um pixel

def write_pixel(x: int, y: int, color: Color):
    glColor4f(*color)
    glBegin(GL_POINTS)
    glVertex2i(x, y)
    glEnd()

# Função para inserir arestas na edge table

def insert_edge(start: Point, end: Point):
    global edge_table
    if start[1] > end[1]:
        start, end = end, start
    if start[1] == end[1]:
        return  # Ignora arestas horizontais
    ymin = start[1]
    ymax = end[1]
    x_of_ymin = start[0]
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    inclination = dx / dy if dy != 0 else 0
    edge = {'ymax': ymax, 'xmin': x_of_ymin, 'inclination': inclination}
    if ymin not in edge_table:
        edge_table[ymin] = []
    edge_table[ymin].append(edge)

# Algoritmo de preenchimento usando scanline e regra da paridade

def fill_polygon(color: Color):
    global edge_table, polygon_filled
    if not edge_table:
        return
    scanlines = sorted(edge_table.keys())
    if not scanlines:
        return
    y = scanlines[0]
    max_y = max(edge['ymax'] for edges in edge_table.values() for edge in edges)
    AET: List[dict] = []
    while y <= max_y:
        if y in edge_table:
            AET.extend(edge_table[y])
        AET = [edge for edge in AET if edge['ymax'] != y]
        intersections = [edge['xmin'] for edge in AET]
        intersections.sort()
        i = 0
        while i + 1 < len(intersections):
            x_start = int(round(intersections[i]))
            x_end = int(round(intersections[i+1]))
            for x in range(x_start, x_end):
                write_pixel(x, y, color)
            i += 2
        for edge in AET:
            edge['xmin'] += edge['inclination']
        y += 1
    polygon_filled = True

def draw_grid():
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_LINES)
    for i in range(orthoWidth + 1):
        glVertex2i(i, 0)
        glVertex2i(i, orthoHeight)
    for j in range(orthoHeight + 1):
        glVertex2i(0, j)
        glVertex2i(orthoWidth, j)
    glEnd()

# Função de desenho principal

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    
    writeText(1, 24, "Pressione ESC para sair", clr=textColor, font=textFont) # type: ignore
    writeText(1, 23, f"Defina os vertices clicando no grid! Aperte ENTER para preencher o poligono", clr=textColor, font=textFont) # type: ignore

    draw_grid()
    
    glColor3f(0.5, 0.5, 0.5)
    glPointSize(10)
    # Desenha os vértices
    glBegin(GL_POINTS)
    for vx, vy in vertices:
        glVertex2i(vx, vy)
    glEnd()
    # Desenha as arestas
    if len(vertices) > 1:
        glColor3f(0, 1, 0)
        glBegin(GL_LINE_STRIP)
        for vx, vy in vertices:
            glVertex2i(vx, vy)
        glVertex2i(vertices[0][0], vertices[0][1])  # Fecha o polígono
        glEnd()
    # Preenche o polígono se solicitado
    if polygon_filled:
        fill_polygon((1, 0, 0, 1))
    glutSwapBuffers()

# Função de callback do mouse

def mouse(button, state, x, y):
    global vertices, polygon_filled
    if state == GLUT_DOWN and button == GLUT_LEFT_BUTTON:
        width = glutGet(GLUT_WINDOW_WIDTH)
        height = glutGet(GLUT_WINDOW_HEIGHT)
        y = height - y
        grid_x = int(round((x / width) * orthoWidth))
        grid_y = int(round((y / height) * orthoHeight))
        vertices.append((grid_x, grid_y))
        polygon_filled = False
        glutPostRedisplay()

# Função de callback do teclado

def keyboard(key, x, y):
    global edge_table, polygon_filled
    if key == b'\x1b':
        glutLeaveMainLoop()
    elif key == b'\r' or key == b'\n':
        if len(vertices) > 2:
            edge_table.clear()
            for i in range(len(vertices)):
                insert_edge(vertices[i], vertices[(i+1)%len(vertices)])
            polygon_filled = True
        glutPostRedisplay()
    elif key == b'r':
        vertices.clear()
        edge_table.clear()
        polygon_filled = False
        glutPostRedisplay()

# Inicialização da tela

def initScreen():
    glClearColor(0, 0, 0, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, orthoWidth, 0, orthoHeight)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA) #type: ignore
    glutInitWindowSize(800, 800)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Preenchimento de Poligono Arbitrario - PyOpenGL")
    initScreen()
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutMainLoop()
