#include <GL/glut.h>

void display() {
    glClear(GL_COLOR_BUFFER_BIT);   // Limpando o buffer de cor
    glBegin(GL_TRIANGLES);  // Definindo o início do desenho de um triângulo
        glColor3f(1.0f, 0.0f, 0.0f); // Definindo cor vermelha (R, G, B)
        glVertex2f(-0.5f, -0.5f);    // Primeiro vértice do triângulo
        glColor3f(0.0f, 1.0f, 0.0f); // Definindo cor verde (R, G, B)
        glVertex2f(0.5f, -0.5f);     // Segundo vértice do triângulo
        glColor3f(0.0f, 0.0f, 1.0f); // Definindo cor azul (R, G, B)
        glVertex2f(0.0f, 0.5f);      // Terceiro vértice do triângulo
    glEnd();    // Encerrando ambiente de desenho do triangulo

    glRotatef(1.0f, 0.0f, 0.0f, 1.0f); // Rotacionando o triângulo em torno do eixo Z
    glFlush();  // Atualizando a tela
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);  // Inicializando o GLUT
    glutCreateWindow("Hello USP!"); // Criando a tela principal com título Hello, USP!
    glutDisplayFunc(display);   // Definindo a função de callback de exibição
    glutMainLoop(); // Iniciando o loop principal do GLUT
    return 0;
}
