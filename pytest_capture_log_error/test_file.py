import a_file

def test_a(capsys):
    assert a_file.bla() == 5
    assert a_file.LOG_MESSAGE in capsys.readouterr().err
