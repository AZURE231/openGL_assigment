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
    def __init__(self, vert_shader, frag_shader, radius, height, colour, facing):
        #  a Cube Made of Two Triangle Strips Using Primitive Restart
        self.sectorCount = 3

        #self.vertices = np.array(self.getUnitCircleVertices(radius, height), dtype=np.float32)
        self.vertices = np.array(self.getUnitCircleVertices(radius, height), dtype=np.float32)
        self.indices = np.array([x for x in range(0, len(self.vertices))])

        if facing:
            normals = []
            face1 = normal_of_face(self.vertices[0], self.vertices[2], self.vertices[1])
            face2 = normal_of_face(self.vertices[0], self.vertices[3], self.vertices[2])
            face3 = normal_of_face(self.vertices[0], self.vertices[4], self.vertices[3])
            normals.append((face1 + face2 + face3) / 3)
            normals.append((face1 + face3)/2)
            normals.append((face1 + face2)/2)
            normals.append((face2 + face3)/2)
            normals.append((face1 + face3)/2)
            self.normals = np.array(normals)
        else:
            normals = []
            face1 = normal_of_face(self.vertices[0], self.vertices[1], self.vertices[2])
            face2 = normal_of_face(self.vertices[0], self.vertices[2], self.vertices[3])
            face3 = normal_of_face(self.vertices[0], self.vertices[3], self.vertices[4])
            normals.append((face1 + face2 + face3) / 3)
            normals.append((face1 + face3) / 2)
            normals.append((face1 + face2) / 2)
            normals.append((face2 + face3) / 2)
            normals.append((face1 + face3) / 2)
            self.normals = np.array(normals)

        # colors: RGB format
        color = []
        for i in range(0, self.sectorCount + 2):
            color.append(colour)
        self.colors = np.array(color, dtype=np.float32)

        self.vao = VAO()

        self.shader = Shader(vert_shader, frag_shader)
        self.uma = UManager(self.shader)
        #

    """
    Create object -> call setup -> call draw
    """
    def getUnitCircleVertices(self, radius, height):
        sectorStep = 2 * math.pi / self.sectorCount
        unitCircleVertices = [[0, height, 0]]
        for x in range(0, self.sectorCount + 1):
            sectorAngle = x * sectorStep
            # unitCircleVertices.append(radius * math.cos(sectorAngle))
            # unitCircleVertices.append(0)
            # unitCircleVertices.append(radius * math.sin(sectorAngle))
            unitCircleVertices.append([radius * math.cos(sectorAngle), 0, radius * math.sin(sectorAngle)])
        return unitCircleVertices

    def draw_circle_array(self, radius, y_coordinate):
        circle_array = [0, y_coordinate, 0]
        angle = 360 / self.sectorCount
        for x in range(0, self.sectorCount + 1):
            x_coordinate = radius * math.cos(angle + (2 * x * math.pi) / self.sectorCount)
            z_coordinate = radius * math.sin(angle + (2 * x * math.pi) / self.sectorCount)
            circle_array.append(x_coordinate)
            circle_array.append(y_coordinate)
            circle_array.append(z_coordinate)
            # circle_array.append(x_coordinate)
            # circle_array.append(y_coordinate)
        return circle_array

    def setup(self):
        self.vao.add_vbo(0, self.vertices, ncomponents=3, stride=0, offset=None)
        self.vao.add_vbo(1, self.colors, ncomponents=3, stride=0, offset=None)
        self.vao.add_vbo(2, self.normals, ncomponents=3, stride=0, offset=None)
        self.vao.add_ebo(self.indices)

        # self.vao.add_vbo(0, self.vertices, ncomponents=3, stride=0, offset=None)
        # self.vao.add_vbo(1, self.colors, ncomponents=3, stride=0, offset=None)
        # self.vao.add_ebo(self.indices)

        # Light
        I_light = np.array([
            [0.6, 0.8, 0.8],  # diffuse
            [1, 0.8, 0.4],  # specular
            [0.6, 0.8, 0.2]  # ambient
        ], dtype=np.float32)
        light_pos = np.array([1, 1, -1], dtype=np.float32)

        # Materials
        K_materials = np.array([
            [0.5, 0.0, 0.7],  # diffuse
            [0.5, 0.0, 0.7],  # specular
            [0.5, 0.0, 0.7]  # ambient
        ], dtype=np.float32)

        shininess = 128.0
        phong_factor = 10.0  # blending factor for phong shading and texture

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
