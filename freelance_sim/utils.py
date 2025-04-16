def calcul_impot_progressif(revenu_imposable):
    tranches = [
        (0, 11294, 0.00),
        (11294, 28797, 0.11),
        (28797, 82341, 0.30),
        (82341, 177106, 0.41),
        (177106, float("inf"), 0.45),
    ]
    impot_total = 0.0

    for bas, haut, taux in tranches:
        if revenu_imposable > bas:
            montant_imposable = min(revenu_imposable, haut) - bas
            impot_total += montant_imposable * taux
        else:
            break
    return round(impot_total, 2)
