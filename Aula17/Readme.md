# 🎨 Aula 17 – Fragment Shaders com GLSL

Este diretório contém os exemplos desenvolvidos durante a **Aula 17 de Computação Gráfica**, com foco na criação e experimentação de **fragment shaders** em **GLSL (OpenGL Shading Language)**.

Foram explorados efeitos visuais utilizando manipulação de cores, funções matemáticas (`step()`, `smoothstep()`, `distance()`, `mix()`), campos de distância, ruído e padrões gerados proceduralmente.

---

## 🧰 Ferramentas Utilizadas

- **Editor de código:** Visual Studio Code  
- **Extensão:** [glsl-canvas](https://marketplace.visualstudio.com/items?itemName=circledev.glsl-canvas)  
- **Execução:** diretamente no VSCode via WebGL (fragment shaders)

---

## 📂 Arquivos do Projeto

| Arquivo                         | Descrição resumida                                      |
|----------------------------------|----------------------------------------------------------|
| Ex1_time_r.glsl                  | Pulso vermelho com base no tempo (`sin(u_time)`)        |
| Ex2.glsl                         | Gradiente RGB baseado em posição XY                     |
| Ex3_Azul.glsl                    | Tela azul sólida                                         |
| Ex4_Normalizacao.glsl           | Cor afetada pela posição do mouse no eixo X             |
| Ex5_Tamanho.glsl                | Faixa preta fina vertical sobre fundo escuro            |
| Ex6_Step.glsl                   | Divisão da tela com `step()`                            |
| Ex7.glsl                         | Base para smoothstep (sem efeito visível direto)        |
| Ex7_Smoothstep.glsl             | Gradiente verde suave com `smoothstep()`                |
| Ex8_Smoothstep.glsl             | Linha diagonal com bordas suaves                        |
| Ex9-1_Shaping.glsl              | Linha reta `y = x` com suavização                       |
| Ex9-2_Shaping.glsl              | Curva `y = sin(10x)`                                     |
| Ex9-3_Shaping.glsl              | Curva `y = sin(5x)` ajustada com zoom                   |
| Ex9_Shaping.glsl                | Base para as shaping functions                         |
| Ex10_Step.glsl                  | Retângulo branco com borda preta usando `step()`        |
| Ex10-b_Step.glsl                | Variação do retângulo com preenchimento alternativo     |
| Ex11_Circulos.glsl              | Círculo branco com `distance()`                         |
| Ex12_Padroes.glsl               | Padrão em grade com `fract()`                           |
| Ex13_Padroes.glsl               | Círculo em cada célula da grade                         |
| Ex14_Padroes.glsl               | Padrão de xadrez rotacionado com `rotate2D()`           |
| Ex15_Ruidos.glsl                | Ruído dinâmico por pixel                                |
| Ex16_Ruidos.glsl                | Ruído em blocos usando `floor()`                        |
| Ex17_DistanceFields.glsl        | Gradiente radial com base na distância                  |
| Ex18_DistanceFields.glsl        | Composição de campos com `+`, `min()`, `max()`          |
| Ex18-b_DistanceCores.glsl       | Variações de cor com campos                             |
| Ex18-c_DistanceMix.glsl         | Efeitos com `mix()` sobre campos de distância           |
| Ex19_CoresMix.glsl              | Mistura avançada de cores com vetores                   |
| Shader_Textura_Cubo.py          | Código extra em Python/OpenGL para cena com texturas    |
| textura.jpg                     | Textura usada no cubo do código Python                  |

---

## ▶️ Como Executar os Shaders

1. Instale a extensão **GLSL Canvas** no VS Code.  
2. Abra qualquer arquivo `.glsl` deste diretório.  
3. Pressione `Ctrl+Shift+P` e selecione `GLSL: Show Shader`.  
4. Visualize a execução em tempo real no painel interativo.

---
