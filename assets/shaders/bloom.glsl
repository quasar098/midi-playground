#version 330 core

uniform sampler2D tex;

in vec2 uvs;
out vec4 f_color;

void main()
{
   vec4 sum = vec4(0);
   vec2 texcoord = uvs;
  
   for( int i= -4 ;i < 4; i++)
   {
        for ( int j = -3; j < 3; j++)
        {
            sum += texture(tex, texcoord + vec2(j, i)*0.0006) * 0.13;
        }
   }
       if (texture(tex, texcoord).r < 0.3)
    {
       f_color = sum*sum*0.012 + texture(tex, texcoord);
    }
    else
    {
        if (texture(tex, texcoord).r < 0.5)
        {
            f_color = sum*sum*0.009 + texture(tex, texcoord);
        }
        else
        {
            f_color = sum*sum*0.0075 + texture(tex, texcoord);
        }
    }
}
