# robdd.py
import graphviz

class BDDNode:
    # A single node in the BDD graph.
    def __init__(self, var, low, high, node_id):
        self.var = var       # Variable name
        self.low = low       # Reference to False branch node
        self.high = high     # Reference to True branch node
        self.id = node_id    # ID for graphviz labeling

class ROBDD:
    """
    Main class for constructing ROBDD.
    Using Shannon Expansion and Reduction Rules.
    """
    def __init__(self, ordering):
        self.ordering = ordering
        self.unique_table = {}  # Stores unique nodes to ensure reduction
        self.node_counter = 2   # 0 and 1 are reserved for terminals
        self.zero = BDDNode(None, None, None, 0)
        self.one = BDDNode(None, None, None, 1)
    
    def get_node(self, var, low, high):
        # Creates a node or returns an existing one (Reduction Rules).
        # Rule 1: Eliminate redundant nodes
        if low == high: 
            return low
        
        # Rule 2: Share equivalent sub-graphs
        key = (var, low.id, high.id)
        if key in self.unique_table: 
            return self.unique_table[key]
        
        new_node = BDDNode(var, low, high, self.node_counter)
        self.unique_table[key] = new_node
        self.node_counter += 1
        return new_node

    def build(self, func):
        """Public method to start building the BDD from a boolean function."""
        return self._build_rec(func, {}, 0)

    def _build_rec(self, func, assignment, idx):
        # Recursive Shannon Expansion.
        # Base case: All variables assigned
        if idx == len(self.ordering):
            return self.one if func(assignment) else self.zero
        
        var = self.ordering[idx]
        
        # Low branch (var = 0)
        assignment[var] = False
        low_node = self._build_rec(func, assignment, idx + 1)
        
        # High branch (var = 1)
        assignment[var] = True
        high_node = self._build_rec(func, assignment, idx + 1)
        
        return self.get_node(var, low_node, high_node)

    def visualize(self, root, filename):
        """Generates and opens a PNG image of the BDD using Graphviz."""
        dot = graphviz.Digraph(comment=filename)
        visited = set()
        
        def traverse(node):
            if node.id in visited: return
            visited.add(node.id)
            
            # Styling: Box for terminals, Circle for variables
            if node.var is None:
                label, shape, color = str(node.id), 'box', 'lightgrey'
            else:
                label, shape, color = node.var, 'circle', 'white'
                
            dot.node(str(node.id), label=label, shape=shape, style='filled', fillcolor=color)
            
            if node.var is not None:
                # Dashed edge for Low (0), Solid edge for High (1)
                dot.edge(str(node.id), str(node.low.id), style='dashed', label='0')
                traverse(node.low)
                dot.edge(str(node.id), str(node.high.id), style='solid', label='1')
                traverse(node.high)

        traverse(root)
        try:
            output_path = dot.render(filename, format='png', view=True)
            print(f"Graph generated: {output_path}")
        except Exception as e:
            print(f"Error generating image: {e}")
            print("Please ensure Graphviz is installed and added to PATH.")
