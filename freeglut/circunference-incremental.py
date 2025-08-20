from os import times
import sys
import time
import math
import numpy as np
import matplotlib.pyplot as plt
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Raio máximo e número de testes
MAX_RADIUS = 200
TESTS_PER_RADIUS = 50

# Estruturas para armazenar os tempos
times_incremental = []
times_second_order = []
times_trig = []

# ===============================
# Algoritmos de desenho de círculo
# ===============================

def draw_circle_trig(radius: int):
    """Desenha um círculo usando seno e cosseno."""
    step = 1 / radius
    angle = 0.0
    while angle <= math.pi / 4:  # apenas 1/8 do círculo (simetria)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        angle += step
    return


def draw_circle_midpoint(radius: int):
    """Desenha um círculo usando o algoritmo do ponto médio incremental."""
    x = 0
    y = radius
    d = 1 - radius
    while x <= y:
        x += 1
        if d < 0:
            d += 2 * x + 1
        else:
            y -= 1
            d += 2 * (x - y) + 1
    return


def draw_circle_midpoint_second_order(radius: int):
    """Desenha um círculo usando ponto médio com diferenças de segunda ordem."""
    x = 0
    y = radius
    d = 1 - radius
    deltaE = 3
    deltaSE = 5 - 2 * radius
    while x <= y:
        x += 1
        if d < 0:
            d += deltaE
            deltaE += 2
            deltaSE += 2
        else:
            y -= 1
            d += deltaSE
            deltaE += 2
            deltaSE += 4
    return

# =================================
# Função para medir tempos
# =================================
def measure_time():
    for r in range(1, MAX_RADIUS + 1):
        # Incremental
        start = time.perf_counter()
        for _ in range(TESTS_PER_RADIUS):
            draw_circle_midpoint(r)
        end = time.perf_counter()
        times_incremental.append((end - start) / TESTS_PER_RADIUS)

        # Segunda ordem
        start = time.perf_counter()
        for _ in range(TESTS_PER_RADIUS):
            draw_circle_midpoint_second_order(r)
        end = time.perf_counter()
        times_second_order.append((end - start) / TESTS_PER_RADIUS)

        # Seno e Cosseno
        start = time.perf_counter()
        for _ in range(TESTS_PER_RADIUS):
            draw_circle_trig(r)
        end = time.perf_counter()
        times_trig.append((end - start) / TESTS_PER_RADIUS)

# =================================
# Função OpenGL para exibir gráfico
# =================================
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glutSwapBuffers()

    if len(times_incremental) > 0:
        glBegin(GL_LINES)
        glColor3f(1, 0, 0)  # Vermelho para incremental
        glVertex2f(0, times_incremental[0])
        for i in range(1, len(times_incremental) + 1):
            # Desenha gráfico para cada algoritmo
            glVertex2f(i, times_incremental[i])
        glEnd()

    if len(times_second_order) > 0:
        glBegin(GL_LINES)
        glColor3f(0, 1, 0)  # Verde para segunda    
        glVertex2f(0, times_second_order[0])
        for i in range(1, len(times_second_order) + 1):
            glVertex2f(i, times_second_order[i])
        glEnd()

    if len(times_trig) > 0:
        glBegin(GL_LINES)
        glColor3f(0, 0, 1)
        glVertex2f(0, times_trig[0])
        for i in range(1, len(times_trig) + 1):
            glVertex2f(i, times_trig[i])
        glEnd()

# =================================
# Execução principal
# =================================
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB) #type: ignore
    glutInitWindowSize(500, 500)
    glutCreateWindow(b"Medindo tempos - Algoritmos de Circulo")
    glClearColor(1, 1, 1, 1)
    gluOrtho2D(0, 500, 0, 500)

    # Mede tempos
    print("Medindo tempos...")
    measure_time()
    print("Finalizado!")

    # Fecha janela após medir
    glutDisplayFunc(display)
    glutMainLoop()

if __name__ == "__main__":
    main()

    # Após medir tempos, plota gráfico
    radii = np.arange(1, MAX_RADIUS + 1)
    plt.figure(figsize=(10, 6))
    plt.plot(radii, times_incremental, label="Incremental 1ª ordem")
    plt.plot(radii, times_second_order, label="Incremental 2ª ordem")
    plt.plot(radii, times_trig, label="Seno/Cosseno")
    plt.xlabel("Raio")
    plt.ylabel("Tempo médio (s)")
    plt.title("Comparação de Algoritmos de Desenho de Círculo")
    plt.legend()
    plt.grid()
    plt.show()
