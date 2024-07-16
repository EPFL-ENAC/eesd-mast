from pydantic import BaseModel


class Counts(BaseModel):
    experiments_count: int
    models_count: int
    references_count: int
    run_results_count: int
