from ideas.examples import nobreak
# from ideas.import_hook import remove_hook


def test_for():
    source_for = """
    for i in range(10):
        pass
    %s:
        pass"""

    source = source_for % "nobreak"
    result = nobreak.nobreak_as_a_keyword(source)
    expected = source_for % "else"

    assert result == expected, "nobreak with for"


def test_while():
    source_while = """
    while True:
        pass
    %s:
        pass"""

    source = source_while % "nobreak"
    result = nobreak.nobreak_as_a_keyword(source)
    expected = source_while % "else"

    assert result == expected, "nobreak with while"


if __name__ == '__main__':
    test_for()
    print("test_nobreak was run successfully.")
