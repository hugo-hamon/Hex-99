import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import time

if __name__ == "__main__":
    # Graph 20x20 wich make a grid
    H = nx.grid_2d_graph(11, 11)
    nx.draw(H, with_labels=True)
    plt.show()
    start = time.time()
    for _ in range(20000):
        H = H.copy()
    print("Time to build graph:", time.time() - start)

    
    

