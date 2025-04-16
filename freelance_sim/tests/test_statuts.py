import pytest
from freelance_sim.statuts import AutoEntrepreneur, SASU, EURL


@pytest.mark.parametrize("ca, expected_net_min", [(50000, 30000), (100000, 60000)])
def test_autoentrepreneur_bnc(ca, expected_net_min):
    ae = AutoEntrepreneur(chiffre_affaires=ca, type_activite="BNC")
    res = ae.calcul_resultat()
    assert res["statut"] == "Auto-entrepreneur (BNC)"
    assert res["revenu_net"] >= expected_net_min
    assert res["revenu_net"] <= ca


def test_sasu_salaire_100():
    sasu = SASU(chiffre_affaires=80000, charges_fixes=10000, ratio_salaire=1.0)
    res = sasu.calcul_resultat()
    assert res["statut"] == "SASU (salaire 100%)"
    assert res["revenu_net"] > 0
    assert res["salaire_net"] > res["dividende_net"]
    assert res["impot_societe"] == 0


def test_sasu_mixte():
    sasu = SASU(chiffre_affaires=100000, charges_fixes=10000, ratio_salaire=0.5)
    res = sasu.calcul_resultat()
    assert res["salaire_net"] > 0
    assert res["dividende_net"] > 0
    assert res["revenu_net"] > 0
    assert res["impot_societe"] > 0


def test_eurl_ir():
    eurl = EURL(chiffre_affaires=80000, charges_fixes=10000)
    res = eurl.calcul_resultat()
    assert res["statut"] == "EURL (IR)"
    assert res["cotisations"] > 0
    assert res["impot_revenu"] >= 0
    assert res["revenu_net"] > 0


def test_eurl_reserve():
    eurl = EURL(chiffre_affaires=60000, charges_fixes=5000, reserve=0.10)
    res = eurl.calcul_resultat()
    assert abs(res["reserve"] - 0.10 * (60000 - 5000)) < 1
    assert res["revenu_net"] > 0


if __name__ == "__main__":
    pytest.main()
