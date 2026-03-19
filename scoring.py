class GradeEngine:
    def __init__(self, graph, alpha=0.7):
        self.graph = graph
        self.alpha = alpha

    def compute(self):
        topo_order = self.graph.topological_sort()

        for course in topo_order:
            course.compute_effective(self.alpha)
