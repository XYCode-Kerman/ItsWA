from ccf_parser import CheckPoint


def test_full_compare():
    ckpt = CheckPoint(
        input='',
        answer='test\ntest',
        comparator='full',
        input_type='STDIN',
        output_type='STDOUT'
    )

    assert ckpt.compare('test\ntest') is True
    assert ckpt.compare('  test\ntest') is False
    assert ckpt.compare('test\ntest  ') is False
    assert ckpt.compare('test  \n  test') is False


def test_full_strip():
    ckpt = CheckPoint(
        input='',
        answer='test\ntest',
        comparator='full_strip',
        input_type='STDIN',
        output_type='STDOUT'
    )

    assert ckpt.compare('test\ntest') is True
    assert ckpt.compare('  test\ntest') is True
    assert ckpt.compare('test\ntest  ') is True
    assert ckpt.compare('test  \n  test') is False


def test_line():
    ckpt = CheckPoint(
        input='',
        answer='test\ntest',
        comparator='line',
        input_type='STDIN',
        output_type='STDOUT'
    )

    assert ckpt.compare('test\ntest') is True
    assert ckpt.compare('  test\ntest') is False
    assert ckpt.compare('test\ntest  ') is False
    assert ckpt.compare('test  \n  test') is False


def test_line_strip():
    ckpt = CheckPoint(
        input='',
        answer='test\ntest',
        comparator='line_strip',
        input_type='STDIN',
        output_type='STDOUT'
    )

    assert ckpt.compare('test\ntest') is True
    assert ckpt.compare('  test\ntest') is True
    assert ckpt.compare('test\ntest  ') is True
    assert ckpt.compare('test  \n  test') is True
    assert ckpt.compare('test  \ntest') is True
    assert ckpt.compare('test\n    test   ') is True


def test_decimal_3():
    ckpt = CheckPoint(
        input='',
        answer='1',
        comparator='decimal_3',
        input_type='STDIN',
        output_type='STDOUT'
    )

    assert ckpt.compare('1') is True
    assert ckpt.compare('2') is False
    assert ckpt.compare('1.1') is False
    assert ckpt.compare('1.01') is False
    assert ckpt.compare('1.001') is True
    assert ckpt.compare('1.0009') is True
    assert ckpt.compare('1.00099') is True
    assert ckpt.compare('big brother is watching you!') is False
