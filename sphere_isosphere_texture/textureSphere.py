from tostudents.libs.shader import *
from tostudents.libs import transform as T
from tostudents.libs.buffer import *
import ctypes
import glfw
import math


class TexSphere(object):
    def __init__(self, vert_shader, frag_shader):
        S = 186 / 2048
        T = 322 / 1024
        self.sectorCount = 100
        self.stackCount = 100

        self.sphereVertices = []
        self.sphereNormal = []
        self.sphereIndices = [0, 1, 2, 0, 2, 3, 0, 3, 4, 0, 4, 5, 0, 5, 1,
                              1, 2, 6, 2, 3, 7, 3, 4, 8, 4, 5, 9, 5, 1, 10,
                              1, 10, 6, 2, 6, 7, 3, 7, 8, 4, 8, 9, 5, 9, 10,
                              11, 6, 7, 11, 7, 8, 11, 8, 9, 11, 9, 10, 11, 10, 6]
        self.sphereColor = []
        self.sphereTexture = [S, 0, 0, T, 2*S, T, 3*S, 0, 2*S, T, 4*S, T, 5*S, 0, 4*S, T, 6*S, T, 7*S, 0, 6*S, T, 8*S, T, 9*S, 0, 8*S, T, 10*S, T,
                              0, T, 2*S, T, S, 2*T, 2*S, T, 4*S, T, 3*S, 2*T, 4*S, T, 6*S, T, 5*S, 2*T, 6*S, T, 8*S, T, 7*S, 2*T, 8*S, T, 10*S, T, 9*S, 2*T,
                              2*S, T, S, 2*T, 3*S, 2*T, 4*S, T, 3*S, 2*T, 5*S, 2*T, 6*S, T, 5*S, 2*T, 7*S, 2*T, 8*S, T, 7*S, 2*T, 9*S, 2*T, 10*S, T, 9*S, 2*T, 11*S, 2*T,
                              2*S, 3*T, S, 2*T, 3*S, 2*T, 4*S, 3*T, 3*S, 2*T, 5*S, 2*T, 6*S, 3*T, 5*S, 2*T, 7*S, 2*T, 8*S, 3*T, 7*S, 2*T, 9*S, 2*T, 10*S, 3*T, 9*S, 2*T, 11*S, 2*T]

        self.drawSphere(1)

        self.buildVerticesFlat(3, 1)

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

    def addVertex(self, x, y, z):
        self.sphereVertices.append(x)
        self.sphereVertices.append(y)
        self.sphereVertices.append(z)

    def addVertices(self, v1, v2, v3):
        self.sphereVertices.append(v1[0])
        self.sphereVertices.append(v1[1])
        self.sphereVertices.append(v1[2])
        self.sphereVertices.append(v2[0])
        self.sphereVertices.append(v2[1])
        self.sphereVertices.append(v2[2])
        self.sphereVertices.append(v3[0])
        self.sphereVertices.append(v3[1])
        self.sphereVertices.append(v3[2])

    def addIndices(self, i1, i2, i3):
        self.sphereIndices.append(i1)
        self.sphereIndices.append(i2)
        self.sphereIndices.append(i3)

    def addNormal(self, nx, ny, nz):
        self.sphereNormal.append(nx)
        self.sphereNormal.append(ny)
        self.sphereNormal.append(nz)

    def addTexCoords(self, t1, t2, t3):
        self.sphereTexture.append(t1[0])
        self.sphereTexture.append(t1[1])
        self.sphereTexture.append(t2[0])
        self.sphereTexture.append(t2[1])
        self.sphereTexture.append(t3[0])
        self.sphereTexture.append(t3[1])

    def computeHalfVertex(self, v1, v2, newV, radius):
        """
        find middle point of 2 vertices
        NOTE: new vertex must be resized, so the length is equal to the radius
        """
        newV[0] = v1[0] + v2[0]  # x
        newV[1] = v1[1] + v2[1]  # y
        newV[2] = v1[2] + v2[2]  # z
        scale = radius / np.sqrt(newV[0] ** 2 + newV[1] ** 2 + newV[2] ** 2)
        newV[0] *= scale
        newV[1] *= scale
        newV[2] *= scale

    def computeHalfTexCoord(self, t1, t2, newT):
        newT[0] = (t1[0] + t2[0]) * 0.5
        newT[1] = (t1[1] + t2[1]) * 0.5

    def drawSphere(self, radius):
        PI = 3.1415926
        H_ANGLE = PI / 180 * 72  # 72 degree = 360 / 5
        V_ANGLE = math.atan(1.0 / 2)  # elevation = 26.565 degree

        vertices = [0] * 36  # array of 12 vertices (x, y, z)
        i1, i2 = 0, 0  # indices
        z, xy = 0.0, 0.0  # coords
        hAngle1 = -PI / 2 - H_ANGLE / 2  # start from -126 deg at 1st row
        hAngle2 = -PI / 2  # start from -90 deg at 2nd row
        # self.sphereIndices.append(0)

        # the first top vertex at (0, 0, r)
        vertices[0] = 0
        vertices[1] = 0
        vertices[2] = radius

        # compute 10 vertices at 1st and 2nd rows
        for i in range(1, 6):
            i1 = i * 3  # index for 1st row
            i2 = (i + 5) * 3  # index for 2nd row
            # self.sphereIndices.append(i1)
            # self.sphereIndices.append(i2)

            z = radius * math.sin(V_ANGLE)  # elevation
            xy = radius * math.cos(V_ANGLE)  # length on XY plane

            vertices[i1] = xy * math.cos(hAngle1)  # x
            vertices[i2] = xy * math.cos(hAngle2)
            vertices[i1 + 1] = xy * math.sin(hAngle1)  # y
            vertices[i2 + 1] = xy * math.sin(hAngle2)
            vertices[i1 + 2] = z  # z
            vertices[i2 + 2] = -z

            # next horizontal angles
            hAngle1 += H_ANGLE
            hAngle2 += H_ANGLE

        # the last bottom vertex at (0, 0, -r)
        i1 = 11 * 3
        vertices[i1] = 0
        vertices[i1 + 1] = 0
        vertices[i1 + 2] = -radius
        # self.sphereIndices.append([x for x in range(0, len(self.sphereVertices))])
        # print(self.sphereIndices)
        self.sphereVertices = vertices

    def buildVerticesFlat(self, subdivision, radius):
        tmpVertices = []
        tmpIndices = []
        tmpTexture = []
        v1, v2, v3 = None, None, None  # ptr to original vertices of a triangle
        t1, t2, t3 = None, None, None
        newV1, newV2, newV3 = np.zeros(3), np.zeros(3), np.zeros(3)  # new vertex positions
        newT1, newT2, newT3 = np.zeros(2), np.zeros(2), np.zeros(2)
        index = 0

        # iterate all subdivision levels
        for i in range(1, subdivision + 1):
            # copy prev vertex/index arrays and clear
            tmpVertices = self.sphereVertices.copy()
            tmpIndices = self.sphereIndices.copy()
            tmpTexture = self.sphereTexture.copy()
            self.sphereVertices.clear()
            self.sphereIndices.clear()
            self.sphereTexture.clear()
            index = 0

            # perform subdivision for each triangle
            for j in range(0, len(tmpIndices), 3):
                # get 3 vertices of a triangle
                v1 = tmpVertices[tmpIndices[j] * 3:tmpIndices[j] * 3 + 3]
                v2 = tmpVertices[tmpIndices[j + 1] * 3:tmpIndices[j + 1] * 3 + 3]
                v3 = tmpVertices[tmpIndices[j + 2] * 3:tmpIndices[j + 2] * 3 + 3]

                t1 = tmpTexture[tmpIndices[j] * 2:tmpIndices[j] * 2 + 2]
                t2 = tmpTexture[tmpIndices[j + 1] * 2:tmpIndices[j + 1] * 2 + 2]
                t3 = tmpTexture[tmpIndices[j + 2] * 2:tmpIndices[j + 2] * 2 + 2]

                # compute 3 new vertices by spliting half on each edge
                #         v1
                #        / \
                # newV1 *---* newV3
                #      / \ / \
                #    v2---*---v3
                #       newV2
                TexSphere.computeHalfVertex(self, v1, v2, newV1, radius)
                TexSphere.computeHalfVertex(self, v2, v3, newV2, radius)
                TexSphere.computeHalfVertex(self, v1, v3, newV3, radius)

                TexSphere.computeHalfTexCoord(self, t1, t2, newT1)
                TexSphere.computeHalfTexCoord(self, t2, t3, newT2)
                TexSphere.computeHalfTexCoord(self, t1, t3, newT3)


                # add 4 new triangles to vertex array
                TexSphere.addVertices(self, v1, newV1, newV3)
                TexSphere.addVertices(self, newV1, v2, newV2)
                TexSphere.addVertices(self, newV1, newV2, newV3)
                TexSphere.addVertices(self, newV3, newV2, v3)

                # add indices of 4 new triangles
                TexSphere.addIndices(self, index, index + 1, index + 2)
                TexSphere.addIndices(self, index + 3, index + 4, index + 5)
                TexSphere.addIndices(self, index + 6, index + 7, index + 8)
                TexSphere.addIndices(self, index + 9, index + 10, index + 11)

                TexSphere.addTexCoords(self, t1, newT1, newT3)
                TexSphere.addTexCoords(self, newT1, t2, newT2)
                TexSphere.addTexCoords(self, newT1, newT2, newT3)
                TexSphere.addTexCoords(self, newT3, newT2, t3)
                index += 12  # next index
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
