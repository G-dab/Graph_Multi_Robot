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

class SimpleGraph(GraphBase):
    def __init__(self, graph, graph_type='undirected', indexBase='0-index', plot_xlim=[-10, 10], plot_ylim=[-10, 10]):
        super().__init__(plot_xlim, plot_ylim)

        if graph_type not in ['undirected', 'directed']:
            raise ValueError('Graph type not supported!')
        self.graph = graph
        self.graph_type = graph_type
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

    def show(self, show_node_id=True, show_node_label=False, show_edge_label=True, node_size=300, edge_width=2):
        # 随机生成节点位置
        node_positions = {}
        for node_id in self.nodes:
            node_positions[node_id] = (self.plot_xlim[0] + 0.8 * (self.plot_xlim[1] - self.plot_xlim[0]) * np.random.rand(),
                                       self.plot_ylim[0] + 0.8 * (self.plot_ylim[1] - self.plot_ylim[0]) * np.random.rand())

        # 绘制节点
        for node_id, pos in node_positions.items():
            self.ax.scatter(pos[0], pos[1], s=node_size, facecolors='white', edgecolors='black')
            if show_node_id:
                self.ax.text(pos[0], pos[1], str(node_id), ha='center', va='center', fontsize=node_size / 30)
            if show_node_label:
                self.ax.text(pos[0], pos[1], str(self.nodes[node_id]), ha='center', va='center', fontsize=node_size / 30)

        # 绘制边
        for edge in self.edges:
            source_id, target_id = edge
            source_pos = node_positions[source_id]
            target_pos = node_positions[target_id]

            # 计算控制点，使边有点弯曲
            control_point_x = (source_pos[0] + target_pos[0]) / 2 + (target_pos[0] - source_pos[0]) * 0.1
            control_point_y = (source_pos[1] + target_pos[1]) / 2 + (target_pos[1] - source_pos[1]) * 0.1

