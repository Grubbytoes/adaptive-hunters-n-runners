from .abstract_logger import AbstractLogger
from critters import runner

class RunnerLogger(AbstractLogger):

    def __init__(self, r: runner.Runner=None):
        super().__init__()
        
        self.name: str
        self.parents: str
        self.status: tuple
        self.genes: tuple
        
        if r is not None:
            self.read(r)

    def read(self, r: runner.Runner):
        self.genes = tuple(r.gene_dump())
        self.name = r.unique_id
        self.parents = str(r.parent_record)
        self.status = self._runner_status(r)
        
        self.payload = {
            "name" : self.name,
            "parents" : self.parents,
            "status" : self.status,
            "genes" : readable_gene_dict(self.genes)
        }

    def _runner_status(self, r: runner.Runner):
        if r.escaped:
            return ("escaped", r.steps)
        elif not r.alive:
            return ("died", r.steps, r.pos[1])
        else:
            return ("lost",)


def empty_gene_dict() -> dict:
    return {
        "bias" : [],
        "hunter_weightings" : [],
        "runner_weightings" : [],
        "obstacle_weightings" : [],
        "impulsiveness" : []
    }


def readable_gene_dict(raw_genes: tuple):
    if 28 > len(raw_genes):
        raise Exception("Not enough genes, my guy")
    
    return {
        "bias" : raw_genes[:4],
        "hunter_weightings" : raw_genes[4:12],
        "runner_weightings" : raw_genes[12:20],
        "obstacle_weightings" : raw_genes[20:28],
        "impulsiveness" : raw_genes[28]
    }
        