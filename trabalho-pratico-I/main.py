# main.py
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from typing import Tuple, Optional

from numpy import poly
from glut import writeText

Point = Tuple[int, int]
Color = Tuple[int, int, int, int]  # OpenGL espera floats entre 0 e 1

#vertices: list[Point] = []
vertices: list[Point] = [(2, 3), (7, 1), (13, 5), (13, 11), (7, 7), (2, 9)]

orthoWidth = 25
orthoHeight = 25

X, Y = 0, 1
gridStart = (1, 1)
gridEnd = (16, 16)
textColor: Color = (1, 1, 1, 1)  # Cor do texto
textFont = GLUT_BITMAP_HELVETICA_12  # Fonte do texto # type: ignore

class Edge:
    def __init__(self, ymax: int, xmin: float, inclination: float):
        self.ymax = ymax
        self.xmin = xmin
        self.inclination = inclination

edge_table: dict[int, list[Edge]] = {}

def write_pixel(x: int, y: int, color: Color):
    glColor4f(*color)
    glBegin(GL_POINTS)
    glVertex2i(x, y)
    glEnd()

def insert_edge(start: Point, end: Point):
    global edge_table
    if start[Y] > end[Y]:
        start, end = end, start

    if start[Y] == end[Y]:
        return  # Ignore horizontal edges

    ymin = start[Y]
    ymax = end[Y]
    denominator = end[Y] - start[Y]
    numerator = end[X] - start[X]
    inclination = numerator / denominator if denominator != 0 else 0
    new_edge = Edge(ymax, start[X], inclination)

    # Adiciona a aresta na lista do dicionário
    if ymin not in edge_table:
        edge_table[ymin] = []
    edge_table[ymin].append(new_edge)


def pause():
    print("Pressione ENTER para continuar...")
    input()

def arbitrary_polygon_drawing(color: Color):
    global edge_table, polygon_processed
    if not edge_table:
        return

    scanlines = sorted(edge_table.keys())
    if not scanlines:
        return

    y = scanlines[0]
    max_y = max(edge.ymax for edges in edge_table.values() for edge in edges)
    AET: list[Edge] = []

    while y <= max_y or AET:
        # 3.1: Adiciona arestas que começam nesta scanline
        if y in edge_table:
            AET.extend(edge_table[y])

        # 3.2: Remove arestas cujo ymax == y
        AET = [edge for edge in AET if edge.ymax != y]


        # 3.3: Ordena AET por xmin
        AET.sort(key=lambda edge: edge.xmin)

        # 3.4: Preenche pixels entre pares de arestas
        i = 0
        while i + 1 < len(AET):
            x_start = int(round(AET[i].xmin))
            x_end = int(round(AET[i+1].xmin))

            for x in range(x_start, x_end):
                write_pixel(x, y, color)
            i += 2

        # 3.5: Atualiza xmin das arestas restantes na AET
        for edge in AET:
            edge.xmin += edge.inclination

        y += 1

    polygon_processed = True

# Exemplo de uso:
# insert_edge((10, 10), (20, 30))
# insert_edge((20, 30), (30, 10))
# insert_edge((30, 10), (10, 10))
# arbitrary_polygon_drawing((1.0, 0.0, 0.0))

##################################### UI FUNCTIONS #####################################    

def draw_grid():
    glColor3f(0.5, 0.5, 0.5)  # cinza claro
    glLineWidth(1)

    glPointSize(10)

    glBegin(GL_POINTS)
    for x in range(gridStart[X], gridEnd[X] + 1):
        for y in range(gridStart[Y], gridEnd[Y] + 1):
            glVertex2i(x, y)
    glEnd()

    glBegin(GL_LINES)
    # Linhas verticais
    for x in range(gridStart[X], gridEnd[X] + 1):
        glVertex2f(x, gridStart[Y])
        glVertex2f(x, gridEnd[Y])
    # Linhas horizontais
    for y in range(gridStart[Y], gridEnd[Y] + 1):
        glVertex2f(gridStart[X], y)
        glVertex2f(gridEnd[X], y)
    glEnd()

    # Desenha os números dos eixos X e Y
    glColor3f(1, 1, 1)  # branco para os números
    for x in range(gridStart[X], gridEnd[X] + 1):
        writeText(x, gridStart[Y] - 0.7, str(x), clr=textColor, font=textFont)  # eixo X
    for y in range(gridStart[Y], gridEnd[Y] + 1):
        writeText(gridStart[X] - 0.7, y, str(y), clr=textColor, font=textFont)  # eixo Y

def mouse(button: int, state: int, x: int, y: int):
    global start, end
    width = glutGet(GLUT_WINDOW_WIDTH)
    height = glutGet(GLUT_WINDOW_HEIGHT)

    width = glutGet(GLUT_WINDOW_WIDTH)
    height = glutGet(GLUT_WINDOW_HEIGHT)

    if width == 0 or height == 0:
        raise ValueError("Erro: largura ou altura da janela são zero.")
    
    y = height - y  # Corrige a coordenada Y

    grid_x = (x / width) * orthoWidth
    grid_y = (y / height) * orthoHeight

    grid_x, grid_y = round(grid_x), round(grid_y)

    if state == GLUT_DOWN:
        if grid_x < gridStart[X] or grid_x > gridEnd[X] or grid_y < gridStart[Y] or grid_y > gridEnd[Y]:
            return
        
        if button == GLUT_LEFT_BUTTON:
            vertices.append((grid_x, grid_y))
    glutPostRedisplay()


def keyboard(key, x: int, y: int):
    global vertices, edge_table
    key = key.lower()  # Normaliza a tecla para minúscula
    match key:
        case b'\x1b':
            # Encerra no ESC
            glutLeaveMainLoop()
        case b'r':
            vertices.clear()
            print("Reiniciando...")
        case b'\r' | b'\n':  # Enter
            if len(vertices) > 2:
                edge_table.clear()
                for i in range(len(vertices)):
                    insert_edge(vertices[i], vertices[(i+1)%len(vertices)])
            else:
                print("Adicione pelo menos 3 vértices.")
        case _:
            print(f"Tecla desconhecida: {key}")
    glutPostRedisplay()


def initScreen():
    glClearColor(0, 0, 0, 1) # Clean screen with black background
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Defining the coordinates system
    gluOrtho2D(0, orthoWidth, 0, orthoHeight)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def display():
    glClear(GL_COLOR_BUFFER_BIT)

    draw_grid()

    glPointSize(12)

    writeText(1, 22, "Pressione 'r' para reiniciar", clr=textColor, font=textFont) # type: ignore
    writeText(1, 21, "Pressione ESC para sair", clr=textColor, font=textFont) # type: ignore
    writeText(1, 20, "Clique para adicionar vertices, ENTER para desenhar o poligono", clr=textColor, font=textFont) # type: ignore

    # Drawing vertices
    glColor3f(0, 1, 0)
    glPointSize(10)
    glBegin(GL_POINTS)
    for vx, vy in vertices:
        glVertex2i(vx, vy)
    glEnd()

    # Drawing edges
    if len(vertices) > 1:
        glColor3f(0, 1, 0)
        glBegin(GL_LINE_STRIP)
        for vx, vy in vertices:
            glVertex2i(vx, vy)
        glVertex2i(vertices[0][0], vertices[0][1])  # Fecha o polígono
        glEnd()

    if len(edge_table) > 0:
        arbitrary_polygon_drawing((1, 0, 0, 1))

    glutSwapBuffers()

if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA) # type: ignore
    glutInitWindowSize(800, 800)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Arbitrary Polygon Filling - PyOpenGL")

    initScreen()
    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutMainLoop()
