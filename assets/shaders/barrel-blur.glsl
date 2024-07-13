#version 330 core

uniform sampler2D tex;

in vec2 uvs;
out vec4 f_color;

vec2 barrelDistortion(vec2 coord, float amt) {
	
	vec2 cc = coord - 0.5;
	float dist = dot(cc, cc);
	return coord - cc * dist * amt * 0.04;

}

void main() {

	vec2 uv=uvs;

	vec4 a1=texture(tex, barrelDistortion(uv,0.0));
	vec4 a2=texture(tex, barrelDistortion(uv,0.2));
	vec4 a3=texture(tex, barrelDistortion(uv,0.4));
	vec4 a4=texture(tex, barrelDistortion(uv,0.6));
	
	vec4 a5=texture(tex, barrelDistortion(uv,0.8));
	vec4 a6=texture(tex, barrelDistortion(uv,1.0));
	vec4 a7=texture(tex, barrelDistortion(uv,1.2));
	vec4 a8=texture(tex, barrelDistortion(uv,1.4));
	
	vec4 a9=texture(tex, barrelDistortion(uv,1.6));
	vec4 a10=texture(tex, barrelDistortion(uv,1.8));
	vec4 a11=texture(tex, barrelDistortion(uv,2.0));
	vec4 a12=texture(tex, barrelDistortion(uv,2.2));

	vec4 tx=(a1+a2+a3+a4+a5+a6+a7+a8+a9+a10+a11+a12)/12.0;
	f_color = vec4(tx.rgb, 1);

}
