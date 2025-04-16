import argparse
from .simulateur import simulation_globale


def main():
    parser = argparse.ArgumentParser(
        description="Simulateur de revenus net en fonction du statut juridique"
    )
    parser.add_argument("ca", type=float, help="Chiffre d'affaires annuel (en €)")
    args = parser.parse_args()

    résultats = simulation_globale(args.ca)
    for statut, data in résultats.items():
        print(f"\n=== {statut} ===")
        for k, v in data.items():
            print(f"{k.replace('_', ' ').capitalize()} : {v} €")


if __name__ == "__main__":
    main()
