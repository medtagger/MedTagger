from data_labeling.hello_world import say_hello


def test_say_hello():
    """Test if function say hello and always return 4"""
    assert say_hello() == 4
