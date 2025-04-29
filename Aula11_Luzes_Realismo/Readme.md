Para executar este código, você precisará das seguintes texturas (você pode criar ou baixar imagens correspondentes):

metal.jpg - uma textura metálica
wood.jpg - uma textura de madeira
grass.jpg - uma textura de grama
brick.jpg - uma textura de tijolo
As principais modificações e adições ao código original são:

Adição da função draw_plane() para criar o chão e as paredes
Carregamento de múltiplas texturas no início do programa
Implementação do totem de cubos com diferentes texturas
Modificação da luz ambiente para ter um tom levemente azulado
Organização da cena com múltiplos objetos usando glPushMatrix() e glPopMatrix()
Para completar a implementação, você precisará:

Criar ou baixar as texturas necessárias (metal.jpg, wood.jpg, grass.jpg, brick.jpg)
Salvar as texturas no mesmo diretório do script Python
Executar o código
O resultado será uma cena 3D com:

Um chão texturizado com grama
Uma parede de fundo com textura de tijolo
Um totem de três cubos com texturas diferentes
Um cubo decorativo adicional
Iluminação ambiente azulada e uma luz direcional branca
Você pode se movimentar na cena usando:

W/S - Mover para frente/trás
A/D - Mover para esquerda/direita
Q/E - Rotacionar a câmera horizontalmente
R/F - Rotacionar a câmera verticalmente
