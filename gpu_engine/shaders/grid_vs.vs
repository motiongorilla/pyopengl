#version 330 core
in vec3 position;

uniform mat4 projection_mat;
uniform mat4 model_mat;
uniform mat4 view_mat;

out vec3 color;
out vec3 nearPoint;
out vec3 farPoint;

vec3 UnprojectPoint(float x, float y, float z, mat4 proj, mat4 view){
    vec4 unprojectedPoint = inverse(proj) * inverse(view) * vec4(x,y,z,1.0);
    return unprojectedPoint.xyz/unprojectedPoint.w;
}

void main(){
        vec3 p = position.xyz;
        nearPoint = UnprojectPoint(p.x, p.y, 0, projection_mat, view_mat).xyz;
        farPoint = UnprojectPoint(p.x, p.y, 1, projection_mat, view_mat).xyz;
        gl_Position = projection_mat * inverse(view_mat) * model_mat * vec4(position, 1);
}
