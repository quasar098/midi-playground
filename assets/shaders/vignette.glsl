#version 330 core

uniform sampler2D tex;

in vec2 uvs;
out vec4 f_color;

void main() {
    vec2 uv = uvs;

    float dist = distance(uv, vec2(0.5, 0.5));

    f_color = vec4(texture(tex, uv).rgb * smoothstep(0.8, 0.2, dist * 0.8), 1);
}