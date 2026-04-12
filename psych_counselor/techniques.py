"""심리상담 기법 정의 모듈

각 상담 기법의 설명, 적용 시점, 예시 응답 패턴을 정의합니다.
"""

from dataclasses import dataclass


@dataclass
class CounselingTechnique:
    name: str
    description: str
    when_to_use: str
    example_pattern: str


TECHNIQUES = {
    "active_listening": CounselingTechnique(
        name="적극적 경청",
        description="내담자의 말을 주의 깊게 듣고, 핵심 내용을 반영하여 되돌려줍니다.",
        when_to_use="내담자가 자신의 이야기를 꺼낼 때, 감정을 표현할 때",
        example_pattern="~라고 느끼셨군요. / ~한 경험을 하셨네요.",
    ),
    "emotion_validation": CounselingTechnique(
        name="감정 인정 및 수용",
        description="내담자의 감정을 있는 그대로 인정하고, 그 감정이 자연스러운 것임을 전달합니다.",
        when_to_use="내담자가 부정적 감정(분노, 슬픔, 불안 등)을 표현할 때",
        example_pattern="그런 상황에서 ~하게 느끼시는 건 매우 자연스러운 반응이에요.",
    ),
    "open_questions": CounselingTechnique(
        name="개방형 질문",
        description="예/아니오로 답할 수 없는 질문을 통해 내담자의 생각과 감정을 더 깊이 탐색합니다.",
        when_to_use="내담자의 경험을 더 깊이 이해하고 싶을 때",
        example_pattern="그때 어떤 기분이 드셨나요? / 그 상황에서 가장 힘들었던 부분은 무엇인가요?",
    ),
    "reframing": CounselingTechnique(
        name="인지적 재구성 (리프레이밍)",
        description="부정적인 사고 패턴을 새로운 관점에서 바라볼 수 있도록 돕습니다.",
        when_to_use="내담자가 부정적 사고 패턴에 갇혀 있을 때",
        example_pattern="다른 관점에서 보면 ~일 수도 있지 않을까요?",
    ),
    "summarizing": CounselingTechnique(
        name="요약 및 정리",
        description="대화 내용을 중간중간 요약하여 내담자가 자신의 상황을 객관적으로 바라보게 합니다.",
        when_to_use="대화가 길어졌거나, 주제가 여러 가지로 흩어졌을 때",
        example_pattern="지금까지 말씀해 주신 내용을 정리해 보면...",
    ),
    "grounding": CounselingTechnique(
        name="그라운딩 기법",
        description="현재 순간에 집중하도록 도와 불안이나 공황 상태를 완화합니다.",
        when_to_use="내담자가 강한 불안이나 공황 증상을 보일 때",
        example_pattern="지금 주변에서 보이는 것 5가지를 말씀해 주시겠어요?",
    ),
    "strength_based": CounselingTechnique(
        name="강점 기반 접근",
        description="내담자의 강점과 자원을 발견하고 강화합니다.",
        when_to_use="내담자가 자존감이 낮거나 무력감을 느낄 때",
        example_pattern="그 어려운 상황에서도 ~하신 것은 정말 대단한 일이에요.",
    ),
}

# 위기 상황 키워드 목록
CRISIS_KEYWORDS = [
    "자살", "죽고 싶", "죽고싶", "자해", "목숨", "세상을 떠나",
    "살고 싶지 않", "살기 싫", "끝내고 싶", "없어지고 싶",
    "사라지고 싶", "죽을", "죽어버리",
]

CRISIS_RESPONSE = """지금 많이 힘드시고 고통스러우시군요.
당신의 고통을 진심으로 이해합니다.

지금 바로 전문적인 도움을 받으실 수 있습니다:

  - 자살예방상담전화: 1393 (24시간)
  - 정신건강위기상담전화: 1577-0199 (24시간)
  - 생명의전화: 1588-9191 (24시간)

전문 상담사와 이야기하는 것이 지금 가장 도움이 될 수 있습니다.
당신은 혼자가 아니며, 도움을 요청하는 것은 매우 용기 있는 일입니다."""


def detect_crisis(text: str) -> bool:
    """내담자의 메시지에서 위기 상황 키워드를 탐지합니다."""
    return any(keyword in text for keyword in CRISIS_KEYWORDS)
