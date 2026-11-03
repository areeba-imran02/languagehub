from dataclasses import dataclass
@dataclass
class AgentResult:
    agent: str
    output: dict
class BaseAgent:
    name='base'
    def run(self, payload:dict)->AgentResult: raise NotImplementedError
