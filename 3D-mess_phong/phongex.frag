#version 330 core

precision mediump float;
in vec3 normalInterp;  // Surface normal
in vec3 vertPos;       // Vertex position
in vec3 colorInterp;

uniform mat3 K_materials;
uniform mat3 I_light;

uniform float phong_factor; // Shininess
uniform float shininess; // Shininess
uniform vec3 light_pos; // Light position
out vec4 fragColor;

void main() {
  vec3 N = normalize(normalInterp);
  vec3 L = normalize(light_pos - vertPos);
  vec3 R = reflect(-L, N);      // Reflected light vector
  vec3 V = normalize(-vertPos); // Vector to viewer

  float lambertian = max(dot(N, L), 0.0);
  float specAngle = max(dot(R, V), 0.0);
  float specular = pow(specAngle, shininess);

  fragColor = vec4(K_materials[0] * 1 + K_materials[1] * 1 * lambertian
                    + K_materials[2] * specular * 1, 1.0);
}
