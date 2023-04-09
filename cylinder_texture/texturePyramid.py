from tostudents.libs.shader import *
from tostudents.libs import transform as T
from tostudents.libs.buffer import *
import ctypes
import glfw
import math

def normal_of_face(A, B, C):
    #YOUR CODE IS HERE
    v1 = B - A
    v2 = C - A
    v = np.cross(v1, v2)
    n = v / np.linalg.norm(v)
    return n
class Circle(object):
    def __init__(self, vert_shader, frag_shader, radius, height):
        #  a Cube Made of Two Triangle Strips Using Primitive Restart
        self.sectorCount = 50
        self.circleText = []
        # self.vertices = np.array(self.getUnitCircleVertices(radius, height), dtype=np.float32)
        self.vertices = np.array(self.draw_circle_array(radius, height), dtype=np.float32)
        self.indices = np.array([x for x in range(0, len(self.vertices))])

        normals = np.random.normal(0, 3, (3, 3)).astype(np.float32)
        normals[:, 2] = np.abs(normals[:, 2])
        self.normals = normals / np.linalg.norm(normals, axis=1,
                                                keepdims=True)  # YOUR CODE HERE to compute vertex's normal using the coordinates
        self.texcoords = np.array(self.circleText, dtype=np.float32)
        # colors: RGB format
        color = []
        for i in range(0, self.sectorCount + 2):
            color.append([1, 0, 0])
        self.colors = np.array(color, dtype=np.float32)

        self.vao = VAO()

        self.shader = Shader(vert_shader, frag_shader)
        self.uma = UManager(self.shader)

    def draw_circle_array(self, radius, y_coordinate):
        circle_array = [0, y_coordinate, 0]
        self.circleText = [0.5, 0.5]
        angle = 360 / self.sectorCount
        for x in range(0, self.sectorCount + 1):
            x_coordinate = radius * math.cos(angle + (2 * x * math.pi) / self.sectorCount)
            z_coordinate = radius * math.sin(angle + (2 * x * math.pi) / self.sectorCount)
            circle_array.append(x_coordinate)
            circle_array.append(y_coordinate)
            circle_array.append(z_coordinate)
            self.circleText.append(x_coordinate + 0.5)
            self.circleText.append(z_coordinate + 0.5)
            # circle_array.append(x_coordinate)
            # circle_array.append(y_coordinate)
        return circle_array

    def setup(self):
        # setup VAO for drawing cylinder's side
        self.vao.add_vbo(0, self.vertices, ncomponents=3, stride=0, offset=None)
        self.vao.add_vbo(1, self.normals, ncomponents=3, stride=0, offset=None)
        self.vao.add_vbo(2, self.texcoords, ncomponents=2, stride=0, offset=None)
        self.vao.add_vbo(3, self.normals, ncomponents=3, stride=0, offset=None)

        # setup EBO for drawing cylinder's side, bottom and top
        self.vao.add_ebo(self.indices)

        # setup textures
        self.uma.setup_texture("texture", "./image/gura.jpg")

        # Light
        I_light = np.array([
            [0.9, 0.4, 0.6],  # diffuse
            [0.9, 0.4, 0.6],  # specular
            [0.9, 0.4, 0.6]  # ambient
        ], dtype=np.float32)
        light_pos = np.array([0, 0.5, 0.9], dtype=np.float32)

        # Materials
        K_materials = np.array([
            [0.5, 0.0, 0.7],  # diffuse
            [0.5, 0.0, 0.7],  # specular
            [0.5, 0.0, 0.7]  # ambient
        ], dtype=np.float32)

        shininess = 100.0
        phong_factor = 0.0  # blending factor for phong shading and texture

        self.uma.upload_uniform_matrix3fv(I_light, 'I_light', False)
        self.uma.upload_uniform_vector3fv(light_pos, 'light_pos')
        self.uma.upload_uniform_matrix3fv(K_materials, 'K_materials', False)
        self.uma.upload_uniform_scalar1f(shininess, 'shininess')
        self.uma.upload_uniform_scalar1f(phong_factor, 'phong_factor')
        return self

    def draw(self, projection, view, model):
        GL.glUseProgram(self.shader.render_idx)
        modelview = view

        self.uma.upload_uniform_matrix4fv(projection, 'projection', True)
        self.uma.upload_uniform_matrix4fv(modelview, 'modelview', True)
        self.uma.upload_uniform_matrix4fv(model, 'normalMat', True)

        self.vao.activate()
        GL.glDrawElements(GL.GL_TRIANGLE_FAN, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)

    def key_handler(self, key):

        if key == glfw.KEY_1:
            self.selected_texture = 1
        if key == glfw.KEY_2:
            self.selected_texture = 2
