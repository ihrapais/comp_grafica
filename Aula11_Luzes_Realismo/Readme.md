# 🎮 Cena 3D em OpenGL com Texturas e Iluminação

## 🛠️ Requisitos

Para executar este projeto, você precisará das seguintes texturas (você pode criar ou baixar imagens correspondentes):

- `metal.jpg` — textura metálica
- `wood.jpg` — textura de madeira
- `grass.jpg` — textura de grama
- `brick.jpg` — textura de tijolo

**Importante:**  
Salve todas as texturas no mesmo diretório do script Python.

---

## ✨ Modificações principais no código original

- Adição da função `draw_plane()` para criar o chão e as paredes.
- Carregamento de múltiplas texturas no início do programa.
- Implementação de um totem de três cubos empilhados, cada um com uma textura diferente.
- Alteração da luz ambiente para um tom levemente azulado.
- Organização da cena utilizando `glPushMatrix()` e `glPopMatrix()` para manipulação hierárquica dos objetos.

---

## 🚀 Como executar

1. Certifique-se de que as texturas (`metal.jpg`, `wood.jpg`, `grass.jpg`, `brick.jpg`) estão no mesmo diretório do script.
2. Execute o script Python.
3. Navegue pela cena utilizando os seguintes controles:

| Tecla | Ação                               |
|------|------------------------------------|
| W/S  | Mover para frente/trás             |
| A/D  | Mover para esquerda/direita        |
| Q/E  | Rotacionar a câmera horizontalmente |
| R/F  | Rotacionar a câmera verticalmente   |

---

## 🎯 Resultado esperado

Ao executar o projeto, a cena 3D incluirá:

- Um chão texturizado com grama (`grass.jpg`).
- Uma parede de fundo com textura de tijolo (`brick.jpg`).
- Um totem de três cubos empilhados, cada um com uma textura diferente (`metal.jpg`, `wood.jpg`, `brick.jpg`).
- Um cubo decorativo adicional com textura metálica.
- Iluminação ambiente com tonalidade azulada e uma luz direcional branca.

---
