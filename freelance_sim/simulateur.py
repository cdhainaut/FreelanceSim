from .statuts import AutoEntrepreneur, SASU, EURL


def simulation_globale(chiffre_affaires):
    résultats = {}

    résultats["AutoEntrepreneur"] = AutoEntrepreneur(chiffre_affaires).calcul_resultat()

    for ratio in [1.0, 0.7, 0.5, 0.0]:
        sasu = SASU(chiffre_affaires, ratio_salaire=ratio)
        résultats[f"SASU_{int(ratio*100)}%_salaire"] = sasu.calcul_resultat()

    return résultats
