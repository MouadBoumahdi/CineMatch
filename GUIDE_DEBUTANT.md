# Movie Intelligence — guide de départ

Ce guide accompagne le [cahier des charges](cahier_des_charges.txt). Il suit la
version de travail du projet : **analyse, classification et clustering**, sans
recommandation.

## 1. Quel problème veut-on résoudre ?

Imagine une plateforme qui possède des milliers de films. Elle veut répondre à
deux questions :

1. **Quels films risquent d'avoir beaucoup d'engagement ?** Nous définirons
   une étiquette `high_engagement` à partir du nombre de votes (`vote_count`).
   Un modèle de **classification** apprendra à prédire oui ou non à partir
   d'autres informations disponibles sur le film.
2. **Quels types de films existent dans le catalogue ?** Un algorithme de
   **clustering** regroupera les films qui se ressemblent, sans connaître les
   groupes à l'avance. Nous décrirons ensuite chaque groupe avec des chiffres
   et des exemples de films.

Avant ces deux questions, il faut récupérer des données fiables. TMDB fournit
les données, Python les récupère et les nettoie, et MongoDB les stocke. Nous
analyserons ensuite les films avec des tableaux et des graphiques. Le résumé
textuel (`overview`) sera transformé en nombres avec TF-IDF pour pouvoir être
utilisé dans l'analyse ou les modèles.

**Exemple imaginaire :** un film a pour genre « animation », une durée de
95 minutes, un résumé et 3 000 votes. Si le seuil choisi pour le fort
engagement est 1 000 votes, son étiquette vaut « oui ». Le nombre de votes
sert à construire la bonne réponse, mais il ne doit pas être donné au modèle
comme indice pour prédire cette réponse.

## 2. Les mots à comprendre, dans l'ordre

| Mot | Explication simple | Quand nous l'utiliserons |
| --- | --- | --- |
| API | Un service auquel un programme demande des données. | J1 : demander des films à TMDB. |
| JSON | Un format de texte qui contient des champs et leurs valeurs. | J1 : conserver les réponses originales. |
| Pandas / DataFrame | Un outil Python pour travailler avec un tableau de données. | J2-J3 : nettoyer et explorer. |
| MongoDB | Une base de données qui stocke des documents proches du JSON. | J2 : enregistrer et interroger les films. |
| Agrégation MongoDB | Une suite d'opérations pour filtrer, regrouper et trier. | J2 : compter des films par genre, par exemple. |
| EDA | Exploration des données avec tableaux et graphiques. | J3 : comprendre ce que contient le catalogue. |
| Feature | Une information donnée à un modèle, comme l'année ou la durée. | J3 : choisir et créer les entrées. |
| Data leakage | Donner au modèle une information qui révèle déjà la réponse ou qui ne serait pas disponible au moment de prédire. | J3-J6 : vérifier les features et la validation. |
| TF-IDF | Une méthode qui représente les mots d'un texte par des nombres en donnant plus de poids aux mots distinctifs. | J4 : transformer `overview`. |
| Classification | Prédire une catégorie connue, ici engagement fort : oui/non. | J5-J6 : entraîner et évaluer trois modèles. |
| Validation croisée | Répéter entraînement et validation sur plusieurs découpages des données. | J6 : vérifier la stabilité des résultats. |
| GridSearchCV | Essayer plusieurs réglages d'un modèle et comparer leurs scores. | J6 : optimiser un modèle. |
| Clustering | Créer des groupes sans étiquette connue à l'avance. | J7-J8 : découvrir des profils de films. |
| K-Means | Un algorithme qui place les films dans K groupes selon leurs caractéristiques. | J7 : essayer plusieurs K. |
| Silhouette Score | Une mesure qui aide à voir si les groupes sont séparés. | J7 : comparer plusieurs K. |
| Streamlit | Un outil Python pour créer une interface web simple. | J10 : montrer le dashboard et les résultats. |
| Airflow | Un outil qui exécute des tâches dans un ordre prévu. | J9 : automatiser le pipeline. |
| Docker | Un moyen d'empaqueter une application et ses dépendances. | J9 : faciliter l'exécution du projet. |
| joblib | Un outil pour sauvegarder un modèle entraîné. | J9-J10 : le réutiliser dans Streamlit. |

## 3. Feuille de route adaptée

| Jour | Travail | Résultat à vérifier |
| --- | --- | --- |
| J1 | Comprendre l'API TMDB, créer l'accès, télécharger quelques films puis gérer pagination et erreurs. | JSON brut enregistré dans `data/raw/`. |
| J2 | Examiner, nettoyer et stocker les films dans MongoDB. | Tableau propre et requêtes, dont une agrégation. |
| J3 | Faire l'EDA et créer des features simples. | Graphiques interprétés et choix de features justifiés. |
| J4 | Comprendre et tester TF-IDF sur les résumés. | Matrice de texte et termes représentatifs expliqués. |
| J5 | Définir `high_engagement` et entraîner trois classifieurs. | Tableau comparatif des métriques. |
| J6 | Faire la validation croisée et GridSearchCV. | Comparaison avant/après optimisation. |
| J7 | Tester K-Means avec plusieurs valeurs de K. | Silhouette Score et premier choix de K. |
| J8 | Décrire les clusters et consolider les analyses. | Profils de groupes compréhensibles et exemples. |
| J9 | Automatiser avec Airflow, conteneuriser avec Docker, sauvegarder les modèles. | Pipeline reproductible. |
| J10 | Terminer Streamlit, tests, README, diagramme et préparation orale. | Démonstration fonctionnelle et livrables vérifiés. |

Le rythme peut changer selon le temps nécessaire pour comprendre chaque
notion. Nous avancerons par petites étapes : **pourquoi, exemple, code court,
résultat, explication du résultat**.

## 4. Documentation officielle à lire au bon moment

Il n'est pas nécessaire de lire tous ces liens aujourd'hui. Nous prendrons
uniquement la partie utile au moment de chaque étape.

- **J1 — TMDB :** [authentification de l'application](https://developer.themoviedb.org/docs/authentication-application), [démarrage](https://developer.themoviedb.org/v4/docs/getting-started) ; [Requests : premiers appels HTTP](https://requests.readthedocs.io/en/latest/user/quickstart/).
- **J2 — Pandas et MongoDB :** [tutoriels Pandas](https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html), [débuter avec MongoDB](https://www.mongodb.com/docs/manual/tutorial/getting-started/), [documents MongoDB](https://www.mongodb.com/docs/v8.0/core/document/), [agrégations](https://www.mongodb.com/docs/manual/aggregation/), [PyMongo](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/get-started/).
- **J4 — TF-IDF :** [extraction de caractéristiques textuelles avec scikit-learn](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction).
- **J5-J6 — Classification :** [métriques](https://scikit-learn.org/stable/modules/model_evaluation.html), [validation croisée](https://scikit-learn.org/stable/modules/cross_validation.html), [recherche de paramètres](https://scikit-learn.org/stable/modules/grid_search.html), [pipelines](https://scikit-learn.org/stable/modules/compose.html), [fuites de données](https://scikit-learn.org/stable/common_pitfalls.html).
- **J7 — Clustering :** [K-Means](https://scikit-learn.org/stable/modules/clustering.html#k-means), [exemple de Silhouette Score](https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html).
- **J9-J10 — Application :** [Airflow et ses DAGs](https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags.html), [Docker](https://docs.docker.com/get-started/docker-overview/), [Streamlit](https://docs.streamlit.io/get-started).

## 5. Notre premier petit pas

Le premier script est `src/extract_tmdb.py`. Il lit `TMDB_TOKEN` dans une
variable d'environnement, récupère la première page de films et enregistre
la réponse brute dans `data/raw/movies_page_1.json`. Nous vérifierons ce
premier résultat avant d'ajouter la pagination et les détails des films.
