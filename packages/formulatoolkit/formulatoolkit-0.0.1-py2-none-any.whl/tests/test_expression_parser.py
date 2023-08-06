
import math
import pytest

from FormulaToolkit import Parser
from FormulaToolkit import InvalidExpressionError, ParsingError, EpressionParityError, UndefinedVariableError, NotAFunctionError

@pytest.fixture()
def parser():
    parser = Parser()
    yield parser.evaluate
    del parser

def test_parser_trigonometric(parser):
    assert 1 == parser('sin(1)^2+cos(1)^2', {})
    assert 1 == parser('sin(x)^2+cos(x)^2', {'x':1})

def test_parser_max_min(parser):
    assert 10 == parser('max(1,2,3,4,5,6,7,8,10)', {})
    assert 1  == parser('min(1,2,3,4,5,6,7,8,10)', {})

def test_parser_if(parser):
    assert 'blue' == parser("if(0,'red', 'blue')",{'red': '', 'blue': ''})
    assert 'red'  == parser("if(1,'red', 'blue')",{'red': '', 'blue': ''})

def test_parser_constants(parser):
    assert math.e == parser('E', {})
    assert math.pi == parser('PI', {})

def test_parser_concat(parser):
    assert 'pippo' == parser("concat('pip', 'po')", {})
    assert 'pippo' == parser("concat('p','i','p','p','o')", {})

def test_parser_pitagora(parser):
    assert 5 == parser('pyt(a,b)',{'a': 3,'b':4})

def test_parser_nested_simple_1(parser):
    assert 6 == parser('a+(b+c)',{'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8})

def test_parser_nested_simple_1(parser):
    assert 2.25 == parser('a+(b+c)/d',{'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8})

def test_parser_nested_simple_2(parser):
    assert 3.25 == parser('a+(b+c)/d-e+f',{'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8})

def test_parser_nested(parser):
    assert 5.25 == parser('a+(b+c)/d-e+f-h/d*a+floor(sin(sqrt(g))*10)',{'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8})


@pytest.mark.parametrize("expression, vars, expected", 
                         [  ('1+1', {}, 1+1), 
                            ('1-1', {}, 1-1),
                            ('1*1', {}, 1*1), 
                            ('1/1', {}, 1/1), 
                            ('1%1', {}, 0), 
                            ('1^1', {}, 1), 
                            ('1,1', {}, [1,1]), 
                            ('1||1',{}, '1.01.0'), 
                            ('1==1',{}, 1==1), 
                            ('1!=1',{}, 1!=1), 
                            ('1>1', {}, 1>1), 
                            ('1<1', {}, 1<1),
                            ('1<=1', {}, 1<=1),                                                         
                            ('1>=1', {}, 1>=1),                                                         
                            ('1 and 1', {}, 1 and 1), 
                            ('1 or 1', {}, 1 or 1)
                         ])
def test_parser_binary_operators(parser, expression,vars,expected):
    assert expected == parser(expression, vars)                        

@pytest.mark.parametrize("expression, vars, expected", 
                        [
                            ('sin(1)', {}, math.sin(1)),
                            ('cos(1)', {}, math.cos(1)),
                            ('tan(1)', {}, math.tan(1)),
                            ('asin(1)', {}, math.asin(1)),
                            ('acos(1)', {}, math.acos(1)),
                            ('atan(0.5)', {}, math.atan(0.5)),
                            ('sqrt(1)', {}, math.sqrt(1)),
                            ('log(1)', {}, math.log(1)),
                            ('abs(-1)', {}, abs(-1)),
                            ('ceil(0.3)', {}, math.ceil(0.3)),
                            ('floor(0.3)', {}, math.floor(0.3)),
                            ('round(1.6)', {}, round(1.6)),                                                                                                                                            
                            ('-(1)', {}, -(1)),
                            ('exp(1)', {}, math.exp(1)),
                            ('atan2(0.5,1)', {}, math.atan2(0.5,1)),                                                                                                                                           
                            ('fac(3)', {}, 3 * 2 * 1),
                            ('exp(1)-E', {}, 0),
                            ('PI/4 - atan(1)', {}, math.pi/4-math.atan(1))
                        ])
def test_parser_functions(parser, expression, vars, expected):
    assert expected == parser(expression, vars)


def test_parser_exceptions_div0(parser):
    with pytest.raises(ZeroDivisionError):
        parser('1/0', {})
    
def test_parser_exception_round_brackets(parser):
    with pytest.raises(ParsingError) as e:
        parser('(((1+1)+1)', {})

def test_parser_exception_not_a_function(parser):
    with pytest.raises(UndefinedVariableError) as e:
        parser('pippo', {})

def test_parser_exception_type_error(parser):
    with pytest.raises(TypeError):
        parser('1+sin(+sin())', {})

def test_parser_exception_unclosed_comment(parser):
    with pytest.raises(ValueError):
        parser('/* 1+1', {})

def test_parser_exception_bad_unicode(parser):
    with pytest.raises(ValueError):
        parser("concat('\u0H41', 'pippo')", {})

def test_parser_exception_bad_escape(parser):
    with pytest.raises(ParsingError):
        parser("concat('\z', 'pippo')", {})

@pytest.mark.bug
def test_parser_exception_var_not_found_bug(parser):
    with pytest.raises(UndefinedVariableError):
        assert 1 == parser('"__a__', {"__a__": 1})

@pytest.mark.bug        
def test_parser_escaped_chars(parser):
    with pytest.raises(ParsingError):
        parser("concat('\'', '\b', '\f', '\n', '\r', '\t', 'A')", {})        

def test_parser_this_is_a_comment_in_expression(parser):
    assert 2 == parser('1+ /* this is a comment */ 1', {})

@pytest.mark.bug
def test_parser_var_in_quotes_bug(parser):
    assert 1 == parser('"__a__"', {'"__a__"': 1})

def test_parser_unicode(parser):
    assert "AA" == parser("concat('\u0041', 'A')", {}) 




