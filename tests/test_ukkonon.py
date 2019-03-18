from pytest import raises
from sources.ukkonon import STree
from math import inf

Node = STree.Node

# for coverage :
# python3.7 -m pytest --cov=sources/ --cov-report=html  tests/test_ukkonon.py

# --------------------------------------------------------------- #
#                   Tree Suffix functions Tests                   #
# --------------------------------------------------------------- #


def test_a_is_substring_from_abaaba():
    T = 'abaaba$'
    abc = '$baa'
    substring = 'a'
    st = STree(T, abc)
    st.suffix_tree()
    assert st.is_substring(substring)


def test_c_not_is_substring_from_abaaba():
    T = 'abaaba$'
    abc = '$baa'
    substring = 'c'
    st = STree(T, abc)
    st.suffix_tree()
    assert not st.is_substring(substring)


def test_baa_is_substring_from_abaaba():
    T = 'abaaba$'
    abc = '$baa'
    substring = 'aba'
    st = STree(T, abc)
    st.suffix_tree()
    assert st.is_substring(substring)


def test_aba_is_substring_from_abaaba():
    T = 'abaaba$'
    abc = '$aba'
    substring = 'aba'
    st = STree(T, abc)
    st.suffix_tree()
    assert st.is_substring(substring)


def test_abaaba_is_substring_from_abaaba():
    T = 'abaaba$'
    abc = '$aba'
    substring = 'abaaba'
    st = STree(T, abc)
    st.suffix_tree()
    assert st.is_substring(substring)


def test_siss_is_substring_from_mississippi():
    T = 'mississippi$'
    abc = '$imps'
    substring = 'siss'
    st = STree(T, abc)
    st.suffix_tree()
    assert st.is_substring(substring)


def test_ss_is_substring_from_mississippi():
    T = 'mississippi$'
    abc = '$imps'
    substring = 'ss'
    st = STree(T, abc)
    st.suffix_tree()
    assert st.is_substring(substring)


def test_aba_is_suffix_from_abaaba():
    T = 'abaaba$'
    abc = '$aba'
    suffix = 'aba'
    st = STree(T, abc)
    st.suffix_tree()
    assert st.is_suffix(suffix)


def test_abb_is_not_suffix_from_abaaba():
    T = 'abaaba$'
    abc = '$aba'
    suffix = 'abb'
    st = STree(T, abc)
    st.suffix_tree()
    assert not st.is_suffix(suffix)


def test_baab_is_not_suffix_from_abaaba():
    T = 'abaaba$'
    abc = '$aba'
    suffix = 'baab'
    st = STree(T, abc)
    st.suffix_tree()
    assert not st.is_suffix(suffix)


def test_baaba_is_suffix_from_abaaba():
    T = 'abaaba$'
    abc = '$aba'
    suffix = 'baaba'
    st = STree(T, abc)
    st.suffix_tree()
    assert st.is_suffix(suffix)

# --------------------------------------------------------------- #
#                      Tree Consrtuction Tests                    #
# --------------------------------------------------------------- #


def test_ukkonen_empty_string():
    s = ''
    bottom, root, alphabet = create_bottom_and_node()
    expected = bottom

    st = STree(s, alphabet)
    st.suffix_tree()
    result = st.bottom
    assert result == expected


def test_ukkonen_string_c():
    s = 'c'
    alphabet, _, expected = create_expected_for_string_c()

    st = STree(s, alphabet)
    st.suffix_tree()
    result = st.bottom

    assert result == expected


def test_ukkonen_string_ca():
    s, alphabet, expected = create_expected_for_string_ca()

    st = STree(s, alphabet)
    st.suffix_tree()
    result = st.bottom
    assert result == expected


def test_ukkonen_string_cac():
    s = 'cac'
    _, alphabet, expected = create_expected_for_string_ca()

    st = STree(s, alphabet)
    st.suffix_tree()
    result = st.bottom
    assert result == expected


def test_ukkonen_string_caca():
    s = 'caca'
    _, alphabet, expected = create_expected_for_string_ca()

    st = STree(s, alphabet)
    st.suffix_tree()
    result = st.bottom
    assert result == expected


def test_ukkonen_string_cacao():
    s = 'cacao'
    _, alphabet, expected = create_expected_for_string_ca()
    bottom = expected
    root = bottom.g[-1][1]
    root.g0(5, inf, None)
    cacao = Node()

    acao = Node()
    cacao.f = acao
    acao.f = root
    root.g0(1, 2, cacao)
    root.g0(2, 2, acao)
    root.g0(5, inf, None)
    cacao.g0(3, inf, None)
    cacao.g0(5, inf, None)
    acao.g0(3, inf, None)
    acao.g0(5, inf, None)

    st = STree(s, alphabet)
    st.suffix_tree()
    result = st.bottom

    assert result == expected


def test_string_banana_wikipedia():
    s = 'banana$'
    expected, root, alphabet = create_bottom_and_node(sorted(set(s)))
    root_a = Node()
    root_na = Node()

    root_a.f = root
    root_na.f = root_a

    a_na = Node()
    a_na.f = root_na

    root.g0(2, 2, root_a)  # a
    root.g0(1, inf, None)  # banana$
    root.g0(3, 4, root_na)   # na
    root.g0(7, inf, None)  # $

    root_a.g0(7, inf, None)  # $
    root_a.g0(3, 4, a_na)  # na

    root_na.g0(7, inf, None)  # $
    root_na.g0(5, inf, None)  # na$

    a_na.g0(7, inf, None)  # $
    a_na.g0(5, inf, None)  # na$

    st = STree(s, alphabet)
    st.suffix_tree()
    result = st.bottom

    assert result == expected


def test_string_mississippi():
    # added for better coverage criteia
    s = 'mississippi$'
    expected, root, alphabet = create_bottom_and_node(sorted(set(s)))
    root_i = Node()
    root_s = Node()
    root_p = Node()

    root_i.f = root
    root_s.f = root
    root_p.f = root

    root.g0(1, inf, None)  # mississiooi$
    root.g0(2, 2, root_i)  # i
    root.g0(3, 3, root_s)  # s
    root.g0(9, 9, root_p)  # p
    root.g0(12, inf, None)  # $

    i_ssi = Node()
    root_i.g0(3, 5, i_ssi)  # ssi
    root_i.g0(9, inf, None)  # ppi$
    root_i.g0(12, inf, None)  # $

    i_ssi.g0(6, inf, None)  # ssippi$
    i_ssi.g0(9, inf, None)  # ppi$

    s_si = Node()
    s_i = Node()
    root_s.g0(4, 5, s_si)
    root_s.g0(5, 5, s_i)
    i_ssi.f = s_si
    s_si.f = s_i
    s_i.f = root_i

    s_si.g0(6, inf, None)  # ssippi$
    s_si.g0(9, inf, None)  # ppi$

    s_i.g0(6, inf, None)  # ssippi$
    s_i.g0(9, inf, None)  # ppi$

    root_p.g0(11, inf, None)  # i$
    root_p.g0(10, inf, None)  # pi$

    st = STree(s, alphabet)
    st.suffix_tree()
    result = st.bottom
    assert result == expected


def create_expected_for_string_ca():
    s = 'ca'
    alphabet, root, expected = create_expected_for_string_c()
    root.g0(2, inf, None)
    return s, alphabet, expected


def create_expected_for_string_c():
    bottom, root, alphabet = create_bottom_and_node()
    root.g0(1, inf, None)
    expected = bottom
    return alphabet, root, expected

# --------------------------------------------------------------- #
#                    Node  equal functio Tests                    #
# --------------------------------------------------------------- #


def test_equal_function_empty_node():
    bottom = Node()
    root = Node()
    assert bottom == root


def test_1():
    bottom, root, alphabet = create_bottom_and_node()
    assert bottom != root


def test_2():
    bottom, root, alphabet = create_bottom_and_node()
    bottom1, root1, _ = create_bottom_and_node()
    assert bottom == bottom1


def test_3():
    bottom, root, alphabet = create_bottom_and_node()
    g = Node()
    root.g0(1, 1, g)
    g.f = root
    bottom1, root1, alphabet = create_bottom_and_node()
    assert bottom != bottom1


def test_4():
    bottom, root, alphabet = create_bottom_and_node()
    g = Node()
    root.g0(1, 1, g)

    bottom1, root1, alphabet = create_bottom_and_node()
    g1 = Node()
    root1.g0(1, 1, g1)
    assert bottom == bottom1


def test_5():
    bottom, root, alphabet = create_bottom_and_node()
    g = Node()
    root.g0(1, 1, g)
    g.g0(2, 1, None)

    bottom1, root1, alphabet = create_bottom_and_node()
    g1 = Node()
    root1.g0(1, 1, g1)
    assert bottom != bottom1


def test_6():
    bottom, root, alphabet = create_bottom_and_node()
    g = Node()
    root.g0(1, 1, g)
    g.g0(2, 1, None)

    bottom1, root1, alphabet = create_bottom_and_node()
    g1 = Node()
    root1.g0(1, 1, g1)
    g1.g0(2, 1, None)
    assert bottom == bottom1


def test_7():
    bottom, root, alphabet = create_bottom_and_node()
    g = Node()
    root.g0(1, 1, g)
    g.g0(2, 1, None)

    bottom1, root1, alphabet = create_bottom_and_node()
    g1 = Node()
    root1.g0(1, 1, g1)
    g1.g0(2, 1, None)
    assert bottom1 == bottom


def test_8():
    bottom, root, alphabet = create_bottom_and_node()
    g = Node()
    root.g0(1, 1, g)
    g.g0(2, 1, None)

    bottom1, root1, alphabet = create_bottom_and_node()
    g1 = Node()
    root1.g0(1, 1, g1)
    g1.g0(2, inf, None)
    assert bottom != bottom1


def test_9():
    bottom, root, alphabet = create_bottom_and_node()
    g = Node()
    root.g0(1, 1, g)
    g.g0(2, 1, None)

    bottom1, root1, alphabet = create_bottom_and_node()
    g1 = Node()
    root1.g0(1, 1, g1)
    g1.g0(2, inf, None)
    assert bottom != bottom1


def test_10():
    bottom, root, alphabet = create_bottom_and_node()
    g = Node()
    root.g0(1, 1, g)
    g.g0(2, 2, None)
    g.g0(3, inf, None)
    g.f = g

    bottom1, root1, alphabet = create_bottom_and_node()
    g1 = Node()
    root1.g0(1, 1, g1)
    g1.g0(2, 2, None)
    g1.g0(3, inf, None)
    assert bottom != bottom1


def test_11():
    bottom, root, alphabet = create_bottom_and_node()
    g = Node()
    root.g0(1, 1, g)
    g.g0(2, 1, None)
    g.g0(2, inf, None)
    g.f = g

    bottom1, root1, alphabet = create_bottom_and_node()
    g1 = Node()
    root1.g0(1, 1, g1)
    g1.g0(2, 1, None)
    g1.g0(2, inf, None)
    assert bottom1 != bottom


def test_12():
    bottom, root, alphabet = create_bottom_and_node()
    g = Node()
    root.g0(1, 1, g)
    g.g0(2, 2, None)
    g.g0(4, inf, None)
    g.f = root

    bottom1, root1, alphabet = create_bottom_and_node()
    g1 = Node()
    root1.g0(1, 1, g1)
    g1.g0(2, 2, None)
    g1.g0(4, inf, None)
    g1.f = root
    assert bottom == bottom1


def test_13():
    bottom, root, alphabet = create_bottom_and_node()
    g = Node()
    root.g0(1, 1, g)
    g.g0(2, 1, None)

    bottom1, root1, alphabet = create_bottom_and_node()
    g1 = Node()
    root1.g0(1, 1, g1)
    g1.g0(3, inf, None)
    assert bottom != bottom1


def test_14():
    bottom, root, alphabet = create_bottom_and_node()
    g = Node()
    root.g0(1, 1, g)
    g.g0(2, 1, None)
    STree.t = alphabet
    STree.alphabet = alphabet
    with raises(Exception):
        g.find_tk_transaction(STree, 1)


def create_bottom_and_node(alphabet='aco'):
    bottom = Node()
    root = Node()
    for j in range(len(alphabet)):
        bottom.g0(-j - 1, -j - 1, root)
    root.f = bottom
    return bottom, root, alphabet
