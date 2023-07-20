#version 330 core

uniform sampler2D tex;

in vec2 uvs;
out vec4 f_color;

void main() {
    f_color = vec4(texture(tex, uvs).rgb, 1);
}