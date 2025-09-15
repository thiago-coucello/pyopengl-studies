cmake_minimum_required(VERSION 3.10)
project(HelloUSP)

set(CMAKE_CXX_STANDARD 11)

find_package(OpenGL REQUIRED)
find_package(GLUT REQUIRED)
find_package(GLU REQUIRED)

add_executable(main main.cpp)

target_link_libraries(main OpenGL::GL GLUT::GLUT GLU)
