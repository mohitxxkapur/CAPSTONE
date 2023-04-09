#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <pigpio.h>
#define PORT 12345
#define BUFFER_SIZE 1024

#define ACTUATOR_UP_PIN 22 // GPIO pin to control the up movement of actuators
#define ACTUATOR_DOWN_PIN 27 // GPIO pin to control the down movement of actuators
#define BUTTON_UP_PIN 23
#define BUTTON_DN_PIN 24
#define MODE_PIN 16
int main(int argc, char const *argv[]) {
    int server_fd, new_socket, valread;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char buffer[BUFFER_SIZE] = {0};
    char *move_up = "move system up";
    char *move_down = "move system down";
    char *stay = "stay";
    gpioInitialise();

    // Create socket file descriptor
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    // Set socket options
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {
        perror("setsockopt failed");
        exit(EXIT_FAILURE);
    }

    // Set server address
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    // Bind socket to address
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    // Listen for incoming connections
    if (listen(server_fd, 3) < 0) {
        perror("listen failed");
        exit(EXIT_FAILURE);
    }

    // Accept incoming connection
    if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
        perror("accept failed");
        exit(EXIT_FAILURE);
    }

    // Receive data from client
    while ((valread = read(new_socket, buffer, BUFFER_SIZE)) > 0) {
    printf("MODE: %d\n",gpioRead(MODE_PIN));
    printf("UP: %d\n",gpioRead(BUTTON_UP_PIN));
    printf("DN: %d\n",gpioRead(BUTTON_DN_PIN));
    if(gpioRead(MODE_PIN) == 0)
        {
        
        if (strcmp(buffer, move_up) == 0) {
            printf("Move system up\n");
            gpioWrite(ACTUATOR_DOWN_PIN, 1);
            gpioWrite(ACTUATOR_UP_PIN, 0);
            // Send signal to RPi
        } else if (strcmp(buffer, move_down) == 0) {
            printf("Move system down\n");
            gpioWrite(ACTUATOR_DOWN_PIN, 0);
            gpioWrite(ACTUATOR_UP_PIN, 1);
            // Send signal to RPi
        } else if (strcmp(buffer, stay) == 0) {
            printf("Stay\n");
            gpioWrite(ACTUATOR_DOWN_PIN, 1);
            gpioWrite(ACTUATOR_UP_PIN, 1);
            // Send signal to RPi
        }
    } else
    {
        if(gpioRead(BUTTON_UP_PIN) == 0)
        {
            gpioWrite(ACTUATOR_DOWN_PIN, 1);
            gpioWrite(ACTUATOR_UP_PIN, 0);
        }
        else if(gpioRead(BUTTON_DN_PIN) == 0)
        {
            gpioWrite(ACTUATOR_DOWN_PIN, 0);
            gpioWrite(ACTUATOR_UP_PIN, 1);
        }else
        {
            gpioWrite(ACTUATOR_DOWN_PIN, 1);
            gpioWrite(ACTUATOR_UP_PIN, 1);
        }
    }
        memset(buffer, 0, BUFFER_SIZE);
    }

    if (valread == 0) {
        printf("Client disconnected\n");
    } else {
        perror("read failed");
    }

    return 0;
}


