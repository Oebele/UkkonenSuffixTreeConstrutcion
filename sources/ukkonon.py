from dataclasses import dataclass, field
from typing import Any, Dict, Tuple
from math import inf


class STree:
    def __init__(self, string, alphabet, hashtag='#'):
        self.t = f' {string}{hashtag}'  # T = t1 t2 ... #
        self.bottom = None
        self.root = None
        self.alphabet = alphabet
        self.hashtag = hashtag

    def suffix_tree(self):
        """Construction of STree(T) for string T = t1 t2 . . . # in alphabet
        Σ = {t −1 , ... , t −m }; # is the end marker not appearing elsewhere
        in T.

        Arguments:
            s {string} -- T = t1 t2 . . .
            alphabet {alphabet} -- Σ = {t −1 , ... , t −m }
        return bottom {Node} -- ⊥
        """
        # self.t is T = t1 t2 ... #
        # create states root and ⊥;
        self.bottom, self.root = STree.Node(), STree.Node()
        for j in range(len(self.alphabet)):  # for j ← 1, ... , m do
            # create transition g0(⊥, (−j, −j)) = root;
            self.bottom.g0(-j - 1, -j - 1, self.root)
        self.root.f = self.bottom  # create suffix link f0(root) = ⊥;
        s, k, i = self.root, 1, 0  # s ← root; k ← 1; i ← 0;
        while self.t[i + 1] != self.hashtag:  # while t i+1 != # do
            i += 1  # i ← i + 1;
            s, k = self.update(s, k, i)  # (s, k) ← update(s, (k, i));
            s, k = self.canonize(s, k, i)  # (s, k) ← canonize(s, (k, i)).

    def update(self, s, k, i):  # procedure update(s, (k, i)):
        # (s, (k, i − 1)) is the canonical reference pair for the active point;
        oldr = self.root  # oldr ← root;
        # (end–point, r) ← test–and–split(s, (k, i − 1), t i );
        end_point, r = self.test_and_split(s, k, i - 1, self.t[i])
        while not end_point:  # while not(end–point) do
            # create new transition g0(r, (i, ∞)) = r0 where r0 is a new state;
            r.g0(i, inf, None)
            # if oldr != root then create new suffix link f0(oldr) = r;
            if oldr is not self.root:
                oldr.f = r
            oldr = r  # oldr ← r;
            # (s, k) ← canonize(f0(s), (k, i − 1));
            s, k = self.canonize(s.f, k, i - 1)
            # (end–point, r) ← test–and–split(s, (k, i − 1), ti);
            end_point, r = self.test_and_split(s, k, i - 1, self.t[i])
        # if oldr != root then create new suffix link f0 (oldr) = s;
        if oldr != self.root:
            oldr.f = s
        # return (s, k).
        return s, k

    def canonize(self, s, k, p):  # procedure canonize(s, (k, p)):
        # if p < k then return (s, k)
        if p < k:
            return s, k
        # else
        # find the tk–transition g0(s, (k0, p0)) = s0 from s;
        k0, p0, s0 = s.find_tk_transaction(self, k)
        while p0 - k0 <= p - k:  # while p0 − k0 ≤ p − k do
            k = k + p0 - k0 + 1  # k ← k + p0 − k0 + 1;
            s = s0  # s ← s0 ;
            # if k ≤ p then find the tk–transition g0(s, (k0, p0)) = s0 from s;
            if k <= p:
                k0, p0, s0 = s.find_tk_transaction(self, k)
        # return (s, k).
        return s, k

    def test_and_split(self, s, k, p, t):
        # procedure test–and–split(s, (k, p), t):
        if k <= p:  # if k ≤ p then
            # let g0(s, (k0, p0 )) = s0 be the tk–transition from s;
            k0, p0, s0 = s.find_tk_transaction(self, k)
            # if t = tk0+p−k+1 then return(true, s)
            if t == self.t[k0 + p - k + 1]:
                return True, s
            # else
            # replace the tk–transition above by transitions
            # g0(s, (k0, k0 + p − k)) = r and g0(r, (k0 + p − k + 1, p0)) = s0
            r = STree.Node()
            s.g0(k0, k0 + p - k, r)
            r.g0(k0 + p - k + 1, p0, s0)
            # where r is a new state;
            # return(false, r)
            return False, r
        else:  # else
            # if there is no t–transition from s then return(false, s)
            if s.no_t_transaction(self, t):
                return False, s
            else:  # else return(true, s).
                return True, s

    def __str__(self):
        return '\nroot' + self.root._to_str(self)

    def is_substring(self, sub):
        s = self.root
        i = 0
        k, p, s = s.get_t_transaction(self, sub[i])
        while i < len(sub) and k and s:
            if sub[i: i + p - k + 1] != self.t[k: p + 1]:
                return False
            if i + p - k + 1 >= len(sub):
                return True
            i = i + p - k + 1
            k, p, s = s.get_t_transaction(self, sub[i])
        return sub[i:] == self.t[k: k + len(sub) - i]

    def is_suffix(self, suffix):
        stop_symbol = self.t[-2]  # needs $ padding
        s = self.root
        i = 0
        k, p, s = s.get_t_transaction(self, suffix[i])
        while i < len(suffix) and k and s:
            if suffix[i: i + p - k + 1] != self.t[k: p + 1]:
                return False
            if i + p - k + 1 >= len(suffix):
                return not s.no_t_transaction(self, stop_symbol)
            i = i + p - k + 1
            k, p, s = s.get_t_transaction(self, suffix[i])
        return (suffix[i:] == self.t[k: k + len(suffix) - i] and
                self.t[k + len(suffix) - i] == stop_symbol)

    @dataclass
    class Node:
        f: Any = None
        g: Dict[int, Tuple[int, Any]] = field(default_factory=dict)

        def g0(self, k, p, s):
            self.g[k] = p, s

        def find_tk_transaction(self, stree, k):
            for k0, (p0, s0) in self.g.items():
                if k0 < 0 and stree.alphabet[-k0 - 1] == stree.t[k]:
                    return k0, p0, s0
                if k0 > 0 and stree.t[k0] == stree.t[k]:
                    return k0, p0, s0
            raise Exception(f'No tk transaction in {self}')

        def get_t_transaction(self, stree, t):
            for k, (p, s) in self.g.items():
                if k < 0 and stree.alphabet[-k - 1] == t:
                    return k, p, s
                if k > 0 and stree.t[k] == t:
                    return k, p, s
            return 0, 0, None

        def no_t_transaction(self, stree, t):
            for k0, _ in self.g.items():
                if k0 < 0 and stree.alphabet[-k0 - 1] == t:
                    return False
                if k0 > 0 and stree.t[k0] == t:
                    return False
            return True

        def __eq__(self, other):
            if self is other:
                return True
            return self._equal(other, set())

        def __hash__(self):
            return id(self)

        def _equal(self, other, processed):
            processed.add(self)
            if not self.f:
                if other.f:
                    return False
            elif not other.f:
                return False
            elif (self.f not in processed and
                    not self.f._equal(other.f, processed)):
                return False

            if len(self.g) != len(other.g):
                return False

            for k, (p, s) in self.g.items():
                if k not in other.g:
                    return False
                p0, s0 = other.g[k]
                if p0 != p:
                    return False
                if s and s not in processed:
                    processed.add(s)
                    if not s._equal(s0, processed):
                        return False
            return True

        def _to_str(self, stree, tabs=4):
            result, tab = '', ''
            for k, (p, s) in self.g.items():
                if k < 0:
                    result += tab * tabs + f'letter = Node({k}, {p} = {stree.alphabet[-k - 1]}) '  # nopep8
                elif s:
                    text = f'-------Node({k}, {p} = {stree.t[k: p + 1]})'
                    result += tab * tabs + text + s._to_str(stree, tabs + 21)  # nopep8
                else:
                    result += tab * tabs + f'-------Node({k}, {p} = {stree.t[k:]})\n'  # nopep8
                tab = ' '
            return result
