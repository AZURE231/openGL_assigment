from tostudents.libs.shader import *
from tostudents.libs import transform as T
from tostudents.libs.buffer import *
import ctypes
import glfw
import math


class Mesh(object):
    def __init__(self, vert_shader, frag_shader, radius, height):
        #  a Cube Made of Two Triangle Strips Using Primitive Restart
        self.sectorCount = 50

        #self.vertices = np.array(self.getUnitCircleVertices(radius, height), dtype=np.float32)
        self.graph = []
        N = 101
        for i in range (0, N):
            for j in range (0, N):
                x = (i - N/2) / (N/2)
                y = (j - N/2) / (N/2)
                t = math.hypot(x,y) * 4
                z = (1 - t*t) * math.exp(t*t/-2)
                self.graph.append(x)
                self.graph.append(y)
                self.graph.append(z)


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

        normals = np.random.normal(0, 3, (3, 3)).astype(np.float32)
        normals[:, 2] = np.abs(normals[:, 2])
        self.normals = normals / np.linalg.norm(normals, axis=1, keepdims=True)  # YOUR CODE HERE to compute vertex's normal using the coordinates

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

        # setup EBO for drawing cylinder's side, bottom and top
        self.vao.add_ebo(self.indices)

        return self

    def draw(self, projection, view, model):
        GL.glUseProgram(self.shader.render_idx)
        modelview = view

        self.uma.upload_uniform_matrix4fv(projection, 'projection', True)
        self.uma.upload_uniform_matrix4fv(modelview, 'modelview', True)

        self.vao.activate()
        for i in range(0, 101):
            GL.glDrawElements(GL.GL_TRIANGLES, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)

    def key_handler(self, key):

        if key == glfw.KEY_1:
            self.selected_texture = 1
        if key == glfw.KEY_2:
            self.selected_texture = 2
