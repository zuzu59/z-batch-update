# Générateur de script de mises à jour Linux à distance

## Objectif

Créer un programme Python qui génère localement un script Bash nommé `start-updates.sh`. Ce script Bash lancera, via SSH, le script de mises à jour indiqué sur chaque serveur sélectionné dans un inventaire CSV.

Le programme Python **génère** le script Bash ; il ne se connecte pas aux serveurs et n’exécute pas les mises à jour.

## Format de l’inventaire

Le chemin de l’inventaire est fourni par l’utilisateur au lancement du programme. Le format et les colonnes peuvent varier : examine le fichier d’entrée et identifie les informations nécessaires pour construire les destinations SSH. Ne code en dur ni le nom ni le chemin d’un fichier d’inventaire particulier.

Traite uniquement les enregistrements dont le champ `tagIds` contient la valeur numérique `6`. Pour ces enregistrements seulement, utilise l’intégralité du contenu de leur champ `ssh1String` comme commande SSH, y compris la commande, ses options et sa destination. N’en extrais pas seulement le couple `utilisateur@adresse_du_serveur` et ne reconstruis pas la commande à partir d’autres champs.

## Entrées et sortie attendues

Le programme Python doit accepter en entrée, au minimum :

1. le chemin du fichier CSV d’inventaire ;
2. la commande distante à exécuter sur les serveurs : elle peut être le chemin absolu d’un script ou une commande shell inline, par exemple `sudo apt update ; sudo apt install -y nano`.

Il génère `start-updates.sh` dans le répertoire courant. Si tu proposes une option permettant de choisir le chemin de sortie, conserve `start-updates.sh` comme valeur par défaut.

Pour chaque enregistrement retenu, le fichier généré doit reprendre intégralement la commande de `ssh1String`, puis lui ajouter la commande distante comme argument SSH unique, correctement citée. Exemple de commande distante inline :

```bash
sshg utilisateur@hôte 'sudo apt update ; sudo apt install -y nano'
```

La même commande distante est utilisée sur tous les serveurs.

## Traitement de l’inventaire

- Lire les données CSV et décoder les champs structurés si le format de l’inventaire en utilise.
- Filtrer d’abord les enregistrements : ne traiter que ceux dont `tagIds` contient la valeur numérique `6` (et non une simple sous-chaîne ou une valeur différente).
- Pour les enregistrements retenus, récupérer l’intégralité de `ssh1String` et l’utiliser comme commande SSH, en préservant la commande, les options et la destination. Le CSV peut nécessiter le décodage de champs structurés pour accéder à cette valeur.
- Ignorer proprement les enregistrements qui ne contiennent pas assez d’informations pour construire une destination SSH ; signaler combien ont été ignorés et pourquoi, sans afficher de données sensibles.
- Ne jamais utiliser ni écrire dans le script généré les mots de passe, données chiffrées ou autres secrets présents dans l’inventaire.
- Vérifier le format réel de `ssh1String` et préserver son contenu complet dans la commande générée. Citer ou analyser les éléments de façon sûre sans supprimer la commande, les options ou la destination.
- Si un enregistrement contient plusieurs connexions SSH, ne lance pas plusieurs mises à jour sur le même serveur sans règle explicite. Si la règle de sélection ne peut pas être déduite sans risque, demande une précision avant de coder ce comportement. Toute règle retenue doit être documentée.

## Qualité et sécurité

- Citer correctement les valeurs insérées dans le script Bash afin que les espaces et caractères spéciaux ne produisent pas de commandes incorrectes ou dangereuses.
- Valider les arguments et afficher des erreurs compréhensibles pour un fichier absent, un CSV invalide, un JSON invalide ou une commande distante manquante/invalide. Accepter les commandes inline contenant des espaces et des opérateurs shell, et les transmettre comme une seule commande distante.
- Ne pas exécuter automatiquement `start-updates.sh` après sa génération.
- Générer un script lisible, avec un shebang Bash. Le script doit définir l’alias `sshg='ssh -A -o SendEnv="GIT*"'` et activer l’expansion des alias Bash (`shopt -s expand_aliases`) avant les commandes générées, afin que les valeurs `ssh1String` utilisant `sshg` fonctionnent dans le script non interactif.
- Activer le mode debug Bash (`set -x`) afin d’afficher les commandes avant leur exécution. Arrêter le script dès qu’une commande échoue (`set -e`) et afficher clairement la ligne et le code de sortie de l’erreur.
- Rendre le script exécutable si cela est approprié.
- Éviter les dépendances externes si la bibliothèque standard Python suffit.
- Ajouter ou mettre à jour les tests et la documentation d’utilisation selon les conventions déjà présentes dans le dépôt.

## Critères d’acceptation

1. Une commande documentée permet de lancer le programme avec un CSV et un chemin de script ou une commande distante inline.
2. Le programme produit `start-updates.sh` avec une commande SSH pour chaque serveur retenu, sans inclure de secrets.
3. Le script généré est syntaxiquement valide et les chemins contenant des caractères spéciaux sont correctement protégés.
4. Les lignes ou enregistrements invalides sont gérés avec des messages utiles, sans échec silencieux.
5. Des tests couvrent au minimum la lecture de l’inventaire, la génération des commandes, les données manquantes et l’échappement des valeurs.
6. La génération n’établit aucune connexion SSH et ne lance aucune mise à jour.

## Consignes de travail

Commence par examiner le dépôt et la structure de l’inventaire fourni par l’utilisateur. Si une décision fonctionnelle nécessaire (notamment le choix entre plusieurs connexions SSH pour un enregistrement) ne peut pas être prise à partir des informations disponibles, pose la question avant de l’implémenter. Ensuite, implémente la solution, ajoute les tests pertinents et indique comment l’utiliser ainsi que les vérifications effectuées.
