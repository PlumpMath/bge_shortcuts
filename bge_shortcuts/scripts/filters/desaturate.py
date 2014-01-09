script = """
// Name: Desaturation Filter
// Author: Printed in XNA Unleashed; Readapted for GLSL by SolarLune
// Date Updated: 6/6/11

uniform sampler2D bgl_RenderedTexture;
uniform float percentage = 1.0;

void main(void)
{
	vec4 color;
	color = texture2D(bgl_RenderedTexture, gl_TexCoord[0].st);

	float gray = dot(color.rgb, vec3(0.299, 0.587, 0.114));
	// The human eye is more sensitive to certain colors (like bright yellow) than others, so you need to use this specific color-formula to average them out to one monotone color (gray)

	vec4 desat = vec4(gray, gray, gray, color.a);

	gl_FragColor = mix(color, desat, percentage);
}
"""