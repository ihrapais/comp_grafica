import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Constantes para teclas
KEY_UP = K_w
KEY_DOWN = K_s
KEY_LEFT = K_a
KEY_RIGHT = K_d
KEY_ROT_X_POS = K_q
KEY_ROT_X_NEG = K_e
KEY_ROT_Y_POS = K_r
KEY_ROT_Y_NEG = K_f
KEY_ZOOM_IN = K_z
KEY_ZOOM_OUT = K_x
KEY_MENU = K_m  # Tecla para voltar ao menu
KEY_EXIT = K_ESCAPE  # Tecla para sair

# Controles individuais (opção 6)
KEY_CUBE_UP = K_i
KEY_CUBE_DOWN = K_k
KEY_CUBE_LEFT = K_j
KEY_CUBE_RIGHT = K_l
KEY_TRI_UP = K_g
KEY_TRI_DOWN = K_b
KEY_TRI_LEFT = K_v
KEY_TRI_RIGHT = K_n
KEY_PYR_UP = K_UP
KEY_PYR_DOWN = K_DOWN
KEY_PYR_LEFT = K_LEFT
KEY_PYR_RIGHT = K_RIGHT

# Variáveis globais
camera_z = -5.0
camera_rot_x = 0.0
camera_rot_y = 0.0

# Dicionário para posições e rotações dos objetos
objects = {
    'cube': {'pos': [0.0, 0.0, 0.0], 'rot': [0.0, 0.0, 0.0]},
    'triangle': {'pos': [0.0, 0.0, 0.0], 'rot': [0.0, 0.0, 0.0]},
    'pyramid': {'pos': [0.0, 0.0, 0.0], 'rot': [0.0, 0.0, 0.0]}
}

# Velocidades para animação (opção 7)
velocities = {
    'cube': {'pos': [0.02, 0.01, 0.0], 'rot': [1.0, 0.5, 0.0]},
    'triangle': {'pos': [-0.01, 0.02, 0.0], 'rot': [0.5, 1.0, 0.0]},
    'pyramid': {'pos': [0.01, -0.02, 0.0], 'rot': [0.0, 0.5, 1.0]}
}

LIMITS = {'min': -3.0, 'max': 3.0}

# Inicialização do OpenGL
def init_opengl():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Fundo preto
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 640 / 480, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

# Renderização do cubo
def render_cube():
    glPushMatrix()
    glTranslatef(*objects['cube']['pos'])
    glRotatef(objects['cube']['rot'][0], 1, 0, 0)
    glRotatef(objects['cube']['rot'][1], 0, 1, 0)
    glBegin(GL_QUADS)
    glColor3f(1, 0, 0)  # Vermelho
    glVertex3f(1, 1, 1); glVertex3f(-1, 1, 1); glVertex3f(-1, -1, 1); glVertex3f(1, -1, 1)  # Frontal
    glVertex3f(1, 1, -1); glVertex3f(-1, 1, -1); glVertex3f(-1, -1, -1); glVertex3f(1, -1, -1)  # Traseira
    glVertex3f(1, 1, 1); glVertex3f(-1, 1, 1); glVertex3f(-1, 1, -1); glVertex3f(1, 1, -1)  # Superior
    glVertex3f(1, -1, 1); glVertex3f(-1, -1, 1); glVertex3f(-1, -1, -1); glVertex3f(1, -1, -1)  # Inferior
    glVertex3f(-1, 1, 1); glVertex3f(-1, 1, -1); glVertex3f(-1, -1, -1); glVertex3f(-1, -1, 1)  # Esquerda
    glVertex3f(1, 1, 1); glVertex3f(1, 1, -1); glVertex3f(1, -1, -1); glVertex3f(1, -1, 1)  # Direita
    glEnd()
    glPopMatrix()

# Renderização do triângulo
def render_triangle():
    glPushMatrix()
    glTranslatef(*objects['triangle']['pos'])
    glRotatef(objects['triangle']['rot'][0], 1, 0, 0)
    glRotatef(objects['triangle']['rot'][1], 0, 1, 0)
    glBegin(GL_TRIANGLES)
    glColor3f(0, 1, 0)  # Verde
    glVertex3f(0, 1, 0); glVertex3f(-1, -1, 0); glVertex3f(1, -1, 0)
    glEnd()
    glPopMatrix()

# Renderização da pirâmide
def render_pyramid():
    glPushMatrix()
    glTranslatef(*objects['pyramid']['pos'])
    glRotatef(objects['pyramid']['rot'][0], 1, 0, 0)
    glRotatef(objects['pyramid']['rot'][1], 0, 1, 0)
    glBegin(GL_TRIANGLES)
    glColor3f(0, 0, 1)  # Azul
    glVertex3f(0, 1, 0); glVertex3f(-1, -1, 1); glVertex3f(1, -1, 1)  # Frontal
    glVertex3f(0, 1, 0); glVertex3f(-1, -1, -1); glVertex3f(1, -1, -1)  # Traseira
    glVertex3f(0, 1, 0); glVertex3f(-1, -1, -1); glVertex3f(-1, -1, 1)  # Esquerda
    glVertex3f(0, 1, 0); glVertex3f(1, -1, -1); glVertex3f(1, -1, 1)  # Direita
    glEnd()
    glBegin(GL_QUADS)
    glVertex3f(-1, -1, -1); glVertex3f(-1, -1, 1); glVertex3f(1, -1, 1); glVertex3f(1, -1, -1)  # Base
    glEnd()
    glPopMatrix()

# Atualização da animação (opção 7)
def update_animation():
    for obj in objects:
        for i in range(3):
            objects[obj]['pos'][i] += velocities[obj]['pos'][i]
            if objects[obj]['pos'][i] > LIMITS['max'] or objects[obj]['pos'][i] < LIMITS['min']:
                velocities[obj]['pos'][i] = -velocities[obj]['pos'][i]
        for i in range(3):
            objects[obj]['rot'][i] += velocities[obj]['rot'][i]

# Resetar posições
def reset_objects():
    global camera_z, camera_rot_x, camera_rot_y
    objects['cube']['pos'] = [0.0, 0.0, 0.0]
    objects['cube']['rot'] = [0.0, 0.0, 0.0]
    objects['triangle']['pos'] = [0.0, 0.0, 0.0]
    objects['triangle']['rot'] = [0.0, 0.0, 0.0]
    objects['pyramid']['pos'] = [0.0, 0.0, 0.0]
    objects['pyramid']['rot'] = [0.0, 0.0, 0.0]
    camera_z = -5.0
    camera_rot_x = 0.0
    camera_rot_y = 0.0

# Exibir menu no terminal
def show_menu():
    print("== MENU DE FORMAS ==")
    print("1 - Cubo")
    print("2 - Triângulo")
    print("3 - Cubo + Triângulo")
    print("4 - Pirâmide")
    print("5 - Cubo + Triângulo + Pirâmide")
    print("6 - Controle individual")
    print("7 - Animação automática")
    print("0 - Sair")
    return int(input("Escolha uma opção: "))

# Função principal
def main():
    global camera_z, camera_rot_x, camera_rot_y
    pygame.init()
    pygame.display.set_mode((640, 480), DOUBLEBUF | OPENGL)
    init_opengl()

    running = True
    option = show_menu()

    while running and option != 0:
        reset_objects()
        if option in [3, 5, 6, 7]:
            objects['cube']['pos'] = [-2.0, 0.0, 0.0]
            objects['triangle']['pos'] = [0.0, 0.0, 0.0]
            objects['pyramid']['pos'] = [2.0, 0.0, 0.0]

        option_running = True
        while option_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    option_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == KEY_MENU:
                        option_running = False
                    elif event.key == KEY_EXIT:
                        running = False
                        option_running = False

            keys = pygame.key.get_pressed()

            # Controles globais
            if keys[KEY_ZOOM_IN]: camera_z += 0.1
            if keys[KEY_ZOOM_OUT]: camera_z -= 0.1
            if keys[KEY_ROT_X_POS]: camera_rot_x += 1
            if keys[KEY_ROT_X_NEG]: camera_rot_x -= 1
            if keys[KEY_ROT_Y_POS]: camera_rot_y += 1
            if keys[KEY_ROT_Y_NEG]: camera_rot_y -= 1

            # Controles por opção
            if option in [1, 2, 3, 4, 5]:
                if keys[KEY_UP]:
                    for obj in objects: objects[obj]['pos'][1] += 0.1
                if keys[KEY_DOWN]:
                    for obj in objects: objects[obj]['pos'][1] -= 0.1
                if keys[KEY_LEFT]:
                    for obj in objects: objects[obj]['pos'][0] -= 0.1
                if keys[KEY_RIGHT]:
                    for obj in objects: objects[obj]['pos'][0] += 0.1
                if keys[KEY_ROT_X_POS]:
                    for obj in objects: objects[obj]['rot'][0] += 1
                if keys[KEY_ROT_X_NEG]:
                    for obj in objects: objects[obj]['rot'][0] -= 1
                if keys[KEY_ROT_Y_POS]:
                    for obj in objects: objects[obj]['rot'][1] += 1
                if keys[KEY_ROT_Y_NEG]:
                    for obj in objects: objects[obj]['rot'][1] -= 1
            elif option == 6:
                if keys[KEY_CUBE_UP]: objects['cube']['pos'][1] += 0.1
                if keys[KEY_CUBE_DOWN]: objects['cube']['pos'][1] -= 0.1
                if keys[KEY_CUBE_LEFT]: objects['cube']['pos'][0] -= 0.1
                if keys[KEY_CUBE_RIGHT]: objects['cube']['pos'][0] += 0.1
                if keys[KEY_TRI_UP]: objects['triangle']['pos'][1] += 0.1
                if keys[KEY_TRI_DOWN]: objects['triangle']['pos'][1] -= 0.1
                if keys[KEY_TRI_LEFT]: objects['triangle']['pos'][0] -= 0.1
                if keys[KEY_TRI_RIGHT]: objects['triangle']['pos'][0] += 0.1
                if keys[KEY_PYR_UP]: objects['pyramid']['pos'][1] += 0.1
                if keys[KEY_PYR_DOWN]: objects['pyramid']['pos'][1] -= 0.1
                if keys[KEY_PYR_LEFT]: objects['pyramid']['pos'][0] -= 0.1
                if keys[KEY_PYR_RIGHT]: objects['pyramid']['pos'][0] += 0.1
            elif option == 7:
                update_animation()

            # Renderização
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            glTranslatef(0, 0, camera_z)
            glRotatef(camera_rot_x, 1, 0, 0)
            glRotatef(camera_rot_y, 0, 1, 0)

            if option == 1: render_cube()
            elif option == 2: render_triangle()
            elif option == 3: render_cube(); render_triangle()
            elif option == 4: render_pyramid()
            elif option == 5 or option == 6: render_cube(); render_triangle(); render_pyramid()
            elif option == 7: render_cube(); render_triangle(); render_pyramid()

            pygame.display.flip()
            pygame.time.wait(10)

        if running:
            option = show_menu()

    pygame.quit()

if __name__ == "__main__":
    main()