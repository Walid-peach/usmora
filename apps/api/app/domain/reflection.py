from dataclasses import dataclass
from typing import Protocol

PROTOTYPE_DISCLAIMER = "Prototype aid — review it as a perspective, not objective truth."


@dataclass(frozen=True)
class Reflection:
    facts: list[str]
    assumptions: list[str]
    feelings: list[str]
    needs: list[str]
    draft: str
    disclaimer: str = PROTOTYPE_DISCLAIMER


class ReflectionProvider(Protocol):
    def reflect(self, situation: str) -> Reflection: ...


class DeterministicReflectionProvider:
    """A local, deterministic provider for prototype UX validation."""

    def reflect(self, situation: str) -> Reflection:
        cleaned = situation.strip()
        lowered = cleaned.lower()
        fact = cleaned.split(", and I felt", maxsplit=1)[0].rstrip(" .") + "."
        feeling = next(
            (
                word
                for word in ("frustrated", "hurt", "worried", "confused", "sad")
                if word in lowered
            ),
            "unsettled",
        )
        if any(word in lowered for word in ("late", "after", "time", "agreed")):
            need = "reliability and shared expectations"
        else:
            need = "clarity and mutual understanding"

        return Reflection(
            facts=[fact],
            assumptions=["The meaning or intention behind what happened is not yet confirmed."],
            feelings=[feeling],
            needs=[need],
            draft=(
                f"Hey, when {cleaned[0].lower() + cleaned[1:]} "
                f"I felt {feeling}. I value {need}. "
                "Could we agree on how to update each other and talk about what would work for us?"
            ),
        )
