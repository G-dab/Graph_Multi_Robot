import matplotlib.pyplot as plt
import numpy as np

# https://csacademy.com/app/graph_editor/

class GraphBase():
    def __init__(self, plot_xlim=[-10, 10], plot_ylim=[-10, 10]):
        self.plot_xlim = plot_xlim
        self.plot_ylim = plot_ylim

    def show(self):
        # show graph
        pass

# 统一使用 0-index
class SimpleGraph(GraphBase):
    def __init__(self, graph, graph_type='undirected', indexBase='0-index', plot_xlim=[-10, 10], plot_ylim=[-10, 10]):
        super().__init__(plot_xlim, plot_ylim)

        if graph_type not in ['undirected', 'directed']:
            raise ValueError('Graph type not supported!')
        
        self.graph = graph
        self.graph_type = graph_type
        self.node_size = graph['node_size']
        if indexBase == '0-index':
            self.edges = graph['edges']
        elif indexBase == '1-index':
            self.edges = [[edge[0]-1, edge[1]-1] for edge in graph['edges']]

        self.adjmatrix = self.__return_adjmatrix(graph, indexBase)
        self.incmatrix = self.__return_incmatrix(graph, indexBase)
        self.degreematrix = np.diag(np.sum(self.adjmatrix, axis=1))
        self.lapmatrix = self.degreematrix - self.adjmatrix

    def __return_adjmatrix(self, graph, indexBase):
        # adjacency matrix
        # edge weight = 1 if not defined
        # return adjacency matrix all in 0-index
        adjmatrix = np.zeros((graph['node_size'], graph['node_size']), dtype=int)
        
        for edge in graph['edges']:
            if indexBase == '1-index':
                if len(edge) == 2:
                    adjmatrix[edge[0]-1, edge[1]-1] += 1
                elif len(edge) == 3:
                    adjmatrix[edge[0]-1, edge[1]-1] += edge[2]
                if self.graph_type == 'undirected':
                    adjmatrix[edge[1]-1, edge[0]-1] += adjmatrix[edge[0]-1, edge[1]-1]
            elif indexBase == '0-index':
                if len(edge) == 2:
                    adjmatrix[edge[0], edge[1]] += 1
                elif len(edge) == 3:
                    adjmatrix[edge[0], edge[1]] += edge[2]
                if self.graph_type == 'undirected':
                    adjmatrix[edge[1], edge[0]] += adjmatrix[edge[0], edge[1]]
        return adjmatrix
    
    def __return_incmatrix(self, graph, indexBase):
        # incidence matrix
        # edge weight = 1 if not defined
        # return incidence matrix all in 0-index
        incmatrix = np.zeros((graph['node_size'], len(graph['edges'])), dtype=int)
        
        if self.graph_type == 'undirected':
            for i, edge in enumerate(graph['edges']):
                if indexBase == '1-index':
                    if len(edge) == 2:
                        incmatrix[edge[0]-1, i] = 1
                        incmatrix[edge[1]-1, i] = 1
                    elif len(edge) == 3:
                        incmatrix[edge[0]-1, i] = edge[2]
                        incmatrix[edge[1]-1, i] = edge[2]
                elif indexBase == '0-index':
                    if len(edge) == 2:
                        incmatrix[edge[0], i] = 1
                        incmatrix[edge[1], i] = 1
                    elif len(edge) == 3:
                        incmatrix[edge[0], i] = edge[2]
                        incmatrix[edge[1], i] = edge[2]
      
        return incmatrix

    def show(self, show_node_id=True, node_size=300, edge_width=2):
        fig, ax = plt.subplots()
        # 随机生成节点位置
        node_positions = [None] * self.node_size
        for node_id in range(self.node_size):
            node_positions[node_id] = (self.plot_xlim[0] + 0.8 * (self.plot_xlim[1] - self.plot_xlim[0]) * np.random.rand(),
                                       self.plot_ylim[0] + 0.8 * (self.plot_ylim[1] - self.plot_ylim[0]) * np.random.rand())

        # 绘制节点
        for node_id in range(self.node_size):
            ax.scatter(node_positions[node_id][0], node_positions[node_id][1],
                       zorder=2,
                       s=node_size, linewidths=edge_width, edgecolors='black', marker='o')
            if show_node_id:
                ax.text(node_positions[node_id][0], node_positions[node_id][1], str(node_id),
                        zorder=3,
                        ha='center', va='center', fontsize=12)
        
        # 绘制边
        for edge in self.edges:
            start_pos = node_positions[edge[0]]
            end_pos = node_positions[edge[1]]
            ax.plot([start_pos[0], end_pos[0]], [start_pos[1], end_pos[1]], 
                    zorder=1,
                    color='black', linewidth=edge_width)
        
        plt.show()