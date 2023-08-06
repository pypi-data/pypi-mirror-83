from znop.core import ZnExpression, ZnEquation

def test_reduce_expr():
    assert str(ZnExpression(10, '3x*9+78-4x')) == '3x+8'
    assert str(ZnExpression(10, '(3x*9)+78-4x')) == '3x+8'

def test_reduce_eq():
    assert str(ZnEquation(8, '6(x-2)+5=3(5+x)')) == '3x=6'
    assert ZnEquation(8, '6(x-2)+5=3(5+x)').solve() == [2]
