precision mediump float;
// Define a precisão padrão para variáveis do tipo float no fragment shader.
// 'mediump' é um nível de precisão média, que é comum em shaders.

void main() {
// Função principal do fragment shader, onde a cor do fragmento será definida.
// Configurar a cor para azul claro
vec3 color = vec3(0.502, 0.6196, 1.0); // Azul claro
// Cria um vetor 3D 'color' com componentes RGB. Neste caso, define a cor como azul claro.






gl_FragColor = vec4(color, 1.0);
// Define a cor final do fragmento. 'gl_FragColor' é uma variável de saída predefinida que
// armazena a cor do fragmento. Aqui, convertendo o vetor 3D 'color' em um vetor 4D (vec4)
// adicionando um componente alfa (opacidade) de 1.0 (totalmente opaco).
}
