# jdparsing/tests/test_jd_parser.py
import pytest
from jdparsing.jd_parser import parse_jd
from jdparsing.tests.sample_jds import SIMPLE_JD

def test_parse_simple_jd():
    out = parse_jd(SIMPLE_JD)
    assert "python" in [s.lower() for s in out.skills_hard]
    assert out.experience.min_years == 5 or out.experience.min_years >= 5
    assert any("Bachelor" in e for e in out.education)
    assert any("aws" in c.lower() for c in out.certifications)
