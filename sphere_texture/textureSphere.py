from tostudents.libs.shader import *
from tostudents.libs import transform as T
from tostudents.libs.buffer import *
import ctypes
import glfw
import math


class TexCube(object):
    def __init__(self, vert_shader, frag_shader):
        self.sectorCount = 100
        self.stackCount = 100

        self.sphereVertices = []
        self.sphereNormal = []
        self.sphereIndices = []
        self.sphereColor = []
        self.sphereTexture = []

        self.drawSphere(1)

        self.vertices = np.array(self.sphereVertices, dtype=np.float32)

        self.indices = np.array(self.sphereIndices)

        self.normals = np.array(self.sphereNormal, dtype=np.float32)

        self.texcoords = np.array(self.sphereTexture, dtype=np.float32)

        self.vao = VAO()

        self.shader = Shader(vert_shader, frag_shader)
        self.uma = UManager(self.shader)
        #

    """
    Create object -> call setup -> call draw
    """

    def drawSphere(self, radius):
        nx, ny, nzm, lenghInv = 1/radius, 1/radius, 1/radius, 1/radius

        sectorStep = 2 * math.pi / self.sectorCount
        stackStep = math.pi / self.stackCount

        for i in range(0, self.stackCount + 1):
            stackAngle = math.pi / 2 - i * stackStep
            xy = radius * math.cos(stackAngle)
            z = radius * math.sin(stackAngle)

            for j in range(0, self.sectorCount + 1):
                sectorAngle = j * sectorStep
                x = xy * math.cos(sectorAngle)
                y = xy * math.sin(sectorAngle)
                self.sphereVertices.append(x)
                self.sphereVertices.append(y)
                self.sphereVertices.append(z)

                nx = x * lenghInv
                ny = y * lenghInv
                nz = z * lenghInv
                self.sphereNormal.append(nx)
                self.sphereNormal.append(ny)
                self.sphereNormal.append(nz)

                s = j / self.sectorCount
                t = i / self.stackCount
                self.sphereTexture.append(s)
                self.sphereTexture.append(t)

        for i in range(0, self.stackCount):
            k1 = i * (self.sectorCount + 1)
            k2 = k1 + self.sectorCount + 1

            for j in range(0, self.sectorCount):
                if i != 0:
                    self.sphereIndices.append(k1)
                    self.sphereIndices.append(k2)
                    self.sphereIndices.append(k1 + 1)
                if i != self.stackCount - 1:
                    self.sphereIndices.append(k1 + 1)
                    self.sphereIndices.append(k2)
                    self.sphereIndices.append(k2 + 1)
                k1 += 1
                k2 += 1
    def setup(self):
        # setup VAO for drawing cylinder's side
        self.vao.add_vbo(0, self.vertices, ncomponents=3, stride=0, offset=None)
        self.vao.add_vbo(1, self.normals, ncomponents=3, stride=0, offset=None)
        self.vao.add_vbo(2, self.texcoords, ncomponents=2, stride=0, offset=None)
        self.vao.add_vbo(3, self.normals, ncomponents=3, stride=0, offset=None)

        # setup EBO for drawing cylinder's side, bottom and top
        self.vao.add_ebo(self.indices)

        # setup textures
        self.uma.setup_texture("texture", "./image/2k_earth_daymap.jpg")

        # Light
        I_light = np.array([
            [1, 1, 1],  # diffuse
            [1, 1, 1],  # specular
            [1, 1, 1]  # ambient
        ], dtype=np.float32)
        light_pos = np.array([20, 0.5, 0.9], dtype=np.float32)

        # Materials
        K_materials = np.array([
            [0.5, 0.0, 0.0],  # diffuse
            [0.5, 0.0, 0.0],  # specular
            [0.5, 0.0, 0.0]  # ambient
        ], dtype=np.float32)

        shininess = 50.0
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
        GL.glDrawElements(GL.GL_TRIANGLES, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)

    def key_handler(self, key):

        if key == glfw.KEY_1:
            self.selected_texture = 1
        if key == glfw.KEY_2:
            self.selected_texture = 2
