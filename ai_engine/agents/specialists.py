"""Focused agent prompt builders. They do not call models directly."""
from dataclasses import dataclass

@dataclass(frozen=True)
class AgentTask:
    name: str
    instruction: str

class SpecialistAgent:
    task = AgentTask('language_tutor', 'Teach clearly, correct gently, and give one useful example.')
    def build_prompt(self, text: str, target_language: str, explanation_language: str) -> str:
        return (f"Role: {self.task.name}. {self.task.instruction}\n"
                f"Target language: {target_language}. Explanation language: {explanation_language}.\n"
                f"User content:\n{text}\nReturn concise, accurate teaching feedback.")

class GrammarAgent(SpecialistAgent):
    task = AgentTask('grammar', 'Identify grammar patterns, explain the rule, and provide corrected examples.')
class VocabularyAgent(SpecialistAgent):
    task = AgentTask('vocabulary', 'Explain meaning, register, collocations, and natural example sentences.')
class WritingEvaluationAgent(SpecialistAgent):
    task = AgentTask('writing_evaluation', 'Review writing for clarity, grammar, vocabulary, and tone; distinguish corrections from stylistic suggestions.')
class ConversationAgent(SpecialistAgent):
    task = AgentTask('conversation', 'Roleplay naturally, stay in character, and adapt language complexity to the learner.')
class LessonGenerationAgent(SpecialistAgent):
    task = AgentTask('lesson_generation', 'Create a structured lesson with objectives, explanation, examples, practice, and answer key.')
class AssessmentAgent(SpecialistAgent):
    task = AgentTask('assessment', 'Create fair level-appropriate questions and explain assessed skills.')
class LearningProgressAgent(SpecialistAgent):
    task = AgentTask('learning_progress', 'Summarize only supplied learning records and recommend the next useful practice.')
class ReviewerAgent(SpecialistAgent):
    task = AgentTask('reviewer', 'Check factual accuracy, language correctness, level fit, and unsupported claims.')

AGENTS = {
    'tutor': SpecialistAgent(), 'grammar': GrammarAgent(), 'vocabulary': VocabularyAgent(),
    'writing': WritingEvaluationAgent(), 'conversation': ConversationAgent(),
    'lesson': LessonGenerationAgent(), 'assessment': AssessmentAgent(),
    'progress': LearningProgressAgent(), 'reviewer': ReviewerAgent(),
}
