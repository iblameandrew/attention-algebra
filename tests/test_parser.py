"""Tests for Cognitive Algebra expression validation."""

from attention_algebra.parser import (
    are_complementary,
    extract_terminals,
    validate_expression,
)


def test_extract_terminals_with_mass():
    found = extract_terminals("7Se oo 3Si -> Ni")
    assert found == [("Se", 7), ("Si", 3), ("Ni", None)]


def test_complementarity_regime_a():
    assert are_complementary("Se", "Si")
    assert are_complementary("Fe", "Fi")


def test_complementarity_regime_b():
    assert are_complementary("Se", "Ni")
    assert are_complementary("Te", "Fi")


def test_valid_orbit():
    result = validate_expression("(Ne ~ Ti)")
    assert result.valid
    assert ("Ne", None) in result.terminals


def test_invalid_orbit_same_domain():
    result = validate_expression("Se ~ Si")
    assert not result.valid
    assert any("Orbit" in e for e in result.errors)


def test_valid_opposition():
    result = validate_expression("7Se oo 3Si -> Ni")
    assert result.valid


def test_invalid_stem_pair():
    result = validate_expression("5Ne :: 3Te")
    assert not result.valid
    assert any("Stem pair" in e for e in result.errors)


def test_valid_stem_pair_cross_axis():
    result = validate_expression("5Ne :: 3Si")
    assert result.valid


def test_valid_stem_pair_attitude():
    result = validate_expression("5Ne :: 4Ni")
    assert result.valid


def test_hairpin_expression():
    result = validate_expression("^(5Ni)")
    assert result.valid
    assert result.terminals == [("Ni", 5)]