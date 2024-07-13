#version 330 core

uniform sampler2D tex;

in vec2 uvs;
out vec4 f_color;

void main() {

	vec2 dir = uvs - vec2( 0.5, 0.5 );
	float d = 0.7 * length( dir );
	normalize(dir);
	vec2 value = d * dir * vec2(0.05, 0.05);

	vec4 c1 = texture( tex, uvs - value * 2.0 );
	vec4 c2 = texture( tex, uvs - value );
	vec4 c3 = texture( tex, uvs );

	f_color = vec4( c1.r, c2.g, c3.b, c1.a + c2.a + c3.b );

}
