from src.trustlens_schema import TrustLensAnalysis
from src.trustlens_prompts import (
    TRUSTLENS_SYSTEM_PROMPT,
    build_trustlens_prompt,
)


def test_trustlens_schema_accepts_valid_analysis():
    result = TrustLensAnalysis(
        risk_level="high",
        confidence="high",
        scam_category="phishing",
        claimed_identity="A delivery company",
        requested_action="click_link",
        requested_action_detail="Click a link to pay a delivery fee.",
        summary="The message creates urgency and asks the recipient to use an external payment link.",
        risk_signals=[
            {
                "signal": "Urgency",
                "explanation": "The message pressures the recipient to act immediately.",
            },
            {
                "signal": "External payment link",
                "explanation": "The message asks the recipient to make a payment through a supplied link.",
            },
        ],
        verification_steps=[
            {
                "step": "Open the delivery company's official website independently.",
                "reason": "This avoids relying on the contact information supplied by the suspicious message.",
            }
        ],
        immediate_action="Do not click the link or make the payment until the delivery claim is independently verified.",
        should_act=False,
        safety_note="The message's claimed identity has not been independently verified.",
    )

    assert result.risk_level == "high"
    assert result.should_act is False
    assert len(result.risk_signals) == 2


def test_trustlens_prompt_contains_message():
    message = "Your account will be suspended. Click here immediately."

    prompt = build_trustlens_prompt(message)

    assert message in prompt
    assert "requested action" in prompt.lower()
    assert "verification" in prompt.lower()


def test_trustlens_system_prompt_requires_json():
    assert "valid JSON" in TRUSTLENS_SYSTEM_PROMPT
    assert "Do not invent information" in TRUSTLENS_SYSTEM_PROMPT
