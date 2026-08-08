from app.domain.reflection import DeterministicReflectionProvider


def test_provider_returns_structured_prototype_reflection() -> None:
    provider = DeterministicReflectionProvider()

    result = provider.reflect(
        "My housemate arrived after our agreed cooking time, and I felt frustrated."
    )

    assert result.facts == ["My housemate arrived after our agreed cooking time."]
    assert result.assumptions == [
        "The meaning or intention behind what happened is not yet confirmed."
    ]
    assert result.feelings == ["frustrated"]
    assert result.needs == ["reliability and shared expectations"]
    assert result.draft.startswith("Hey, when")
    assert "Could we agree on how to update each other" in result.draft
    assert result.disclaimer == "Prototype aid — review it as a perspective, not objective truth."
