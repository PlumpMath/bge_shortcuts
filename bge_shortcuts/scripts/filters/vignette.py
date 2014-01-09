script = """
uniform sampler2D bgl_RenderedTexture;

const float vignette_size = 0.5;
const float tolerance = 0.6;

void main(void)
{
	vec2 powers = pow(abs(gl_TexCoord[3].st - 0.5),vec2(2.0));
	float radiusSqrd = pow(vignette_size,2.0);
	float gradient = smoothstep(radiusSqrd-tolerance, radiusSqrd+tolerance, powers.x+powers.y);
   	    
	gl_FragColor = mix(texture2D(bgl_RenderedTexture, gl_TexCoord[0].st), vec4(0.0), gradient);
	gl_FragColor.a = 1.0;
}
"""