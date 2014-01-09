script = """
uniform sampler2D bgl_DepthTexture;

void main(void)
{
	vec4 color = texture2D(bgl_DepthTexture, gl_TexCoord[0].st);
	float value = (color.r + color.g + color.b) / 3.0;
	float factor = (1.000 - value) * 20.0000;
	color -= vec4(factor, factor, factor, factor);
	gl_FragColor = color;
}
"""