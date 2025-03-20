import json

from critters import runner

class RunnerLogger:

    def __init__(self):
        self.name: str
        self.parents: str
        self.status: tuple = None
        self.genes: dict = None

    def read_runner(self, r: runner.Runner):
        r_genes = r.gene_dump()
        self.genes = empty_gene_dict()

        self.name = r.unique_id
        self.parents = str(r.parent_record)
        self.status = self._runner_status(r)
        self.genes.update({
            "bias" : r_genes[:4],
            "hunter_weightings" : r_genes[4:12],
            "runner_weightings" : r_genes[12:20],
            "obstacle_weightings" : r_genes[20:28],
            "impulsiveness" : r_genes[28]
        })
        
    def write_runner_log(self) -> str:
        # TODO keep on going!!
        return json.dumps({
            "name" : self.name,
            "parents" : self.parents,
            "status" : self.status,
            "genes" : self.genes
        })

    def _runner_status(self, r: runner.Runner):
        if r.escaped:
            return ("escaped", r.steps)
        elif not r.alive:
            return ("died", r.steps)
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
        