#include <GL/glut.h>
#include <iostream>

float angleX = 0.0f;
float angleY = 0.0f;
float angleZ = 0.0f;

void display() {
    glClear(GL_COLOR_BUFFER_BIT);   // Limpando o buffer de cor

    glTranslatef(0.0f, 0.0f, -5.0f); // Movendo a cena para trás no eixo Z
    glBegin(GL_TRIANGLES);  // Definindo o início do desenho de um triângulo
        glColor3f(1.0f, 0.0f, 0.0f); // Definindo cor vermelha (R, G, B)
        glVertex2f(-0.5f, -0.5f);    // Primeiro vértice do triângulo (esquerda)
        glColor3f(0.0f, 1.0f, 0.0f); // Definindo cor verde (R, G, B)
        glVertex2f(0.5f, -0.5f);     // Segundo vértice do triângulo (direita)
        glColor3f(0.0f, 0.0f, 1.0f); // Definindo cor azul (R, G, B)
        glVertex2f(0.0f, 0.5f);      // Terceiro vértice do triângulo (topo)
    glEnd();    // Encerrando ambiente de desenho do triangulo

    glFlush();  // Atualizando a tela
}

// Função deve ser vinculada dentro do main como callback do teclado
// glutKeyboardFunc(keyboard);
void keyboard(unsigned char key, int x, int y) {
    if (key == 27) { // Tecla 'Esc' para sair
        exit(0);
    }
    glutPostRedisplay(); // Solicita a atualização da tela
}

// Função deve ser vinculada dentro do main como callback de teclas especiais
// Serve para teclas como F1-12, setas, Page Up/Down, Home, End, Insert
// glutSpecialFunc(special);
void special(int key, int x, int y) {
    switch (key) {
        case GLUT_KEY_UP:
            break;
        case GLUT_KEY_DOWN:
            break;
        case GLUT_KEY_LEFT:
            break;
        case GLUT_KEY_RIGHT:
            break;
    }
    glutPostRedisplay(); // Solicita a atualização da tela
}

// Função deve ser vinculada dentro do main como callback do mouse
// glutMouseFunc(mouse);
void mouse(int button, int state, int x, int y) {
    if (button == GLUT_LEFT_BUTTON && state == GLUT_DOWN) {
        // Clique com o botão esquerdo do mouse
    } else if (button == GLUT_RIGHT_BUTTON && state == GLUT_DOWN) {
        // Clique com o botão direito do mouse
    }
    glutPostRedisplay(); // Solicita a atualização da tela
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);  // Inicializando o GLUT
    glutCreateWindow("Hello USP!"); // Criando a tela principal com título Hello, USP!

    // Propriedades da janela
    glutInitWindowSize(300, 300); // Definindo o tamanho da janela
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA);   // Criando uma janela com buffer simples e esquema de cores RGBA
    
    // Alterações na matriz de projeção da janela
    glMatrixMode(GL_PROJECTION); // Definindo o modo de matriz para projeção
    glLoadIdentity(); // Carregando a matriz identidade
    //gluOrtho2D(-1.0, 1.0, -1.0, 1.0); // Definindo a projeção ortográfica
    //glFrustum(-1.0, 1.0, -1.0, 1.0, 1.0, 10.0); // Definindo a projeção em perspectiva
    gluPerspective(45.0, 1.0, 1.0, 10.0); // Definindo a projeção em perspectiva

    // Alterações na matriz de modelo
    glMatrixMode(GL_MODELVIEW); // Definindo o modo de matriz para modelo
    glLoadIdentity(); // Carregando a matriz identidade

    glutSpecialFunc(special); // Definindo a função de callback para teclas especiais
    glutKeyboardFunc(keyboard); // Definindo a função de callback do teclado
    glutDisplayFunc(display);   // Definindo a função de callback de exibição
    glutMainLoop(); // Iniciando o loop principal do GLUT
    return 0;
}
