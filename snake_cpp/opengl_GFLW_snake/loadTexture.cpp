#include <GLFW/glfw3.h>
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#include <iostream>

float imageSize = 0.2f;
float imageSizeBuffer = 0.0f;

int main() {
    // Initialize GLFW
    if (!glfwInit()) {
        std::cerr << "Failed to initialize GLFW" << std::endl;
        return -1;
    }

    // Create a windowed mode window and its OpenGL context
    GLFWwindow* window = glfwCreateWindow(1024, 768, "Texture Display", nullptr, nullptr);
    if (!window) {
        std::cerr << "Failed to create GLFW window" << std::endl;
        glfwTerminate();
        return -1;
    }

    // Make the window's context current
    glfwMakeContextCurrent(window);

    // Load the head texture
    int headWidth, headHeight, headChannels;
    unsigned char* headData = stbi_load("textures/head.png", &headWidth, &headHeight, &headChannels, 4);
    if (!headData) {
        std::cerr << "Failed to load head texture" << std::endl;
        glfwTerminate();
        return -1;
    }

    // Load the body texture
    int bodyWidth, bodyHeight, bodyChannels;
    unsigned char* bodyData = stbi_load("textures/body.png", &bodyWidth, &bodyHeight, &bodyChannels, 4);
    if (!bodyData) {
        std::cerr << "Failed to load body texture" << std::endl;
        stbi_image_free(headData);
        glfwTerminate();
        return -1;
    }

    // Load the tail texture
    int tailWidth, tailHeight, tailChannels;
    unsigned char* tailData = stbi_load("textures/tail.png", &tailWidth, &tailHeight, &tailChannels, 4);
    if (!tailData) {
        std::cerr << "Failed to load tail texture" << std::endl;
        stbi_image_free(headData);
        stbi_image_free(bodyData);
        glfwTerminate();
        return -1;
    }

    // Generate head texture
    GLuint headTexture;
    glGenTextures(1, &headTexture);
    glBindTexture(GL_TEXTURE_2D, headTexture);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, headWidth, headHeight, 0, GL_RGBA, GL_UNSIGNED_BYTE, headData);
    stbi_image_free(headData);

    // Generate body texture
    GLuint bodyTexture;
    glGenTextures(1, &bodyTexture);
    glBindTexture(GL_TEXTURE_2D, bodyTexture);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, bodyWidth, bodyHeight, 0, GL_RGBA, GL_UNSIGNED_BYTE, bodyData);
    stbi_image_free(bodyData);

    // Generate tail texture
    GLuint tailTexture;
    glGenTextures(1, &tailTexture);
    glBindTexture(GL_TEXTURE_2D, tailTexture);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, tailWidth, tailHeight, 0, GL_RGBA, GL_UNSIGNED_BYTE, tailData);
    stbi_image_free(tailData);

    // Set the desired size for the displayed images
    float imageSize = 0.2f;

    // Loop until the user closes the window
    while (!glfwWindowShouldClose(window)) {
        // Render here
        glClear(GL_COLOR_BUFFER_BIT);

        // Draw tail texture
        glEnable(GL_TEXTURE_2D);
        glBindTexture(GL_TEXTURE_2D, tailTexture);
        glBegin(GL_QUADS);
            glTexCoord2f(0, 0); glVertex2f(-imageSize, 3 * imageSize);
            glTexCoord2f(1, 0); glVertex2f(imageSize, 3 * imageSize);
            glTexCoord2f(1, 1); glVertex2f(imageSize, 5 * imageSize);
            glTexCoord2f(0, 1); glVertex2f(-imageSize, 5 * imageSize);
        glEnd();

        // Draw body texture
        glEnable(GL_TEXTURE_2D);
        glBindTexture(GL_TEXTURE_2D, bodyTexture);
        glBegin(GL_QUADS);
            glTexCoord2f(0, 0); glVertex2f(-imageSize, imageSize - imageSizeBuffer);
            glTexCoord2f(1, 0); glVertex2f(imageSize, imageSize - imageSizeBuffer);
            glTexCoord2f(1, 1); glVertex2f(imageSize, 3 * imageSize);
            glTexCoord2f(0, 1); glVertex2f(-imageSize, 3 * imageSize);
        glEnd();

        // Draw head texture
        glBindTexture(GL_TEXTURE_2D, headTexture);
        glBegin(GL_QUADS);
            glTexCoord2f(0, 0); glVertex2f(-imageSize, -imageSize - imageSizeBuffer);
            glTexCoord2f(1, 0.); glVertex2f(imageSize, -imageSize - imageSizeBuffer);
            glTexCoord2f(1, 1); glVertex2f(imageSize, imageSize + imageSizeBuffer);
            glTexCoord2f(0, 1); glVertex2f(-imageSize, imageSize + imageSizeBuffer);
        glEnd();

        // Swap front and back buffers
        glfwSwapBuffers(window);

        // Poll for and process events
        glfwPollEvents();
    }

    glfwTerminate();
    return 0;
}
