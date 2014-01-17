script = """
// Name: Sepia Filter
// Author: Derived from Desaturate and Blender's source Sepia filter
// Date Updated: 2/21/11

uniform sampler2D bgl_RenderedTexture;
const float percentage = $shader_warm_sepia_strength;

void main(void)
{
	vec4 color;
	color = texture2D(bgl_RenderedTexture, gl_TexCoord[0].st);

	float gray = dot(color.rgb, vec3(0.299, 0.587, 0.114));
	// The human eye is more sensitive to certain colors (like bright yellow) than others, so you need to use this specific color-formula to average them out to one monotone color (gray)

	vec4 desat = vec4(gray * vec3(1.2, 1.0, 0.8), color.a);

	gl_FragColor = mix(color, desat, percentage);
}
"""