import pygraphviz as pgv

# Create the graph
G = pgv.AGraph(directed=True)

# Add the nodes
G.add_node("Prior Knowledge")
G.add_node("Observations")
G.add_node("Model")
G.add_node("Results")

# Add the edges
G.add_edge("Prior Knowledge", "Model")
G.add_edge("Observations", "Model")
G.add_edge("Model", "Results")

# Set node properties
G.node_attr["shape"] = "ellipse"
G.node_attr["fontsize"] = "14"

# Set edge properties
G.edge_attr["arrowsize"] = "0.5"

# Draw the graph and save to file
G.draw("graph.png", prog="dot")
