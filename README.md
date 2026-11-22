# z-batch-update

Génère un script Bash pour lancer une commande sur des machines distantes via SSH.

## Utilisation

```bash
python3 generate_updates.py chemin/vers/inventaire.csv 'sudo apt update ; sudo apt install -y nano'
```

Le programme crée `start-updates.sh` dans le répertoire courant. Il retient les enregistrements dont `tagIds` contient le nombre `6`, puis reprend l’intégralité de leur champ `ssh1String` (commande, options et destination) en lui ajoutant la commande distante, qui peut être un chemin de script ou une commande shell inline. Pour une commande inline, entourez-la de guillemets dans l’appel Python afin que les opérateurs comme `;` soient transmis comme argument. Les commandes identiques sont dédupliquées. Le script généré définit l’alias `sshg='ssh -A -o SendEnv="GIT*"'` et active l’expansion des alias Bash pour que les commandes de l’inventaire puissent l’utiliser. Les secrets du CSV ne sont pas copiés dans le script généré.

Le programme **ne lance pas** le script généré. Lorsqu’il est exécuté manuellement, le script affiche les commandes (`set -x`), s’arrête à la première erreur (`set -e`) et signale la ligne et le code de sortie en cas d’échec. Vérifiez son contenu avant de l’exécuter vous-même :

```bash
less start-updates.sh
```

Les fichiers CSV d’inventaire sont ignorés par Git (`*.csv`) et ne doivent pas être commités.

## Tests

```bash
python3 -m unittest discover -s tests
```
