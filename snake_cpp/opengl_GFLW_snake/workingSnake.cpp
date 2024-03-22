#include <GLFW/glfw3.h>
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#include <iostream>
#include <cstdlib>
#include <vector>
#include <chrono>
#include <random>

using namespace std;
using namespace std::chrono;

// Board size
const int width = 32;
const int height = 24;

// Snake and fruit positions
int x, y, fruitX, fruitY, score;
int tailX[100], tailY[100];
int nTail;

// FPS
auto lastFrameTime = high_resolution_clock::now();
double deltaTime = 0;
double fpsNew = 0;
double fps = 0;

// Directional movement
const int dx[] = {0, -1, 1, 0, 0};
const int dy[] = {0, 0, 0, -1, 1};
enum eDirection { STOP = 0, LEFT, RIGHT, UP, DOWN };
eDirection dir;
enum eDirection tailDirection[100];

bool gameOver;

float imageSize = 0.05f;

// Global variables for texture IDs
GLuint headTexture, bodyTexture, tailTexture, fruitTexture;

// Load and create a texture from file
GLuint loadTexture(const char* path) {
    int width, height, channels;
    unsigned char* data = stbi_load(path, &width, &height, &channels, 4); // Load with forced RGBA
    if (!data) {
        std::cerr << "Failed to load texture at " << path << std::endl;
        return 0;
    }

    GLuint texture;
    glGenTextures(1, &texture);
    glBindTexture(GL_TEXTURE_2D, texture);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data);
    stbi_image_free(data);

    return texture;
}

void Setup() {
    gameOver = false;
    dir = STOP;
    x = width / 2;
    y = height / 2;
    fruitX = rand() % (width - 2) + 1;
    fruitY = rand() % (height - 2) + 1;
    score = 0;
    nTail = 0;
}

void GameOver(GLFWwindow* window) {
    // Display game over message and prompt for restart or quit
    // ...
}

void Draw(GLFWwindow* window) {
    glClear(GL_COLOR_BUFFER_BIT);

    float cellWidth = 2.0f / width;
    float cellHeight = 2.0f / height;

    // Draw snake tail
    glEnable(GL_TEXTURE_2D);

    // Draw snake head
    glBindTexture(GL_TEXTURE_2D, headTexture);
    float headXPos = (float)x / width * 2 - 1 + cellWidth / 2;
    float headYPos = (float)y / height * 2 - 1 + cellHeight / 2;
    glBegin(GL_QUADS);

    // Head texture coordinates need to be adjusted based on the direction
    if (dir == LEFT) {
        glTexCoord2f(1, 0); glVertex2f(headXPos - cellWidth / 2, headYPos - cellHeight / 2);
        glTexCoord2f(1, 1); glVertex2f(headXPos + cellWidth / 2, headYPos - cellHeight / 2);
        glTexCoord2f(0, 1); glVertex2f(headXPos + cellWidth / 2, headYPos + cellHeight / 2);
        glTexCoord2f(0, 0); glVertex2f(headXPos - cellWidth / 2, headYPos + cellHeight / 2);
    } else if (dir == RIGHT) {
        glTexCoord2f(0, 1); glVertex2f(headXPos - cellWidth / 2, headYPos - cellHeight / 2);
        glTexCoord2f(0, 0); glVertex2f(headXPos + cellWidth / 2, headYPos - cellHeight / 2);
        glTexCoord2f(1, 0); glVertex2f(headXPos + cellWidth / 2, headYPos + cellHeight / 2);
        glTexCoord2f(1, 1); glVertex2f(headXPos - cellWidth / 2, headYPos + cellHeight / 2);
    } else if (dir == DOWN) {
        glTexCoord2f(0, 0); glVertex2f(headXPos - cellWidth / 2, headYPos - cellHeight / 2);
        glTexCoord2f(1, 0); glVertex2f(headXPos + cellWidth / 2, headYPos - cellHeight / 2);
        glTexCoord2f(1, 1); glVertex2f(headXPos + cellWidth / 2, headYPos + cellHeight / 2);
        glTexCoord2f(0, 1); glVertex2f(headXPos - cellWidth / 2, headYPos + cellHeight / 2);
    } else if (dir == UP) {
        glTexCoord2f(1, 1); glVertex2f(headXPos - cellWidth / 2, headYPos - cellHeight / 2);
        glTexCoord2f(0, 1); glVertex2f(headXPos + cellWidth / 2, headYPos - cellHeight / 2);
        glTexCoord2f(0, 0); glVertex2f(headXPos + cellWidth / 2, headYPos + cellHeight / 2);
        glTexCoord2f(1, 0); glVertex2f(headXPos - cellWidth / 2, headYPos + cellHeight / 2);
    } else {
        glTexCoord2f(0, 0); glVertex2f(headXPos - cellWidth / 2, headYPos - cellHeight / 2);
        glTexCoord2f(1, 0); glVertex2f(headXPos + cellWidth / 2, headYPos - cellHeight / 2);
        glTexCoord2f(1, 1); glVertex2f(headXPos + cellWidth / 2, headYPos + cellHeight / 2);
        glTexCoord2f(0, 1); glVertex2f(headXPos - cellWidth / 2, headYPos + cellHeight / 2);
    }
    glEnd();

    // Draw snake body
    glBindTexture(GL_TEXTURE_2D, bodyTexture);
    for (int i = 0; i < nTail; i++) {
        float bodyXPos = (float)tailX[i] / width * 2 - 1 + cellWidth / 2;
        float bodyYPos = (float)tailY[i] / height * 2 - 1 + cellHeight / 2;
        glBegin(GL_QUADS);
        switch (tailDirection[i]) {
            case LEFT:
                glTexCoord2f(1, 0); glVertex2f(bodyXPos - cellWidth / 2, bodyYPos - cellHeight / 2);
                glTexCoord2f(1, 1); glVertex2f(bodyXPos + cellWidth / 2, bodyYPos - cellHeight / 2);
                glTexCoord2f(0, 1); glVertex2f(bodyXPos + cellWidth / 2, bodyYPos + cellHeight / 2);
                glTexCoord2f(0, 0); glVertex2f(bodyXPos - cellWidth / 2, bodyYPos + cellHeight / 2);
                break;
            case RIGHT:
                glTexCoord2f(0, 1); glVertex2f(bodyXPos - cellWidth / 2, bodyYPos - cellHeight / 2);
                glTexCoord2f(0, 0); glVertex2f(bodyXPos + cellWidth / 2, bodyYPos - cellHeight / 2);
                glTexCoord2f(1, 0); glVertex2f(bodyXPos + cellWidth / 2, bodyYPos + cellHeight / 2);
                glTexCoord2f(1, 1); glVertex2f(bodyXPos - cellWidth / 2, bodyYPos + cellHeight / 2);
                break;
            case DOWN:
                glTexCoord2f(0, 0); glVertex2f(bodyXPos - cellWidth / 2, bodyYPos - cellHeight / 2);
                glTexCoord2f(1, 0); glVertex2f(bodyXPos + cellWidth / 2, bodyYPos - cellHeight / 2);
                glTexCoord2f(1, 1); glVertex2f(bodyXPos + cellWidth / 2, bodyYPos + cellHeight / 2);
                glTexCoord2f(0, 1); glVertex2f(bodyXPos - cellWidth / 2, bodyYPos + cellHeight / 2);
                break;
            case UP:
                glTexCoord2f(1, 1); glVertex2f(bodyXPos - cellWidth / 2, bodyYPos - cellHeight / 2);
                glTexCoord2f(0, 1); glVertex2f(bodyXPos + cellWidth / 2, bodyYPos - cellHeight / 2);
                glTexCoord2f(0, 0); glVertex2f(bodyXPos + cellWidth / 2, bodyYPos + cellHeight / 2);
                glTexCoord2f(1, 0); glVertex2f(bodyXPos - cellWidth / 2, bodyYPos + cellHeight / 2);
            }
        }
    glEnd();

    // Draw snake tail
    glBindTexture(GL_TEXTURE_2D, tailTexture);
    float tailXPos = (float)tailX[nTail - 1] / width * 2 - 1 + cellWidth / 2;
    float tailYPos = (float)tailY[nTail - 1] / height * 2 - 1 + cellHeight / 2;
    glBegin(GL_QUADS);
    switch (tailDirection[nTail - 1]) {
        case LEFT:
            glTexCoord2f(1, 0); glVertex2f(tailXPos - cellWidth / 2, tailYPos - cellHeight / 2);
            glTexCoord2f(1, 1); glVertex2f(tailXPos + cellWidth / 2, tailYPos - cellHeight / 2);
            glTexCoord2f(0, 1); glVertex2f(tailXPos + cellWidth / 2, tailYPos + cellHeight / 2);
            glTexCoord2f(0, 0); glVertex2f(tailXPos - cellWidth / 2, tailYPos + cellHeight / 2);
            break;
        case RIGHT:
            glTexCoord2f(0, 1); glVertex2f(tailXPos - cellWidth / 2, tailYPos - cellHeight / 2);
            glTexCoord2f(0, 0); glVertex2f(tailXPos + cellWidth / 2, tailYPos - cellHeight / 2);
            glTexCoord2f(1, 0); glVertex2f(tailXPos + cellWidth / 2, tailYPos + cellHeight / 2);
            glTexCoord2f(1, 1); glVertex2f(tailXPos - cellWidth / 2, tailYPos + cellHeight / 2);
            break;
        case DOWN:
            glTexCoord2f(0, 0); glVertex2f(tailXPos - cellWidth / 2, tailYPos - cellHeight / 2);
            glTexCoord2f(1, 0); glVertex2f(tailXPos + cellWidth / 2, tailYPos - cellHeight / 2);
            glTexCoord2f(1, 1); glVertex2f(tailXPos + cellWidth / 2, tailYPos + cellHeight / 2);
            glTexCoord2f(0, 1); glVertex2f(tailXPos - cellWidth / 2, tailYPos + cellHeight / 2);
            break;
        case UP:
            glTexCoord2f(1, 1); glVertex2f(tailXPos - cellWidth / 2, tailYPos - cellHeight / 2);
            glTexCoord2f(0, 1); glVertex2f(tailXPos + cellWidth / 2, tailYPos - cellHeight / 2);
            glTexCoord2f(0, 0); glVertex2f(tailXPos + cellWidth / 2, tailYPos + cellHeight / 2);
            glTexCoord2f(1, 0); glVertex2f(tailXPos - cellWidth / 2, tailYPos + cellHeight / 2);
        }
    glEnd();

    // Draw fruit
    glBindTexture(GL_TEXTURE_2D, fruitTexture);
    float fruitXPos = (float)fruitX / width * 2 - 1 + cellWidth / 2;
    float fruitYPos = (float)fruitY / height * 2 - 1 + cellHeight / 2;
    glBegin(GL_QUADS);
    glTexCoord2f(0, 1); glVertex2f(fruitXPos - cellWidth / 2, fruitYPos - cellHeight / 2);
    glTexCoord2f(1, 1); glVertex2f(fruitXPos + cellWidth / 2, fruitYPos - cellHeight / 2);
    glTexCoord2f(1, 0); glVertex2f(fruitXPos + cellWidth / 2, fruitYPos + cellHeight / 2);
    glTexCoord2f(0, 0); glVertex2f(fruitXPos - cellWidth / 2, fruitYPos + cellHeight / 2);
    glEnd();

    // Swap front and back buffers
    glfwSwapBuffers(window);
}

void Input(GLFWwindow* window) {
    if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS && dir != RIGHT)
        dir = LEFT;
    else if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS && dir != LEFT)
        dir = RIGHT;
    else if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS && dir != DOWN)
        dir = UP;
    else if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS && dir != UP)
        dir = DOWN;
}

void Logic(GLFWwindow* window) {
    std::random_device rd;
    std::mt19937 rng(rd());
    std::uniform_int_distribution<int> dist_width(1, width - 2);
    std::uniform_int_distribution<int> dist_height(1, height - 2);
    int prevX = tailX[0];
    int prevY = tailY[0];
    int prev2X, prev2Y;
    eDirection prevDir = tailDirection[0], prev2Dir;

    // Update the position and direction of the first tail segment to follow the head
    if (nTail > 0) {
        tailDirection[0] = dir;
        tailX[0] = x;
        tailY[0] = y;
    }

    // Update the position and direction of the rest of the tail segments
    for (int i = 1; i < nTail; i++) {
        prev2X = tailX[i];
        prev2Y = tailY[i];
        prev2Dir = tailDirection[i];

        tailX[i] = prevX;
        tailY[i] = prevY;
        tailDirection[i] = prevDir;

        prevX = prev2X;
        prevY = prev2Y;
        prevDir = prev2Dir;
    }

    // Move the head in the direction of the arrow key
    x += dx[dir];
    y += -dy[dir];

    // Check for wall collision
    if (x >= width || x < 0 || y >= height || y < 0)
        GameOver(window);

    // Check for collision with the tail
    for (int i = 0; i < nTail; i++) {
        if (tailX[i] == x && tailY[i] == y)
            GameOver(window);
    }

    // Check if snake has eaten the fruit
    if (x == fruitX && y == fruitY) {
        score += 10;
        fruitX = rand() % (width - 2) + 1;
        fruitY = rand() % (height - 2) + 1;

        // Grow the snake
        tailX[nTail] = prevX; // New segment takes the previous last position
        tailY[nTail] = prevY;
        tailDirection[nTail] = prevDir; // New segment takes the previous last direction
        nTail++;
    }
}

int main() {
    // Initialize GLFW
    if (!glfwInit()) {
        std::cerr << "Failed to initialize GLFW" << std::endl;
        return -1;
    }

    // Create a windowed mode window and its OpenGL context
    GLFWwindow* window = glfwCreateWindow(1024, 768, "Snake Game", nullptr, nullptr);
    if (!window) {
        std::cerr << "Failed to create GLFW window" << std::endl;
        glfwTerminate();
        return -1;
    }

    // Make the window's context current
    glfwMakeContextCurrent(window);

    // Load textures using the loadTexture function
    headTexture = loadTexture("./textures/head.png");
    bodyTexture = loadTexture("./textures/body.png");
    tailTexture = loadTexture("./textures/tail.png");
    fruitTexture = loadTexture("./textures/apple.png");

    // Check if any texture failed to load and handle the error
    if (!headTexture || !bodyTexture || !tailTexture || !fruitTexture) {
        std::cerr << "Error loading one or more textures." << std::endl;
        glfwTerminate();
        return -1;
    }

    // Set the clear color
    glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(-1, 1, -1, 1, -1, 1);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    // Set up the game

    Setup();
    auto lastMoveTime = steady_clock::now();
    double delay = 0.1;

    while (!glfwWindowShouldClose(window)) {
        auto currentTime = steady_clock::now();
        Draw(window);
        Input(window);

        if (duration<double>(currentTime - lastMoveTime).count() >= delay) {
            Logic(window);
            lastMoveTime = currentTime;
        }

        if (gameOver) {
            GameOver(window);
        }

        glfwPollEvents();
    }

    glfwTerminate();
    return 0;
}
