#version 330 core
in vec3 color;
in vec3 normal;
in vec3 fragpos;
in vec3 view_pos;
in vec2 uv;

uniform sampler2D tex;

out vec4 frag_color;

struct light{
        vec3 position;
        vec3 color;
        };

#define NUM_LIGHTS 2
uniform light light_data[NUM_LIGHTS];


vec4 Create_Light(vec3 light_pos, vec3 light_color, vec3 normal, vec3 fragpos, vec3 view_dir, vec3 color){
        //ambient
        float ambient_strength = 0.1;
        vec3 ambient_light = ambient_strength * light_color;

        // diffuse
        vec3 norm = normalize(normal);
        vec3 light_dir = normalize(light_pos-fragpos);
        float diff = max(dot(norm, light_dir), 0);
        vec3 diffuse = diff * light_color * 2.0f;

        // specular
        float specular_strength = 0.8;
        vec3 reflection_dir = normalize(-light_dir - norm);
        float spec = pow(max(dot(view_dir, reflection_dir), 0), 32);
        vec3 specular = specular_strength * spec * light_color;

        return vec4(color * (ambient_light + diffuse + specular),1);
        }

void main(){
        vec3 view_dir = normalize(view_pos-fragpos);
        frag_color = vec4(0,0,0,1);

        for(int i=0; i < NUM_LIGHTS; i++) {
            frag_color += Create_Light(light_data[i].position, light_data[i].color, normal, fragpos, view_dir, color);
        }

        frag_color = frag_color * texture(tex, uv);
}
