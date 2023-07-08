#version 330 core

uniform sampler2D tex;

in vec2 uvs;
out vec4 f_color;

void main() {

	float d = 1.0 / 200;
	float u = floor( uvs.x / d ) * d;
	float v = floor( uvs.y / d ) * d;

	f_color = vec4(texture(tex, vec2(u, v)).rgb, 1);

}