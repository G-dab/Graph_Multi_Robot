from matplotlib import pyplot as plt
from .GraphEditor import SimpleGraph

class MultiRobot():
    def __init__(self, graph, graph_type='undirected', indexBase='1-index'):
        self.Graph = SimpleGraph(graph, graph_type, indexBase)
    
    def simulation(self, config, xlabel='Time', ylabel='State', title='Multi Robot System Simulation'):
        time = config['time']
        time_step = config['time_step']
        mode = config['mode']

        fig, ax = plt.subplots()
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(True)
        ax.set_xlim(0, time)

        if mode == 'limear controller':
            controller = config['controller']
            initial_state = config['initial_state']
            state = []
            state.append(initial_state)
            for t in range(time):
                state.append(state[-1] + time_step * controller @ state[-1])
            state = list(map(list, zip(*state)))
            for i in range(len(state)):
                ax.plot(state[i], label='Robot'+str(i+1))
            ax.legend()

        else:
            raise ValueError('Mode not supported!')
        
        plt.show()

