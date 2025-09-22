def test_smoke():
    """Basic smoke test"""
    assert 1 + 1 == 2

def test_python_version():
    """Check Python environment"""
    import sys
    assert sys.version_info.major == 3
    assert sys.version_info.minor >= 8
