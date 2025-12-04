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
        Build the pass→lot graph using the loaded data.
        Nodes: passes + lots
        Edges: which passes allow which lots
        """
        pass

    # ---------------------------
    # Search: Pass → Lots (BFS)
    # ---------------------------
    def search_by_pass(self, pass_name):
        """Return all lots reachable from a pass using BFS."""
        pass

    # ---------------------------
    # Search: Lot → Passes (Reverse)
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
    # Visualization (Matplotlib + NetworkX)
    # ---------------------------
    def draw_graph(self):
        """Draw the permissions graph."""
        pass

    # ---------------------------
    # Command-Line Interface
    # ---------------------------
    def cli(self):
        """Simple CLI for Progress Report 1."""
        pass


# ---------------------------
# Script Execution
# ---------------------------
if __name__ == "__main__":
    parking = UNLParking("src/data/parking_data.xlsx")
    parking.load_data()
    # parking.build_graph()
    # parking.cli()
