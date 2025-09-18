import networkx as nx
import matplotlib.pyplot as plt
import argparse
import random
import pickle
import os

# 引数処理
parser = argparse.ArgumentParser()
parser.add_argument('--m', type=int, default=12, help='縦のマスの数 + 1')
parser.add_argument('--n', type=int, default=10, help='横のマスの数 + 1')
parser.add_argument('--p', type=int, default=5, help='初期C属性の数')
parser.add_argument('--output', type=str, default='maze_graph.pkl', help='出力ファイル名')
args = parser.parse_args()
m, n, P = args.m, args.n, args.p

# グラフ作成
G = nx.grid_2d_graph(n, m)
attr = {node: 'A' for node in G.nodes()}

# 外周ノード判定
outer_nodes = [
    node for node in G.nodes()
    if node[0] == 0 or node[0] == n - 1 or node[1] == 0 or node[1] == m - 1
]
for node in outer_nodes:
    attr[node] = 'B'

# 外周の辺のみを使って部分グラフ作成
maze = nx.Graph()
for u, v in G.edges():
    if attr[u] == 'B' and attr[v] == 'B':
        maze.add_edge(u, v)

# 入り口・出口の除外
entry = (n - 1, 0)
exit = (0, m - 1)
if maze.has_edge((n - 1, 0), (n - 1, 1)):
    maze.remove_edge((n - 1, 0), (n - 1, 1))
if maze.has_edge((0, m - 1), (0, m - 2)):
    maze.remove_edge((0, m - 1), (0, m - 2))

# ランダムにCを選ぶ
B_nodes = [node for node in attr if attr[node] == 'B']
C_nodes = random.sample(B_nodes, min(P, len(B_nodes)))
for node in C_nodes:
    attr[node] = 'C'

# 成長ステップ関数
def grow():
    D_nodes = [node for node in attr if attr[node] == 'D']
    for node in D_nodes:
        neighbors = list(G.neighbors(node))
        A_neighbors = [n for n in neighbors if attr[n] == 'A']
        if not A_neighbors:
            attr[node] = 'F'
        else:
            new_D = random.choice(A_neighbors)
            attr[new_D] = 'D'
            attr[node] = 'C'
            maze.add_edge(node, new_D)

# 選択ステップ関数
def select():
    C_nodes = [node for node in attr if attr[node] == 'C']
    select_num = min(len(C_nodes), random.randint(1, 10))
    selected = random.sample(C_nodes, select_num)
    for node in selected:
        attr[node] = 'D'

# 最初のCノードに対する処理
for node in C_nodes:
    neighbors = list(G.neighbors(node))
    A_neighbors = [n for n in neighbors if attr[n] == 'A']
    if not A_neighbors:
        attr[node] = 'F'
    else:
        new_D = random.choice(A_neighbors)
        attr[new_D] = 'D'
        attr[node] = 'F'
        maze.add_edge(node, new_D)

# メインループ：成長と選択
while any(attr[n] == 'A' for n in attr):
    grow()
    select()

# 結果の表示
basename = os.path.splitext(os.path.basename(args.output))[0]

image_file = f"{basename}.png"

pos = dict((n, n) for n in G.nodes())
plt.figure(figsize=(8, 6))
# nx.draw(G, pos, node_size=0, edge_color='lightgray', width=0.5)
nx.draw(maze, pos, node_size=0, edge_color='black', width=2)
plt.axis('equal')
plt.title('Generated Maze')
plt.savefig(image_file, dpi=300, bbox_inches='tight')

plt.show()

# plt.savefig("generated_maze.png")

# グラフの保存
# with open(args.output, 'wb') as f:
#     pickle.dump(maze, f)
# print(f"迷路グラフを保存しました: {args.output}")

