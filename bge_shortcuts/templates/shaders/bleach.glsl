uniform sampler2D bgl_RenderedTexture;
const float amount = $shader_bleach_strength;

vec2 texCoord = vec2(gl_TexCoord[0]).st;

//constant variables.
const vec4 one = vec4(1.0);	
const vec4 two = vec4(2.0);
const vec4 lumcoeff = vec4(0.2125,0.7154,0.0721,0.0);


vec4 overlay(vec4 myInput, vec4 previousmix, vec4 amount)
{
	float luminance = dot(previousmix,lumcoeff);
	float mixamount = clamp((luminance - 0.45) * 10., 0., 1.);

	vec4 branch1 = two * previousmix * myInput;
	vec4 branch2 = one - (two * (one - previousmix) * (one - myInput));
	
	vec4 result = mix(branch1, branch2, vec4(mixamount) );

	return mix(previousmix, result, amount);
}

void main (void) 
{ 		
	vec4 input0 = texture2D(bgl_RenderedTexture, texCoord);
				
	vec4 luma = vec4(dot(input0,lumcoeff));

	gl_FragColor = overlay(luma, input0, vec4(amount));
	gl_FragColor.a = 1.0;	
}
