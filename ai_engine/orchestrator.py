from ai_engine.agents.tutor import TutorAgent
class AgentOrchestrator:
    """Deterministic dispatcher; agents do not recursively invoke each other."""
    def __init__(self): self.agents={'tutor':TutorAgent()}
    def execute(self,task:str,payload:dict):
        if task not in self.agents: raise ValueError(f"Unknown task: {task}")
        return self.agents[task].run(payload)
