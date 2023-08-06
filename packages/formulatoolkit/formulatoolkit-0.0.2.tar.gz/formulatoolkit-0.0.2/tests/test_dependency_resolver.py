import pytest
from FormulaToolkit import DependencyResolver  

@pytest.fixture()
def dependency_resolver():
    dependency_resolver = DependencyResolver()
    yield dependency_resolver
    del dependency_resolver


def test_depencies_resolver_on_case_one(dependency_resolver):
    """This case is correct"""
    DEPENDENCIES_CASE = dict(
        a=('b', 'c'),
        d=('b' ), 
        c=('j', 'h', 'i', 'l'),
        e=('a', 'b', 'l', 'h'),
        f=('i', 'l' )
    )
    SOLUTION = [
        set(['i', 'h', 'b', 'l', 'j']),
        set(['c', 'd', 'f']),
        set(['a']),
        set(['e'])
    ]
    assert dependency_resolver.solve(DEPENDENCIES_CASE) == SOLUTION


def test_dependency_resolver_detect_loop(dependency_resolver):
    """LOOP"""
    DEPENDENCIES_CASE = dict(
        a=('b', 'c'),  # a depends on b and c 
        d=('b' ), 
        c=('a', 'h', 'i', 'l'), # c depends on a ( loop )
        e=('a', 'b', 'l', 'h'),
        f=('i', 'l' )
    )
    with pytest.raises(RuntimeError):
        dependency_resolver.solve(DEPENDENCIES_CASE)
        