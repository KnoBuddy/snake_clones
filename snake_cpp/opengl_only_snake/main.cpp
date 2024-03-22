// Use createWindow.h to create a window and set up OpenGL
#include "createWindow.h"

// The message structure
MSG msg;

// Use the following to create a window and set up OpenGL
int main() {
    // Create a window
    if (!CreateGLWindow("OpenGL Window", 640, 480, 16)) {
        return 1;
    }

    // Set up OpenGL

    // Main loop
    while (1) {
        // Handle messages
        if (PeekMessage(&msg, NULL, 0, 0, PM_REMOVE)) {
            if (msg.message == WM_QUIT) {
                break;
            }
            TranslateMessage(&msg);
            DispatchMessage(&msg);
        } else {
            // Draw
        }
    }

    // Clean up
    KillGLWindow();
    return 0;
}