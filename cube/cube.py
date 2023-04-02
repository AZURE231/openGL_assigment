from tostudents.libs.shader import *
from tostudents.libs import transform as T
from tostudents.libs.buffer import *
import ctypes
import glfw


class Cube(object):
    def __init__(self, vert_shader, frag_shader):
        #  a Cube Made of Two Triangle Strips Using Primitive Restart
        self.vertices = np.array([
            # YOUR CODE HERE to specify vertex's coordinates
            [-1, -1, -1],
            [-1, -1, 1],
            [-1, 1, -1],
            [-1, 1, 1],
            [1, -1, -1],
            [1, -1, 1],
            [1, 1, -1],
            [1, 1, 1]
        ], dtype=np.float32)

        # self.vertices = np.array([
        #     # YOUR CODE HERE to specify vertex's coordinates
        #     [+1, -1, -1],  # D 0
        #     [+1, -1, +1],  # A 1
        #     [-1, -1, -1],  # C 2
        #     [-1, -1, +1],  # B 3
        #     [-1, +1, -1],  # G 4
        #     [-1, +1, +1],  # F 5
        #     [+1, +1, -1],  # H 6
        #     [+1, +1, +1],  # E 7
        #     [+1, -1, -1],  # D 8
        #     [+1, -1, +1]  # A 9
        # ], dtype=np.float32)
        #
        # self.indices = np.array(
        #     # YOUR CODE HERE to specify index data
        #     [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 8]
        # )
        self.indices = np.array(
            # YOUR CODE HERE to specify index data
            [0, 1, 2, 3, 6, 7, 4, 5, 0xFFFF, 2, 6, 0, 4, 1, 5, 3, 7]
        )
        normals = np.random.normal(0, 3, (3, 3)).astype(np.float32)
        normals[:, 2] = np.abs(normals[:, 2])
        self.normals = normals / np.linalg.norm(normals, axis=1, keepdims=True)  # YOUR CODE HERE to compute vertex's normal using the coordinates

        # colors: RGB format
        self.colors = np.array([
            # YOUR CODE HERE to specify vertex's color
            [1, 1, 1],
            [1, 1, 0],
            [1, 0, 1],
            [1, 0, 0],
            [0, 1, 1],
            [0, 1, 0],
            [0, 0, 1],
            [0, 0, 0]
        ], dtype=np.float32)

        self.vao = VAO()

        self.shader = Shader(vert_shader, frag_shader)
        self.uma = UManager(self.shader)
        #

    """
    Create object -> call setup -> call draw
    """

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
        GL.glDrawElements(GL.GL_TRIANGLE_STRIP, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)
        #GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)

    def key_handler(self, key):

        if key == glfw.KEY_1:
            self.selected_texture = 1
        if key == glfw.KEY_2:
            self.selected_texture = 2
