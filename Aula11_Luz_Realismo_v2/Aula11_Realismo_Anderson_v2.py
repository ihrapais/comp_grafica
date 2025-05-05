# Importação das bibliotecas necessárias
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import os
import math

# Variáveis globais para posição e rotação da câmera
camera_x, camera_y, camera_z = 0, 1, 5  # Posição inicial DENTRO da sala
rot_x, rot_y = 0, 0                  # Rotação inicial olhando para o centro

# Posição da fonte de luz - Fixa no mundo
# AJUSTADO: Posição Y da luz ligeiramente abaixo do teto
light_pos = [2.0, 7.7, 2.0, 1.0]

# Função para carregar uma textura
# AJUSTADO: Adicionado parâmetro flip=True
def load_texture(filename, flip=True):
    """
    Carrega uma imagem e a transforma em textura OpenGL.
    Parâmetro:
        filename: Nome do arquivo da imagem.
        flip: Se True (padrão), inverte a imagem verticalmente.
    Retorna:
        ID da textura ou None em caso de erro.
    """
    try:
        filepath = os.path.join(os.getcwd(), filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Arquivo '{filename}' não encontrado em: {filepath}")
        img = Image.open(filepath)
        # Inverte condicionalmente
        if flip:
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = img.convert("RGBA").tobytes()
        width, height = img.size
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        print(f"Textura '{filename}' carregada com sucesso (flip={flip}).")
        return tex_id
    except FileNotFoundError as e:
        print(f"Erro: {e}")
        print("Verifique se o arquivo está na mesma pasta do script.")
        print("Arquivos na pasta atual:")
        try:
            for file in os.listdir(os.getcwd()):
                 if file.lower().endswith(('.jpg', '.png')):
                     print(f" - {file}")
        except Exception as list_e:
             print(f"  (Não foi possível listar arquivos: {list_e})")
        return None
    except Exception as e:
        print(f"Erro inesperado ao carregar textura '{filename}': {e}")
        return None

# Vértices do cubo
cube_vertices = [
    (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
    (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)
]

# Função para desenhar um cubo com textura
def draw_textured_cube():
    # (Código da função draw_textured_cube sem alterações)
    glBegin(GL_QUADS)
    # Face Traseira (Z = -1)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[0])
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[1])
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[2])
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[3])
    # Face Frontal (Z = 1)
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[4])
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[5])
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[6])
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[7])
    # Face Inferior (Y = -1)
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[0])
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[1])
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[5])
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[4])
    # Face Superior (Y = 1)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[3])
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[2])
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[6])
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[7])
    # Face Esquerda (X = -1)
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[0])
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[3])
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[7])
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[4])
    # Face Direita (X = 1)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[1])
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[2])
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[6])
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[5])
    glEnd()

# Função para desenhar um plano
def draw_textured_plane(width=10.0, height=10.0, tex_repeat_s=1.0, tex_repeat_t=1.0):
    # (Código da função draw_textured_plane sem alterações)
    half_width = width / 2.0
    half_height = height / 2.0
    glBegin(GL_QUADS)
    glTexCoord2f(0, tex_repeat_t); glVertex3f(-half_width, 0, -half_height)
    glTexCoord2f(tex_repeat_s, tex_repeat_t); glVertex3f(half_width, 0, -half_height)
    glTexCoord2f(tex_repeat_s, 0); glVertex3f(half_width, 0, half_height)
    glTexCoord2f(0, 0); glVertex3f(-half_width, 0, half_height)
    glEnd()

# Configuração inicial do ambiente OpenGL
def init_opengl(display_width, display_height):
    # (Código da função init_opengl sem alterações significativas)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Luz ambiente mais azulada e mais forte
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.3, 0.3, 0.6, 1.0))

    # Propriedades de cor e atenuação da luz pontual (posição é definida no loop)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.2, 1.2, 1.2, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.5, 1.5, 1.5, 1.0])
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.5)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.01)

    # Material padrão
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 80.0)

    glClearColor(0.1, 0.1, 0.1, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, display_width / display_height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

# Função principal
def main():
    pygame.init()
    display = (800, 600)
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Atividade OpenGL - Quarto Fechado Final v2")
    init_opengl(display[0], display[1])

    # Carrega texturas
    tex_metal = load_texture("metal.jpg")
    tex_wood = load_texture("wood.jpg")
    tex_ground = load_texture("grass.jpg")
    tex_brick = load_texture("brick.jpg")
    # AJUSTADO: Carrega textura da lâmpada sem inverter
    tex_light_bulb = load_texture("light_bulb.png", flip=False)

    # Verifica texturas essenciais
    if None in [tex_metal, tex_wood, tex_ground, tex_brick]:
         print("Erro: Falha ao carregar uma ou mais texturas essenciais. Saindo.")
         pygame.quit()
         return

    # Cria quadric para esfera (se textura carregou)
    quadric = None
    if tex_light_bulb is not None:
        quadric = gluNewQuadric()
        gluQuadricTexture(quadric, GL_TRUE) # Habilita textura no quadric

    clock = pygame.time.Clock()
    global camera_x, camera_y, camera_z, rot_x, rot_y

    # Dimensões da sala
    room_width = 20.0
    room_depth = 20.0
    room_height = 10.0
    floor_y = -2.0
    wall_center_y = floor_y + room_height / 2.0
    ceiling_y = floor_y + room_height # Calcula a posição Y do teto

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        move_speed = 7.0 * dt
        rot_speed = 80.0 * dt

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        # Controles
        keys = pygame.key.get_pressed()
        # (Código dos controles WASD QERF sem alterações)
        if keys[K_q]: rot_y -= rot_speed
        if keys[K_e]: rot_y += rot_speed
        if keys[K_r]: rot_x -= rot_speed
        if keys[K_f]: rot_x += rot_speed
        rot_x = max(-89.0, min(89.0, rot_x))

        rad_y = math.radians(rot_y)
        forward_dx = math.sin(rad_y)
        forward_dz = -math.cos(rad_y)
        right_dx = -forward_dz
        right_dz = forward_dx

        if keys[K_w]: camera_x += forward_dx * move_speed; camera_z += forward_dz * move_speed
        if keys[K_s]: camera_x -= forward_dx * move_speed; camera_z -= forward_dz * move_speed
        if keys[K_a]: camera_x -= right_dx * move_speed; camera_z -= right_dz * move_speed
        if keys[K_d]: camera_x += right_dx * move_speed; camera_z += right_dz * move_speed
        if keys[K_SPACE]: camera_y += move_speed
        if keys[K_LSHIFT] or keys[K_RSHIFT]: camera_y -= move_speed

        # --- Renderização ---
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Define posição da LUZ 0 no MUNDO (antes da câmera)
        glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

        # Aplica transformações da Câmera
        glRotatef(rot_x, 1, 0, 0)
        glRotatef(rot_y, 0, 1, 0)
        glTranslatef(-camera_x, -camera_y, -camera_z)

        # Desenha a Cena
        glEnable(GL_LIGHTING)

        # Chão
        glPushMatrix(); glTranslatef(0, floor_y, 0); glBindTexture(GL_TEXTURE_2D, tex_ground); draw_textured_plane(width=room_width, height=room_depth, tex_repeat_s=4.0, tex_repeat_t=4.0); glPopMatrix()

        # Paredes
        glBindTexture(GL_TEXTURE_2D, tex_brick)
        wall_tex_repeat_s = room_width / 5.0
        wall_tex_repeat_t = room_height / 5.0
        glPushMatrix(); glTranslatef(0, wall_center_y, -room_depth / 2.0); glRotatef(-90, 1, 0, 0); draw_textured_plane(width=room_width, height=room_height, tex_repeat_s=wall_tex_repeat_s, tex_repeat_t=wall_tex_repeat_t); glPopMatrix() # Fundo
        glPushMatrix(); glTranslatef(0, wall_center_y, room_depth / 2.0); glRotatef(-90, 1, 0, 0); draw_textured_plane(width=room_width, height=room_height, tex_repeat_s=wall_tex_repeat_s, tex_repeat_t=wall_tex_repeat_t); glPopMatrix() # Frente
        glPushMatrix(); glTranslatef(-room_width / 2.0, wall_center_y, 0); glRotatef(90, 0, 1, 0); glRotatef(-90, 1, 0, 0); draw_textured_plane(width=room_depth, height=room_height, tex_repeat_s=wall_tex_repeat_s, tex_repeat_t=wall_tex_repeat_t); glPopMatrix() # Esquerda
        glPushMatrix(); glTranslatef(room_width / 2.0, wall_center_y, 0); glRotatef(-90, 0, 1, 0); glRotatef(-90, 1, 0, 0); draw_textured_plane(width=room_depth, height=room_height, tex_repeat_s=wall_tex_repeat_s, tex_repeat_t=wall_tex_repeat_t); glPopMatrix() # Direita

        # Teto
        glPushMatrix(); glTranslatef(0, ceiling_y, 0); glRotatef(180, 0, 0, 1); glBindTexture(GL_TEXTURE_2D, tex_wood); draw_textured_plane(width=room_width, height=room_depth, tex_repeat_s=3.0, tex_repeat_t=3.0); glPopMatrix()

        # Objetos (Cubos, Totem, Mesa)
        glPushMatrix(); glTranslatef(0, floor_y + 1, 0); glBindTexture(GL_TEXTURE_2D, tex_metal); draw_textured_cube(); glPopMatrix() # Cubo Principal
        glPushMatrix(); glTranslatef(3, floor_y + 1, 0); glBindTexture(GL_TEXTURE_2D, tex_wood); draw_textured_cube(); glPopMatrix() # Segundo Cubo
        totem_x, totem_z = -5, -3
        glPushMatrix(); glTranslatef(totem_x, floor_y + 1, totem_z); glBindTexture(GL_TEXTURE_2D, tex_brick); draw_textured_cube(); glPopMatrix() # Totem Base
        glPushMatrix(); glTranslatef(totem_x, floor_y + 3, totem_z); glBindTexture(GL_TEXTURE_2D, tex_metal); draw_textured_cube(); glPopMatrix() # Totem Meio
        glPushMatrix(); glTranslatef(totem_x, floor_y + 5, totem_z); glBindTexture(GL_TEXTURE_2D, tex_wood); draw_textured_cube(); glPopMatrix() # Totem Topo
        table_x, table_z = 5, -5
        glPushMatrix(); glTranslatef(table_x, floor_y + 1.5, table_z); glScalef(1.5, 0.1, 1.5); glBindTexture(GL_TEXTURE_2D, tex_wood); draw_textured_cube(); glPopMatrix() # Mesa Base
        glPushMatrix(); glTranslatef(table_x, floor_y + 0.75, table_z); glScalef(0.2, 1.5, 0.2); glBindTexture(GL_TEXTURE_2D, tex_wood); draw_textured_cube(); glPopMatrix()# Mesa Perna

        # Lâmpada (Esfera Visual)
        if tex_light_bulb is not None and quadric is not None:
            glPushMatrix()
            glDisable(GL_LIGHTING) # Sem iluminação da cena na própria lâmpada
            glColor3f(1.0, 1.0, 0.8) # Cor emissiva clara
            glTranslatef(light_pos[0], light_pos[1], light_pos[2]) # Posição Y ajustada para 7.5
            glBindTexture(GL_TEXTURE_2D, tex_light_bulb) # Textura carregada com flip=False
            # Tenta rotacionar a esfera 180 graus APÓS transladar para corrigir orientação da textura
            # glRotatef(180, 1, 0, 0) # Rotação em X pode corrigir (teste se necessário)
            gluSphere(quadric, 0.3, 16, 16)
            glEnable(GL_LIGHTING) # Reabilita iluminação
            glPopMatrix()

        pygame.display.flip() # Atualiza a tela

    # Limpeza
    if quadric is not None:
        gluDeleteQuadric(quadric)
    pygame.quit()

if __name__ == "__main__":
    main()