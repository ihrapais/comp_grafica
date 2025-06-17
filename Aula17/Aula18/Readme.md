# 🎨 Shaders em GLSL — Aula 18

Este repositório contém cinco exemplos de shaders desenvolvidos na disciplina de Computação Gráfica — Jogos Digitais, utilizando GLSL. Cada shader demonstra um efeito visual diferente, utilizando funções matemáticas e operacionais para manipulação gráfica de pixels.

---

## 🚀 Exemplos de Shaders

### 🟦 Shader-1_Onda-Seno.glsl
- Cria uma onda senoidal animada que se move na horizontal.
- O efeito é gerado através da função seno, criando uma linha branca oscilante no eixo X.
- 🔧 Funções usadas: `sin()`, `smoothstep()`, `u_time`

### 🟩 Shader-2_TVantiga.glsl
- Simula o efeito de uma TV antiga (CRT) com linhas horizontais (scanlines).
- As linhas escuras alternadas geram o efeito visual clássico de telas analógicas.
- 🔧 Funções usadas: `fract()`, `step()`

### 🔲 Shader-3_Noise.glsl
- Gera um padrão de ruído estático pseudoaleatório, similar a uma TV fora do ar.
- Cada pixel recebe um valor aleatório, produzindo um efeito de "chuvisco".
- 🔧 Função personalizada `random()` baseada em `sin()` e `dot()`

### ♟️ Shader-4_Xadrez-Cores.glsl
- Cria um padrão de tabuleiro de xadrez colorido, alternando entre azul e amarelo.
- O padrão pode ser ajustado em tamanho modificando os parâmetros.
- 🔧 Funções usadas: `mod()`, `floor()`, `step()`

### 🔘 Shader-5_Vinheta.glsl
- Adiciona uma vinheta, escurecendo suavemente as bordas da tela para destacar o centro.
- Efeito muito utilizado em jogos, fotos e interfaces.
- 🔧 Funções usadas: `distance()`, `smoothstep()`

---

## 📂 Organização dos Arquivos

