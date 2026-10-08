from typing import Literal

from pydantic import BaseModel, Field


class ProjectIdea(BaseModel):
    title: str
    problem: str
    solution: str
    impact: str


RiskLevel = Literal[
    "low",
    "medium",
    "high",
    "critical",
]

ConfidenceLevel = Literal[
    "low",
    "medium",
    "high",
]

ScamCategory = Literal[
    "phishing",
    "impersonation",
    "payment_fraud",
    "credential_theft",
    "account_takeover",
    "delivery_scam",
    "job_scam",
    "investment_scam",
    "romance_scam",
    "social_engineering",
    "ai_impersonation",
    "malware",
    "other",
    "unclear",
]

RequestedAction = Literal[
    "click_link",
    "make_payment",
    "share_credentials",
    "share_personal_information",
    "download_file",
    "reply",
    "call_number",
    "transfer_money",
    "login",
    "share_verification_code",
    "other",
    "none",
    "unclear",
]


class RiskSignal(BaseModel):
    signal: str = Field(min_length=1, max_length=300)
    explanation: str = Field(min_length=1, max_length=600)


class VerificationStep(BaseModel):
    step: str = Field(min_length=1, max_length=300)
    reason: str = Field(min_length=1, max_length=500)


class TrustLensAnalysis(BaseModel):
    risk_level: RiskLevel
    confidence: ConfidenceLevel
    scam_category: ScamCategory

    claimed_identity: str = Field(
        min_length=1,
        max_length=300,
    )

    requested_action: RequestedAction

    requested_action_detail: str = Field(
        min_length=1,
        max_length=500,
    )

    summary: str = Field(
        min_length=1,
        max_length=800,
    )

    risk_signals: list[RiskSignal] = Field(
        min_length=1,
        max_length=8,
    )

    verification_steps: list[VerificationStep] = Field(
        min_length=1,
        max_length=6,
    )

    immediate_action: str = Field(
        min_length=1,
        max_length=500,
    )

    should_act: bool

    safety_note: str = Field(
        min_length=1,
        max_length=500,
    )
