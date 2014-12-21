uniform sampler2D bgl_RenderedTexture;

uniform float timer;
const float noise_amount = $shader_movie_noise_strength;



void main(void)
{ 	
	
	float noiseR =  (fract(sin(dot(gl_TexCoord[0].st ,vec2(12.9898,78.233)+timer)) * 43758.5453));
	float noiseG =  (fract(sin(dot(gl_TexCoord[0].st ,vec2(12.9898,78.233)+timer*2)) * 43758.5453)); 
	float noiseB =  (fract(sin(dot(gl_TexCoord[0].st ,vec2(12.9898,78.233)+timer*3)) * 43758.5453));
	
	vec4 noise = vec4(noiseR,noiseG,noiseB,1.0);
	   
	gl_FragColor = texture2D(bgl_RenderedTexture, gl_TexCoord[0].st) + (noise*(noise_amount * -1));
}
