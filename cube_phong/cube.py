from tostudents.libs.shader import *
from tostudents.libs import transform as T
from tostudents.libs.buffer import *
import ctypes
import glfw

def normal_of_face(A, B, C):
    #YOUR CODE IS HERE
    v1 = B - A
    v2 = C - A
    v = np.cross(v1, v2)
    n = v / np.linalg.norm(v)
    return n

class Cube(object):
    def __init__(self, vert_shader, frag_shader):
        # a Cube Made of Two Triangle Strips Using Primitive Restart
        # self.vertices = np.array([
        #     # YOUR CODE HERE to specify vertex's coordinates
        #     [-1, -1, -1],
        #     [-1, -1, 1],
        #     [-1, 1, -1],
        #     [-1, 1, 1],
        #     [1, -1, -1],
        #     [1, -1, 1],
        #     [1, 1, -1],
        #     [1, 1, 1]
        # ], dtype=np.float32)
        #
        # self.indices = np.array(
        #     # YOUR CODE HERE to specify index data
        #     [0, 1, 2, 3, 6, 7, 4, 5, 0xFFFF, 2, 6, 0, 4, 1, 5, 3, 7]
        # )

        self.vertices = np.array([
            # YOUR CODE HERE to specify vertex's coordinates
            [-1.0,-1.0,-1.0],
            [-1.0,-1.0, 1.0],
            [-1.0, 1.0, 1.0],
            [1.0, 1.0,-1.0],
            [-1.0,-1.0,-1.0],
            [-1.0, 1.0,-1.0],
            [1.0,-1.0, 1.0],
            [-1.0,-1.0,-1.0],
            [1.0,-1.0,-1.0],
            [1.0, 1.0,-1.0],
            [1.0,-1.0,-1.0],
            [-1.0,-1.0,-1.0],
            [-1.0,-1.0,-1.0],
            [-1.0, 1.0, 1.0],
            [-1.0, 1.0,-1.0],
            [1.0,-1.0, 1.0],
            [-1.0,-1.0, 1.0],
            [-1.0,-1.0,-1.0],
            [-1.0, 1.0, 1.0],
            [-1.0,-1.0, 1.0],
            [1.0,-1.0, 1.0],
            [1.0, 1.0, 1.0],
            [1.0,-1.0,-1.0],
            [1.0, 1.0,-1.0],
            [1.0,-1.0,-1.0],
            [1.0, 1.0, 1.0],
            [1.0,-1.0, 1.0],
            [1.0, 1.0, 1.0],
            [1.0, 1.0,-1.0],
            [-1.0, 1.0,-1.0],
            [1.0, 1.0, 1.0],
            [-1.0, 1.0,-1.0],
            [-1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0],
            [-1.0, 1.0, 1.0],
            [1.0,-1.0, 1.0]
        ], dtype=np.float32)

        self.indices = np.array(
            # YOUR CODE HERE to specify index data
            [x for x in range(0, len(self.vertices))]
        )


        normals = []
        for i in range(0, 34, 3):
            normals.append(normal_of_face(self.vertices[i], self.vertices[i + 1], self.vertices[i + 2]))
            normals.append(normal_of_face(self.vertices[i], self.vertices[i + 1], self.vertices[i + 2]))
            normals.append(normal_of_face(self.vertices[i], self.vertices[i + 1], self.vertices[i + 2]))
        self.normals = np.array(normals)  # YOUR CODE HERE to compute vertex's normal using the coordinates

        # colors: RGB format
        self.colors = np.array([
            # YOUR CODE HERE to specify vertex's color
            [1, 1, 0],
            [1, 1, 0],
            [1, 1, 0],
            [1, 1, 0],
            [1, 1, 0],
            [1, 1, 0],
            [1, 1, 0],
            [1, 1, 0]
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
        #GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)

    def key_handler(self, key):

        if key == glfw.KEY_1:
            self.selected_texture = 1
        if key == glfw.KEY_2:
            self.selected_texture = 2
