"""Tests for spectrogram rendering."""

import numpy as np

from attention_algebra.spectrum import SpectrogramReader, TERMINAL_FREQS


def _sample_schedule(logic: str = "Orbital") -> dict:
    return {
        "original_expression": "(Ne ~ Ti)",
        "schedule_logic": logic,
        "global_frequency": 2.0,
        "fold_energy": None,
        "score": [
            {
                "voice": "Extraverted Intuition (Ne)",
                "symbol": "ExtrapolationObjective",
                "mass": 7.0,
                "formula": "e^{||s||}",
                "description": "Novelty",
                "role": "primary",
            },
            {
                "voice": "Introverted Thinking (Ti)",
                "symbol": "ContrastObjective",
                "mass": 5.0,
                "formula": "|d(a)-d(b)|",
                "description": "Discrimination",
                "role": "secondary",
            },
        ],
        "math_narrative": "Orbital interplay between novelty and logic.",
    }


def test_synthesize_produces_signal():
    reader = SpectrogramReader(duration=0.5)
    signal, labels, _ = reader.synthesize(_sample_schedule())
    assert len(signal) > 0
    assert labels == ["Ne", "Ti"]
    assert np.max(np.abs(signal)) <= 1.0


def test_render_returns_image():
    reader = SpectrogramReader(duration=0.5)
    result = reader.render(_sample_schedule())
    assert result.image.ndim == 3
    assert result.image.shape[2] == 3
    assert result.image.shape[0] > 64
    assert "Cognitive Spectrogram" in result.report
    assert "Ne" in result.report


def test_read_tuple_api():
    reader = SpectrogramReader(duration=0.5)
    image, report = reader.read(_sample_schedule("Linear"))
    assert isinstance(image, np.ndarray)
    assert "Dominant bands" in report or "Terminal" in report


def test_all_schedule_logics_smoke():
    reader = SpectrogramReader(duration=0.3)
    logics = [
        "Orbital",
        "Drag",
        "Stochastic Switching",
        "Adversarial",
        "Linear",
        "Cooperative Binding",
        "Feedback Loop",
        "Partial Adversarial",
        "Crossing Constraints",
        "Softmax Junction",
        "Amplified Binding",
        "Global Equilibrium",
        "Sequential Commitment",
    ]
    for logic in logics:
        sched = _sample_schedule(logic)
        if logic == "Global Equilibrium":
            sched["fold_energy"] = -8.0
        result = reader.render(sched)
        assert result.image.size > 0, f"Failed for {logic}"


def test_terminal_freq_ordering():
    assert TERMINAL_FREQS["Se"] < TERMINAL_FREQS["Fi"]