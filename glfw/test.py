import glfw
import glm
from OpenGL.GL import *
import numpy as np
from shaders import load_shader
from PIL import Image
import time

# ---- Inicialização do GLFW ----
if not glfw.init():
    raise Exception("Falha ao inicializar GLFW")

# Criar janela
window = glfw.create_window(800, 600, "GLFW + PyOpenGL", None, None)
if not window:
    glfw.terminate()
    raise Exception("Falha ao criar a janela")

glfw.make_context_current(window)

# ---- Compilar e linkar shaders ----
vertex_shader = load_shader("shaders/vertex.glsl", GL_VERTEX_SHADER)
fragment_shader = load_shader("shaders/fragment.glsl", GL_FRAGMENT_SHADER)

shader_program = glCreateProgram()
glAttachShader(shader_program, vertex_shader)
glAttachShader(shader_program, fragment_shader)
glLinkProgram(shader_program)

# Verificar erros de linkagem
if not glGetProgramiv(shader_program, GL_LINK_STATUS):
    error = glGetProgramInfoLog(shader_program).decode()
    raise Exception(f"Erro linkando programa: {error}")

# Deletar shaders após linkagem
glDeleteShader(vertex_shader)
glDeleteShader(fragment_shader)

shaderColorLocation = glGetUniformLocation(shader_program, "uColor")

# ---- Dados do triângulo ----
vertices = np.array([
     # posições        # tex coords
     0.0,  0.5, 0.0,   0.5, 1.0,
    -0.5, -0.5, 0.0,   0.0, 0.0,
     0.5, -0.5, 0.0,   1.0, 0.0
], dtype=np.float32)

# VAO e VBO
VAO = glGenVertexArrays(1)
VBO = glGenBuffers(1)

glBindVertexArray(VAO)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

# posição
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * vertices.itemsize, None)
glEnableVertexAttribArray(0)
# tex coord
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * vertices.itemsize, ctypes.c_void_p(3 * vertices.itemsize))
glEnableVertexAttribArray(1)

# ---------------- Carregar textura ----------------
texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture)
# parâmetros de repetição e filtro
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

# carregar imagem
image = Image.open("tartaruga.tga").transpose(Image.Transpose.FLIP_TOP_BOTTOM)
img_data = image.convert("RGBA").tobytes()
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
glGenerateMipmap(GL_TEXTURE_2D)

# ---------------- Loop principal ----------------
start_time = time.time()
currentPos = 0
dPos = 0.01
while not glfw.window_should_close(window):
    glfw.poll_events()
    glClearColor(0.2, 0.3, 0.3, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # Ativar shader e textura
    glUseProgram(shader_program)
    glBindTexture(GL_TEXTURE_2D, texture)

    # Criar matriz de transformação com rotação
    current_time = time.time() - start_time
    transform = glm.mat4(1.0)
    transform = glm.rotate(transform, glm.radians(current_time * 50), glm.vec3(0.0, 0.0, 1.0))  # rotaciona no eixo Z #type: ignore

    currentPos += dPos

    if currentPos > 1 or currentPos < -1:
        dPos = dPos * -1

    transform = glm.translate(transform, glm.vec3(currentPos, 0, 0)) #type: ignore

    # Enviar matriz para o shader
    transform_loc = glGetUniformLocation(shader_program, "transform")
    glUniformMatrix4fv(transform_loc, 1, GL_FALSE, np.array(transform.to_list(), dtype=np.float32))

    glBindVertexArray(VAO)
    glDrawArrays(GL_TRIANGLES, 0, 3)

    glfw.swap_buffers(window)

# ---------------- Encerramento ----------------
glDeleteVertexArrays(1, [VAO])
glDeleteBuffers(1, [VBO])
glDeleteProgram(shader_program)
glfw.terminate()
