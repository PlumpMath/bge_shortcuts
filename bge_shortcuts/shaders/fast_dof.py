script = """

uniform sampler2D bgl_RenderedTexture;
uniform sampler2D bgl_DepthTexture;
 
#define blurclamp $shader_dof_blur_clamp
#define bias $shader_dof_bias 
#define KERNEL_SIZE  $shader_dof_kernel_size
 
void main() 
{
	vec4 depth = texture2D( bgl_DepthTexture, gl_TexCoord[0].xy );
 
	vec4 focus = texture2D( bgl_DepthTexture, vec2( 0.5, 0.5));

	float factor = ( depth.r - focus.r );
	 
	vec2 dofblur = clamp( factor * bias, -blurclamp, blurclamp );


	vec4 col = vec4(0.0);
	for ( float x = -KERNEL_SIZE + 1.0; x < KERNEL_SIZE; x += 1.0 )
	{
	for ( float y = -KERNEL_SIZE + 1.0; y < KERNEL_SIZE; y += 1.0 )
	{
		 col += texture2D(bgl_RenderedTexture, gl_TexCoord[0].xy + vec2( dofblur.x * x, dofblur.y * y ) );
	}
	}
	col /= ((KERNEL_SIZE+KERNEL_SIZE)-1)*((KERNEL_SIZE+KERNEL_SIZE)-1);
	 
	gl_FragColor = col;
	gl_FragColor.a = 1;
}

"""