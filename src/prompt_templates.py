from dataclasses import dataclass


@dataclass
class PromptTemplate:
    system: str
    user_template: str

    def build(self, **kwargs) -> tuple[str, str]:
        return self.system.strip(), self.user_template.format(**kwargs).strip()


GENERAL_ANALYSIS = PromptTemplate(
    system="""
You are an AI assistant helping solve practical real-world problems.

Prioritize:
- Accuracy
- Practicality
- Technical feasibility
- Clear reasoning
- Real-world usefulness

Do not invent facts.
If information is unknown, say so clearly.
""",
    user_template="""
Analyze the following problem:

{problem}

Identify:
1. The core problem
2. The target users
3. Possible solution approaches
4. Where AI provides meaningful value
5. Expected real-world impact
""",
)


def build_analysis_prompt(problem: str) -> tuple[str, str]:
    return GENERAL_ANALYSIS.build(problem=problem)
