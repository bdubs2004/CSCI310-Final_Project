"""
UNL_Parking.py
---------------
Graph-based parking search tool for UNL campus.

Author: Bryce Kwiecinski
Date: 2025 December 03
"""

import pandas as pd
import networkx as nx
from pathlib import Path


class UNLParking:
    """
    Main class for building and querying the UNL parking graph.
    """

    def __init__(self, filepath):
        # Store Excel file path
        self.filepath = Path(filepath)

        # DataFrame storage
        self.df = None

        # Graph structure
        self.graph = nx.DiGraph()

    # ---------------------------
    # Data Loading
    # ---------------------------
    def load_data(self):
        """Load the Excel dataset into a DataFrame."""
        self.df = pd.read_excel(self.filepath)
        return self.df

# ---------------------------
# Graph Construction
# ---------------------------
def build_graph(self):
    """
    Build the pass to lot graph using the data.
    Nodes: passes and lots
    Edges: which passes allow which lots
    """
    if self.df is None:
        raise ValueError("Data not loaded. Call load_data() first.")

    # Add pass nodes
    passes = self.df['Permit'].unique()
    for p in passes:
        self.graph.add_node(p, type='pass')

    # Add lot nodes and edges
    for _, row in self.df.iterrows():
        permit = row['Permit']
        lots = row['City Campus Parking/Location(s)']

        # Handle multiple lots in one cell (split by comma if needed)
        lot_list = [lot.strip() for lot in lots.split(',')]

        for lot in lot_list:
            # Add lot node if not already added
            if lot not in self.graph:
                self.graph.add_node(lot, type='lot')

            # Add directed edge: pass → lot
            self.graph.add_edge(permit, lot)


# ---------------------------
# Search: Pass → Lots (BFS)
# ---------------------------
def search_by_pass(self, pass_name):
    """
    Return all lots reachable from a pass using BFS.

    Parameters
    ----------
    pass_name : str
        The name of the parking pass to search for.

    Returns
    -------
    list
        List of lot names accessible by this pass.
    """
    if pass_name not in self.graph:
        raise ValueError(f"Pass '{pass_name}' not found in the graph.")

    # Perform a BFS from the pass node
    bfs_nodes = nx.bfs_tree(self.graph, source=pass_name).nodes()

    # Filters only lot nodes
    lots = [node for node in bfs_nodes if self.graph.nodes[node]['type'] == 'lot']

    return lots


    # ---------------------------
    # Search: Lot to Passes (Reverse)
    # ---------------------------
    def search_by_lot(self, lot_name):
        """Return all passes that can access a given lot."""
        pass

    # ---------------------------
    # DFS Validation / Connectivity
    # ---------------------------
    def validate_graph(self):
        """Use DFS to check if graph has isolated nodes."""
        pass

    # ---------------------------
    # Visualization
    # ---------------------------
    def draw_graph(self):
        """Draw the permissions graph."""
        pass

    # ---------------------------
    # Command Line Interface
    # ---------------------------
    def cli(self):
        """Simple CLI for Progress Report 1."""
        pass


# ---------------------------
# if __name__ block
# ---------------------------
if __name__ == "__main__":
    parking = UNLParking("src/data/parking_data.xlsx")
    parking.load_data()
    # parking.build_graph()
    # parking.cli()
