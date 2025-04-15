TRABALHO 01 - COMPUTACAO GRÁFICA
CURSO DE JOGOS DIGITAIS
UNIVERSIDADE FRANCISCANA – UFN. 2025-01.
PROFESSOR: André F. dos Santos.
Nome do aluno:__________________________________________________.
Data: ___/___/_____. Peso 3,0.
Trabalho 01: Interatividade com Objetos em OpenGL
Objetivo
Implementar, usando PyOpenGL e pygame, um programa com menu de opções no terminal. A cada opção, diferentes objetos devem ser renderizados na tela com controle via teclado. O foco é praticar renderização, movimentação, rotação e interação via teclado.
Instruções Gerais
1- O programa deve exibir um menu no terminal, com pelo menos 7 opções numeradas.
2- Com base na opção escolhida pelo usuário, diferentes objetos devem ser renderizados na janela OpenGL.
3- O usuário deve conseguir movimentar e rotacionar os objetos com as teclas indicadas.
4- Utilize teclas específicas para cada modo de interação.
5- Cada opção deve funcionar de forma independente.
Menu de Opções – O que implementar
Opção 1 – Cubo
•
Renderizar um cubo 3D colorido.
•
Deve permitir movimentação com:
o
W, S → cima / baixo
o
A, D → esquerda / direita
o
Q, E → rotacionar eixo X
o
R, F → rotacionar eixo Y
o
Z, X → zoom in / out
Opção 2 – Triângulo
•
Renderizar um triângulo 2D com cor definida.
•
Deve permitir movimentação com as mesmas teclas da opção 1.
Opção 3 – Cubo + Triângulo
•
Renderizar ambos os objetos lado a lado.
•
Ao movimentar, ambos devem se mover juntos com ‘WASD’, e as mesmas teclas anteriores para rotação ‘QERF’, e zoom ‘ZX’.
Opção 4 – Pirâmide
•
Renderizar uma pirâmide 3D com base quadrada.
•
Movimentação padrão com WASD, QERF, ZX.
Opção 5 – Cubo + Triângulo + Pirâmide
•
Renderizar os três objetos lado a lado.
• Todos devem se mover e rotacionar juntos com:
o
W, S, A, D
o
Q, E, R, F
o
Z, X
Opção 6 – Controle individual
• Renderizar os três objetos, cada um com controle independente.
•
Teclas de movimentação:
o
Cubo: I, K → cima/baixo J, L → esquerda/direita
o
Triângulo: G, B → cima/baixo V, N → esquerda/direita
o
Pirâmide: ↑, ↓ : cima/baixo (direcional do teclado) ←, → : esquerda/direita (direcional do teclado)
o
Zoom e rotação global: Z, X, Q, E, R, F
Opção 7 – Animação automática dos objetos
•
Renderizar os três objetos (Cubo, Triângulo e Pirâmide) e aplicar movimentação e rotação automática contínua.
•
Cada objeto se move em uma direção diferente e com velocidade distinta.
•
O movimento se inverte automaticamente ao atingir certos limites da tela.
•
Aqui os objetos não precisam ser controlados por teclas, eles apenas ficam se movimentando aleatoriamente.
Exemplo do Menu em execução:
Exemplo se opção 6 escolhida (movimentação independente de cada objeto):
- Avaliação do Professor será ao final da aula quando o aluno estiver pronto para apresentar!!
- Logo após submeter o trabalho (link do github ou código) na atividade da aula de hoje.
