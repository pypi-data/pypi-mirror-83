from helloNoushi import sayhello

def test_helloworld_no_param():
    assert sayhello() == "Hello Lovely World ...!!!"

def test_helloworld_with_param():
    assert sayhello('guys') == "Hello Lovely guys ...!!!"


