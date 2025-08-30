import unittest
import math
from analise_entropia import calculate_shannon_entropy

class TestShannonEntropy(unittest.TestCase):
    """Testes para a função calculate_shannon_entropy."""

    def test_empty_string(self):
        """Testa se uma string vazia retorna entropia 0."""
        self.assertEqual(calculate_shannon_entropy(""), 0.0)

    def test_string_with_no_variety(self):
        """Testa se uma string com apenas um caractere repetido tem entropia 0."""
        self.assertEqual(calculate_shannon_entropy("aaaaa"), 0.0)

    def test_string_with_perfect_balance(self):
        """Testa uma string com dois caracteres em igual proporção (entropia máxima de 1 bit)."""
        self.assertAlmostEqual(calculate_shannon_entropy("ababab"), 1.0)
        self.assertAlmostEqual(calculate_shannon_entropy("01"), 1.0)

    def test_known_entropy_value(self):
        """
        Testa uma string com um valor de entropia conhecido.
        Para "abc", P(a)=1/3, P(b)=1/3, P(c)=1/3.
        Entropia = -[3 * (1/3 * log2(1/3))] = log2(3)
        """
        expected_entropy = math.log2(3)
        self.assertAlmostEqual(calculate_shannon_entropy("abc"), expected_entropy)

    def test_case_sensitivity(self):
        """Testa se a função diferencia maiúsculas e minúsculas."""
        # "aA" tem entropia 1.0, enquanto "aa" tem 0.0
        self.assertAlmostEqual(calculate_shannon_entropy("aA"), 1.0)
        self.assertNotEqual(calculate_shannon_entropy("aA"), calculate_shannon_entropy("aa"))

    def test_string_with_varied_probabilities(self):
        """
        Testa uma string com probabilidades desiguais: "aaab"
        P(a) = 3/4, P(b) = 1/4
        Entropia = -[(3/4 * log2(3/4)) + (1/4 * log2(1/4))]
        """
        expected_entropy = -((3/4 * math.log2(3/4)) + (1/4 * math.log2(1/4)))
        self.assertAlmostEqual(calculate_shannon_entropy("aaab"), expected_entropy)

if __name__ == '__main__':
    unittest.main()
