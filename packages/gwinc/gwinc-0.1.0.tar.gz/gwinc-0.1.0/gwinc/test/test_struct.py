import pytest
import yaml

from ..struct import Struct, yaml_loader
YAMLSafeLoader = yaml_loader


TEST_YAML = '''
N: 'Test'
I:
  L: 1.3e5
  T:
    - 1
    - 2
  R:
    P: 1e-9
S:
  - M: 40
    L: 4
  - M: 30
    L: 3
'''


def validate(ifo):
    assert ifo.N == 'Test'
    assert ifo['N'] == 'Test'
    assert ifo.I.L == 1.3e5
    assert ifo['I'].L == 1.3e5
    assert ifo['I']['L'] == 1.3e5
    assert ifo['I.L'] == 1.3e5
    # assert getattr(ifo, 'I.L') == 1.3e5
    assert ifo.I.T == [1, 2]
    assert ifo['I'].T == [1, 2]
    assert ifo['I']['T'] == [1, 2]
    assert ifo['I.T'] == [1, 2]
    # assert getattr(ifo, 'I.T') == [1, 2]
    assert ifo.I.R.P == 1e-9
    assert ifo['I.R.P'] == 1e-9
    assert ifo.S[0].M == 40
    assert ifo['S[1].L'] == 3
    # assert len(ifo) == 3
    assert set(ifo) == set(['I', 'N', 'S'])
    assert set(ifo.keys()) == set(['I', 'N', 'S'])
    # assert set(ifo.values()) == []
    assert hasattr(ifo, 'N')
    assert hasattr(ifo.I, 'L')
    assert 'N' in ifo
    assert 'L' in ifo.I
    assert ifo.to_dict() == yaml.load(TEST_YAML, Loader=YAMLSafeLoader)
    assert ifo.diff(Struct.from_yaml(TEST_YAML)) == []
    with pytest.raises(AttributeError):
        ifo.A
    with pytest.raises(KeyError):
        ifo['B']


    # def basic_assert(self, ifo):
    #     assert ifo.a == 1
    #     assert ifo['a'] == 1
    #     assert ifo.b.c == 2
    #     assert ifo['b.c'] == 2
    #     assert ifo.to_dict() == self.tdict
    #     assert ifo.to_yaml() == self.tyaml
    #     # assert dict(ifo) == self.tdict
    #     assert set(ifo.keys()) == set(['a', 'b'])
    #     assert set(ifo.values()) == set([1, ifo.b])
    #     assert hasattr(ifo, 'a')
    #     assert hasattr(ifo.b, 'c')
    #     assert 'a' in ifo
    #     assert 'c' in ifo.b
    #     assert ifo.diff(Struct.from_dict(self.tdict)) == []


class TestStruct:
    def test_basic(self):
        ifo = Struct()
        ifo.N = 'Test'
        ifo.I = Struct()
        ifo.I.L = 1.3e5
        ifo['I'].T = [1, 2]
        ifo['I.R'] = Struct(dict(P=1e-9))
        ifo.S = [
            Struct(dict(M=40, L=4)),
            Struct(dict(M=30, L=3)),
        ]
        validate(ifo)

    def test_from_dict(self):
        d = yaml.load(TEST_YAML, Loader=YAMLSafeLoader)
        ifo = Struct(d)
        validate(ifo)

    def test_from_yaml(self):
        ifo = Struct.from_yaml(TEST_YAML)
        validate(ifo)

    # def test_classdef(self):
    #     class Rs(Struct):
    #         @property
    #         def P(self):
    #             return 1e-9
    #     class Is(Struct):
    #         L = 1.3e5
    #         T = [1, 2]
    #         R = Rs()
    #     class IFO(Struct):
    #         N = 'Test'
    #         I = Is()
    #         S = [
    #             Struct(dict(M=40, L=4)),
    #             Struct(dict(M=30, L=3)),
    #         ]
    #     ifo = IFO()
    #     validate(ifo)

    def test_load_override(self):
        class Is(Struct):
            @property
            def T(self):
                return [-1, -2]
        class IFO(Struct):
            N = 'Foo'
            I = Is()
        ifo = IFO.from_yaml(TEST_YAML)
        validate(ifo)

    def test_root_ref(self):
        class Ts(Struct):
            @property
            def P(self):
                return self._root * 4
        class IFO(Struct):
            T = Ts
            T.asdf = 4
            N = 'Foo'
        ifo = IFO.from_yaml(TEST_YAML)
        print(ifo.T)
        validate(ifo)

    # def test_property(self):
    #     class B(Struct):
    #         @property
    #         def c(self):
    #             return 1+1
    #     ifo = Struct()
    #     ifo.a = 1
    #     ifo.b = B()
    #     self.basic_assert(ifo)

    # def test_properties(self):
    #     ifo = Foo()
    #     with pytest.raises(AttributeError):
    #         ifo['Bar'] = 3
    #     with pytest.raises(AttributeError):
    #         ifo.Bar = 3
    #     assert ifo.Bar == 4
    #     assert 'Bar' in ifo
    #     assert hassattr(ifo, 'Bar')

    # @pytest.mark.xfail
    # def test_properties(self):
    #     ifo = Foo()
    #     assert ifo.to_dict() == dict(Bar=4)
