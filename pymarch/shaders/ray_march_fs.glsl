#version 330

const int MAX_INTERATIONS = 100;
const float MIN_INTERACTION_SIZE = 0.0001;
const float MAX_TRAVEL_LENGTH = 1000.0;

struct Sphere {
    vec3 pos;
    vec3 colour;
    float radius;
};

uniform SceneBlock {
    ivec4 shape_counts;
    Sphere spheres[];
} scene;

uniform sampler2D texture0;

in vec2 vs_uv;

out vec4 fs_colour;


float SDFSphere(vec3 position, vec3 origin, float radius){
    return length(position - origin) - radius;
}


float get_world_dist(vec3 position){
    return 0.0;
}

vec3 get_world_normal(vec3 position){
    return vec3(1.0, 0.0, 0.0);
}



void main() {
    fs_colour = texture(texture0, vs_uv);
}
