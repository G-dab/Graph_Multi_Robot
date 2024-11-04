'''
example2 比较稀疏图和密集图在模拟仿真中的速度
控制器: u = -L
'''
from GMR import MultiRobot

spares_graph = {
    'node_size': 5,
    'edges': [[1,2], [2,3], [2,5], [3,4], [3,5], [4,5]]
}
dense_graph = {
    'node_size': 5,
    'edges': [[1,2], [1,3], [1,4], [1,5], [2,3], [2,4], [2,5], [3,4], [3,5], [4,5]]
}

# ----- 创建多机器人系统 -----
spares_MRobot = MultiRobot(spares_graph, graph_type='undirected', indexBase='1-index')
dense_MRobot = MultiRobot(dense_graph, graph_type='undirected', indexBase='1-index')

# ----- 查看相应参数 -----
# # 邻接矩阵
# print('Adjacency Matrix: ', spares_MRobot.Graph.adjmatrix)
# # 关联矩阵
# print('Incidence Matrix: ', spares_MRobot.Graph.incmatrix)
# # 度矩阵
# print('Degree Matrix: ', spares_MRobot.Graph.degreematrix)
# # 拉普拉斯矩阵
# print('Laplacian Matrix: ', spares_MRobot.Graph.lapmatrix)

# ----- 仿真 -----
# 仿真参数
config = {
    'time': 800,
    'time_step': 0.01,
    'mode': 'limear controller',
    'controller': -spares_MRobot.Graph.lapmatrix,
    'initial_state': [-10, 5, 0, 5, 10],
}
spares_MRobot.simulation(config, title='Sparse Graph Simulation')
dense_MRobot.simulation(config, title='Dense Graph Simulation')