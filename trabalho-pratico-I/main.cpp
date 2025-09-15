#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glut.h>
#include <bits/stdc++.h>

using namespace std;

typedef pair<int, int> Point;
typedef tuple<int, int, int> Color;

typedef struct Edge {
    int ymax, xmin, inclination;
    Edge* next;
} Edge;

typedef struct EdgeTable {
    int scanline;
    Edge* edges;
    EdgeTable* next;
} EdgeTable;

EdgeTable* edge_table = nullptr;

void write_pixel(int x, int y, Color color) {
    glBegin(GL_POINTS);
    glColor3f(get<0>(color), get<1>(color), get<2>(color));
    glVertex2i(x, y);
    glEnd();
}

void insert_edge(Point start, Point end) {
    if (start.second > end.second) {
        // Order points by y-coordinate (start always has the smaller y)
        swap(start, end);
    }

    if (start.first == end.first) {
        return; // Vertical edge, ignore
    }

    if (edge_table == nullptr) {
        edge_table = new EdgeTable();
        edge_table->scanline = start.second;
        edge_table->edges = nullptr;
        edge_table->next = nullptr;
    } else {
        // Create new edge table entry for new scanline
        EdgeTable* current = edge_table;
        EdgeTable* previous = nullptr;
        
        while (current != nullptr && current->scanline < start.second) {
            // Search for the correct position to insert
            previous = current;
            current = current->next;
        }

        if (previous == nullptr || previous->scanline != start.second) {
            // Insert new edge table entry
            EdgeTable* new_table = new EdgeTable();
            new_table->scanline = start.second;
            new_table->edges = nullptr;
            new_table->next = current;

            if (previous == nullptr) {
                // Insert at the beginning
                edge_table = new_table;
            } else {
                // Insert in the middle or end
                previous->next = new_table;
            }
        }
    }

    // Searching for the correct edge table entry
    EdgeTable* current_table = edge_table;
    while (current_table != nullptr && current_table->scanline < start.second) {
        current_table = current_table->next;
    }

    Edge* new_edge = new Edge();
    new_edge->ymax = end.second;
    new_edge->xmin = start.first;
    new_edge->inclination = (end.first - start.first) / (end.second - start.second);
    new_edge->next = nullptr;

    if (current_table->edges == nullptr) {
        // Empty edge table entry - insert directly
        current_table->edges = new_edge;
    } else {
        // Search for the correct position to insert the edge
        Edge* current = current_table->edges;
        Edge* previous = nullptr;

        while (current != nullptr && current->xmin < new_edge->xmin) {
            previous = current;
            current = current->next;
        }

        if (previous == nullptr) {
            // Insert at the beginning
            new_edge->next = current_table->edges;
            current_table->edges = new_edge;
        } else {
            // Insert in the middle or end
            previous->next = new_edge;
            new_edge->next = current;
        }
    }
}

// 3.1 - Transfer edges to AET from ET where scanline == y
void transfer_edges_to_AET(EdgeTable*& ET, Edge*& AET, int y) {
    while (ET != nullptr && ET->scanline == y) {
        Edge* e = ET->edges;
        while (e != nullptr) {
            Edge* next = e->next;
            // Inserção ordenada na AET por xmin
            if (AET == nullptr || e->xmin < AET->xmin) {
                e->next = AET;
                AET = e;
            } else {
                Edge* a = AET;
                while (a->next != nullptr && a->next->xmin < e->xmin) {
                    a = a->next;
                }
                e->next = a->next;
                a->next = e;
            }
            e = next;
        }
        EdgeTable* to_delete = ET;
        ET = ET->next;
        delete to_delete;
    }
}

// 3.2 - Remove from AET all edges whose ymax == y
void remove_edges_from_AET(Edge*& AET, int y) {
    Edge* prev = nullptr;
    Edge* curr = AET;
    while (curr != nullptr) {
        if (curr->ymax == y) {
            Edge* to_delete = curr;
            if (prev == nullptr) {
                AET = curr->next;
                curr = AET;
            } else {
                prev->next = curr->next;
                curr = curr->next;
            }
            delete to_delete;
        } else {
            prev = curr;
            curr = curr->next;
        }
    }
}

// 3.3 - Fill pixels between pairs of edges in AET
void fill_scanline_from_AET(Edge* AET, int y, Color color) {
    Edge* e = AET;
    while (e != nullptr && e->next != nullptr) {
        int x_start = e->xmin;
        int x_end = e->next->xmin;
        for (int x = x_start; x < x_end; x++) {
            write_pixel(x, y, color);
        }
        e = e->next->next; // Advance to the next pair
    }
}

// 3.5 - Update xmin of remaining edges in AET
void update_AET_edges(Edge* AET) {
    for (Edge* e = AET; e != nullptr; e = e->next) {
        e->xmin += e->inclination;
    }
}

// 3.6 - Reorder AET by xmin (insertion sort)
void order_AET(Edge*& AET) {
    Edge* sorted = nullptr;
    while (AET != nullptr) {
        Edge* next = AET->next;
        if (sorted == nullptr || AET->xmin < sorted->xmin) {
            AET->next = sorted;
            sorted = AET;
        } else {
            Edge* s = sorted;
            while (s->next != nullptr && s->next->xmin < AET->xmin) {
                s = s->next;
            }
            AET->next = s->next;
            s->next = AET;
        }
        AET = next;
    }
    AET = sorted;
}

void arbitrary_polygon_drawing(Color color) {
    if (edge_table == nullptr) return;

    int y = edge_table->scanline;
    Edge* AET = nullptr;
    EdgeTable* ET = edge_table;

    while (ET != nullptr || AET != nullptr) {
        transfer_edges_to_AET(ET, AET, y);           // 3.1
        remove_edges_from_AET(AET, y);               // 3.2
        fill_scanline_from_AET(AET, y, color);       // 3.3
        y++;                                         // 3.4
        update_AET_edges(AET);                       // 3.5
        order_AET(AET);                              // 3.6
    }
}

int main() {

}