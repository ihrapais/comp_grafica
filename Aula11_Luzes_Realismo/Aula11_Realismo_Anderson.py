# Importação das bibliotecas necessárias
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np
import os # Necessário para manipulação de caminhos

# Variáveis globais de posição e rotação da câmera
camera_x, camera_y, camera_z = 0, 2, -10 # Ajustei Y inicial para ver melhor o chão
rot_x, rot_y = 0, 0

# Função que carrega uma imagem e a transforma em textura OpenGL (versão robusta)
def load_texture(filename):
    try:
        # Construir caminho absoluto para o arquivo de textura
        # __file__ é o caminho do script atual
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, filename)

        # Verificar se o arquivo existe
        if not os.path.exists(file_path):
            print(f"ERRO: Arquivo de textura não encontrado em: '{file_path}'")
            return None # Retorna None se não encontrar

        # Verificar permissão de leitura (menos comum ser problema, mas bom ter)
        if not os.access(file_path, os.R_OK):
            print(f"ERRO: Sem permissão para ler o arquivo: '{file_path}'")
            return None # Retorna None se não tiver permissão

        print(f"Tentando carregar: {file_path}")
        img = Image.open(file_path)
        print(f"Carregou {filename} com sucesso! Formato: {img.format}, Tamanho: {img.size}")

        # Processamento da imagem para OpenGL
        img = img.transpose(Image.FLIP_TOP_BOTTOM) # Vira a imagem
        img_data = img.convert("RGBA").tobytes()   # Converte para bytes RGBA
        width, height = img.size

        # Geração e configuração da textura OpenGL
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        print(f"Textura {filename} carregada com ID: {tex_id}")
        return tex_id # Retorna o ID da textura em caso de sucesso

    except FileNotFoundError:
        # Esta exceção pode não ser necessária devido ao os.path.exists, mas por segurança
        print(f"ERRO (Exceção FileNotFoundError): Arquivo '{file_path}' não encontrado.")
        return None
    except Exception as e:
        # Captura outros erros possíveis (formato inválido, etc.)
        print(f"ERRO ao carregar ou processar textura '{file_path}': {str(e)}")
        return None

# Função que desenha um cubo com textura E NORMAIS
def draw_textured_cube():
    glBegin(GL_QUADS)

    # FACE TRASEIRA (Normal: 0, 0, -1)
    glNormal3f(0.0, 0.0, -1.0) # <<< NORMAL ADICIONADA
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[0])
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[1])
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[2])
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[3])

    # FACE FRONTAL (Normal: 0, 0, 1)
    glNormal3f(0.0, 0.0, 1.0) # <<< NORMAL ADICIONADA
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[4])
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[5])
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[6])
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[7])

    # FACE INFERIOR (Normal: 0, -1, 0)
    glNormal3f(0.0, -1.0, 0.0) # <<< NORMAL ADICIONADA
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[0])
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[1])
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[5])
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[4])

    # FACE SUPERIOR (Normal: 0, 1, 0)
    glNormal3f(0.0, 1.0, 0.0) # <<< NORMAL ADICIONADA
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[3])
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[2])
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[6])
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[7])

    # FACE DIREITA (Normal: 1, 0, 0)
    glNormal3f(1.0, 0.0, 0.0) # <<< NORMAL ADICIONADA
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[1])
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[2])
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[6])
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[5])

    # FACE ESQUERDA (Normal: -1, 0, 0)
    glNormal3f(-1.0, 0.0, 0.0) # <<< NORMAL ADICIONADA
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[0])
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[3])
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[7])
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[4])

    glEnd()

# Função para desenhar um plano (chão ou parede) com normais
def draw_plane(width=4.0, height=4.0, tex_repeat_s=2.0, tex_repeat_t=2.0): # Ajustei tamanho e repetição padrão
    half_w = width / 2.0
    half_h = height / 2.0
    glBegin(GL_QUADS)
    # Normal para cima (adequada para o chão)
    glNormal3f(0.0, 1.0, 0.0) # <<< NORMAL ADICIONADA
    glTexCoord2f(0, 0); glVertex3f(-half_w, 0, half_h)
    glTexCoord2f(tex_repeat_s, 0); glVertex3f(half_w, 0, half_h)
    glTexCoord2f(tex_repeat_s, tex_repeat_t); glVertex3f(half_w, 0, -half_h)
    glTexCoord2f(0, tex_repeat_t); glVertex3f(-half_w, 0, -half_h)
    glEnd()

# Vértices do cubo
cube_vertices = [
    (-1, -1, -1),  # 0
    ( 1, -1, -1),  # 1
    ( 1,  1, -1),  # 2
    (-1,  1, -1),  # 3
    (-1, -1,  1),  # 4
    ( 1, -1,  1),  # 5
    ( 1,  1,  1),  # 6
    (-1,  1,  1)   # 7
]

# Função de inicialização do OpenGL
def init_opengl(display):
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.1, 0.2, 0.5, 1.0))
    light_position = (5.0, 5.0, -5.0, 1.0) # Mudei Z da luz para frente da câmera
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.7, 1.0, 0.7, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))

    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    glMaterialf(GL_FRONT, GL_SHININESS, 50.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

# Função principal
def main():
    print("Iniciando Pygame...")
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Cena 3D - Aula 11 Corrigido")

    print("Inicializando OpenGL...")
    init_opengl(display)

    print("Carregando texturas...")
    texture_metal = load_texture("metal.jpg")
    texture_wood = load_texture("wood.jpg")
    texture_grass = load_texture("grass.jpg")
    texture_brick = load_texture("brick.jpg")

    # ----- VERIFICAÇÃO CRÍTICA -----
    # Checa se alguma textura falhou ao carregar (retornou None)
    textures_loaded = {
        "metal.jpg": texture_metal,
        "wood.jpg": texture_wood,
        "grass.jpg": texture_grass,
        "brick.jpg": texture_brick
    }
    failed_textures = [name for name, tex_id in textures_loaded.items() if tex_id is None]

    if failed_textures:
        print("\n-----------------------------------------------------")
        print("ERRO CRÍTICO: As seguintes texturas não puderam ser carregadas:")
        for name in failed_textures:
            print(f"- {name}")
        print("Verifique se os arquivos existem na mesma pasta do script,")
        print("se os nomes estão corretos e se não estão corrompidos.")
        print("Encerrando aplicação.")
        print("-----------------------------------------------------")
        pygame.quit()
        return # Sai da função main e termina o programa
    # ----- FIM DA VERIFICAÇÃO -----

    print("\nTodas as texturas carregadas com sucesso. Iniciando loop principal...")
    clock = pygame.time.Clock()
    global camera_x, camera_y, camera_z, rot_x, rot_y

    while True:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("Aplicação encerrada.")
                return

        keys = pygame.key.get_pressed()
        move_speed = 0.1
        rot_speed = 1

        if keys[K_w]: camera_z += move_speed
        if keys[K_s]: camera_z -= move_speed
        if keys[K_a]: camera_x += move_speed
        if keys[K_d]: camera_x -= move_speed
        if keys[K_UP]: camera_y -= move_speed # Movimento vertical
        if keys[K_DOWN]: camera_y += move_speed # Movimento vertical
        if keys[K_q]: rot_y -= rot_speed
        if keys[K_e]: rot_y += rot_speed
        if keys[K_r]: rot_x -= rot_speed
        if keys[K_f]: rot_x += rot_speed

        # Limpeza
        glClearColor(0.1, 0.1, 0.2, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Câmera
        glLoadIdentity()
        # Ajuste no gluLookAt para usar camera_y corretamente
        gluLookAt(camera_x, camera_y, camera_z,
                  camera_x, camera_y, camera_z + 1, # Ponto para onde olha
                  0, 1, 0) # Vetor UP

        glRotatef(rot_x, 1, 0, 0)
        glRotatef(rot_y, 0, 1, 0)

        # --- Desenho da Cena ---

        # Chão
        glPushMatrix()
        glTranslatef(0, -2, 0)
        glBindTexture(GL_TEXTURE_2D, texture_grass) # <--- Agora seguro, pois texture_grass não será None
        draw_plane(width=10.0, height=10.0, tex_repeat_s=5.0, tex_repeat_t=5.0)
        glPopMatrix()

        # Parede (desenhada manualmente com normal correta)
        glPushMatrix() # Isola transformações da parede
        wall_size = 5.0
        wall_y_base = -2.0 # Base da parede no nível do chão
        wall_height = 4.0
        wall_z = 5.0 # Posição Z da parede
        glTranslatef(0, wall_y_base + wall_height/2 , wall_z) # Move para o centro da parede
        glScalef(wall_size*2, wall_height, 1.0) # Escala para dar tamanho

        glBindTexture(GL_TEXTURE_2D, texture_brick)
        glBegin(GL_QUADS)
        glNormal3f(0.0, 0.0, -1.0) # Normal apontando para a câmera
        # Vértices relativos ao centro (após translate/scale) - tamanho 1x1
        s_repeat = 5.0 # Repetição da textura
        t_repeat = 2.0
        glTexCoord2f(0, 0); glVertex3f(-0.5, -0.5, 0)
        glTexCoord2f(s_repeat, 0); glVertex3f( 0.5, -0.5, 0)
        glTexCoord2f(s_repeat, t_repeat); glVertex3f( 0.5,  0.5, 0)
        glTexCoord2f(0, t_repeat); glVertex3f(-0.5,  0.5, 0)
        glEnd()
        glPopMatrix() # Restaura matriz


        # Totem de cubos
        totem_x = -3.0
        # Cubo inferior (Metal)
        glPushMatrix()
        glTranslatef(totem_x, -1.0, 0)
        glBindTexture(GL_TEXTURE_2D, texture_metal)
        draw_textured_cube()
        glPopMatrix()

        # Cubo médio (Madeira)
        glPushMatrix()
        glTranslatef(totem_x, 1.0, 0)
        glBindTexture(GL_TEXTURE_2D, texture_wood)
        draw_textured_cube()
        glPopMatrix()

        # Cubo superior (Metal)
        glPushMatrix()
        glTranslatef(totem_x, 3.0, 0)
        glBindTexture(GL_TEXTURE_2D, texture_metal)
        draw_textured_cube()
        glPopMatrix()

        # Cubo decorativo central (Madeira)
        glPushMatrix()
        glTranslatef(3.0, -1.0, 0) # No chão
        glBindTexture(GL_TEXTURE_2D, texture_wood)
        draw_textured_cube()
        glPopMatrix()


        pygame.display.flip()

# Ponto de entrada
if __name__ == "__main__":
    print(f"Executando script Python em: {os.getcwd()}")
    print(f"Localização do script: {os.path.dirname(os.path.abspath(__file__))}")
    main()