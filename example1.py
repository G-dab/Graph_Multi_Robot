from GMR import MultiRobot

# 创建无向图
# 简单无向图: 无环和平行边
# 允许设置平行边(非简单图)和闭环
# node的id必须连续
graph = {
    'node_size': 5,
    'edges': [[1,2], [2,3], [2,5], [3,4], [3,5], [4,5]]
}
graph = {
    'node_size': 5,
    'edges': [[1,2], [1,3], [1,4], [1,5], [2,3], [2,4], [2,5], [3,4], [3,5], [4,5]]
}

# ----- 创建多机器人系统 -----
MRobot = MultiRobot(graph, graph_type='undirected', indexBase='1-index')

# ----- 查看相应参数 -----
# 邻接矩阵
print('Adjacency Matrix: ', MRobot.Graph.adjmatrix)
# 关联矩阵
print('Incidence Matrix: ', MRobot.Graph.incmatrix)
# 度矩阵
print('Degree Matrix: ', MRobot.Graph.degreematrix)
# 拉普拉斯矩阵
print('Laplacian Matrix: ', MRobot.Graph.lapmatrix)

# ----- 仿真 -----
# 仿真参数
config = {
    'time': 800,
    'time_step': 0.01,
    'mode': 'limear controller',
    'controller': -MRobot.Graph.lapmatrix,
    'initial_state': [-10, 5, 0, 5, 10],
}
MRobot.simulation(config)