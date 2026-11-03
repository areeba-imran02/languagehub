from ai_engine.agents.base import BaseAgent,AgentResult
class TutorAgent(BaseAgent):
    name='language_tutor'
    def run(self,payload):
        required={'message','target_language','known_language'}
        missing=required-set(payload)
        if missing: raise ValueError(f"Missing fields: {', '.join(sorted(missing))}")
        return AgentResult(self.name,{"task":"tutor_response","input":payload,"status":"ready_for_model"})
