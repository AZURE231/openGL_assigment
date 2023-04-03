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
    #n = v / np.linalg.norm(v)
    return v
class Mesh(object):
    def __init__(self, vert_shader, frag_shader):
        #  a Cube Made of Two Triangle Strips Using Primitive Restart

        #self.vertices = np.array(self.getUnitCircleVertices(radius, height), dtype=np.float32)
        self.graph = []
        N = 101
        for i in range (0, N):
            for j in range (0, N):
                x = (i - N/2) / (N/2)
                y = (j - N/2) / (N/2)
                t = math.hypot(x,y) * 4
                z = (1 - t*t) * math.exp(t*t/-2)
                self.graph.append([x, y, z])

        self.vertices = np.array(self.graph, dtype=np.float32)

        indices = []
        # for y in range(0, 101):
        #     for x in range (0, 100):
        #         indices.append(y * 101 + x)
        #         indices.append(y * 101 + x + 1)
        # for x in range(0, 101):
        #     for y in range(0, 100):
        #         indices.append(y * 101 + x)
        #         indices.append((y+1)*100 + x)
        for y in range(0, 100):
            for x in range (0, 100):
                indices.append(y * 101 + x)
                indices.append(y * 101 + x + 1)
                indices.append((y + 1) * 101 + x + 1)

                indices.append(y * 101 + x)
                indices.append((y + 1) * 101 + x + 1)
                indices.append((y + 1) * 101 + x)


        self.indices = np.array(indices)
        for x in range(0, 10):
            print(self.indices[x])
        print(self.vertices[self.indices[0]])
        print(self.vertices[self.indices[2]])
        print(self.vertices[self.indices[1]])
        print(len(self.indices))

        normals = []
        for i in range(0, len(self.vertices)-3, 3):
            normals.append(normal_of_face(self.vertices[self.indices[i]], self.vertices[self.indices[i+2]], self.vertices[self.indices[i+1]]))
            normals.append(normal_of_face(self.vertices[self.indices[i]], self.vertices[self.indices[i+2]], self.vertices[self.indices[i+1]]))
            normals.append(normal_of_face(self.vertices[self.indices[i]], self.vertices[self.indices[i+2]], self.vertices[self.indices[i+1]]))
        self.normals = np.array(normals)  # YOUR CODE HERE to compute vertex's normal using the coordinates

        # colors: RGB format
        color = []
        for i in range(0, len(self.vertices)):
            color.append([1, 0, 0])
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
        unitCircleVertices = [0, height, 0]
        for x in range(0, self.sectorCount + 1):
            sectorAngle = x * sectorStep
            unitCircleVertices.append(radius * math.cos(sectorAngle))
            unitCircleVertices.append(height)
            unitCircleVertices.append(radius * math.sin(sectorAngle))
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
        # setup VAO for drawing cylinder's side
        self.vao.add_vbo(0, self.vertices, ncomponents=3, stride=0, offset=None)
        self.vao.add_vbo(1, self.colors, ncomponents=3, stride=0, offset=None)
        self.vao.add_vbo(2, self.normals, ncomponents=3, stride=0, offset=None)
        self.vao.add_ebo(self.indices)

        # Light
        I_light = np.array([
            [0.6, 0.8, 0.8],  # diffuse
            [1, 0.8, 0.4],  # specular
            [0.6, 0.8, 0.2]  # ambient
        ], dtype=np.float32)
        light_pos = np.array([100, 100, 100], dtype=np.float32)

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
        GL.glDrawElements(GL.GL_TRIANGLES, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)

    def key_handler(self, key):

        if key == glfw.KEY_1:
            self.selected_texture = 1
        if key == glfw.KEY_2:
            self.selected_texture = 2
