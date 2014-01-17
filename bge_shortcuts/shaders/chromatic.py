script = """

// SolarLune

uniform sampler2D bgl_RenderedTexture;
const float dist = $shader_chromatic_strength;

void main()
{
	vec2 texcoord = gl_TexCoord[0].xy;
	vec3 sum = vec3(0.0);

	sum.r = vec3(texture2D(bgl_RenderedTexture, texcoord * 1 + vec2(0.00,0.00))).r;
	sum.g = vec3(texture2D(bgl_RenderedTexture, texcoord * (1.0 - (0.005 * dist)) + vec2(0.002,0.002))).g;
	sum.b = vec3(texture2D(bgl_RenderedTexture, texcoord * (1.0 - (0.01 * dist)) + vec2(0.004,0.004))).b;

	gl_FragColor = vec4(sum, 1.0);
}
"""