# Importação das bibliotecas necessárias
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import os
import math

# Variáveis globais para posição e rotação da câmera
# AJUSTADO: Câmera começa DENTRO da sala (z=5), virada 180 graus
camera_x, camera_y, camera_z = 0, 1, 5 # Posição inicial DENTRO da sala
rot_x, rot_y = 0, 180                 # Rotação inicial em Y para olhar para -Z

# Posição da fonte de luz
light_pos = [2.0, 5.0, 2.0, 1.0]

# Função para carregar uma textura (sem alterações)
def load_texture(filename):
    try:
        filepath = os.path.join(os.getcwd(), filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Arquivo '{filename}' não encontrado em: {filepath}")
        img = Image.open(filepath)
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
        print(f"Textura '{filename}' carregada com sucesso.")
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

# Vértices do cubo (sem alterações)
cube_vertices = [
    (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
    (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)
]

# Função para desenhar um cubo com textura (sem alterações)
def draw_textured_cube():
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

# Função para desenhar um plano (sem alterações)
def draw_textured_plane(width=10.0, height=10.0, tex_repeat_s=1.0, tex_repeat_t=1.0):
    half_width = width / 2.0
    half_height = height / 2.0
    glBegin(GL_QUADS)
    glTexCoord2f(0, tex_repeat_t); glVertex3f(-half_width, 0, -half_height)
    glTexCoord2f(tex_repeat_s, tex_repeat_t); glVertex3f(half_width, 0, -half_height)
    glTexCoord2f(tex_repeat_s, 0); glVertex3f(half_width, 0, half_height)
    glTexCoord2f(0, 0); glVertex3f(-half_width, 0, half_height)
    glEnd()

# Configuração inicial do ambiente OpenGL (sem alterações)
def init_opengl(display_width, display_height):
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.2, 0.2, 0.5, 1.0))
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
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
    pygame.display.set_caption("Atividade OpenGL - Quarto Fechado v2")
    init_opengl(display[0], display[1])

    tex_metal = load_texture("metal.jpg")
    tex_wood = load_texture("wood.jpg")
    tex_ground = load_texture("grass.jpg")
    tex_brick = load_texture("brick.jpg")
    tex_light_bulb = load_texture("light_bulb.png")

    if None in [tex_metal, tex_wood, tex_ground, tex_brick]:
         print("Erro: Falha ao carregar uma ou mais texturas essenciais. Saindo.")
         pygame.quit()
         return

    quadric = None
    if tex_light_bulb is not None:
        quadric = gluNewQuadric()
        gluQuadricTexture(quadric, GL_TRUE)

    clock = pygame.time.Clock()
    global camera_x, camera_y, camera_z, rot_x, rot_y

    room_width = 20.0
    room_depth = 20.0
    room_height = 10.0
    floor_y = -2.0
    wall_center_y = floor_y + room_height / 2.0

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        move_speed = 7.0 * dt
        rot_speed = 80.0 * dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        keys = pygame.key.get_pressed()
        # --- CONTROLES ---
        # Rotação (Q E R F)
        if keys[K_q]: rot_y -= rot_speed # Gira esquerda (Yaw)
        if keys[K_e]: rot_y += rot_speed # Gira direita (Yaw)
        if keys[K_r]: rot_x -= rot_speed # Inclina cima (Pitch)
        if keys[K_f]: rot_x += rot_speed # Inclina baixo (Pitch)
        # Limita rotação X para evitar gimbal lock ou virar de cabeça para baixo
        rot_x = max(-89.0, min(89.0, rot_x))

        # Movimento (W A S D + Space/Shift)
        # Calcula vetor de direção baseado na rotação Y (ignorando X por simplicidade de movimento no plano)
        rad_y = math.radians(rot_y)
        forward_dx = math.sin(rad_y)
        forward_dz = -math.cos(rad_y) # Negativo porque cosseno dá direção +Z com angulo 0, queremos -Z

        # Calcula vetor lateral (perpendicular ao forward no plano XZ)
        right_dx = -forward_dz
        right_dz = forward_dx

        if keys[K_w]: # Frente
            camera_x += forward_dx * move_speed
            camera_z += forward_dz * move_speed
        if keys[K_s]: # Trás
            camera_x -= forward_dx * move_speed
            camera_z -= forward_dz * move_speed
        if keys[K_a]: # Esquerda (Strafe)
            camera_x -= right_dx * move_speed
            camera_z -= right_dz * move_speed
        if keys[K_d]: # Direita (Strafe)
            camera_x += right_dx * move_speed
            camera_z += right_dz * move_speed
        if keys[K_SPACE]: camera_y += move_speed # Subir
        if keys[K_LSHIFT] or keys[K_RSHIFT]: camera_y -= move_speed # Descer


        # Limpa e prepara matriz
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Aplica transformações da Câmera
        # AJUSTADO: Ordem de rotação Y primeiro, X depois
        glRotatef(rot_y, 0, 1, 0) # Rotação Horizontal (Yaw)
        glRotatef(rot_x, 1, 0, 0) # Rotação Vertical (Pitch)
        glTranslatef(-camera_x, -camera_y, -camera_z) # Translação da câmera

        # --- Desenho da Cena ---
        glEnable(GL_LIGHTING)

        # Chão
        glPushMatrix()
        glTranslatef(0, floor_y, 0)
        glBindTexture(GL_TEXTURE_2D, tex_ground)
        draw_textured_plane(width=room_width, height=room_depth, tex_repeat_s=4.0, tex_repeat_t=4.0)
        glPopMatrix()

        # Paredes - Lógica igual anterior
        glBindTexture(GL_TEXTURE_2D, tex_brick)
        wall_tex_repeat_s = room_width / 5.0
        wall_tex_repeat_t = room_height / 5.0
        # Parede Fundo
        glPushMatrix()
        glTranslatef(0, wall_center_y, -room_depth / 2.0)
        glRotatef(-90, 1, 0, 0)
        draw_textured_plane(width=room_width, height=room_height, tex_repeat_s=wall_tex_repeat_s, tex_repeat_t=wall_tex_repeat_t)
        glPopMatrix()
        # Parede Frontal
        glPushMatrix()
        glTranslatef(0, wall_center_y, room_depth / 2.0)
        glRotatef(-90, 1, 0, 0)
        draw_textured_plane(width=room_width, height=room_height, tex_repeat_s=wall_tex_repeat_s, tex_repeat_t=wall_tex_repeat_t)
        glPopMatrix()
        # Parede Esquerda
        glPushMatrix()
        glTranslatef(-room_width / 2.0, wall_center_y, 0)
        glRotatef(90, 0, 1, 0)
        glRotatef(-90, 1, 0, 0)
        draw_textured_plane(width=room_depth, height=room_height, tex_repeat_s=wall_tex_repeat_s, tex_repeat_t=wall_tex_repeat_t)
        glPopMatrix()
        # Parede Direita
        glPushMatrix()
        glTranslatef(room_width / 2.0, wall_center_y, 0)
        glRotatef(-90, 0, 1, 0)
        glRotatef(-90, 1, 0, 0)
        draw_textured_plane(width=room_depth, height=room_height, tex_repeat_s=wall_tex_repeat_s, tex_repeat_t=wall_tex_repeat_t)
        glPopMatrix()

        # Objetos (Cubos e Totem) - Lógica igual anterior
        # Cubo Principal
        glPushMatrix()
        glTranslatef(0, floor_y + 1, 0)
        glBindTexture(GL_TEXTURE_2D, tex_metal)
        draw_textured_cube()
        glPopMatrix()
        # Segundo Cubo
        glPushMatrix()
        glTranslatef(3, floor_y + 1, 0)
        glBindTexture(GL_TEXTURE_2D, tex_wood)
        draw_textured_cube()
        glPopMatrix()
        # Totem
        totem_x, totem_z = -5, -3
        glPushMatrix(); glTranslatef(totem_x, floor_y + 1, totem_z); glBindTexture(GL_TEXTURE_2D, tex_brick); draw_textured_cube(); glPopMatrix()
        glPushMatrix(); glTranslatef(totem_x, floor_y + 3, totem_z); glBindTexture(GL_TEXTURE_2D, tex_metal); draw_textured_cube(); glPopMatrix()
        glPushMatrix(); glTranslatef(totem_x, floor_y + 5, totem_z); glBindTexture(GL_TEXTURE_2D, tex_wood); draw_textured_cube(); glPopMatrix()


        # Lâmpada - Lógica igual anterior
        if tex_light_bulb is not None and quadric is not None:
            glPushMatrix()
            glDisable(GL_LIGHTING)
            glColor3f(1.0, 1.0, 1.0)
            glTranslatef(light_pos[0], light_pos[1], light_pos[2])
            # Removi a rotação extra da esfera, geralmente não é necessária para gluSphere com textura
            glBindTexture(GL_TEXTURE_2D, tex_light_bulb)
            gluSphere(quadric, 0.3, 32, 32)
            glEnable(GL_LIGHTING)
            glPopMatrix()

        # Atualiza
        pygame.display.flip()

    # Limpeza
    if quadric is not None:
        gluDeleteQuadric(quadric)
    pygame.quit()

if __name__ == "__main__":
    main()