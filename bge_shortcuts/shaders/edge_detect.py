script = """
// Name: Edge Detect
// Author: SolarLune
// Date Updated: 6/6/11

// Notes: Detects the edges in the screenshot and outputs the edge colors.

uniform sampler2D bgl_RenderedTexture;
const float thickness = $shader_edge_detect_thickness;
const float edgef = $shader_edge_detect_edge;
const vec4 col = (1.0,1.0,1.0,1.0);

void main(void)
{
	float value = 0.001 * thickness;    // Value here controls how large the samples (and hence how thick the lines) are
	vec4 sample = texture2D(bgl_RenderedTexture, vec2(gl_TexCoord[0].st.x + value, gl_TexCoord[0].st.y + value));
	sample += texture2D(bgl_RenderedTexture, vec2(gl_TexCoord[0].st.x - value, gl_TexCoord[0].st.y - value));
	sample += texture2D(bgl_RenderedTexture, vec2(gl_TexCoord[0].st.x + value, gl_TexCoord[0].st.y - value));
	sample += texture2D(bgl_RenderedTexture, vec2(gl_TexCoord[0].st.x - value, gl_TexCoord[0].st.y + value));
	sample /= 4.0;
	vec4 center = texture2D(bgl_RenderedTexture, vec2(gl_TexCoord[0].st.x, gl_TexCoord[0].st.y));

	float edge = 0.01 / edgef;          // 'Edge' here controls how easy it is to get an outline on objects

	vec4 diff;
	diff = vec4(abs(sample.r - center.r), abs(sample.g - center.g), abs(sample.b- center.b), abs(sample.a - center.a));

	if ((diff.r < edge) || (diff.g < edge) || (diff.b < edge))
	{
		vec4 color = vec4(col.rgb, 1.0);
		gl_FragColor = mix(center, color, col.a);
	}
	else
		gl_FragColor = center;
}
"""