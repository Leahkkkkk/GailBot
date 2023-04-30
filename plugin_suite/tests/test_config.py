from gb_hilab_suite.src.configs import load_label, load_internal_marker, load_threshold

def test_config():
    print(load_threshold())
    print(load_label())
    print(load_internal_marker())