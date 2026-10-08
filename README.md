# CineMatch AI

Analyse du catalogue TMDB et classification des films selon leur engagement.
Le code actif est conserve jusqu'a la classification. Les ajouts separes de validation, clustering, Streamlit, Airflow et Docker ont ete retires a la demande de l'utilisateur.
Le cahier_des_charges.txt conserve les exigences initiales.

## Notebooks conserves

1. notebooks/01_extraction.ipynb : extraction TMDB et cache JSON.
2. notebooks/02_cleaning_mongodb.ipynb : nettoyage, MongoDB, requetes et agregations.
3. notebooks/03_eda.ipynb : exploration et visualisations.
4. notebooks/04_feature_engineering.ipynb : features et indicateurs de genres.
5. notebooks/05_tfidf.ipynb : vectorisation des synopsis.
6. notebooks/04_classification.ipynb : Logistic Regression, Random Forest et Linear SVM.

Le notebook de classification reste inchange, y compris ses cellules preexistantes de validation croisee, GridSearchCV et sauvegarde.

## Utilisation

Depuis la racine, installer les dependances avec `python -m pip install -r requirements.txt`, puis lancer `python -m notebook`.
Configurer son propre TMDB_TOKEN dans .env pour l'extraction. MongoDB doit etre accessible pour les cellules de stockage. Ne pas publier .env.

## Donnees et modele

- data/raw/tmdb_raw.json : donnees brutes.
- data/processed/movies_clean.csv : donnees nettoyees.
- data/processed/movies_features.csv : donnees enrichies.
- models/classifier_rf.pkl : sauvegarde produite par le notebook de classification.

La cible high_engagement utilise le troisieme quartile de vote_count. Cette colonne est exclue des entrees du modele.
La validation croisee preexistante utilise l'ensemble de X et y, y compris les lignes du test; ce n'est pas une validation independante du jeu de test. Les resultats restent experimentaux.

## Jira et nettoyage

[Tableau Jira du projet CineMatch AI](https://mouadboumahdicode.atlassian.net/jira/software/projects/CIN/boards/2?filter=&groupBy=none&atlOrigin=eyJpIjoiNTEyMThkNGUyOWFmNDYwNmI0MDg4YzU3YTkxZjY1MDYiLCJwIjoiaiJ9)

docs/jira_project_completed.csv contient 19 taches pour les etapes 1 a 6. Modifier le CSV local ne modifie pas les taches deja importees dans Jira.

Les commandes de suppression ont ete bloquees par la politique d'execution. Les fichiers texte ont ete retires avec l'outil d'edition. Restent a supprimer manuellement : models/optimized_classifier_rf.joblib, models/movie_clusters.joblib, models/cluster_svd.joblib, docs/screenshots/ et les caches __pycache__ des modules retires. Ils ne sont plus utilises par le code conserve.
