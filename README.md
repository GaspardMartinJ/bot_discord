# ReminderBot

## Description du bot

Ce bot permet de ping une liste de personnes située dans un tableau google sheets et de vérifier en combien de temps il réagissent en l'écrivant dans le tableau.

## Prérequis

pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

Vous pouvez utiliser le tableau fourni (en remplaçant les noms par les membres de votre serveur) ou en créer un autre et mettre son ID dans un fichier sheetID.json
Pour utiliser l'API google sheets il faut normalement se créer un fichier credentials.json qui va demander confirmation à un compte google qui à accès au projet google cloud mais je vous ai envoyé un fichier token.json qui permet de ne pas avoir à s'identifier pendant un certain temps.

## Fonction

Le bot a une seule commande qui éxecute une action: !ping