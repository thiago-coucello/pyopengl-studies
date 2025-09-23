#include <GL/glut.h>
#include <GL/glu.h>
#include <GL/gl.h>
#include <random>
#include <cstring>

#define GRID_SIZE 40
#define CELL_SIZE 2
#define GAME_SPEED 100 // Velocidade do jogo (menor é mais rápido)

typedef enum Direction { UP, DOWN, LEFT, RIGHT } Direction;

typedef struct Element {
    float x;
    float y;
    float velX;
    float velY;
    Direction dir;
    std::tuple<float, float, float> color; // RGB color
} Element;

std::vector<Element> snake;
Element food;
Element poison;

int score = 0;
bool gameOver = false;

void writeText(const char* text, float x, float y) {
    glRasterPos2f(x, y);
    for (const char* p = text; *p != '\0'; p++) {
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, *p);
    }
}

bool collided(Element item, Element snakeHead) {
    // Verifica se a cabeça da cobra colidiu com a comida
    if (item.x == snakeHead.x && item.y == snakeHead.y) {
        return true;
    }
    return false;
}

bool autoCollision(std::vector<Element> snake) {
    // Verifica se a cabeça da cobra colidiu com seu próprio corpo
    for (size_t i = 1; i < snake.size(); ++i) {
        if (snake[0].x == snake[i].x && snake[0].y == snake[i].y) {
            return true;
        }
    }
    return false;
}

void startSnake() {
    snake.clear();
    Element head = {0.0f, 0.0f, 0.0f, 0.0f, RIGHT, {0.0f, 1.0f, 0.0f}};
    snake.push_back(head);
    score = 0;
    gameOver = false;
}

std::pair<float, float> getRandomPosition() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(-GRID_SIZE / CELL_SIZE + 1, GRID_SIZE / CELL_SIZE - 1);
    float x = dis(gen) * CELL_SIZE;
    float y = dis(gen) * CELL_SIZE;
    return {x, y};
}

void createFood() {
    std::tie(food.x, food.y) = getRandomPosition();
    food.color = {1.0f, 0.0f, 0.0f}; // Cor vermelha para a comida
}

void createPoison() {
    std::tie(poison.x, poison.y) = getRandomPosition();
    poison.color = {0.0f, 1.0f, 1.0f}; // Cor azul para o veneno
}

void drawGrid() {
    glColor3f(0.5f, 0.5f, 0.5f); // Cor cinza para a grade

    glBegin(GL_LINES);
        // Linhas verticais
        for (int x = -GRID_SIZE + CELL_SIZE / 2; x <= GRID_SIZE; x += CELL_SIZE) {
            glVertex2f(x, -GRID_SIZE);
            glVertex2f(x, GRID_SIZE);
        }
        // Linhas horizontais
        for (int y = -GRID_SIZE + CELL_SIZE / 2; y <= GRID_SIZE; y += CELL_SIZE) {
            glVertex2f(-GRID_SIZE, y);
            glVertex2f(GRID_SIZE, y);
        }
    glEnd();
}

void drawPoison(Element poison) {
    float r, g, b;
    glPushMatrix();
        std::tie(r, g, b) = poison.color;
        glColor3f(r, g, b); // Cor do veneno
        glBegin(GL_QUADS);
            /*
            glVertex2f(poison.x - CELL_SIZE / 2.0f, poison.y - CELL_SIZE / 2.0f);
            glVertex2f(poison.x + CELL_SIZE / 2.0f, poison.y - CELL_SIZE / 2.0f);
            glVertex2f(poison.x + CELL_SIZE / 2.0f, poison.y + CELL_SIZE / 2.0f);
            glVertex2f(poison.x - CELL_SIZE / 2.0f, poison.y + CELL_SIZE / 2.0f);
            */
            glVertex2f(poison.x, poison.y + CELL_SIZE / 2.0f);           // Topo
            glVertex2f(poison.x + CELL_SIZE / 2.0f, poison.y);           // Direita
            glVertex2f(poison.x, poison.y - CELL_SIZE / 2.0f);           // Base
            glVertex2f(poison.x - CELL_SIZE / 2.0f, poison.y);           // Esquerda
        glEnd();
    glPopMatrix();
}

void drawFood(Element food) {
    float r, g, b;
    glPushMatrix();
        std::tie(r, g, b) = food.color;
        glColor3f(r, g, b); // Cor da comida
        glBegin(GL_QUADS);
            glVertex2f(food.x - CELL_SIZE / 2.0f, food.y - CELL_SIZE / 2.0f);
            glVertex2f(food.x + CELL_SIZE / 2.0f, food.y - CELL_SIZE / 2.0f);
            glVertex2f(food.x + CELL_SIZE / 2.0f, food.y + CELL_SIZE / 2.0f);
            glVertex2f(food.x - CELL_SIZE / 2.0f, food.y + CELL_SIZE / 2.0f);
        glEnd();
    glPopMatrix();
}

void drawSnake(std::vector<Element> snake) {
    float r, g, b;
    glPushMatrix();
        std::tie(r, g, b) = snake[0].color;
        glColor3f(r, g, b); // Cor da cobra
        glBegin(GL_QUADS);
            for (const auto& segment : snake) {
                glVertex2f(segment.x - CELL_SIZE / 2.0f, segment.y - CELL_SIZE / 2.0f);
                glVertex2f(segment.x + CELL_SIZE / 2.0f, segment.y - CELL_SIZE / 2.0f);
                glVertex2f(segment.x + CELL_SIZE / 2.0f, segment.y + CELL_SIZE / 2.0f);
                glVertex2f(segment.x - CELL_SIZE / 2.0f, segment.y + CELL_SIZE / 2.0f);
            }
        glEnd();
    glPopMatrix();
}

void updateSnakeBody() {
    // Atualiza a posição da cobra com base na direção
    if (snake.size() > 1) {
        for (size_t i = snake.size() - 1; i > 0; --i) {
            snake[i] = snake[i - 1];
        }
    }
    switch (snake[0].dir) {
        case UP:
            snake[0].y += CELL_SIZE;
            break;
        case DOWN:
            snake[0].y -= CELL_SIZE;
            break;
        case LEFT:
            snake[0].x -= CELL_SIZE;
            break;
        case RIGHT:
            snake[0].x += CELL_SIZE;
            break;
    }
}

void display() {
    glClear(GL_COLOR_BUFFER_BIT); // Limpa o buffer de cor
    
    drawGrid(); // Desenha a grade
    
    glColor3f(1.0f, 1.0f, 1.0f); // Cor branca para o texto
    
    std::string scoreText = "Score: " + std::to_string(score);
    writeText(scoreText.c_str(), -GRID_SIZE + 1, GRID_SIZE - 2);
    if (gameOver) {
        glColor3f(1.0f, 0.0f, 0.0f); // Cor vermelha para o texto de game over
        char gameOverText[100];
        sprintf(gameOverText, "Game Over! Your Score: %d", score);
        std::string restartText = "Press R to Restart";
        writeText(gameOverText, -(strlen(gameOverText) / 2.0f), 0.0f);
        writeText(restartText.c_str(), -(restartText.length() / 2.0f), -2.0f);
    }
    
    drawSnake(snake); // Desenha a cobra
    drawFood(food); // Desenha a comida
    drawPoison(poison); // Desenha o veneno
    glFlush();  // Atualiza a tela
}

void animate(int value) {
    // Atualiza a posição da cobra inteira
    Element snakeTail = snake.back();
    updateSnakeBody();

    if (collided(food, snake[0])) {
        score += 1;
        snake.push_back(snakeTail); // Adiciona novo segmento na posição do último segmento
        createFood();
    }

    if (collided(poison, snake[0])) {
        score -= 1;
        if (snake.size() > 1) {
            snake.pop_back();
        } else {
            gameOver = true;
        }
        createPoison();
    } else {
        static std::mt19937 gen(std::random_device{}());
        std::uniform_real_distribution<float> dist(0.0f, 1.0f);
        if (dist(gen) < 0.005f) {
            createPoison();
        }
    }

    if (autoCollision(snake) || 
        snake[0].x + CELL_SIZE / 2.0f > GRID_SIZE || snake[0].x - CELL_SIZE / 2.0f < -GRID_SIZE || 
        snake[0].y + CELL_SIZE / 2.0f > GRID_SIZE || snake[0].y - CELL_SIZE / 2.0f < -GRID_SIZE) {
        gameOver = true;
    } else if (!gameOver){
        int minSpeed = 20; // Valor mínimo para não acelerar demais
        int nextSpeed = std::max(GAME_SPEED - (value * 0.01f), (float)minSpeed);
        glutTimerFunc(nextSpeed, animate, value + 1);
    }

    glutPostRedisplay(); // Solicita uma nova exibição
}

void keyboard(unsigned char key, int x, int y) {
    switch (key) {
        case 27:
            exit(0);
            break;
        case 'r':
            if (gameOver) {
                // Reinicia o jogo
                startSnake();
                createFood();
                gameOver = false;
                glutTimerFunc(0, animate, 0); // Reinicia a animação
            }
            break;
        case 'w':
            if (!gameOver && snake[0].dir != DOWN)
                snake[0].dir = UP;
            break;
        case 's':
            if (!gameOver && snake[0].dir != UP)
                snake[0].dir = DOWN;
            break;
        case 'a':
            if (!gameOver && snake[0].dir != RIGHT)
                snake[0].dir = LEFT;
            break;
        case 'd':
            if (!gameOver && snake[0].dir != LEFT)
                snake[0].dir = RIGHT;
            break;
    }
    glutPostRedisplay(); // Atualiza a tela após mover a barra
}

void special(int key, int x, int y) {
    switch (key) {
        case GLUT_KEY_UP:
            if (!gameOver && snake[0].dir != DOWN)
                snake[0].dir = UP;
            break;
        case GLUT_KEY_DOWN:
            if (!gameOver && snake[0].dir != UP)
                snake[0].dir = DOWN;
            break;
        case GLUT_KEY_LEFT:
            if (!gameOver && snake[0].dir != RIGHT)
                snake[0].dir = LEFT;
            break;
        case GLUT_KEY_RIGHT:
            if (!gameOver && snake[0].dir != LEFT)
                snake[0].dir = RIGHT;
            break;
    }
    glutPostRedisplay(); // Atualiza a tela após mover a barra
}

void initWindow() {
    glClearColor(0.0f, 0.0f, 0.0f, 1.0f); // Cor de fundo preta
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(-GRID_SIZE, GRID_SIZE, -GRID_SIZE, GRID_SIZE); // Define a projeção ortográfica
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
}

int main(int argc, char **argv)
{
    startSnake();
    createFood();
    createPoison();

    glutInit(&argc, argv); // Inicializa o GLUT
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB); // Define o modo de exibição
    glutInitWindowSize(800, 800); // Define o tamanho da janela
    glutCreateWindow("Snake Game"); // Cria uma janela
    
    initWindow(); // Inicializa as configurações da janela
    
    glutDisplayFunc(display); // Registra a função de exibição
    glutKeyboardFunc(keyboard); // Registra a função de teclado
    glutSpecialFunc(special);

    glutTimerFunc(0, animate, 0); // Inicia a animação
    glutMainLoop(); // Inicia o loop principal do GLUT
    return 0;
}
