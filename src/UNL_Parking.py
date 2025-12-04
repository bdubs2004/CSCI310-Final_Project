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
import matplotlib.pyplot as plt


class UNLParking:
    """
    Main class for building and querying the UNL parking graph.

    Parameters
    ----------
    filepath : str or Path
        Path to the Excel file containing UNL parking data.

    Attributes
    ----------
    filepath : Path
        Filepath to the dataset.
    df : pandas.DataFrame or None
        Loaded dataset.
    graph : networkx.DiGraph
        Directed graph containing passes and lots.
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
        """
        Load the Excel dataset into a DataFrame.

        Returns
        -------
        pandas.DataFrame
            The loaded dataset.
        """
        self.df = pd.read_excel(self.filepath)
        return self.df

    # ---------------------------
    # Graph Construction
    # ---------------------------
    def build_graph(self):
        """
        Build the pass to lot graph using the dataset.

        Nodes
        -----
        - Pass nodes (type='pass')
        - Lot nodes (type='lot')

        Edges
        -----
        - A directed edge is added from each pass to each lot it allows.

        Raises
        ------
        ValueError
            If data has not been loaded before calling this method.
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

            # Handle multiple
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
        list of str
            List of lot names accessible by this pass.

        Raises
        ------
        ValueError
            If the pass name is not found in the graph.
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
        """
        Return all passes that can access a given lot.

        Parameters
        ----------
        lot_name : str
            The name of the parking lot to search for.

        Returns
        -------
        list of str
            List of passes that can access the specified lot.

        Raises
        ------
        ValueError
            If the lot name is not found in the graph.
        """
        if lot_name not in self.graph:
            raise ValueError(f"Lot '{lot_name}' not found in the graph.")

        # Incoming edges point from passes to this lot
        passes = [
            node for node in self.graph.predecessors(lot_name)
            if self.graph.nodes[node]['type'] == 'pass'
        ]

        return passes

    # ---------------------------
    # DFS Connectivity Search
    # ---------------------------
    def validate_graph(self):
        """
        Check for isolated nodes in the graph.

        Returns
        -------
        dict
            A dictionary with two lists:
            - isolated_passes : list of str
                Passes with no edges.
            - isolated_lots : list of str
                Lots with no edges.
        """
        isolated_passes = []
        isolated_lots = []

        for node, data in self.graph.nodes(data=True):
            if self.graph.degree(node) == 0:
                if data['type'] == 'pass':
                    isolated_passes.append(node)
                elif data['type'] == 'lot':
                    isolated_lots.append(node)

        return {
            'isolated_passes': isolated_passes,
            'isolated_lots': isolated_lots
        }

    # ---------------------------
    # Visualizations
    # ---------------------------
    def draw_graph(self):
        """
        Draw a left-right graph showing passes on the left and
        lots on the right. Passes are drawn as blue squares, lots as green
        rectangles.

        Notes
        -----
        - Uses a custom vertical spacing layout.
        - Uses matplotlib patches for shapes.
        - Shows arrows representing allowed parking relationships.
        """

        pass_nodes = [n for n, attr in self.graph.nodes(data=True) if attr['type'] == 'pass']
        lot_nodes = [n for n, attr in self.graph.nodes(data=True) if attr['type'] == 'lot']

        # Vertical positions with total_height fraction
        def vertical_positions(nodes, x_pos, total_height=0.9):
            """
            Compute evenly spaced vertical positions for a column of nodes.

            Parameters
            ----------
            nodes : list of str
                Node names.
            x_pos : float
                The x-coordinate to assign to each node.
            total_height : float, optional
                Fraction of vertical axis to occupy.

            Returns
            -------
            dict
                Mapping of node → (x, y) coordinates.
            """
            n = len(nodes)
            if n == 1:
                return {nodes[0]: (x_pos, 0.5)}
            spacing = total_height / (n - 1)
            start = (1 - total_height) / 2
            return {node: (x_pos, start + i * spacing) for i, node in enumerate(nodes)}

        pos = {}
        pos.update(vertical_positions(pass_nodes, x_pos=0, total_height=0.9))
        pos.update(vertical_positions(lot_nodes, x_pos=2, total_height=0.9))

        fig, ax = plt.subplots(figsize=(12, 6))

        # Draw pass nodes as squares
        square_size = 0.06
        for node in pass_nodes:
            x, y = pos[node]
            rect = plt.Rectangle(
                (x - square_size/2, y - square_size/2),
                square_size,
                square_size,
                facecolor='lightblue',
                edgecolor='black',
                linewidth=1.5
            )
            ax.add_patch(rect)

        # Draw lot nodes as rectangles
        rect_width = 0.75
        rect_height = 0.06
        for node in lot_nodes:
            x, y = pos[node]
            rect = plt.Rectangle(
                (x - rect_width / 2, y - rect_height / 2),
                rect_width,
                rect_height,
                facecolor='lightgreen',
                edgecolor='black',
                linewidth=1.5
            )
            ax.add_patch(rect)

        # Draw edges
        for start, end in self.graph.edges():
            x1, y1 = pos[start]
            x2, y2 = pos[end]
            ax.annotate(
                '',
                xy=(x2, y2),
                xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='gray', lw=1.2)
            )

        # Draw labels
        for node, (x, y) in pos.items():
            ax.text(x, y, node, fontsize=8, ha='center', va='center')

        # Legend
        ax.scatter([], [], c='lightblue', marker='s', s=200, label='Passes')
        ax.scatter([], [], c='lightgreen', marker='s', s=200, label='Lots')
        ax.legend(loc='lower right')

        # Axis settings
        ax.set_xlim(-0.5, 2.5 + rect_width/2)
        ax.set_ylim(0, 1)
        ax.axis('off')
        plt.title("UNL Parking Pass → Lot Graph")
        plt.tight_layout()
        plt.show()

    # ---------------------------
    # Command Line Interface
    # ---------------------------
    def cli(self):
        """
        Run an interactive command line interface for users to query
        pass to lot and lot to pass.

        Commands
        --------
        - 'P' : Search by pass
        - 'L' : Search by lot
        - 'quit' : Exit the program

        Notes
        -----
        Provides text prompts and prints search results to the console.
        """

        print("Welcome to the UNL Parking Graph Search Tool!")
        print("Type 'P' to search by Pass, 'L' to search by Lot, or 'quit' to exit: ")

        while True:
            choice = input("\nSearch by (P)ass or (L)ot? Or type 'quit' to quit:").strip().upper()

            if choice == 'QUIT':
                print("Exiting UNL Parking Graph Search Tool. Goodbye!")
                break
            elif choice == 'P':
                pass_name = input("Enter Pass name: ").strip()
                try:
                    lots = self.search_by_pass(pass_name)
                    if lots:
                        print(f"You can park in: {', '.join(lots)}")
                    else:
                        print(f"No lots found for pass '{pass_name}'.")
                except ValueError as e:
                    print(e)
            elif choice == 'L':
                lot_name = input("Enter Lot name: ").strip()
                try:
                    passes = self.search_by_lot(lot_name)
                    if passes:
                        print(f"Passes that can access '{lot_name}': {', '.join(passes)}")
                    else:
                        print(f"No passes found for lot '{lot_name}'.")
                except ValueError as e:
                    print(e)
            else:
                print("Invalid choice. Type 'P', 'L', or 'quit'.")


# ---------------------------
# Script Execution
# ---------------------------
if __name__ == "__main__":
    # Opens data
    parking = UNLParking("UNL_Parking.xlsx")

    # Load the data
    parking.load_data()

    # Build the graph
    parking.build_graph()

    # Validate graph
    isolated = parking.validate_graph()
    if isolated['isolated_passes'] or isolated['isolated_lots']:
        print("Warning: There are isolated nodes in the graph.")
        print("Isolated passes:", isolated['isolated_passes'])
        print("Isolated lots:", isolated['isolated_lots'])

    # Draw the graph every time
    parking.draw_graph()

    # Launch the CLI
    parking.cli()
