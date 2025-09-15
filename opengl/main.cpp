#include <GL/glut.h>
#include <GL/glu.h>
#include <cmath>

float elementX = 0.0f;
float elementY = 0.0f;
float stepX = 0.03f;
float stepY = 0.05f;
float angle = 0.0f;

void drawCircle(float centerX, float centerY, float radius, int numSegments) {
    glBegin(GL_LINE_LOOP);
    for (int i = 0; i < numSegments; ++i) {
        float theta = 2.0f * M_PI * float(i) / float(numSegments); // Ângulo atual
        float x = radius * cosf(theta); // Coordenada x
        float y = radius * sinf(theta); // Coordenada y
        glVertex2f(x + centerX, y + centerY); // Adiciona o vértice ao círculo
    }
    glEnd();
}

void display() {
    glClear(GL_COLOR_BUFFER_BIT);   // Limpando o buffer de cor
    glPushMatrix();
        glRotatef(angle, 0.0f, 0.0f, 1.0f); // Rotacionando o triângulo em torno do eixo Z
        glTranslatef(elementX, elementY, 0.0f); // Movendo o triângulo para a posição (elementX, elementY)
        glBegin(GL_TRIANGLES);  // Definindo o início do desenho de um triângulo
            glColor3f(1.0f, 0.0f, 0.0f); // Definindo cor vermelha (R, G, B)
            glVertex2f(-0.5f, -0.5f);    // Primeiro vértice do triângulo
            glColor3f(0.0f, 1.0f, 0.0f); // Definindo cor verde (R, G, B)
            glVertex2f(0.5f, -0.5f);     // Segundo vértice do triângulo
            glColor3f(0.0f, 0.0f, 1.0f); // Definindo cor azul (R, G, B)
            glVertex2f(0.0f, 0.5f);      // Terceiro vértice do triângulo
        glEnd();    // Encerrando ambiente de desenho do triangulo
    glPopMatrix();

    glPointSize(5.0f); // Definindo o tamanho do ponto

    glBegin(GL_POINTS);
        glColor3f(1.0f, 1.0f, 1.0f); // Definindo cor branca (R, G, B)
        glVertex2f(0.0f, 0.0f);      // Ponto no centro do triângulo
    glEnd();

    glBegin(GL_LINES);
        glColor3f(1.0f, 1.0f, 1.0f); // Definindo cor branca (R, G, B)
        glVertex2f(-0.5f, -0.5f);    // Linha do primeiro vértice ao centro
        glVertex2f(0.0f, 0.0f);
        glVertex2f(0.5f, -0.5f);     // Linha do segundo vértice ao centro
        glVertex2f(0.0f, 0.0f);
        glVertex2f(0.0f, 0.5f);      // Linha do terceiro vértice ao centro
        glVertex2f(0.0f, 0.0f);
    glEnd();

    drawCircle(0.0f, -0.1667f, 0.309f, 100); // Desenhando uma circunferência inscrita no triângulo
    glFlush();  // Atualizando a tela
}

void update(int value) {
    angle += 0.01f; // Incrementa o ângulo de rotação
    elementX += stepX; // Atualiza a posição X
    elementY += stepY; // Atualiza a posição Y

    if (elementX > 1.0f || elementX < -1.0f) stepX = -stepX; // Inverte a direção se atingir os limites X
    if (elementY > 1.0f || elementY < -1.0f) stepY = -stepY; // Inverte a direção se atingir os limites Y

    if (angle >= 360.0f) angle -= 360.0f; // Garante que o ângulo fique dentro de 0-360 graus
    glutPostRedisplay();  // Atualizando a tela
    glutTimerFunc(16, update, 0); // Chama esta função novamente após 16 ms (~60 FPS)
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);  // Inicializando o GLUT
    
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA);   // Criando uma janela com buffer simples e esquema de cores RGBA
    glutInitWindowSize(300, 300); // Definindo o tamanho da janela
    glutCreateWindow("Hello USP!"); // Criando a tela principal com título Hello, USP!
    
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0); // Define a projeção ortográfica 2D

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    
    glutDisplayFunc(display);   // Definindo a função de callback de exibição
    glutTimerFunc(0, update, 0); // Inicia a função de atualização
    glutMainLoop(); // Iniciando o loop principal do GLUT
    return 0;
}