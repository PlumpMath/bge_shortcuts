uniform sampler2D bgl_RenderedTexture;

const float retinex = $shader_retinex_strength;

vec4 sample( in vec2 coord ) 
{
 	return texture2D(bgl_RenderedTexture, coord )*0.5*texture2D(bgl_RenderedTexture, coord )*0.5; 	
}


void main(void)
{

vec4 bloom = vec4(0);
	
int j;
int i;

for( i= -5 ;i < 5; i++)
{
for (j = -5; j < 5; j++)
	{
	bloom += sample (gl_TexCoord[0].st + vec2(j, i)*0.003) * 0.06;           
	}
}	


	vec4 value =  texture2D(bgl_RenderedTexture, gl_TexCoord[0].st);
	vec4 pow_value = pow(value,(bloom*(retinex * -1)));
	
	gl_FragColor = pow_value*value;

}

