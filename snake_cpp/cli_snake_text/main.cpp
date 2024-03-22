#include <iostream>
#include <cstdlib>
#include <conio.h>
#include <windows.h>
#include <vector>
#include <chrono>
#include <regex>
#include <array>
#include <random>

using namespace std;
using namespace std::chrono;

// Board size
const int width = 40;  
const int height = 20; 

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

bool gameOver;

void Setup() {
    gameOver = false;
    dir = STOP;
    x = width / 2;
    y = height / 2;
    fruitX = rand() % (width - 2) + 1;  // Ensure fruit spawns away from the walls
    fruitY = rand() % (height - 2) + 1; // Ensure fruit spawns away from the walls
    score = 0;
    nTail = 0;
    system("cls");
}

void GameOver() {
    system("cls");
    cout << "Game Over!" << endl;
    cout << "Score: " << score << endl;
    cout << "Press 'c' to continue or 'q' to quit." << endl;

    while (true) {
        if (_kbhit()) {
            char ch = _getch();
            if (ch == 'c') {
                Setup();  // Reset the game
                break;
            } else if (ch == 'q') {
                gameOver = true;
                break;
            }
        }
    }
}

void gotoxy(int x, int y) {
    COORD coord;
    coord.X = x;
    coord.Y = y;
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), coord);
}

void Draw() {
    vector<string> buffer(height + 2, string(width + 2, ' '));

    // Calculate FPS
    auto currentTime = high_resolution_clock::now();
    deltaTime = duration_cast<duration<double>>(currentTime - lastFrameTime).count();
    if (deltaTime > 0) {
        fpsNew = 1 / deltaTime;
    }
    lastFrameTime = currentTime;

    // Draw borders
    for (int i = 0; i < width + 2; i++) {
        buffer[0][i] = '#';
        buffer[height + 1][i] = '#';
    }
    for (int i = 0; i < height; i++) {
        buffer[i + 1][0] = '#';
        buffer[i + 1][width + 1] = '#';
    }

    // Draw snake, fruit, and tail
    buffer[y + 1][x + 1] = 'O';  // Snake head
    buffer[fruitY + 1][fruitX + 1] = 'F';  // Fruit
    for (int i = 0; i < nTail; i++) {
        buffer[tailY[i] + 1][tailX[i] + 1] = 'o';  // Snake tail
    }

    // Convert buffer to string for output
    string output;
    for (const auto& line : buffer) {
        output += line + "\n";
    }

    // Add color codes for snake and fruit
    output = regex_replace(output, regex("O"), "\033[32mO\033[0m");  // Green snake head
    output = regex_replace(output, regex("o"), "\033[32mo\033[0m");  // Green snake tail
    output = regex_replace(output, regex("F"), "\033[31mF\033[0m");  // Red fruit

    // Update fps only if it has been 333ms since the last fps update. This is to prevent flickering
    // Create a new counter to keep track of the time since the last fps update
    static auto lastFpsUpdateTime = high_resolution_clock::now();
    auto currentTimeFps = high_resolution_clock::now();
    double deltaTimeFps = duration_cast<duration<double>>(currentTimeFps - lastFpsUpdateTime).count();
    if (deltaTimeFps > 0.333) {
        fps = fpsNew;
        lastFpsUpdateTime = currentTimeFps;
    }

    // else, just output the previous fps
    output += "Score: " + to_string(score) + " " + "FPS: " + to_string(fps) + "\n";

    // Position cursor at top-left and draw from buffer
    gotoxy(0, 0);

    cout << output;

}

void Input() {
    if (_kbhit()) {
        char key = _getch();
        switch (key) {
        case 'a':
            if (dir != RIGHT) dir = LEFT;
            break;
        case 'd':
            if (dir != LEFT) dir = RIGHT;
            break;
        case 'w':
            if (dir != DOWN) dir = UP;
            break;
        case 's':
            if (dir != UP) dir = DOWN;
            break;
        case 'x':
            exit(0);
            break;
        }
    }
}

void Logic() {
    std::random_device rd;
    std::mt19937 rng(rd());
    std::uniform_int_distribution<int> dist_width(1, width - 2);
    std::uniform_int_distribution<int> dist_height(1, height - 2);
    int prevX = tailX[0];
    int prevY = tailY[0];
    int prev2X, prev2Y;
    tailX[0] = x;
    tailY[0] = y;
    for (int i = 1; i < nTail; i++) {
        prev2X = tailX[i];
        prev2Y = tailY[i];
        tailX[i] = prevX;
        tailY[i] = prevY;
        prevX = prev2X;
        prevY = prev2Y;
    }

    // Move the head in the direction of the arrow key
    x += dx[dir];
    y += dy[dir];

    // Check for wall collision
    if (x >= width || x < 0 || y >= height || y < 0)
        GameOver();

    for (int i = 0; i < nTail; i++)
        if (tailX[i] == x && tailY[i] == y)
            GameOver();

    if (x == fruitX && y == fruitY) {
        score += 10;
        fruitX = dist_width(rng);
        fruitY = dist_height(rng);
        nTail++;
    }
}

int main() {
    Setup();
    auto lastMoveXTime = steady_clock::now();
    auto lastMoveYTime = steady_clock::now();
    double delayX = 0.1;  // Delay for horizontal and vertical movement
    double delayY = delayX * 1.5;  // Terminal characters are taller than they are wide

    while (!gameOver) {
        auto currentTime = steady_clock::now();
        Draw();
        Input();

        // Move the snake every delayX seconds
        if (dir == LEFT || dir == RIGHT) {
            if (duration<double>(currentTime - lastMoveXTime).count() >= delayX) {
                Logic();
                lastMoveXTime = currentTime;
            }
        }
        if (dir == UP || dir == DOWN) {
            if (duration<double>(currentTime - lastMoveYTime).count() >= delayY) {
                Logic();
                lastMoveYTime = currentTime;
            }
        }

        if (gameOver) {
            GameOver();
        }
    }
    return 0;
}