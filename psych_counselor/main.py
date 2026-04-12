"""심리상담 에이전트 CLI 메인 모듈

터미널에서 대화형 심리상담을 진행할 수 있는 인터페이스입니다.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.theme import Theme

from .agent import CounselorAgent
from .prompts import DISCLAIMER, GREETING_MESSAGE

custom_theme = Theme({
    "counselor": "cyan",
    "user_label": "green",
    "info": "dim",
})

console = Console(theme=custom_theme)


def print_counselor(text: str) -> None:
    """상담사 응답을 패널 형태로 출력합니다."""
    console.print()
    console.print(
        Panel(
            Markdown(text),
            title="[counselor]상담사[/counselor]",
            border_style="cyan",
            padding=(1, 2),
        )
    )


def print_disclaimer() -> None:
    """면책 안내 메시지를 출력합니다."""
    console.print()
    console.print(
        Panel(
            DISCLAIMER,
            border_style="yellow",
            padding=(1, 2),
        )
    )


def run(model: str = "claude-sonnet-4-6", save_dir: str | None = None) -> None:
    """대화형 상담 세션을 실행합니다."""
    agent = CounselorAgent(model=model)

    # 면책 안내 및 인사
    print_disclaimer()
    print_counselor(GREETING_MESSAGE)
    console.print()
    console.print("[info]종료: 'quit' 또는 'exit' 입력 | 세션 저장: 'save'[/info]")
    console.print("[info]세션 정보: 'status'[/info]")
    console.print()

    while True:
        try:
            user_input = console.input("[user_label]나 > [/user_label]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n")
            break

        if not user_input:
            continue

        # 특수 명령어 처리
        if user_input.lower() in ("quit", "exit", "종료"):
            print_counselor(
                "오늘 이야기를 나눠 주셔서 감사합니다. "
                "언제든 다시 찾아오셔도 좋습니다. 편안한 하루 보내세요."
            )
            break

        if user_input.lower() == "save":
            if save_dir:
                save_path = Path(save_dir)
            else:
                save_path = Path.home() / ".psych_counselor" / "sessions"
            filename = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = save_path / filename
            agent.session.save(filepath)
            console.print(f"[info]세션이 저장되었습니다: {filepath}[/info]")
            continue

        if user_input.lower() == "status":
            console.print(f"[info]{agent.get_session_summary()}[/info]")
            continue

        # 상담 응답 생성
        with console.status("[counselor]생각하고 있어요...[/counselor]", spinner="dots"):
            try:
                response = agent.respond(user_input)
            except Exception as e:
                console.print(f"[red]오류가 발생했습니다: {e}[/red]")
                continue

        print_counselor(response)
        console.print()


def main() -> None:
    parser = argparse.ArgumentParser(description="AI 심리상담 에이전트")
    parser.add_argument(
        "--model",
        default="claude-sonnet-4-6",
        help="사용할 Claude 모델 (기본: claude-sonnet-4-6)",
    )
    parser.add_argument(
        "--save-dir",
        default=None,
        help="세션 저장 디렉토리",
    )
    args = parser.parse_args()
    run(model=args.model, save_dir=args.save_dir)


if __name__ == "__main__":
    main()
