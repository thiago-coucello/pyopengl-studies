from OpenGL.GL import *

# ---- Função para carregar shaders ----
def load_shader(shader_file, shader_type):
    with open(shader_file, 'r') as f:
        shader_src = f.read()

    shader = glCreateShader(shader_type)
    glShaderSource(shader, shader_src)
    glCompileShader(shader)

    # Verificar erros de compilação
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(shader).decode()
        raise Exception(f"Erro compilando shader {shader_file}: {error}")

    return shader