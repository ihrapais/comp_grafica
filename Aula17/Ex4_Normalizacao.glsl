// Define a precisão dos números de ponto flutuante no WebGL.
precision mediump float;
// Uniformes que armazenam a resolução da tela e as coordenadas do ponteiro do mouse. uniform vec2 
u_resolution;
uniform vec2 u_mouse;
void main() {
  // Normalizamos a posição do pixel em relação à resolução da tela,
  // para que ambas as coordenadas fiquem na mesma faixa de valores (entre 0 e 1).
  vec2 st = gl_FragCoord.xy / u_resolution;
  // Normalizamos as coordenadas do ponteiro do mouse em relação à resolução da tela,
  // para que ambas as coordenadas fiquem na mesma faixa de valores (entre 0 e 1).
  vec2 mouse_normalized = u_mouse / u_resolution;
  // Definimos a cor do fragmento usando a coordenada x normalizada do ponteiro do mouse como
o canal vermelho (R),
  // enquanto os canais verde (G) e azul (B) são fixados em 0. O canal alfa (A) é definido como 1,  
tornando o fragmento completamente opaco.
  gl_FragColor = vec4(mouse_normalized.x, 0.0, 1.0, 1.0);
}