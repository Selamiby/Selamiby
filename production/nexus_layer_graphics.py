import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

# Define shader program for 3D rendering
def create_shader_program():
    vertex_shader = compileShader("""
        # version 330 core
        layout (location = 0) in vec3 aPos;
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;
        void main()
        {
            gl_Position = projection * view * model * vec4(aPos, 1.0);
        }
    """, GL_VERTEX_SHADER)

    fragment_shader = compileShader("""
        # version 330 core
        out vec4 FragColor;
        uniform vec3 objectColor;
        void main()
        {
            FragColor = vec4(objectColor, 1.0);
        }
    """, GL_FRAGMENT_SHADER)

    shader_program = compileProgram(vertex_shader, fragment_shader)
    return shader_program

# Define function to render 3D objects
def render_object(shader_program, object_vertices, object_color, model_matrix, view_matrix, projection_matrix):
    # Create VAO and VBO
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)

    # Bind VAO and VBO
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    # Fill VBO with vertex data
    glBufferData(GL_ARRAY_BUFFER, np.array(object_vertices, dtype=np.float32), GL_STATIC_DRAW)

    # Specify vertex attributes
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * np.float32.itemsize, None)
    glEnableVertexAttribArray(0)

    # Use shader program
    glUseProgram(shader_program)

    # Set uniform variables
    glUniformMatrix4fv(glGetUniformLocation(shader_program, "model"), 1, GL_FALSE, model_matrix)
    glUniformMatrix4fv(glGetUniformLocation(shader_program, "view"), 1, GL_FALSE, view_matrix)
    glUniformMatrix4fv(glGetUniformLocation(shader_program, "projection"), 1, GL_FALSE, projection_matrix)
    glUniform3fv(glGetUniformLocation(shader_program, "objectColor"), 1, object_color)

    # Draw object
    glDrawArrays(GL_TRIANGLES, 0, len(object_vertices))

    # Unbind VAO and VBO
    glBindVertexArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

# Define example usage
if __name__ == "__main__":
    import pygame
    from pygame.locals import *

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    shader_program = create_shader_program()

    object_vertices = [
        -0.5, -0.5, 0.0,
         0.5, -0.5, 0.0,
         0.0,  0.5, 0.0
    ]

    object_color = [1.0, 0.0, 0.0]

    model_matrix = [
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0
    ]

    view_matrix = [
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0
    ]

    projection_matrix = [
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        render_object(shader_program, object_vertices, object_color, model_matrix, view_matrix, projection_matrix)
        pygame.display.flip()
        pygame.time.wait(10)