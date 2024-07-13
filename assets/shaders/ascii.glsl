#version 330 core

uniform sampler2D tex;
uniform sampler2D asciipng;

in vec2 uvs;
out vec4 f_color;

const vec2 fontSize = vec2(8.0, 16.0);

vec4 lookupASCII(float asciiValue) {

	vec2 pos = mod(gl_FragCoord.xy, fontSize.xy);

	pos = pos / vec2(2048.0, 16.0);
	pos.x += asciiValue;
	return vec4(texture(asciipng,pos).rgb, 1.0);

}

void main(void) {

	vec2 invViewport = vec2(1.0) / vec2(1920, 1080);
	vec2 pixelSize = fontSize;
	vec4 sum = vec4(0.0);
	vec2 uvClamped = uvs-mod(uvs,pixelSize * invViewport);
	for (float x=0.0;x<fontSize.x;x++){
		for (float y=0.0;y<fontSize.y;y++){
			vec2 offset = vec2(x,y);
			sum += texture(tex,uvClamped+(offset*invViewport));
		}
	}
	vec4 avarage = sum / vec4(fontSize.x*fontSize.y);
	float brightness = (avarage.x+avarage.y+avarage.z)*0.33333;
	vec4 clampedColor = floor(avarage*8.0)/8.0;
	float asciiChar = floor((1.0-brightness)*256.0)/256.0;
	f_color = clampedColor*lookupASCII(asciiChar);

}
