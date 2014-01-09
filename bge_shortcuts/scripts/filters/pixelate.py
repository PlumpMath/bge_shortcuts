script = """
// Name: Pixellate
// Author: SolarLune
// Date: 6/6/11
//
// Notes: Pixellates the screen using blocks consisting of cellx size on the
// X-axis and celly size on the Y-axis.

uniform sampler2D bgl_RenderedTexture;
const float cellw = 1;
const float cellh = 1;
const vec2 winsize = 100;

float Round(float value){       // Rounds off the specified number
	if (ceil(value) - value < 0.5)
		return ceil(value);
	else
		return floor(value);
}

void main(void)
{
	vec2 uv = gl_TexCoord[0].xy;

	float dx = cellw * (1.0 / winsize.x);
	float dy = cellh * (1.0 / winsize.y);

	vec2 coord = vec2(dx * Round(uv.x / dx), dy * Round(uv.y / dy));

	coord.x = min(max(0.0, coord.x), 1.0);
	coord.y = min(max(0.0, coord.y), 1.0);

	gl_FragColor = vec4(texture2D(bgl_RenderedTexture, coord));
}
"""