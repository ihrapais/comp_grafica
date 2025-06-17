#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;

void main() {
    vec2 st = gl_FragCoord.xy / u_resolution;
    vec2 center = vec2(0.5);

    float d = distance(st, center);
    float vignette = smoothstep(0.8, 0.4, d);

    vec3 baseColor = vec3(0.2, 0.7, 1.0);
    vec3 color = baseColor * vignette;

    gl_FragColor = vec4(color, 1.0);
}
