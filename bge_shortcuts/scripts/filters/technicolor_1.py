script = """
uniform sampler2D bgl_RenderedTexture;
const float amount = 1.0;

vec2 texCoord = vec2(gl_TexCoord[0]).st;

const vec4 redfilter 		= vec4(1.0, 0.0, 0.0, 0.0);
const vec4 bluegreenfilter 	= vec4(0.0, 1.0, 0.7, 0.0);


void main(void)
{
	
	vec4 input0 = texture2D(bgl_RenderedTexture, texCoord);

	vec4 redrecord = input0 * redfilter;
	vec4 bluegreenrecord = input0 * bluegreenfilter;
	
	vec4 rednegative = vec4(redrecord.r);
	vec4 bluegreennegative = vec4((bluegreenrecord.g + bluegreenrecord.b)/2.0);

	vec4 redoutput = rednegative * redfilter;
	vec4 bluegreenoutput = bluegreennegative * bluegreenfilter;

	// additive 'projection"
	vec4 result = redoutput + bluegreenoutput;

	gl_FragColor = vec4(vec3(mix(input0, result, amount).rgb), 1.0);
} 
"""