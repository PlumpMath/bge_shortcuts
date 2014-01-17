script = """
uniform sampler2D bgl_RenderedTexture;
uniform float percentage = $shader_saturate_strength;

void main(void)
{
	vec4 color;
	color = texture2D(bgl_RenderedTexture, gl_TexCoord[0].st);

	float gray = dot(color.rgb, vec3(0.299, 0.587, 0.114));

	vec4 desat = vec4(gray, gray, gray, color.a);

	gl_FragColor = mix(color, desat, (percentage * -1));
}
"""