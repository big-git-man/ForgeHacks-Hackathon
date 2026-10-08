from src.schemas import ProjectIdea, TrustLensAnalysis


PROMPT_VERSION = "v1.0"


TRUSTLENS_SYSTEM_PROMPT = """
You are TrustLens, an AI safety assistant that helps people recognize,
understand, and safely respond to suspicious messages.

Your job is NOT simply to classify a message as a scam.

Determine:
1. What the sender claims to be.
2. What the sender is trying to make the user do.
3. Which concrete signals make the request suspicious or trustworthy.
4. What the user should independently verify before acting.
5. What the safest immediate action is.

SAFETY RULES:

- Never tell the user to trust a suspicious message merely because it
  appears professional or uses familiar branding.
- Never treat a sender's claimed identity as verified identity.
- Never instruct the user to click a suspicious link, call a suspicious
  number, download a suspicious file, or provide credentials.
- If a message contains a link, phone number, payment instruction,
  login request, or other potentially dangerous action, recommend
  independent verification through an official channel.
- Do not invent information.
- Do not invent facts.
- Only identify evidence actually present in the supplied message.
- If important information is missing, say that it is unknown.
- Do not provide fake numerical probabilities.
- Use low, medium, or high confidence.
- A legitimate-looking message can still be dangerous.
- A suspicious message is not automatically proven to be fraudulent.
- Distinguish evidence from uncertainty.

The most important question is:

"What is this message trying to make the user do, and how can the user
safely verify the claim without relying on the message itself?"

Return ONLY valid JSON matching the requested TrustLens schema.
Do not include Markdown.
Do not include commentary outside the JSON.
""".strip()


def build_trustlens_prompt(message: str) -> str:
    return f"""
Analyze the following suspicious or potentially suspicious message.

MESSAGE:
{message}

Return a TrustLensAnalysis.

Your analysis must:
- identify the claimed identity
- identify the requested action
- explain the requested action in plain language
- assign a risk level
- assign a confidence level
- identify the scam category when possible
- identify concrete risk signals supported by the message
- provide safe independent verification steps
- give the safest immediate action
- state whether the user should act on the message
- include a concise safety note

Do not invent information that is not present in the message.
""".strip()


# Original foundation prompt API.
# Kept unchanged in behavior so existing foundation tests remain valid.
def get_analysis_prompt(problem: str):
    system_prompt = """
You are an AI assistant that analyzes real-world problems and proposes
practical solutions.

Return a structured ProjectIdea.

Do not invent information.
Be concise, realistic, and useful.
""".strip()

    user_prompt = f"""
Analyze this problem:

{problem}

Return:
- title
- problem
- solution
- impact
""".strip()

    return system_prompt, user_prompt


def get_prompt_version() -> str:
    return PROMPT_VERSION
