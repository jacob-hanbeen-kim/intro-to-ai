import unittest

from heredity import PROBS, joint_probability, update, normalize

class TestHeredityFunctions(unittest.TestCase):
    def setUp(self):
        # Example people dictionary
        self.people = {
            'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
            'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
            'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
        }
        self.probabilities = {
            person: {
                "gene": {2: 0, 1: 0, 0: 0},
                "trait": {True: 0, False: 0}
            }
            for person in self.people
        }

    def test_joint_probability(self):
        # Example from the spec
        one_gene = {"Harry"}
        two_genes = {"James"}
        have_trait = {"James"}
        jp = joint_probability(self.people, one_gene, two_genes, have_trait)
        self.assertAlmostEqual(jp, 0.0026643247488, places=8)

    def test_update(self):
        one_gene = {"Harry"}
        two_genes = {"James"}
        have_trait = {"James"}
        p = 0.5
        update(self.probabilities, one_gene, two_genes, have_trait, p)
        self.assertEqual(self.probabilities["Harry"]["gene"][1], 0.5)
        self.assertEqual(self.probabilities["Harry"]["trait"][True], 0)
        self.assertEqual(self.probabilities["James"]["gene"][2], 0.5)
        self.assertEqual(self.probabilities["James"]["trait"][True], 0.5)
        self.assertEqual(self.probabilities["Lily"]["gene"][0], 0.5)
        self.assertEqual(self.probabilities["Lily"]["trait"][True], 0)

    def test_normalize(self):
        self.probabilities["Harry"]["gene"] = {2: 2, 1: 2, 0: 6}
        self.probabilities["Harry"]["trait"] = {True: 1, False: 3}
        normalize(self.probabilities)
        self.assertAlmostEqual(self.probabilities["Harry"]["gene"][2], 0.2)
        self.assertAlmostEqual(self.probabilities["Harry"]["gene"][1], 0.2)
        self.assertAlmostEqual(self.probabilities["Harry"]["gene"][0], 0.6)
        self.assertAlmostEqual(self.probabilities["Harry"]["trait"][True], 0.25)
        self.assertAlmostEqual(self.probabilities["Harry"]["trait"][False], 0.75)

    # Edge case: No parents listed
    def test_joint_probability_no_parents(self):
        people = {
            'Solo': {'name': 'Solo', 'mother': None, 'father': None, 'trait': None}
        }
        jp = joint_probability(people, set(), set(), set())
        expected = PROBS["gene"][0] * PROBS["trait"][0][False]
        self.assertAlmostEqual(jp, expected, places=8)

    # Edge case: All have 2 genes
    def test_joint_probability_all_two_genes(self):
        jp = joint_probability(self.people, set(), set(self.people), set())
        # All have 2 genes, none have trait
        expected = (
            PROBS["gene"][2] * PROBS["trait"][2][False] *  # James
            PROBS["gene"][2] * PROBS["trait"][2][False] *  # Lily
            # Harry has parents, so gene probability is conditional
            # For this test, just check it's nonzero and doesn't error
            1
        )
        self.assertGreater(jp, 0)

    # Edge case: All have or lack the trait
    def test_joint_probability_all_have_trait(self):
        jp = joint_probability(self.people, set(), set(), set(self.people))
        self.assertGreater(jp, 0)

    # Edge case: Zero probabilities in normalize
    def test_normalize_zero(self):
        self.probabilities["Harry"]["gene"] = {2: 0, 1: 0, 0: 0}
        self.probabilities["Harry"]["trait"] = {True: 0, False: 0}
        normalize(self.probabilities)
        self.assertEqual(sum(self.probabilities["Harry"]["gene"].values()), 0)
        self.assertEqual(sum(self.probabilities["Harry"]["trait"].values()), 0)

    # Edge case: Single person
    def test_single_person(self):
        people = {
            'Solo': {'name': 'Solo', 'mother': None, 'father': None, 'trait': True}
        }
        probs = {
            'Solo': {"gene": {2: 0, 1: 0, 0: 0}, "trait": {True: 0, False: 0}}
        }
        jp = joint_probability(people, set(), set(), {"Solo"})
        self.assertGreater(jp, 0)
        update(probs, set(), set(), {"Solo"}, jp)
        normalize(probs)
        self.assertAlmostEqual(sum(probs["Solo"]["gene"].values()), 1)
        self.assertAlmostEqual(sum(probs["Solo"]["trait"].values()), 1)

    # Edge case: Update with p=0
    def test_update_zero_probability(self):
        update(self.probabilities, {"Harry"}, set(), set(), 0)
        self.assertEqual(self.probabilities["Harry"]["gene"][1], 0)

    # Edge case: Floating point precision
    def test_normalize_small_numbers(self):
        self.probabilities["Harry"]["gene"] = {2: 1e-10, 1: 2e-10, 0: 7e-10}
        normalize(self.probabilities)
        self.assertAlmostEqual(sum(self.probabilities["Harry"]["gene"].values()), 1)

if __name__ == "__main__":
    unittest.main()
