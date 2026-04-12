"""심리상담 에이전트 핵심 모듈

Anthropic Claude API를 사용하여 심리상담을 제공하는 에이전트입니다.
"""

from __future__ import annotations

import anthropic

from .conversation import Session
from .prompts import build_system_prompt
from .techniques import CRISIS_RESPONSE, detect_crisis


class CounselorAgent:
    """AI 심리상담 에이전트"""

    def __init__(
        self,
        model: str = "claude-sonnet-4-6",
        max_tokens: int = 1024,
    ):
        self.client = anthropic.Anthropic()
        self.model = model
        self.max_tokens = max_tokens
        self.system_prompt = build_system_prompt()
        self.session = Session()

    def respond(self, user_input: str) -> str:
        """사용자 입력에 대한 상담 응답을 생성합니다.

        위기 상황이 감지되면 즉시 위기 대응 메시지를 반환하고,
        일반적인 경우 Claude API를 통해 공감적 상담 응답을 생성합니다.
        """
        # 위기 상황 감지
        if detect_crisis(user_input):
            self.session.add_message("user", user_input)
            crisis_msg = CRISIS_RESPONSE
            self.session.add_message("assistant", crisis_msg)
            return crisis_msg

        # 세션에 사용자 메시지 추가
        self.session.add_message("user", user_input)
        self.session.update_phase()

        # 현재 단계 정보를 시스템 프롬프트에 추가
        phase_context = (
            f"\n\n[현재 상담 단계: {self.session.phase.value}] "
            f"이 단계에 적합한 상담 접근을 사용하세요."
        )
        system = self.system_prompt + phase_context

        # API 호출
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system,
            messages=self.session.get_api_messages(),
        )

        assistant_message = response.content[0].text

        # 세션에 응답 저장
        self.session.add_message("assistant", assistant_message)

        return assistant_message

    def get_session_summary(self) -> str:
        """현재 세션 요약 정보를 반환합니다."""
        return (
            f"상담 단계: {self.session.phase.value}\n"
            f"총 대화 수: {self.session.message_count()}회\n"
            f"내담자 발화: {self.session.user_message_count()}회"
        )
