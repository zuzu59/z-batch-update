# Générateur de script de mises à jour Linux à distance

## Objectif

Créer un programme Python qui génère localement un script Bash nommé `start-updates.sh`. Ce script Bash lancera, via SSH, le script de mises à jour indiqué sur chaque serveur sélectionné dans un inventaire CSV.

Le programme Python **génère** le script Bash ; il ne se connecte pas aux serveurs et n’exécute pas les mises à jour.

## Format de l’inventaire

Le chemin de l’inventaire est fourni par l’utilisateur au lancement du programme. Le format et les colonnes peuvent varier : examine le fichier d’entrée et identifie les informations nécessaires pour construire les destinations SSH. Ne code en dur ni le nom ni le chemin d’un fichier d’inventaire particulier.

Traite uniquement les enregistrements dont le champ `tagIds` contient la valeur numérique `6`. Pour ces enregistrements seulement, recherche le champ `ssh1String` dans les données du CSV et extrais-en le couple `utilisateur@adresse_du_serveur`. Ce champ est la source à utiliser pour la destination ; ne reconstruis pas celle-ci à partir d’autres champs lorsque `ssh1String` est présent.

## Entrées et sortie attendues

Le programme Python doit accepter en entrée, au minimum :

1. le chemin du fichier CSV d’inventaire ;
2. le chemin absolu du script de mises à jour à exécuter sur les serveurs.

Il génère `start-updates.sh` dans le répertoire courant. Si tu proposes une option permettant de choisir le chemin de sortie, conserve `start-updates.sh` comme valeur par défaut.

Pour chaque serveur retenu, le fichier généré doit contenir une commande de la forme :

```bash
ssh utilisateur@adresse_du_serveur '/chemin/absolu/du/script.sh'
```

Le chemin du script distant est le même pour toutes les commandes.

## Traitement de l’inventaire

- Lire les données CSV et décoder les champs structurés si le format de l’inventaire en utilise.
- Filtrer d’abord les enregistrements : ne traiter que ceux dont `tagIds` contient la valeur numérique `6` (et non une simple sous-chaîne ou une valeur différente).
- Pour les enregistrements retenus, repérer `ssh1String`, en extraire le couple `utilisateur@adresse_du_serveur` et construire la destination SSH à partir de ce couple. Le CSV peut nécessiter le décodage de champs structurés pour accéder à ces valeurs.
- Ignorer proprement les enregistrements qui ne contiennent pas assez d’informations pour construire une destination SSH ; signaler combien ont été ignorés et pourquoi, sans afficher de données sensibles.
- Ne jamais utiliser ni écrire dans le script généré les mots de passe, données chiffrées ou autres secrets présents dans l’inventaire.
- Vérifier le format réel de `ssh1String` et en extraire uniquement le couple `utilisateur@adresse_du_serveur` ; ne pas recopier aveuglément toute la valeur comme commande OpenSSH, car elle peut contenir un préfixe ou un alias.
- Si un enregistrement contient plusieurs connexions SSH, ne lance pas plusieurs mises à jour sur le même serveur sans règle explicite. Si la règle de sélection ne peut pas être déduite sans risque, demande une précision avant de coder ce comportement. Toute règle retenue doit être documentée.

## Qualité et sécurité

- Citer correctement les valeurs insérées dans le script Bash afin que les espaces et caractères spéciaux ne produisent pas de commandes incorrectes ou dangereuses.
- Valider les arguments et afficher des erreurs compréhensibles pour un fichier absent, un CSV invalide, un JSON invalide ou un chemin de script distant manquant/invalide.
- Ne pas exécuter automatiquement `start-updates.sh` après sa génération.
- Générer un script lisible, avec un shebang Bash. Le rendre exécutable si cela est approprié.
- Éviter les dépendances externes si la bibliothèque standard Python suffit.
- Ajouter ou mettre à jour les tests et la documentation d’utilisation selon les conventions déjà présentes dans le dépôt.

## Critères d’acceptation

1. Une commande documentée permet de lancer le programme avec un CSV et un chemin de script distant.
2. Le programme produit `start-updates.sh` avec une commande SSH pour chaque serveur retenu, sans inclure de secrets.
3. Le script généré est syntaxiquement valide et les chemins contenant des caractères spéciaux sont correctement protégés.
4. Les lignes ou enregistrements invalides sont gérés avec des messages utiles, sans échec silencieux.
5. Des tests couvrent au minimum la lecture de l’inventaire, la génération des commandes, les données manquantes et l’échappement des valeurs.
6. La génération n’établit aucune connexion SSH et ne lance aucune mise à jour.

## Consignes de travail

Commence par examiner le dépôt et la structure de l’inventaire fourni par l’utilisateur. Si une décision fonctionnelle nécessaire (notamment le choix entre plusieurs connexions SSH pour un enregistrement) ne peut pas être prise à partir des informations disponibles, pose la question avant de l’implémenter. Ensuite, implémente la solution, ajoute les tests pertinents et indique comment l’utiliser ainsi que les vérifications effectuées.
