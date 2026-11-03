# Student Manager AZ

Application de bureau en Python pour gérer les étudiants, leurs matières et leurs notes, avec une interface graphique Tkinter et une base SQLite locale.

## Fonctionnalités

- Ajouter, afficher, rechercher et supprimer des étudiants.
- Enregistrer les coordonnées et la classe des étudiants.
- Consulter les matières prédéfinies : Python, SQL, Réseaux, Systèmes et Web.
- Ajouter des notes entre 0 et 20 et consulter les notes et la moyenne par étudiant.
- Afficher le nombre d’étudiants, la moyenne générale et les moyennes par classe.
- Conserver les données dans SQLite entre deux lancements.

## Prérequis

- Python 3.12 ou supérieur, inférieur à Python 4.
- Tkinter disponible dans l’installation Python et un environnement graphique.
- Poetry 2 pour installer le projet depuis les sources et construire les distributions.

SQLite et Tkinter font partie de la bibliothèque standard Python ; certaines distributions Linux nécessitent l’installation du paquet système `python3-tk`. Vérification de Tkinter :

```sh
python -m tkinter
```

## Installation depuis les sources

Ouvrir un terminal dans le dossier contenant `pyproject.toml` :

```sh
poetry install
```

## Lancement

Depuis la racine du projet :

```sh
poetry run student-manager
```

Alternative :

```sh
poetry run python -m student_manager_az
```

Dans PyCharm, utiliser une configuration Python avec le **nom de module** `student_manager_az`, le dossier racine du projet comme répertoire de travail et l’interpréteur de l’environnement Poetry.

La base `student_manager.db` est créée automatiquement dans le répertoire de travail au premier lancement, avec les matières prédéfinies. Utiliser un dossier accessible en écriture et conserver le même répertoire de travail pour retrouver ses données. Les bases existantes du projet ne sont pas distribuées.

## Tests

```sh
poetry run python -m pytest student_manager_az/tests
```

Pytest est une dépendance de développement ; il n’est pas requis pour utiliser l’application installée.

## Construction du package

```sh
poetry check
poetry build
```

Les deux distributions sont générées dans `dist/` :

- `student_manager_az_chhay_baert_gonzales-0.1.0-py3-none-any.whl` : roue installable.
- `student_manager_az_chhay_baert_gonzales-0.1.0.tar.gz` : archive des sources avec les tests et le README.

Installation de la roue depuis la racine du projet :

```sh
python -m pip install dist/student_manager_az_chhay_baert_gonzales-0.1.0-py3-none-any.whl
student-manager
```

Le nom de distribution est `student-manager-az-chhay-baert-gonzales`. Le module Python reste `student_manager_az` et la commande reste `student-manager`.

Le nom de distribution ne renvoyait aucun projet sur TestPyPI lors de la vérification du 3 novembre 2026. Cela ne réserve pas le nom : sa disponibilité doit être vérifiée à nouveau avant publication. Cette étape prépare les distributions, sans les publier.

## Structure

- `student_manager_az/database/` : connexions et initialisation SQLite.
- `student_manager_az/services/` : étudiants, matières, notes et statistiques.
- `student_manager_az/ui/` : interface graphique.
- `student_manager_az/main.py` : démarrage de l’application.
- `student_manager_az/tests/` : tests automatisés, inclus uniquement dans l’archive source.

Les bases de données, les caches Python et la configuration de l’IDE sont exclus des distributions.

## Auteurs

Nathan Chhay-Trinh, Astrid Baërt et Nathaniel Gonzales Librea.
