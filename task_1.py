import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# Створюємо граф
G = nx.DiGraph()

vertices = {
    0: "Термінал 1",
    1: "Термінал 2",
    2: "Склад 1",
    3: "Склад 2",
    4: "Склад 3",
    5: "Склад 4",
    6: "Магазин 1",
    7: "Магазин 2",
    8: "Магазин 3",
    9: "Магазин 4",
    10: "Магазин 5",
    11: "Магазин 6",
    12: "Магазин 7",
    13: "Магазин 8",
    14: "Магазин 9",
    15: "Магазин 10",
    16: "Магазин 11",
    17: "Магазин 12",
    18: "Магазин 13",
    19: "Магазин 14",
}

# Додаємо ребра з пропускною здатністю
edges = [
    (0, 2, 25),  # Термінал 1 (0) -> Склад 1 (2)
    (0, 3, 20),  # Термінал 1 (0) -> Склад 2 (3)
    (0, 4, 15),  # Термінал 1 (0) -> Склад 3 (4)
    (1, 3, 10),  # Термінал 2 (1) -> Склад 2 (3)
    (1, 4, 15),  # Термінал 2 (1) -> Склад 3 (4)
    (1, 5, 30),  # Термінал 2 (1) -> Склад 4 (5)
    (2, 6, 15),  # Склад 1 (2) -> Магазин 1 (6)
    (2, 7, 10),  # Склад 1 (2) -> Магазин 2 (7)
    (2, 8, 20),  # Склад 1 (2) -> Магазин 3 (8)
    (3, 9, 15),  # Склад 2 (3) -> Магазин 4 (9)
    (3, 10, 10),  # Склад 2 (3) -> Магазин 5 (10)
    (3, 11, 25),  # Склад 2 (3) -> Магазин 6 (11)
    (4, 12, 20),  # Склад 3 (4) -> Магазин 7 (12)
    (4, 13, 15),  # Склад 3 (4) -> Магазин 8 (13)
    (4, 14, 10),  # Склад 3 (4) -> Магазин 9 (14)
    (5, 15, 20),  # Склад 4 (5) -> Магазин 10 (15)
    (5, 16, 10),  # Склад 4 (5) -> Магазин 11 (16)
    (5, 17, 15),  # Склад 4 (5) -> Магазин 12 (17)
    (5, 18, 5),  # Склад 4 (5) -> Магазин 13 (18)
    (5, 19, 10),  # Склад 4 (5) -> Магазин 14 (19)
]

# Додаємо всі ребра до графа
G.add_weighted_edges_from(edges)

# Позиції для малювання графа
pos = {
    0: (2, 0),  # Термінал 1
    1: (6, 0),  # Термінал 2
    2: (3, 1),  # Склад 1
    3: (5, 1),  # Склад 2
    4: (3, -1),  # Склад 3
    5: (5, -1),  # Склад 4
    6: (1, 2),  # Магазин 1
    7: (2, 2),  # Магазин 2
    8: (3, 2),  # Магазин 3
    9: (4, 2),  # Магазин 4
    10: (5, 2),  # Магазин 5
    11: (6, 2),  # Магазин 6
    12: (1, -2),  # Магазин 7
    13: (2, -2),  # Магазин 8
    14: (3, -2),  # Магазин 9
    15: (4, -2),  # Магазин 10
    16: (5, -2),  # Магазин 11
    17: (6, -2),  # Магазин 12
    18: (7, -2),  # Магазин 13
    19: (8, -2),  # Магазин 14
}

# Малюємо граф
plt.figure(figsize=(10, 6))
nx.draw(G, pos, labels=vertices, with_labels=True, node_size=2000, node_color="skyblue", font_size=7, font_weight="bold", arrows=True)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)


# Функція для пошуку збільшуючого шляху (BFS)
def bfs(capacity_matrix, flow_matrix, source, sink, parent):
    visited = [False] * len(capacity_matrix)
    queue = deque([source])
    visited[source] = True

    while queue:
        current_node = queue.popleft()

        for neighbor in range(len(capacity_matrix)):
            # Перевірка, чи є залишкова пропускна здатність у каналі
            if not visited[neighbor] and capacity_matrix[current_node][neighbor] - flow_matrix[current_node][
                neighbor] > 0:
                parent[neighbor] = current_node
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)

    return False


# Основна функція для обчислення максимального потоку
def edmonds_karp(capacity_matrix, source, sink):
    num_nodes = len(capacity_matrix)
    flow_matrix = [[0] * num_nodes for _ in range(num_nodes)]  # Ініціалізуємо матрицю потоку нулем
    parent = [-1] * num_nodes
    max_flow = 0

    # Поки є збільшуючий шлях, додаємо потік
    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        # Знаходимо мінімальну пропускну здатність уздовж знайденого шляху (вузьке місце)
        path_flow = float('Inf')
        current_node = sink

        while current_node != source:
            previous_node = parent[current_node]
            path_flow = min(path_flow,
                            capacity_matrix[previous_node][current_node] - flow_matrix[previous_node][current_node])
            current_node = previous_node

        # Оновлюємо потік уздовж шляху, враховуючи зворотний потік
        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            flow_matrix[previous_node][current_node] += path_flow
            flow_matrix[current_node][previous_node] -= path_flow
            current_node = previous_node

        # Збільшуємо максимальний потік
        max_flow += path_flow

    return max_flow


# Матриця пропускної здатності для каналів у мережі (capacity_matrix)
capacity_matrix = [[0] * len(vertices) for _ in range(len(vertices))]
for v in edges:
    capacity_matrix[v[0]][v[1]] = v[2]

for i in [0, 1]: # Термінали
    for j in range(6, 20): # Магазини
        source = i  # Термінал
        sink = j  # Магазин
        print(f"Термінал {i + 1} ->  Магазин {j - 5} - Максимальний потік: {edmonds_karp(capacity_matrix, source, sink)}\n")

# Відображаємо граф
plt.ioff()
plt.show()