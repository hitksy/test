"""대화 세션 관리 모듈

상담 대화의 히스토리를 관리하고, 세션 상태를 추적합니다.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path


class SessionPhase(Enum):
    """상담 진행 단계"""
    INTRO = "도입"        # 라포 형성, 주제 파악
    EXPLORE = "탐색"      # 감정/경험 탐색
    UNDERSTAND = "이해"   # 핵심 감정, 패턴 발견
    INTEGRATE = "통합"    # 새로운 관점, 대처 방법 모색
    CLOSING = "마무리"    # 요약, 긍정적 메시지


@dataclass
class Message:
    """단일 메시지"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Session:
    """상담 세션"""
    messages: list[Message] = field(default_factory=list)
    phase: SessionPhase = SessionPhase.INTRO
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    mood_log: list[str] = field(default_factory=list)

    def add_message(self, role: str, content: str) -> None:
        self.messages.append(Message(role=role, content=content))

    def get_api_messages(self) -> list[dict]:
        """Anthropic API 형식의 메시지 리스트를 반환합니다."""
        return [{"role": m.role, "content": m.content} for m in self.messages]

    def message_count(self) -> int:
        return len(self.messages)

    def user_message_count(self) -> int:
        return sum(1 for m in self.messages if m.role == "user")

    def update_phase(self) -> None:
        """대화 진행 상황에 따라 세션 단계를 자동 업데이트합니다."""
        user_msgs = self.user_message_count()
        if user_msgs <= 2:
            self.phase = SessionPhase.INTRO
        elif user_msgs <= 6:
            self.phase = SessionPhase.EXPLORE
        elif user_msgs <= 10:
            self.phase = SessionPhase.UNDERSTAND
        elif user_msgs <= 14:
            self.phase = SessionPhase.INTEGRATE
        else:
            self.phase = SessionPhase.CLOSING

    def save(self, path: Path) -> None:
        """세션을 JSON 파일로 저장합니다."""
        data = {
            "started_at": self.started_at,
            "phase": self.phase.value,
            "mood_log": self.mood_log,
            "messages": [
                {"role": m.role, "content": m.content, "timestamp": m.timestamp}
                for m in self.messages
            ],
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    @classmethod
    def load(cls, path: Path) -> Session:
        """JSON 파일에서 세션을 복원합니다."""
        data = json.loads(path.read_text())
        session = cls(
            started_at=data["started_at"],
            phase=SessionPhase(data["phase"]),
            mood_log=data.get("mood_log", []),
        )
        for m in data["messages"]:
            session.messages.append(
                Message(role=m["role"], content=m["content"], timestamp=m["timestamp"])
            )
        return session
