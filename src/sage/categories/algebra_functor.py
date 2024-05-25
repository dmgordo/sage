# sage.doctest: needs sage.groups
r"""
Group algebras and beyond: the Algebra functorial construction

Introduction: group algebras
============================

Let `G` be a group and `R` be a ring.  For example::

    sage: G = DihedralGroup(3)
    sage: R = QQ

The *group algebra* `A = RG` of `G` over `R` is the space of formal
linear combinations of elements of `group` with coefficients in `R`::

    sage: A = G.algebra(R); A
    Algebra of Dihedral group of order 6 as a permutation group
            over Rational Field
    sage: a = A.an_element(); a
    () + (1,2) + 3*(1,2,3) + 2*(1,3,2)

This space is endowed with an algebra structure, obtained by extending
by bilinearity the multiplication of `G` to a multiplication on `RG`::

    sage: A in Algebras
    True
    sage: a * a
    14*() + 5*(2,3) + 2*(1,2) + 10*(1,2,3) + 13*(1,3,2) + 5*(1,3)

In particular, the product of two basis elements is induced by the
product of the corresponding elements of the group, and the unit of
the group algebra is indexed by the unit of the group::

    sage: (s, t) = A.algebra_generators()
    sage: s*t
    (1,2)
    sage: A.one_basis()
    ()
    sage: A.one()
    ()

For the user convenience and backward compatibility, the group algebra
can also be constructed with::

    sage: GroupAlgebra(G, R)
    Algebra of Dihedral group of order 6 as a permutation group
            over Rational Field

Since :issue:`18700`, both constructions are strictly equivalent::

    sage: GroupAlgebra(G, R) is G.algebra(R)
    True

Group algebras are further endowed with a Hopf algebra structure; see
below.

Generalizations
===============

The above construction extends to weaker multiplicative structures
than groups: magmas, semigroups, monoids. For a monoid `S`, we obtain
the monoid algebra `RS`, which is defined exactly as above::

     sage: S = Monoids().example(); S
     An example of a monoid: the free monoid generated by ('a', 'b', 'c', 'd')
     sage: A = S.algebra(QQ); A
     Algebra of An example of a monoid: the free monoid generated by ('a', 'b', 'c', 'd')
             over Rational Field
     sage: A.category()
     Category of monoid algebras over Rational Field

This construction also extends to additive structures: magmas,
semigroups, monoids, or groups::

    sage: S = CommutativeAdditiveMonoids().example(); S
    An example of a commutative monoid:
     the free commutative monoid generated by ('a', 'b', 'c', 'd')
    sage: U = S.algebra(QQ); U
    Algebra of An example of a commutative monoid:
               the free commutative monoid generated by ('a', 'b', 'c', 'd')
            over Rational Field

Despite saying "free module", this is really an algebra, whose
multiplication is induced by the addition of elements of `S`::

    sage: U in Algebras(QQ)
    True
    sage: (a,b,c,d) = S.additive_semigroup_generators()
    sage: U(a) * U(b)
    B[a + b]

To catter uniformly for the use cases above and some others, for `S` a
set and `K` a ring, we define in Sage the *algebra of `S`* as the
`K`-free module with basis indexed by `S`, endowed with whatever
algebraic structure can be induced from that of `S`.

.. WARNING::

    In most use cases, the result is actually an algebra, hence the
    name of this construction. In other cases this name is
    misleading::

        sage: A = Sets().example().algebra(QQ); A
        Algebra of Set of prime numbers (basic implementation)
                over Rational Field
        sage: A.category()
        Category of set algebras over Rational Field
        sage: A in Algebras(QQ)
        False

    Suggestions for a uniform, meaningful, and non misleading name are
    welcome!

To achieve this flexibility, the features are implemented as a
:ref:`sage.categories.covariant_functorial_construction` that is
essentially a hierarchy of categories each providing the relevant
additional features::

    sage: A = DihedralGroup(3).algebra(QQ)
    sage: A.categories()
    [Category of finite group algebras over Rational Field,
     ...
     Category of group algebras over Rational Field,
     ...
     Category of monoid algebras over Rational Field,
     ...
     Category of semigroup algebras over Rational Field,
     ...
     Category of unital magma algebras over Rational Field,
     ...
     Category of magma algebras over Rational Field,
     ...
     Category of set algebras over Rational Field,
     ...]


Specifying the algebraic structure
==================================

Constructing the algebra of a set endowed with both an
additive and a multiplicative structure is ambiguous::

    sage: Z3 = IntegerModRing(3)
    sage: A = Z3.algebra(QQ)
    Traceback (most recent call last):
    ...
    TypeError:  `S = Ring of integers modulo 3` is both
     an additive and a multiplicative semigroup.
     Constructing its algebra is ambiguous.
     Please use, e.g., S.algebra(QQ, category=Semigroups())

This ambiguity can be resolved using the ``category`` argument
of the construction::

    sage: A = Z3.algebra(QQ, category=Monoids()); A
    Algebra of Ring of integers modulo 3 over Rational Field
    sage: A.category()
    Category of finite dimensional monoid algebras over Rational Field

    sage: A = Z3.algebra(QQ, category=CommutativeAdditiveGroups()); A
    Algebra of Ring of integers modulo 3 over Rational Field
    sage: A.category()
    Category of finite dimensional commutative additive group algebras
     over Rational Field

In general, the ``category`` argument can be used to specify which
structure of `S` shall be extended to `KS`.

Group algebras, continued
=========================

Let us come back to the case of a group algebra `A=RG`. It is endowed
with more structure and in particular that of a *Hopf algebra*::

    sage: G = DihedralGroup(3)
    sage: A = G.algebra(R); A
    Algebra of Dihedral group of order 6 as a permutation group
            over Rational Field
    sage: A in HopfAlgebras(R).FiniteDimensional().WithBasis()
    True

The basis elements are *group-like* for the coproduct:
`\Delta(g) = g \otimes g`::

    sage: s
    (1,2,3)
    sage: s.coproduct()
    (1,2,3) # (1,2,3)

The counit is the constant function `1` on the basis elements::

    sage: A = GroupAlgebra(DihedralGroup(6), QQ)
    sage: [A.counit(g) for g in A.basis()]
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

The antipode is given on basis elements by `\chi(g) = g^{-1}`::

    sage: A = GroupAlgebra(DihedralGroup(3), QQ)
    sage: s
    (1,2,3)
    sage: s.antipode()
    (1,3,2)

By Maschke's theorem, for a finite group whose cardinality does not
divide the characteristic of the base field, the algebra is
semisimple::

    sage: SymmetricGroup(5).algebra(QQ) in Algebras(QQ).Semisimple()
    True
    sage: CyclicPermutationGroup(10).algebra(FiniteField(7)) in Algebras.Semisimple
    True
    sage: CyclicPermutationGroup(10).algebra(FiniteField(5)) in Algebras.Semisimple
    False


Coercions
=========

Let `RS` be the algebra of some structure `S`. Then `RS` admits the
natural coercion from any other algebra `R'S'` of some structure `S'`,
as long as `R'` coerces into `R` and `S'` coerces into `S`.

For example, since there is a natural inclusion from the dihedral
group `D_2` of order 4 into the symmetric group `S_4` of order 4!, and
since there is a natural map from the integers to the rationals, there
is a natural map from `\ZZ[D_2]` to `\QQ[S_4]`::

    sage: A = DihedralGroup(2).algebra(ZZ)
    sage: B = SymmetricGroup(4).algebra(QQ)
    sage: a = A.an_element(); a
    () + 2*(3,4) + 3*(1,2) + (1,2)(3,4)
    sage: b = B.an_element(); b
    () + (2,3,4) + 2*(1,3)(2,4) + 3*(1,4)(2,3)
    sage: B(a)
    () + 2*(3,4) + 3*(1,2) + (1,2)(3,4)
    sage: a * b  # a is automatically converted to an element of B
    () + 2*(3,4) + 2*(2,3) + (2,3,4) + 3*(1,2) + (1,2)(3,4) + (1,3,2)
     + 3*(1,3,4,2) + 5*(1,3)(2,4) + 13*(1,3,2,4) + 12*(1,4,2,3) + 5*(1,4)(2,3)
    sage: parent(a * b)
    Symmetric group algebra of order 4 over Rational Field

There is no obvious map in the other direction, though::

    sage: A(b)
    Traceback (most recent call last):
    ...
    TypeError: do not know how to make x (= () + (2,3,4) + 2*(1,3)(2,4) + 3*(1,4)(2,3))
     an element of self
     (=Algebra of Dihedral group of order 4 as a permutation group over Integer Ring)

If `S` is a unital (additive) magma, then `RS` is a unital algebra,
and thus admits a coercion from its base ring `R` and any ring that
coerces into `R`. ::

    sage: G = DihedralGroup(2)
    sage: A = G.algebra(ZZ)
    sage: A(2)
    2*()

If `S` is a multiplicative group, then `RS` admits a coercion from `S`
and from any group which coerce into `S`::

    sage: g = DihedralGroup(2).gen(0); g
    (3,4)
    sage: A(g)
    (3,4)
    sage: A(2) * g
    2*(3,4)

Note that there is an ambiguity if `S'` is a group which coerces into
both `R` and `S`. For example) if `S` is the additive group `(\ZZ,+)`,
and `A = RS` is its group algebra, then the integer `2` can be coerced
into `A` in two ways -- via `S`, or via the base ring `R` -- and *the
answers are different*. It that case the coercion to `R` takes
precedence. In particular, if `\ZZ` is the ring (or group) of
integers, then `\ZZ` will coerce to any `RS`, by sending `\ZZ` to `R`.
In generic code, it is therefore recommended to always explicitly use
``A.monomial(g)`` to convert an element of the group into `A`.

TESTS:

Given a group and a base ring, the corresponding group algebra is
unique::

    sage: A = GL(3, QQ).algebra(ZZ)
    sage: B = GL(3, QQ).algebra(ZZ)
    sage: A is B
    True
    sage: C = GL(3, QQ).algebra(QQ)
    sage: A == C
    False

Equality tests::

    sage: AbelianGroup(1).algebra(QQ) == AbelianGroup(1).algebra(QQ)
    True
    sage: AbelianGroup(1).algebra(QQ) == AbelianGroup(1).algebra(ZZ)
    False
    sage: AbelianGroup(2).algebra(QQ) == AbelianGroup(1).algebra(QQ)
    False

    sage: A = KleinFourGroup().algebra(ZZ)
    sage: B = KleinFourGroup().algebra(QQ)
    sage: A == B
    False
    sage: A == A
    True

Properties of group algebras::

    sage: SU(2, GF(4, 'a')).algebra(IntegerModRing(12)).category()
    Category of finite group algebras over Ring of integers modulo 12

    sage: SymmetricGroup(2).algebra(QQ).is_commutative()
    True
    sage: SymmetricGroup(3).algebra(QQ).is_commutative()
    False

    sage: G = DihedralGroup(4)
    sage: A = G.algebra(QQ['x'])
    sage: A(1)
    ()
    sage: A(2)
    2*()
    sage: A(0)
    0
    sage: A(int(2)).coefficients()
    [2]
    sage: A(int(2)).coefficients()[0].parent()
    Univariate Polynomial Ring in x over Rational Field
    sage: g = G.an_element()
    sage: A(g)
    (1,3)

Hopf algebra structure::

    sage: D4 = DihedralGroup(4)
    sage: kD4 = D4.algebra(GF(7))
    sage: kD4 in HopfAlgebras
    True
    sage: a = kD4.an_element(); a
    () + (1,3) + 2*(1,3)(2,4) + 3*(1,4,3,2)
    sage: a.antipode()
    () + 3*(1,2,3,4) + (1,3) + 2*(1,3)(2,4)
    sage: a.coproduct()
    () # () + (1,3) # (1,3) + 2*(1,3)(2,4) # (1,3)(2,4) + 3*(1,4,3,2) # (1,4,3,2)

Coercions from the base ring::

    sage: A = GL(3, GF(7)).algebra(ZZ); A
    Algebra of General Linear Group of degree 3 over Finite Field of size 7
            over Integer Ring
    sage: A.has_coerce_map_from(GL(3, GF(7)))
    True

Coercion from the group::

    sage: G = GL(3, GF(7))
    sage: ZG = G.algebra(ZZ)
    sage: c, d = G.random_element(), G.random_element()
    sage: zc, zd = ZG(c), ZG(d)
    sage: zc * d == zc * zd  # d is automatically converted to an element of ZG
    True

    sage: G = SymmetricGroup(5)
    sage: x,y = G.gens()
    sage: A = G.algebra(QQ)
    sage: A( A(x) )
    (1,2,3,4,5)

    sage: G = KleinFourGroup()
    sage: f = G.gen(0)
    sage: ZG = GroupAlgebra(G)
    sage: ZG(f)  # indirect doctest
    (3,4)
    sage: ZG(1) == ZG(G(1))
    True

Coercion from the base ring takes precedences over coercion from the
group::

    sage: G = GL(2,7)
    sage: OG = GroupAlgebra(G, ZZ[AA(5).sqrt()])
    sage: OG(2)
    2*[1 0]
    [0 1]
    sage: OG(G(2))
    [2 0]
    [0 2]

    sage: OG(FormalSum([ (1, G(2)), (2, RR(0.77)) ]) )
    Traceback (most recent call last):
    ...
    TypeError: Attempt to coerce non-integral RealNumber to Integer
    sage: OG(OG.base_ring().basis()[1])
    a*[1 0]
    [0 1]

Coercions from other group algebras::

    sage: P = RootSystem(['A',2,1]).weight_lattice()
    sage: W = RootSystem(['A',2,1]).weight_space()
    sage: PA = P.algebra(QQ)
    sage: WA = W.algebra(QQ)
    sage: WA.coerce_map_from(PA)
    Generic morphism:
      From: Algebra of the Weight lattice of the Root system of type ['A', 2, 1] over Rational Field
      To:   Algebra of the Weight space over the Rational Field of the Root system of type ['A', 2, 1] over Rational Field

Using the functor `R \mapsto RG` to build the base ring extension
morphism::

    sage: G = SymmetricGroup(3)
    sage: A = G.algebra(ZZ)
    sage: h = GF(5).coerce_map_from(ZZ)

    sage: functor = A.construction()[0]; functor
    GroupAlgebraFunctor
    sage: hh = functor(h)
    sage: hh
    Generic morphism:
      From: Symmetric group algebra of order 3 over Integer Ring
      To: Symmetric group algebra of order 3 over Finite Field of size 5
    sage: a = 2 * A.an_element(); a
    2*() + 2*(2,3) + 6*(1,2,3) + 4*(1,3,2)

    sage: hh(a)
    2*() + 2*(2,3) + (1,2,3) + 4*(1,3,2)

Conversion from a formal sum::

    sage: G = AbelianGroup(1)
    sage: ZG = G.algebra(ZZ)
    sage: f = G.gen()
    sage: ZG(FormalSum([(1,f), (2, f**2)]))
    f + 2*f^2


AUTHORS:

- David Loeffler (2008-08-24): initial version
- Martin Raum (2009-08): update to use new coercion model -- see
  :issue:`6670`.
- John Palmieri (2011-07): more updates to coercion, categories, etc.,
  group algebras constructed using CombinatorialFreeModule -- see
  :issue:`6670`.
- Nicolas M. Thiéry (2010-2017), Travis Scrimshaw (2017):
  generalization to a covariant functorial construction for
  monoid algebras, and beyond -- see e.g. :issue:`18700`.
"""
# ****************************************************************************
#  Copyright (C) 2010-2017 Nicolas M. Thiéry <nthiery at users.sf.net>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  https://www.gnu.org/licenses/
# ****************************************************************************

from sage.categories.pushout import ConstructionFunctor
from sage.categories.morphism import SetMorphism

from sage.categories.covariant_functorial_construction import CovariantFunctorialConstruction, CovariantConstructionCategory, FunctorialConstructionCategory
from sage.categories.category_types import Category_over_base_ring

# TODO: merge the two univariate functors below into a bivariate one


class AlgebraFunctor(CovariantFunctorialConstruction):
    r"""
    For a fixed ring, a functor sending a group/...  to the
    corresponding group/...  algebra.

    EXAMPLES::

        sage: from sage.categories.algebra_functor import AlgebraFunctor
        sage: F = AlgebraFunctor(QQ); F
        The algebra functorial construction
        sage: F(DihedralGroup(3))
        Algebra of Dihedral group of order 6 as a permutation group
                over Rational Field
    """
    _functor_name = "algebra"
    _functor_category = "Algebras"

    def __init__(self, base_ring):
        """
        EXAMPLES::

            sage: from sage.categories.algebra_functor import AlgebraFunctor
            sage: F = AlgebraFunctor(QQ); F
            The algebra functorial construction
            sage: TestSuite(F).run()
        """
        from sage.categories.rings import Rings
        assert base_ring in Rings()
        self._base_ring = base_ring

    def base_ring(self):
        """
        Return the base ring for this functor.

        EXAMPLES::

            sage: from sage.categories.algebra_functor import AlgebraFunctor
            sage: AlgebraFunctor(QQ).base_ring()
            Rational Field
        """
        return self._base_ring

    def __call__(self, G, category=None):
        """
        Return the algebra of ``G``.

        See :ref:`sage.categories.algebra_functor` for details.

        INPUT:

        - ``G`` -- a group
        - ``category`` -- a category, or ``None``

        EXAMPLES::

            sage: from sage.categories.algebra_functor import AlgebraFunctor
            sage: F = AlgebraFunctor(QQ)
            sage: G = DihedralGroup(3)
            sage: A = F(G, category=Monoids()); A
            Algebra of Dihedral group of order 6 as a permutation group
                    over Rational Field
            sage: A.category()
            Category of finite dimensional monoid algebras over Rational Field
        """
        return G.algebra(self._base_ring, category=category)


class GroupAlgebraFunctor(ConstructionFunctor):
    r"""
    For a fixed group, a functor sending a commutative ring to the
    corresponding group algebra.

    INPUT:

    - ``group`` -- the group associated to each group algebra under
      consideration

    EXAMPLES::

        sage: from sage.categories.algebra_functor import GroupAlgebraFunctor
        sage: F = GroupAlgebraFunctor(KleinFourGroup()); F
        GroupAlgebraFunctor
        sage: A = F(QQ); A
        Algebra of The Klein 4 group of order 4, as a permutation group over Rational Field

    TESTS::

        sage: loads(dumps(F)) == F
        True
        sage: A is KleinFourGroup().algebra(QQ)
        True
    """
    def __init__(self, group):
        r"""
        See :class:`GroupAlgebraFunctor` for full documentation.

        EXAMPLES::

            sage: from sage.categories.algebra_functor import GroupAlgebraFunctor
            sage: GroupAlgebra(SU(2, GF(4, 'a')), IntegerModRing(12)).category()
            Category of finite group algebras over Ring of integers modulo 12
        """
        self.__group = group
        from sage.categories.rings import Rings
        ConstructionFunctor.__init__(self, Rings(), Rings())

    def group(self):
        r"""
        Return the group which is associated to this functor.

        EXAMPLES::

            sage: from sage.categories.algebra_functor import GroupAlgebraFunctor
            sage: GroupAlgebraFunctor(CyclicPermutationGroup(17)).group() == CyclicPermutationGroup(17)
            True
        """
        return self.__group

    def _apply_functor(self, base_ring):
        r"""
        Create the group algebra with given base ring over ``self.group()``.

        INPUT:

        - ``base_ring`` -- the base ring of the group algebra

        OUTPUT:

        A group algebra.

        EXAMPLES::

            sage: from sage.categories.algebra_functor import GroupAlgebraFunctor
            sage: F = GroupAlgebraFunctor(CyclicPermutationGroup(17))
            sage: F(QQ)
            Algebra of Cyclic group of order 17 as a permutation group
             over Rational Field
        """
        return self.__group.algebra(base_ring)

    def _apply_functor_to_morphism(self, f):
        r"""
        Lift a homomorphism of rings to the corresponding homomorphism
        of the group algebras of ``self.group()``.

        INPUT:

        - ``f`` -- a morphism of rings

        OUTPUT:

        A morphism of group algebras.

        EXAMPLES::

            sage: G = SymmetricGroup(3)
            sage: A = GroupAlgebra(G, ZZ)
            sage: h = GF(5).coerce_map_from(ZZ)
            sage: hh = A.construction()[0](h); hh
            Generic morphism:
              From: Symmetric group algebra of order 3 over Integer Ring
              To:   Symmetric group algebra of order 3 over Finite Field of size 5

            sage: a = 2 * A.an_element(); a
            2*() + 2*(2,3) + 6*(1,2,3) + 4*(1,3,2)
            sage: hh(a)
            2*() + 2*(2,3) + (1,2,3) + 4*(1,3,2)
        """
        from sage.categories.rings import Rings
        domain = self(f.domain())
        codomain = self(f.codomain())
        # we would want to use something like:
        # domain.module_morphism(on_coefficients=h, codomain=codomain, category=Rings())
        return SetMorphism(domain.Hom(codomain, category=Rings()),
                           lambda x: codomain.sum_of_terms((g, f(c)) for (g, c) in x))


class AlgebrasCategory(CovariantConstructionCategory, Category_over_base_ring):
    r"""
    An abstract base class for categories of monoid algebras,
    groups algebras, and the like.

    .. SEEALSO::

        - :meth:`Sets.ParentMethods.algebra`
        - :meth:`Sets.SubcategoryMethods.Algebras`
        - :class:`~sage.categories.covariant_functorial_construction.CovariantFunctorialConstruction`

    INPUT:

    - ``base_ring`` -- a ring

    EXAMPLES::

        sage: C = Groups().Algebras(QQ); C
        Category of group algebras over Rational Field
        sage: C = Monoids().Algebras(QQ); C
        Category of monoid algebras over Rational Field

        sage: C._short_name()
        'Algebras'
        sage: latex(C) # todo: improve that
        \mathbf{Algebras}(\mathbf{Monoids})
    """

    _functor_category = "Algebras"

    def _repr_object_names(self):
        """
        EXAMPLES::

            sage: Semigroups().Algebras(QQ) # indirect doctest
            Category of semigroup algebras over Rational Field
        """
        return "{} algebras over {}".format(self.base_category()._repr_object_names()[:-1],
                                            self.base_ring())

    @staticmethod
    def __classcall__(cls, category=None, R=None):
        """
        Make ``CatAlgebras(**)`` a shorthand for ``Cat().Algebras(**)``.

        EXAMPLES::

            sage: GradedModules(ZZ)   # indirect doctest
            Category of graded modules over Integer Ring
            sage: Modules(ZZ).Graded()
            Category of graded modules over Integer Ring
            sage: Modules.Graded(ZZ)
            Category of graded modules over Integer Ring
            sage: GradedModules(ZZ) is Modules(ZZ).Graded()
            True

        .. SEEALSO:: :meth:`_base_category_class`

        .. TODO::

            The logic is very similar to the default implementation
            :class:`FunctorialConstructionCategory.__classcall__`;
            the only difference is whether the additional arguments
            should be passed to ``Cat`` or to the construction.

            Find a way to refactor this to avoid the duplication.
        """
        base_category_class = cls._base_category_class[0]
        if isinstance(category, base_category_class):
            return super(FunctorialConstructionCategory, cls).__classcall__(cls, category, R)
        else:
            # category should now be the base ring ...
            return cls.category_of(base_category_class(), category)

    class ParentMethods:

        # coalgebra structure

        def coproduct_on_basis(self, g):
            r"""
            Return the coproduct of the element ``g`` of the basis.

            Each basis element ``g`` is group-like. This method is
            used to compute the coproduct of any element.

            EXAMPLES::

                sage: PF = NonDecreasingParkingFunctions(4)
                sage: A = PF.algebra(ZZ); A
                Algebra of Non-decreasing parking functions of size 4 over Integer Ring
                sage: g = PF.an_element(); g
                [1, 1, 1, 1]
                sage: A.coproduct_on_basis(g)
                B[[1, 1, 1, 1]] # B[[1, 1, 1, 1]]
                sage: a = A.an_element(); a
                2*B[[1, 1, 1, 1]] + 2*B[[1, 1, 1, 2]] + 3*B[[1, 1, 1, 3]]
                sage: a.coproduct()
                2*B[[1, 1, 1, 1]] # B[[1, 1, 1, 1]] +
                2*B[[1, 1, 1, 2]] # B[[1, 1, 1, 2]] +
                3*B[[1, 1, 1, 3]] # B[[1, 1, 1, 3]]
            """
            from sage.categories.tensor import tensor
            g = self.term(g)
            return tensor([g, g])
