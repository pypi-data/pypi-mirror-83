# -*- coding: utf-8 -*-

"""
Implements distributional compositional models.

>>> from discopy.tensor import TensorFunctor
>>> s, n = Ty('s'), Ty('n')
>>> Alice, Bob = Word('Alice', n), Word('Bob', n)
>>> loves = Word('loves', n.r @ s @ n.l)
>>> grammar = Cup(n, n.r) @ Id(s) @ Cup(n.l, n)
>>> sentence = grammar << Alice @ loves @ Bob
>>> ob = {s: 1, n: 2}
>>> ar = {Alice: [1, 0], loves: [0, 1, 1, 0], Bob: [0, 1]}
>>> F = TensorFunctor(ob, ar)
>>> assert F(sentence) == True

>>> from discopy.quantum import qubit, Ket, CX, H, X, sqrt, CircuitFunctor
>>> s, n = Ty('s'), Ty('n')
>>> Alice = Word('Alice', n)
>>> loves = Word('loves', n.r @ s @ n.l)
>>> Bob = Word('Bob', n)
>>> grammar = Cup(n, n.r) @ Id(s) @ Cup(n.l, n)
>>> sentence = grammar << Alice @ loves @ Bob
>>> ob = {s: Ty(), n: qubit}
>>> ar = {Alice: Ket(0),
...       loves: CX << sqrt(2) @ H @ X << Ket(0, 0),
...       Bob: Ket(1)}
>>> F = CircuitFunctor(ob, ar)
>>> assert abs(F(sentence).eval().array) ** 2
"""

from functools import reduce as fold
import random

from discopy import messages, drawing
from discopy.rigid import Ty, Box, Diagram, Id, Cup


class Word(Box):
    """
    Implements words as boxes with a pregroup type as codomain.

    >>> Alice = Word('Alice', Ty('n'))
    >>> loves = Word('loves',
    ...     Ty('n').r @ Ty('s') @ Ty('n').l)
    >>> Alice
    Word('Alice', Ty('n'))
    >>> loves
    Word('loves', Ty(Ob('n', z=1), 's', Ob('n', z=-1)))
    """
    def __init__(self, name, cod, dom=Ty(), data=None, _dagger=False):
        if not isinstance(name, str):
            raise TypeError(messages.type_err(str, name))
        if not isinstance(dom, Ty):
            raise TypeError(messages.type_err(Ty, dom))
        if not isinstance(cod, Ty):
            raise TypeError(messages.type_err(Ty, cod))
        super().__init__(name, dom, cod, data, _dagger)

    def __repr__(self):
        return "Word({}, {}{})".format(
            repr(self.name), repr(self.cod),
            ", dom={}".format(repr(self.dom)) if self.dom else "")


class CFG:
    """
    Implements context-free grammars.

    >>> s, n, v, vp = Ty('S'), Ty('N'), Ty('V'), Ty('VP')
    >>> R0, R1 = Box('R0', vp @ n, s), Box('R1', n @ v , vp)
    >>> Jane, loves = Word('Jane', n), Word('loves', v)
    >>> cfg = CFG(R0, R1, Jane, loves)
    >>> gen = cfg.generate(start=s, max_sentences=2, max_depth=6)
    >>> for sentence in gen:
    ...     print(sentence)
    Jane >> loves @ Id(N) >> Jane @ Id(V @ N) >> R1 @ Id(N) >> R0
    Jane >> loves @ Id(N) >> Jane @ Id(V @ N) >> R1 @ Id(N) >> R0
    >>> gen = cfg.generate(
    ...     start=s, max_sentences=2, max_depth=6,
    ...     remove_duplicates=True, max_iter=10)
    >>> for sentence in gen:
    ...     print(sentence)
    Jane >> loves @ Id(N) >> Jane @ Id(V @ N) >> R1 @ Id(N) >> R0
    """
    def __init__(self, *productions):
        self._productions = productions

    @property
    def productions(self):
        """
        Production rules, i.e. boxes with grammatical types as dom and cod.
        """
        return self._productions

    def __repr__(self):
        return "CFG{}".format(repr(self._productions))

    def generate(self, start, max_sentences, max_depth, max_iter=100,
                 remove_duplicates=False, not_twice=[]):
        """
        Generate sentences from a context-free grammar.
        Assumes the only terminal symbol is Ty().
        Parameters
        ----------
        start : type
            root of the generated trees.
        max_sentences : int
            maximum number of sentences to generate.
        max_depth : int
            maximum depth of the trees.
        max_iter : int
            maximum number of iterations, set to 100 by default.
        remove_duplicates : bool
            if set to True only distinct syntax trees will be generated.
        not_twice : list
            list of productions that you don't want appearing twice
            in a sentence, set to the empty list by default
        """
        prods, cache = list(self.productions), set()
        n, i = 0, 0
        while (not max_sentences or n < max_sentences) and i < max_iter:
            i += 1
            sentence = Id(start)
            depth = 0
            while depth < max_depth:
                recall = depth
                if sentence.dom == Ty():
                    if remove_duplicates and sentence in cache:
                        break
                    yield sentence
                    if remove_duplicates:
                        cache.add(sentence)
                    n += 1
                    break
                tag = sentence.dom[0]
                random.shuffle(prods)
                for prod in prods:
                    if prod in not_twice and prod in sentence.boxes:
                        continue
                    if Ty(tag) == prod.cod:
                        sentence = sentence << prod @ Id(sentence.dom[1:])
                        depth += 1
                        break
                if recall == depth:  # in this case, no production was found
                    break


def eager_parse(*words, target=Ty('s')):
    """
    Tries to parse a given list of words in an eager fashion.
    """
    result = fold(lambda x, y: x @ y, words)
    scan = result.cod
    while True:
        fail = True
        for i in range(len(scan) - 1):
            if scan[i: i + 1].r != scan[i + 1: i + 2]:
                continue
            cup = Cup(scan[i: i + 1], scan[i + 1: i + 2])
            result = result >> Id(scan[: i]) @ cup @ Id(scan[i + 2:])
            scan, fail = result.cod, False
            break
        if result.cod == target:
            return result
        if fail:
            raise NotImplementedError


def brute_force(*vocab, target=Ty('s')):
    """
    Given a vocabulary, search for grammatical sentences.
    """
    test = [()]
    for words in test:
        for word in vocab:
            try:
                yield eager_parse(*(words + (word, )), target=target)
            except NotImplementedError:
                pass
            test.append(words + (word, ))


def draw(diagram, **params):
    """
    Draws a pregroup diagram, i.e. one slice of word boxes followed by any
    number of slices of cups.

    Parameters
    ----------
    width : float, optional
        Width of the word triangles, default is :code:`2.0`.
    space : float, optional
        Space between word triangles, default is :code:`0.5`.
    textpad : pair of floats, optional
        Padding between text and wires, default is :code:`(0.1, 0.2)`.
    draw_types : bool, optional
        Whether to draw type labels, default is :code:`True`.
    aspect : string, optional
        Aspect ratio, one of :code:`['equal', 'auto']`.
    margins : tuple, optional
        Margins, default is :code:`(0.05, 0.05)`.
    fontsize : int, optional
        Font size for the words, default is :code:`12`.
    fontsize_types : int, optional
        Font size for the types, default is :code:`12`.
    figsize : tuple, optional
        Figure size.
    path : str, optional
        Where to save the image, if `None` we call :code:`plt.show()`.

    Raises
    ------
    ValueError
        Whenever the input is not a pregroup diagram.
    """
    if not isinstance(diagram, Diagram):
        raise TypeError(messages.type_err(Diagram, diagram))
    words, *cups = diagram.foliation().boxes
    is_pregroup = all(isinstance(box, Word) for box in words.boxes)\
        and all(isinstance(box, Cup) for s in cups for box in s.boxes)
    if not is_pregroup:
        raise ValueError(messages.expected_pregroup())
    drawing.pregroup_draw(words, cups, **params)
