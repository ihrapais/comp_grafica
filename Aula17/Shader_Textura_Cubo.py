# -*- coding: utf-8 -*-
"""
Exemplo: cubo texturizado que pulsa de verde para vermelho no tempo
Usa OpenGL 4.0 core em Python (PyOpenGL + GLFW + Pyrr)
Padronizado: inicializa_opengl(), inicializa_shaders(), inicializa_resources(), render_loop(), main()
Inclui movimentação de câmera com WSAD.

Produto de Aprendizagem 03 - Anderson Schieck Lopes
Baseado nos conceitos de fragment shaders da Aula 17
"""
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
from PIL import Image
import time
import pyrr
import ctypes

# --- Parâmetros da janela e variáveis globais ---
WIDTH, HEIGHT = 800, 600      # resolução da janela
window = None                 # handle da janela GLFW
program = None                # ID do programa de shaders
vao = None                    # ID do VAO do cubo
texture_id = None             # ID da textura carregada
start_time = None             # hora de início para animação

# Vetores de câmera - conceitos aplicados da disciplina
cam_pos = pyrr.Vector3([0.0, 0.0, 3.0])   # posição da câmera no espaço 3D
cam_front = pyrr.Vector3([0.0, 0.0, -1.0]) # direção para onde a câmera aponta
cam_up = pyrr.Vector3([0.0, 1.0, 0.0])    # vetor "para cima" da câmera

# ## SUGESTÃO APLICADA: Variáveis para armazenar as localizações dos uniforms ##
loc_model, loc_view, loc_proj, loc_time = None, None, None, None

# ---------- Inicialização do contexto OpenGL ----------
def inicializa_opengl():
    """
    Inicia GLFW, cria janela e contexto OpenGL.
    Configura o ambiente gráfico necessário para renderização.
    """
    global window
    if not glfw.init():
        raise RuntimeError("Falha ao inicializar GLFW")
    
    # Configuração do contexto OpenGL 4.0 Core Profile
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 0)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    
    window = glfw.create_window(WIDTH, HEIGHT, "Cubo Pulsante - PA03", None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError("Falha ao criar janela GLFW")
    
    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST) # ativa teste de profundidade para renderização 3D

# ---------- Compilação e linkagem de shaders ----------
def inicializa_shaders():
    """
    Compila fontes GLSL e configura o programa de shaders.
    Implementa os conceitos de fragment shaders estudados na Aula 17.
    """
    global program, loc_model, loc_view, loc_proj, loc_time
    
    # Vertex shader - transforma vértices do espaço objeto para espaço de tela
    vertex_src = """
        #version 400 core
        layout(location=0) in vec3 in_pos;   // posição do vértice (x,y,z)
        layout(location=1) in vec2 in_uv;    // coordenadas de textura (u,v)
        
        // Matrizes de transformação MVP (Model-View-Projection)
        uniform mat4 model;      // transforma do espaço objeto para mundo
        uniform mat4 view;       // transforma do espaço mundo para câmera  
        uniform mat4 projection; // transforma do espaço câmera para tela
        
        out vec2 frag_uv;        // passa coordenadas UV para fragment shader
        
        void main() {
            frag_uv = in_uv;
            // Pipeline de transformação: objeto -> mundo -> câmera -> tela
            gl_Position = projection * view * model * vec4(in_pos, 1.0);
        }
    """
    
    # Fragment shader - aplica conceitos da Aula 17: mix(), sin(), manipulação de cores
    fragment_src = """
        #version 400 core
        in vec2 frag_uv;                 // coordenadas UV interpoladas
        uniform sampler2D texture1;      // textura aplicada ao cubo
        uniform float u_time;            // tempo para animação
        out vec4 FragColor;              // cor final do pixel
        
        void main() {
            // Amostra a cor da textura nas coordenadas UV atuais
            vec4 tex = texture(texture1, frag_uv);
            
            // Cria pulso senoidal (Exemplo 09 - Curvas Matemáticas)
            // abs(sin(u_time)) varia de 0 a 1 no tempo
            float pulse = abs(sin(u_time));
            
            // Interpolação de cores (conceito mix() - Exemplo 19)
            // Verde (0,1,0) para Vermelho (1,0,0) baseado no pulso
            vec3 color = mix(vec3(0.0, 1.0, 0.0), vec3(1.0, 0.0, 0.0), pulse);
            
            // Aplica a cor pulsante sobre a textura (multiplicação de cores)
            FragColor = vec4(tex.rgb * color, tex.a);
        }
    """
    
    # Compilação e linkagem dos shaders
    vs = OpenGL.GL.shaders.compileShader(vertex_src, GL_VERTEX_SHADER)
    fs = OpenGL.GL.shaders.compileShader(fragment_src, GL_FRAGMENT_SHADER)
    program = OpenGL.GL.shaders.compileProgram(vs, fs)

    # ## SUGESTÃO APLICADA: Otimização de uniforms ##
    # Busca e armazena a localização dos uniforms uma única vez aqui.
    loc_model = glGetUniformLocation(program, "model")
    loc_view = glGetUniformLocation(program, "view")
    loc_proj = glGetUniformLocation(program, "projection")
    loc_time = glGetUniformLocation(program, "u_time")

# ---------- Carregamento do VAO e textura ----------
def inicializa_resources():
    """
    Cria VAO do cubo e carrega textura.
    Configura os buffers de vértices com posições e coordenadas UV.
    """
    global vao, texture_id
    
    # Stride: 5 componentes por vértice (3 posição + 2 textura) × 4 bytes por float
    stride = 5 * ctypes.sizeof(ctypes.c_float)
    
    # Dados do cubo: posição (x,y,z) + coordenadas UV (u,v) para cada vértice
    vertices = np.array([
        # Face frontal
        -0.5, -0.5,  0.5,  0.0, 0.0,   # vértice inferior esquerdo
         0.5, -0.5,  0.5,  1.0, 0.0,   # vértice inferior direito
         0.5,  0.5,  0.5,  1.0, 1.0,   # vértice superior direito
        -0.5, -0.5,  0.5,  0.0, 0.0,   # repete para formar triângulos
         0.5,  0.5,  0.5,  1.0, 1.0,
        -0.5,  0.5,  0.5,  0.0, 1.0,   # vértice superior esquerdo
        
        # Face traseira
        -0.5, -0.5, -0.5,  1.0, 0.0,
        -0.5,  0.5, -0.5,  1.0, 1.0,
         0.5,  0.5, -0.5,  0.0, 1.0,
        -0.5, -0.5, -0.5,  1.0, 0.0,
         0.5,  0.5, -0.5,  0.0, 1.0,
         0.5, -0.5, -0.5,  0.0, 0.0,
        
        # Face esquerda
        -0.5, -0.5, -0.5,  0.0, 0.0,
        -0.5, -0.5,  0.5,  1.0, 0.0,
        -0.5,  0.5,  0.5,  1.0, 1.0,
        -0.5, -0.5, -0.5,  0.0, 0.0,
        -0.5,  0.5,  0.5,  1.0, 1.0,
        -0.5,  0.5, -0.5,  0.0, 1.0,
        
        # Face direita
         0.5, -0.5, -0.5,  1.0, 0.0,
         0.5,  0.5, -0.5,  1.0, 1.0,
         0.5,  0.5,  0.5,  0.0, 1.0,
         0.5, -0.5, -0.5,  1.0, 0.0,
         0.5,  0.5,  0.5,  0.0, 1.0,
         0.5, -0.5,  0.5,  0.0, 0.0,
        
        # Face superior
        -0.5,  0.5, -0.5,  0.0, 1.0,
        -0.5,  0.5,  0.5,  0.0, 0.0,
         0.5,  0.5,  0.5,  1.0, 0.0,
        -0.5,  0.5, -0.5,  0.0, 1.0,
         0.5,  0.5,  0.5,  1.0, 0.0,
         0.5,  0.5, -0.5,  1.0, 1.0,
        
        # Face inferior
        -0.5, -0.5, -0.5,  0.0, 0.0,
         0.5, -0.5, -0.5,  1.0, 0.0,
         0.5, -0.5,  0.5,  1.0, 1.0,
        -0.5, -0.5, -0.5,  0.0, 0.0,
         0.5, -0.5,  0.5,  1.0, 1.0,
        -0.5, -0.5,  0.5,  0.0, 1.0,
    ], dtype=np.float32)

    # Configuração do VAO (Vertex Array Object)
    vao = glGenVertexArrays(1)           # 1) Gera ID do VAO
    vbo = glGenBuffers(1)                # 2) Gera ID do VBO (Vertex Buffer Object)
    
    glBindVertexArray(vao)               # 3) Vincula VAO para configuração
    
    # Envia dados dos vértices para a GPU
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    
    # Configura atributo 0: posições (x,y,z)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    
    # ## SUGESTÃO APLICADA: Offset calculado ##
    # O offset agora é calculado para maior clareza, em vez de usar o número "mágico" 12.
    offset_uv = ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float))
    # Configura atributo 1: coordenadas UV (u,v)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, offset_uv)
    
    glBindVertexArray(0) # Desvincula VAO para evitar modificações acidentais
    
    # === Carregamento de textura ===
    try:
        # Carrega imagem e inverte verticalmente (OpenGL usa coordenadas invertidas)
        img = Image.open("textura.jpg").transpose(Image.FLIP_TOP_BOTTOM)
        data = img.convert("RGBA").tobytes() # Converte para formato RGBA
        w, h = img.size
    except FileNotFoundError:
        raise RuntimeError("Arquivo 'textura.jpg' não encontrado!")

    # Configuração da textura OpenGL
    texture_id = glGenTextures(1)                # Gera ID da textura
    glActiveTexture(GL_TEXTURE0)                 # Seleciona texture unit 0
    glBindTexture(GL_TEXTURE_2D, texture_id)   # Vincula textura

    # Parâmetros de filtragem (suavização quando textura é ampliada/reduzida)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Envia dados da imagem para a GPU
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    
    glBindTexture(GL_TEXTURE_2D, 0) # Desvincula textura

    # Vincula sampler do fragment shader à texture unit 0
    glUseProgram(program)
    loc = glGetUniformLocation(program, "texture1")
    glUniform1i(loc, 0)

# ---------- Loop principal de renderização ----------
def render_loop():
    """
    Loop de eventos e renderização com controle WSAD.
    Implementa o ciclo de renderização em tempo real.
    """
    global start_time, cam_pos
    start_time = time.time()
    glfw.set_time(0) # Reinicia contador de tempo do GLFW
    
    # Matriz modelo (identidade - sem transformações no objeto)
    model = pyrr.matrix44.create_identity(dtype=np.float32)
    
    while not glfw.window_should_close(window):
        # Cálculo do delta time para movimento independente de framerate
        delta_time = glfw.get_time()
        glfw.set_time(0)
        current_time = time.time() - start_time
        
        glfw.poll_events() # Processa eventos de entrada
        
        # === Controle de câmera WSAD (corrigido) ===
        speed = 2.5 * delta_time # Velocidade baseada no tempo real
        
        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS: 
            cam_pos += cam_front * speed     # Move para frente
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS: 
            cam_pos -= cam_front * speed     # Move para trás
            
        # Calcula vetor direito (perpendicular ao front e up)
        right = pyrr.vector.normalize(pyrr.vector3.cross(cam_front, cam_up))
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS: 
            cam_pos += right * speed         # Move para direita
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS: 
            cam_pos -= right * speed         # Move para esquerda
        
        # === Renderização ===
        glClearColor(0.1, 0.1, 0.1, 1.0) # Cor de fundo cinza escuro
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glUseProgram(program) # Ativa programa de shaders
        
        # Matriz view (câmera): define posição e orientação da câmera
        view = pyrr.matrix44.create_look_at(
            cam_pos,               # posição da câmera
            cam_pos + cam_front,   # ponto para onde olha
            cam_up,                # vetor up
            dtype=np.float32
        )
        
        # Matriz de projeção em perspectiva
        proj = pyrr.matrix44.create_perspective_projection_matrix(
            45.0,             # campo de visão (FOV) em graus
            WIDTH / HEIGHT,   # proporção da tela (aspect ratio)
            0.1,              # plano próximo (near)
            100.0,            # plano distante (far)
            dtype=np.float32
        )
        
        # ## SUGESTÃO APLICADA: Usa as localizações cacheadas ##
        # Envia matrizes e tempo para os shaders usando os IDs armazenados
        glUniformMatrix4fv(loc_model, 1, GL_FALSE, model)
        glUniformMatrix4fv(loc_view, 1, GL_FALSE, view)
        glUniformMatrix4fv(loc_proj, 1, GL_FALSE, proj)
        glUniform1f(loc_time, current_time)
        
        # Renderiza o cubo
        glActiveTexture(GL_TEXTURE0)                 # Ativa texture unit 0
        glBindTexture(GL_TEXTURE_2D, texture_id)   # Vincula textura
        glBindVertexArray(vao)                       # Vincula VAO com dados do cubo
        glDrawArrays(GL_TRIANGLES, 0, 36)            # Desenha 36 vértices (12 triângulos)
        
        glfw.swap_buffers(window) # Exibe frame renderizado
    
    glfw.terminate() # Limpa recursos do GLFW

# ---------- Função principal ----------
def main():
    """
    Função principal que coordena a inicialização e execução.
    Segue a estrutura padronizada da disciplina.
    """
    inicializa_opengl()     # Configura contexto OpenGL
    inicializa_shaders()    # Compila e linka shaders
    inicializa_resources()  # Carrega geometria e texturas
    render_loop()           # Executa loop principal

if __name__ == "__main__":
    main()