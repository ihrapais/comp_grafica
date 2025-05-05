# 🎮 Cena 3D em OpenGL com Texturas e Iluminação

## 🛠️ Requisitos

Para executar este projeto, você precisará das seguintes texturas (você pode criar ou baixar imagens correspondentes):

- `metal.jpg` — textura metálica
- `wood.jpg` — textura de madeira
- `grass.jpg` — textura de grama
- `brick.jpg` — textura de tijolo
- `light_bulb.png` — textura para a lâmpada (opcional)

**Importante:**  
Salve todas as texturas no mesmo diretório do script Python.

---

## ✨ Modificações principais no código original

- Adição da função `draw_textured_plane()` para criar o chão, paredes e teto
- Carregamento de múltiplas texturas no início do programa
- Implementação de um totem de três cubos empilhados, cada um com uma textura diferente
- Criação de uma mesa decorativa com base e perna
- Alteração da luz ambiente para um tom azulado para criar atmosfera
- Aprimoramento do sistema de iluminação com maior intensidade e atenuação realista
- Adição de suporte visual para a lâmpada ligando do teto até o ponto de luz
- Organização da cena utilizando `glPushMatrix()` e `glPopMatrix()` para manipulação hierárquica dos objetos

---

## 🚀 Como executar

1. Certifique-se de que as texturas estão no mesmo diretório do script.
2. Execute o script Python.
3. Navegue pela cena utilizando os seguintes controles:

| Tecla | Ação                               |
|------|------------------------------------|
| W/S  | Mover para frente/trás             |
| A/D  | Mover para esquerda/direita        |
| Q/E  | Rotacionar a câmera horizontalmente |
| R/F  | Rotacionar a câmera verticalmente   |
| ESPAÇO | Subir                            |
| SHIFT | Descer                            |
| ESC  | Sair do programa                   |

---

## 🎯 Resultado esperado

Ao executar o projeto, a cena 3D incluirá:

- Um quarto completo com paredes texturizadas de tijolo, chão de grama e teto de madeira
- Um totem de três cubos empilhados, cada um com uma textura diferente (tijolo, metal e madeira)
- Um cubo principal central com textura metálica
- Um cubo secundário com textura de madeira
- Uma mesa decorativa na lateral do quarto
- Uma lâmpada suspensa no teto com suporte visual
- Iluminação ambiente azulada e uma luz pontual branca mais intensa

---

## 📝 Notas técnicas

- O sistema de iluminação implementa o modelo de Phong com componentes ambiente, difusa e especular
- A atenuação da luz foi configurada para simular uma diminuição realista da intensidade com a distância
- A câmera começa posicionada de modo a visualizar o centro da sala, não voltada para a parede
- A lâmpada foi posicionada mais alto (Y=8.0) para melhor distribuição da luz
- A intensidade da iluminação foi aumentada para melhor visualização dos efeitos de reflexão

  ---

---
