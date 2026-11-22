Buts: je veux faire un script bash pour pouvoir passer les updates linux sur des machines en remote ssh

Je veux un script en python qui va créer le script bash start-updates.sh sous cette forme:

ssh utilisateur@ip_du_serveur1 '/chemin/vers/mon_script.sh'
ssh utilisateur@ip_du_serveur2 '/chemin/vers/mon_script.sh'
ssh utilisateur@ip_du_serveur3 '/chemin/vers/mon_script.sh'
ssh utilisateur@ip_du_serveur4 '/chemin/vers/mon_script.sh'
...

'utilisateur@ip_du_serveur' est à rechercher dans un fichier d'inventaire de services .csv, qui sera un argument d'input du script python

'/chemin/vers/mon_script.sh' sera toujours le même, qui sera un argument d'input du script python
