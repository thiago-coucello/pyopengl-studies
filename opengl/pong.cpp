#include <GL/glut.h>
#include <GL/glu.h>
#include <GL/gl.h>
#include <random>
#include <cstring>

#define GRID_SIZE 40
#define CELL_SIZE 2
#define BAR_HEIGHT 16
#define BAR_WIDTH 3
#define BALL_SIZE 2

typedef struct Element {
    float x;
    float y;
    float velX;
    float velY;
} Element;

Element ball = {0.0f, 0.0f, 0.3f, 0.25f};
Element bar1 = {-GRID_SIZE + BAR_WIDTH, 0.0f, 0.0f, 0.0f};
Element bar2 = {GRID_SIZE - BAR_WIDTH, 0.0f, 0.0f, 0.3f};
bool gameOver = false;
bool won = false;

void writeText(const char* text, float x, float y) {
    glRasterPos2f(x, y);
    for (const char* p = text; *p != '\0'; p++) {
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, *p);
    }
}

bool collided(Element ball, Element bar) {
    // Verifica se a bola colidiu com a barra
    if (ball.x + BALL_SIZE / 2.0f >= bar.x - BAR_WIDTH / 2.0f &&
        ball.x - BALL_SIZE / 2.0f <= bar.x + BAR_WIDTH / 2.0f &&
        ball.y + BALL_SIZE / 2.0f >= bar.y - BAR_HEIGHT / 2.0f &&
        ball.y - BALL_SIZE / 2.0f <= bar.y + BAR_HEIGHT / 2.0f) {
        return true;
    }
    return false;
}

void drawGrid() {
    glColor3f(0.5f, 0.5f, 0.5f); // Cor cinza para a grade

    glBegin(GL_LINES);
    // Linhas verticais
    for (int x = -GRID_SIZE; x <= GRID_SIZE; x += CELL_SIZE) {
        glVertex2f(x, -GRID_SIZE);
        glVertex2f(x, GRID_SIZE);
    }
    // Linhas horizontais
    for (int y = -GRID_SIZE; y <= GRID_SIZE; y += CELL_SIZE) {
        glVertex2f(-GRID_SIZE, y);
        glVertex2f(GRID_SIZE, y);
    }
    glEnd();
}

void drawBall(Element element) {
    glPushMatrix();
        glColor3f(1.0f, 1.0f, 1.0f); // Cor branca para a bola
        glBegin(GL_QUADS);
            glVertex2f(element.x - BALL_SIZE / 2.0f, element.y - BALL_SIZE / 2.0f);
            glVertex2f(element.x + BALL_SIZE / 2.0f, element.y - BALL_SIZE / 2.0f);
            glVertex2f(element.x + BALL_SIZE / 2.0f, element.y + BALL_SIZE / 2.0f);
            glVertex2f(element.x - BALL_SIZE / 2.0f, element.y + BALL_SIZE / 2.0f);
        glEnd();
    glPopMatrix();
}

void drawBar(Element element) {
    glPushMatrix();
        glColor3f(1.0f, 1.0f, 1.0f); // Cor branca para a barra
        glBegin(GL_QUADS);
            glVertex2f(element.x - BAR_WIDTH / 2.0f, element.y - BAR_HEIGHT / 2.0f);
            glVertex2f(element.x + BAR_WIDTH / 2.0f, element.y - BAR_HEIGHT / 2.0f);
            glVertex2f(element.x + BAR_WIDTH / 2.0f, element.y + BAR_HEIGHT / 2.0f);
            glVertex2f(element.x - BAR_WIDTH / 2.0f, element.y + BAR_HEIGHT / 2.0f);
        glEnd();
    glPopMatrix();
}

void display() {
    glClear(GL_COLOR_BUFFER_BIT); // Limpa o buffer de cor
    //drawGrid(); // Desenha a grade
    if (gameOver) {
        char gameOverText[100];
        sprintf(gameOverText, "Game Over! You %s!", won ? "Won!" : "Lost!");
        std::string restartText = "Press R to Restart";
        writeText(gameOverText, -(strlen(gameOverText) / 2.0f), 0.0f);
        writeText(restartText.c_str(), -(restartText.length() / 2.0f), -2.0f);
    }
    
     // --- IGNORE ---

    drawBall(ball); // Desenha a bola
    drawBar(bar1);
    drawBar(bar2);
    glFlush();  // Atualiza a tela
}

void animate(int value) {
    // Atualiza a posição da bola
    // Fator de aceleração baseado no tempo (value)
    float acceleration = 1.0f + value * 0.0005f; // Ajuste o fator conforme necessário
    ball.x += ball.velX * acceleration;
    ball.y += ball.velY * acceleration;
    // Aumenta a velocidade da barra 2 com o tempo, mas limita para não ficar impossível
    bar2.velY = std::min(0.5f + acceleration / 5.0f, 2.5f); // Limite máximo ajustável
    float theta = (rand() % 100) / 1000.0f - 0.05f;

    // Verifica se a bola passou de alguma das barras
    if (ball.x + BALL_SIZE / 2.0f > bar2.x + BAR_WIDTH / 2.0f || ball.x - BALL_SIZE / 2.0f < bar1.x - BAR_WIDTH / 2.0f) {
        gameOver = true;
        won = ball.x + BALL_SIZE / 2.0f > bar2.x + BAR_WIDTH / 2.0f;
    } else {
        glutTimerFunc(16, animate, value + 1); // Chama novamente após ~16ms (aproximadamente 60 FPS)
    }
    
    // Verifica colisão com os tetos
    if (ball.y + BALL_SIZE / 2.0f >= GRID_SIZE || ball.y - BALL_SIZE / 2.0f <= -GRID_SIZE) {
        ball.y = ball.y + BALL_SIZE / 2.0f >= GRID_SIZE ? GRID_SIZE - BALL_SIZE / 2.0f : -GRID_SIZE + BALL_SIZE / 2.0f;
        ball.velY = -ball.velY; // Inverte a direção vertical
    }


    // Verifica colisão com as barras
    if (collided(ball, bar1) || collided(ball, bar2)) {
        ball.velY += theta;
        ball.velX = -ball.velX;
    }

    // Trata da movimentação automática da barra 2 (inimigo)
    if (ball.velX > 0) { // Só move se a bola estiver vindo em sua direção
        if (bar2.y + BAR_HEIGHT / 2.0f < ball.y && bar2.y + BAR_HEIGHT / 2.0f < GRID_SIZE) {
            bar2.y += bar2.velY;
        } else if (bar2.y - BAR_HEIGHT / 2.0f > ball.y && bar2.y - BAR_HEIGHT / 2.0f > -GRID_SIZE) {
            bar2.y -= bar2.velY;
        }   
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
                ball = {0.0f, 0.0f, 0.3f, 0.25f};
                bar1 = {-GRID_SIZE + BAR_WIDTH, 0.0f, 0.0f, 0.0f};
                bar2 = {GRID_SIZE - BAR_WIDTH, 0.0f, 0.0f, 0.3f};
                gameOver = false;
                won = false;
                glutTimerFunc(0, animate, 0); // Reinicia a animação
            }
        case 'w':
            if (bar1.y + BAR_HEIGHT / 2.0f < GRID_SIZE && !gameOver)
                bar1.y += CELL_SIZE;
            break;
        case 's':
            if (bar1.y - BAR_HEIGHT / 2.0f > -GRID_SIZE && !gameOver)
                bar1.y -= CELL_SIZE;
            break;
    }
    glutPostRedisplay(); // Atualiza a tela após mover a barra
}

void special(int key, int x, int y) {
    switch (key) {
        case GLUT_KEY_UP:
            if (bar1.y + BAR_HEIGHT / 2.0f < GRID_SIZE && !gameOver)
                bar1.y += CELL_SIZE;
            break;
        case GLUT_KEY_DOWN:
            if (bar1.y - BAR_HEIGHT / 2.0f > -GRID_SIZE && !gameOver)
                bar1.y -= CELL_SIZE;
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
    glutInit(&argc, argv); // Inicializa o GLUT
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB); // Define o modo de exibição
    glutInitWindowSize(800, 800); // Define o tamanho da janela
    glutCreateWindow("Pong"); // Cria uma janela
    
    initWindow(); // Inicializa as configurações da janela
    
    glutDisplayFunc(display); // Registra a função de exibição
    glutKeyboardFunc(keyboard); // Registra a função de teclado
    glutSpecialFunc(special);

    glutTimerFunc(0, animate, 0); // Inicia a animação
    glutMainLoop(); // Inicia o loop principal do GLUT
    return 0;
}
