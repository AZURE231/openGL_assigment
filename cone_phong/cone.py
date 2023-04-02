from tostudents.libs.shader import *
from tostudents.libs import transform as T
from tostudents.libs.buffer import *
import ctypes
import glfw
import math


class Cube(object):
    def __init__(self, vert_shader, frag_shader):
        #  a Cube Made of Two Triangle Strips Using Primitive Restart
        self.blue = [0.37, 0.66, 1]
        self.num_side = 100
        self.num_circle = 200
        self.radius = 1
        vertices_cone = []
        dif = self.radius/self.num_circle
        for x in range(0, self.num_circle):
            rad_dif = self.radius - x * dif
            y_dif = x * dif
            vertices_cone.append(self.draw_circle_array(rad_dif, y_dif))

        self.vertices = np.array(vertices_cone, dtype=np.float32)
        # indices_con = [x for x in range(0, self.num_side * self.num_circle)]
        # for x in range(1, self.num_circle):
        #     indices_con.insert(x * self.num_side, 0xFFFF)
        self.indices = np.array([x for x in range(0, self.num_side * self.num_circle)])

        normals = np.random.normal(0, 3, (3, 3)).astype(np.float32)
        normals[:, 2] = np.abs(normals[:, 2])
        self.normals = normals / np.linalg.norm(normals, axis=1, keepdims=True)  # YOUR CODE HERE to compute vertex's normal using the coordinates

        # colors: RGB format
        color = []
        for x in range(0, self.num_side * self.num_circle):
            color.append(self.blue)
        self.colors = np.array(color, dtype=np.float32)

        self.vao = VAO()

        self.shader = Shader(vert_shader, frag_shader)
        self.uma = UManager(self.shader)
        #

    """
    Create object -> call setup -> call draw
    """
    def draw_circle_array(self, radius, y_coordinate):
        circle_array = []
        angle = 360 / self.num_side
        for x in range(0, self.num_side + 1):
            x_coordinate = radius * math.cos(angle + (2 * x * math.pi) / self.num_side)
            z_coordinate = radius * math.sin(angle + (2 * x * math.pi) / self.num_side)
            circle_array.append([x_coordinate, y_coordinate, z_coordinate])
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
        GL.glDrawElements(GL.GL_TRIANGLE_FAN, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)
        #GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)

    def key_handler(self, key):

        if key == glfw.KEY_1:
            self.selected_texture = 1
        if key == glfw.KEY_2:
            self.selected_texture = 2
