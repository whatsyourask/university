import unittest
from backend import pollards_rho_method, AttackOnRSA


class TestBackend(unittest.TestCase):
    def __test_pollards_rho_method(self, p: int, q: int):
        n = p * q
        possible_divisor = pollards_rho_method(n)
        self.assertIn(possible_divisor, (p, q))
        self.assertIn(n / possible_divisor, (p, q))

    def test_12bits(self):
        p = 1327
        q = 1181
        self.__test_pollards_rho_method(p, q)

    def test_30bits(self):
        p = 486996833
        q = 770135917
        self.__test_pollards_rho_method(p, q)

    def test_50bits(self):
        p = 338201456447623
        q = 645273123397939
        self.__test_pollards_rho_method(p, q)

    def __test_attack(self, plaintext: str, encrypted: str, e: int, n: int):
        _, _, _, decrypted = AttackOnRSA.attack(e, n, encrypted)
        self.assertEqual(decrypted, plaintext)

    def test_attack_15bits(self):
        plaintext = "Hello, World!"
        encrypted = "26515931 12610670 24803395 24803395 17814658 27471753 19794384 13471508 17814658 25618726 24803395 9494046 19690139"
        e = 14354001
        n = 32863981
        self.__test_attack(plaintext, encrypted, e, n)

    def test_attack_30bits(self):
        plaintext = "Hello, World!"
        encrypted = "233314989601659798 176294785143253597 286331027717199362 286331027717199362 6109062196030731 100510058167785442 7002488460440039 117993167963309807 6109062196030731 170473700256848875 286331027717199362 365293760505648362 45957498795509591"
        e = 277448968873825999
        n = 370429619997018499
        # 72257551216679941
        self.__test_attack(plaintext, encrypted, e, n)

    def test_attack_50bits(self):
        plaintext = "Hello, World!"
        encrypted = "1190532331065494131737455560 42389204164982006601344956876 48440431754228245186466002107 48440431754228245186466002107 64579062017041776934678890039 58242098670621416576045286032 60540328738793107446109700662 46966415825434763989369075668 64579062017041776934678890039 8972962971596065397802832624 48440431754228245186466002107 69231792106454421441506481367 14862963429665234199837786822"
        e = 13430419676232286936440638547
        n = 74690913542475549876549042727
        self.__test_attack(plaintext, encrypted, e, n)
