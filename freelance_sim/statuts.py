from .utils import calcul_impot_progressif


class Entreprise:
    def __init__(self, chiffre_affaires):
        self.chiffre_affaires = chiffre_affaires

    def calcul_resultat(self):
        raise NotImplementedError("Méthode à implémenter par chaque statut")


class AutoEntrepreneur(Entreprise):
    def __init__(self, chiffre_affaires, taux_micro_social=0.22, type_activite="BNC"):
        super().__init__(chiffre_affaires)
        self.taux_micro_social = taux_micro_social
        self.type_activite = type_activite.upper()

        self.abattements = {"BIC": 0.50, "BNC": 0.34, "VENTE": 0.71}

    def calcul_resultat(self):
        if self.type_activite not in self.abattements:
            raise ValueError(
                f"Type d’activité invalide. Choisis parmi {list(self.abattements.keys())}"
            )

        # 1. Charges sociales
        revenu_avant_ir = self.chiffre_affaires * (1 - self.taux_micro_social)

        # 2. Revenu imposable après abattement fiscal
        abattement_fiscal = self.abattements[self.type_activite]
        revenu_imposable = self.chiffre_affaires * (1 - abattement_fiscal)

        # 3. Impôt sur le revenu (barème progressif)
        impot_ir = calcul_impot_progressif(revenu_imposable)

        # 4. Revenu net final
        revenu_net = revenu_avant_ir - impot_ir

        return {
            "statut": f"Auto-entrepreneur ({self.type_activite})",
            "revenu_net": round(revenu_net, 2),
            "charges_sociales": round(
                self.chiffre_affaires * self.taux_micro_social, 2
            ),
            "revenu_imposable": round(revenu_imposable, 2),
            "impot_revenu": round(impot_ir, 2),
        }


class SASU(Entreprise):
    def __init__(
        self,
        chiffre_affaires,
        charges_fixes=0,
        reserve_rnd=0,
        ratio_salaire=1.0,
    ):
        super().__init__(chiffre_affaires)
        self.charges_fixes = charges_fixes
        self.reserve_rnd = reserve_rnd
        self.ratio_salaire = ratio_salaire

        # Cotisations sociales en SASU : environ 65 % du salaire brut
        self.taux_cotisations = 0.65

    def calcul_is_progressif(self, resultat_societe):
        """
        Calcule l’impôt sur les sociétés selon le barème progressif :
        - 15 % jusqu'à 42 500 €
        - 25 % au-delà
        Source : https://www.impots.gouv.fr
        """
        is_total = 0
        if resultat_societe <= 0:
            return 0
        if resultat_societe <= 42500:
            is_total = resultat_societe * 0.15
        else:
            is_total = 42500 * 0.15 + (resultat_societe - 42500) * 0.25
        return is_total

    def calcul_resultat(self):
        # Bénéfice brut avant rémunération
        resultat = self.chiffre_affaires - self.charges_fixes

        # Réserve R&D (non déductible pour l'instant)
        reserve = resultat * self.reserve_rnd
        resultat_avant_ir = resultat - reserve

        # Répartition entre salaire et dividendes
        salaire_brut = resultat_avant_ir * self.ratio_salaire
        dividendes_bruts = resultat_avant_ir * (1 - self.ratio_salaire)

        # Cotisations sociales sur salaire
        cotisations = salaire_brut * self.taux_cotisations
        salaire_net = salaire_brut - cotisations

        # Résultat restant en société = bénéfice imposable
        resultat_societe = resultat_avant_ir - salaire_brut

        # Impôt sur les sociétés (IS) progressif
        is_ = self.calcul_is_progressif(resultat_societe)

        # Dividendes soumis au PFU (30 %)
        dividendes_net = (
            dividendes_bruts * 0.70
        )  # 30 % PFU (12.8 % IR + 17.2 % prélèvements sociaux)

        # Total revenu perçu par le dirigeant
        revenu_total = salaire_net + dividendes_net

        return {
            "statut": f"SASU (salaire {int(self.ratio_salaire * 100)}%)",
            "revenu_net": round(revenu_total, 2),
            "salaire_net": round(salaire_net, 2),
            "dividende_net": round(dividendes_net, 2),
            "cotisations": round(cotisations, 2),
            "impot_societe": round(is_, 2),
            "reserve_rnd": round(reserve, 2),
        }


class EURL(Entreprise):
    def __init__(
        self,
        chiffre_affaires,
        charges_fixes=0,
        taux_cotisations=0.45,  # ⚠️ Peut varier entre 40 % et 50 % selon le cas
        reserve=0.0,
    ):
        """
        EURL à l'IR (impôt sur le revenu), gérant majoritaire assimilé travailleur non salarié (TNS)

        Sources :
        - Cotisations TNS : https://www.service-public.fr/professionnels-entreprises/vosdroits/F32351
        - Barème IR : https://www.impots.gouv.fr/particulier/les-tranches-du-bareme-de-limpot-sur-le-revenu
        """
        super().__init__(chiffre_affaires)
        self.charges_fixes = charges_fixes
        self.taux_cotisations = taux_cotisations
        self.reserve = reserve  # proportion du résultat mise en réserve (optionnelle)

    def calcul_resultat(self):
        # 1. Résultat comptable brut (avant rémunération)
        resultat = self.chiffre_affaires - self.charges_fixes

        # 2. Réserve (utile pour R&D ou auto-financement)
        reserve_val = resultat * self.reserve
        resultat_net = resultat - reserve_val

        # 3. Cotisations sociales (environ 45 % du revenu)
        cotisations = resultat_net * self.taux_cotisations

        # 4. Revenu imposable (avant IR)
        revenu_avant_ir = resultat_net - cotisations

        # 5. IR progressif
        impot = calcul_impot_progressif(revenu_avant_ir)

        # 6. Revenu net perçu par le gérant
        revenu_net = revenu_avant_ir - impot

        return {
            "statut": "EURL (IR)",
            "revenu_net": round(revenu_net, 2),
            "revenu_imposable": round(revenu_avant_ir, 2),
            "cotisations": round(cotisations, 2),
            "impot_revenu": round(impot, 2),
            "reserve": round(reserve_val, 2),
        }
