import pytest
from freelance_sim.utils import calcul_impot_progressif


@pytest.mark.parametrize(
    "revenu_imposable, expected_impot",
    [
        # Tranche 1 : 0%
        (10000, 0.0),  # Pas d'impôt pour un revenu inférieur ou égal à 11294 €
        # Tranche 2 : 11%
        (
            15000,
            11294 * 0.00 + (15000 - 11294) * 0.11,
        ),  # Revenu entre 11294 € et 28797 €
        # Tranche 3 : 30%
        (
            50000,
            11294 * 0.00 + (28797 - 11294) * 0.11 + (50000 - 28797) * 0.30,
        ),  # Revenu entre 28797 € et 82341 €
        # Tranche 4 : 41%
        (
            100000,
            11294 * 0.00
            + (28797 - 11294) * 0.11
            + (82341 - 28797) * 0.30
            + (100000 - 82341) * 0.41,
        ),  # Revenu entre 82341 € et 177106 €
        # Tranche 5 : 45%
        (
            200000,
            11294 * 0.00
            + (28797 - 11294) * 0.11
            + (82341 - 28797) * 0.30
            + (177106 - 82341) * 0.41
            + (200000 - 177106) * 0.45,
        ),  # Revenu au-delà de 177106 €
    ],
)
def test_calcul_impot_progressif(revenu_imposable, expected_impot):
    """
    Teste le calcul de l'impôt sur le revenu en fonction des tranches progressives.
    """
    impot_calculé = calcul_impot_progressif(revenu_imposable)
    assert round(impot_calculé, 2) == round(expected_impot, 2), (
        f"Erreur: pour un revenu imposable de {revenu_imposable}, "
        f"l'impôt calculé est {impot_calculé}, mais {expected_impot} était attendu."
    )


if __name__ == "__main__":
    pytest.main()
