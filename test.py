

from plant import Plant

class Test:
    def __init__(self, dna):
        """
        Initializes the Test class with plant DNA.

        Args:
            dna (dict): Growth rules for the plant.
        """
        self.dna = dna

    def sow(self, time_simulated):
        """
        Grows a plant using the specified DNA and time simulation.

        Args:
            time_simulated (int): The number of growth cycles to simulate.
        """
        seed = Plant(width=1.0, height=1.0, orientation=0.0, dna=self.dna)
        seed.grow(time_simulated)
        graph = seed.export_to_graphviz()
        graph.render("plant_tree", view=True)
