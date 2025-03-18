import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Variáveis globais para controle de transformação
translate_x = 0.0
translate_y = 0.0
rotation_angle = 0.0
zoom = -5.0

def init():
    """Configuração inicial do OpenGL."""
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Cor de fundo
    glClearDepth(1.0)  # Profundidade do buffer
    glEnable(GL_DEPTH_TEST)  # Ativa o teste de profundidade
    glDepthFunc(GL_LEQUAL)  # Função de profundidade
    glMatrixMode(GL_PROJECTION)  # Matriz de projeção
    glLoadIdentity()  # Reseta a matriz de projeção
    gluPerspective(45.0, 640.0 / 480.0, 0.1, 100.0)  # Perspectiva 3D
    glMatrixMode(GL_MODELVIEW)  # Retorna à matriz de modelo/visualização

def draw_circle(radius, num_segments=100):
    """Desenha um círculo usando OpenGL."""
    glLineWidth(3)  # Define a espessura da linha para 3
    glBegin(GL_LINE_LOOP)  # Inicia o desenho de uma linha fechada (círculo)
    for i in range(num_segments):
        angle = 2.0 * math.pi * i / num_segments  # Calcula o ângulo do ponto atual
        x = radius * math.cos(angle)  # Coordenada X
        y = radius * math.sin(angle)  # Coordenada Y
        glVertex2f(x, y)  # Define o ponto no círculo
    glEnd()  # Finaliza o desenho do círculo

def main():
    """Função principal para inicializar o Pygame e renderizar o círculo."""
    global translate_x, translate_y, rotation_angle, zoom
    pygame.init()  # Inicializa o Pygame
    pygame.display.set_mode((640, 480), DOUBLEBUF | OPENGL)  # Cria a janela com suporte a OpenGL
    init()  # Configurações iniciais do OpenGL

    running = True  # Variável de controle do loop principal
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_w:  # Move para cima
                    translate_y += 0.1
                if event.key == K_s:  # Move para baixo
                    translate_y -= 0.1
                if event.key == K_a:  # Move para a esquerda
                    translate_x -= 0.1
                if event.key == K_d:  # Move para a direita
                    translate_x += 0.1
                if event.key == K_f:  # Rotação horário
                    rotation_angle += 5.0
                if event.key == K_r:  # Rotação anti-horário
                    rotation_angle -= 5.0
                if event.key == K_z:  # Zoom out
                    zoom += 0.5
                if event.key == K_x:  # Zoom in
                    zoom -= 0.5

            if event.type == MOUSEBUTTONDOWN:  # Controle de zoom com scroll do mouse
                if event.button == 4:  # Scroll up
                    zoom -= 0.5
                elif event.button == 5:  # Scroll down
                    zoom += 0.5

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpa a tela e o buffer de profundidade
        glLoadIdentity()  # Reseta a matriz de modelagem
        glTranslatef(translate_x, translate_y, zoom)  # Aplica translação e zoom
        glRotatef(rotation_angle, 0, 0, 1)  # Aplica rotação

        glColor3f(0.0, 0.0, 1.0)  # Define a cor do círculo como azul
        draw_circle(1)  # Chama a função para desenhar o círculo
        pygame.display.flip()  # Atualiza a tela
        pygame.time.wait(10)  # Pequeno atraso para controlar a taxa de atualização

    pygame.quit()  # Finaliza o Pygame quando o loop termina

if __name__ == "__main__":
    main()  # Executa a função principal se o script for rodado diretamente