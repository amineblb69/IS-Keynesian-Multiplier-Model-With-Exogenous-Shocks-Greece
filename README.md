# Simulation d’un choc exogène — Multiplicateur keynésien (Grèce)

Ce projet implémente un modèle simplifié du **multiplicateur keynésien en économie fermée** afin de simuler l’impact macroéconomique de **chocs exogènes** sur l’économie grecque.

Toutes les donees sont en millions d'euros. Source : OCDE

Le modèle permet d’étudier comment des variations sur :
- la consommation autonome (**c0**),
- l’investissement (**I**),
- les dépenses gouvernementales (**G**),

affectent :
- la demande globale (**Z**),
- le PIB / revenu d’équilibre (**Y**),
- le revenu disponible (**Yd**),
- l’épargne (**S**),

via le mécanisme du multiplicateur keynésien.

---

## Contexte

- Pays étudié : **Grèce**
- Période : **2014–2024**
- Cadre théorique : **modèle du multiplicateur keynésien (économie fermée)**
- Équation principale : **Z = C + I + G**

Le projet est basé sur la note de conjoncture associée (PDF fourni dans le dépôt).

---

## Fonctionnalités

- Importation des séries macroéconomiques depuis un fichier Excel (`data.xlsx`) Source
- Estimation de la **fonction de consommation** par régression linéaire :
  - consommation autonome `c0`
  - propension marginale à consommer `c1`
- Calcul de :
  - la demande globale `Z`
  - la production / PIB `Y`
  - les impôts `T` (taux proportionnel `t`)
  - l’épargne et sa fonction estimée
- Application de **chocs exogènes** (au choix) sur `c0`, `I` et/ou `G`
- Calcul du **multiplicateur keynésien** :
  - `k = 1 / (1 - c1(1 - t))`
- Génération de graphiques :
  1. Consommation vs Revenu disponible (avant choc)
  2. Épargne vs Revenu disponible (avant choc)
  3. Équilibre keynésien (Z vs Y) avant choc
  4. Investissement et dépenses publiques (avec moyennes)
  5. Comparaison avant/après choc

---

## Structure du projet

├── choc_exogene.py # script principal
├── data.xlsx # données (obligatoire)
├── Note de Conjoncture P2.pdf # rapport associé
└── README.md


---

## Prérequis

Python 3.9+ recommandé.

Installer les dépendances :

```bash
pip install pandas numpy matplotlib openpyxl pandas_datareader

