import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import multiprocessing

from utils import *
import time

def perform_algos(graph: nx.Graph, algos: dict, verbose: bool = False, timeout = 600):
    """
    Perform all the algorithms in the algos dict on the graph.
    """
    results = {}
    for algo_name, algo in algos.items():
        if verbose:
            print(f"Running {algo_name}...", flush=True)
        
        start_time = time.time()
        community = call_function_with_timeout(timeout, algo, graph)
        end_time = time.time()
        runtime = end_time - start_time
        
        if community is None:
            print(f"Algorithm {algo_name} timed out.")
            results[algo_name] = {
                'runtime': None,
                'modularity': None,
                'community': None
            }
            continue

        modularity = nx.algorithms.community.modularity(graph, community)
        
        results[algo_name] = {
            'runtime': runtime,
            'modularity': modularity,
            'community': community
        }
        
    return results

def call_function_with_timeout(timeout, func, *args, **kargs):
    # Create a multiprocessing pool with a single process
    with multiprocessing.Pool(1) as pool:

        # Start func in the pool
        result_async = pool.apply_async(func, args, kargs)

        try:
            # Get the result of func, with a timeout
            result = result_async.get(timeout)
            return result
        except multiprocessing.TimeoutError:
            # Terminate the process if it is taking too long
            pool.terminate()
            return None
