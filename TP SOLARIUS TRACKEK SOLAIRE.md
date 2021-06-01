TP211-SOLARIUS

L'objectif est de construire un programme en Python qui gèrera le changement de position du panneau solaire, pour qu'il suive la course du soleil.

Nous découperons la phase de développement en 3 étapes distinctes:

    Créez un Flowchart pour chacun des sénarios suivant.
    Prendre contrôle des Servos Moteurs
    Faire interagir les moteurs en fonction des résultats de capteurs de luminosités

- Scénario 1 :
Flowchart n°1 :
https://lucid.app/lucidchart/40d2b70c-0aa2-4439-b235-f6b58229d0df/edit?viewport_loc=216%2C-124%2C1480%2C595%2C0_0&invitationId=inv_a30fe013-a4ad-4072-aad6-ad4289be47d3


- Scénario 2 :
Flowchart n°2 :
...

- Programme arduino :
Il y a deux codes arduinos : les versions v2 et v3. Ces deux versions sont différentes mais permettent toutes les deux de contrôler un tracker solaire à 2 axes.
(la version v3 doit mieux fonctionner que la version v2, c'est à tester)

- Enregistrer de la date avec un datalogger :
Il y a deux programmes : l'un de base qui fonctionne mais qui s'avère être inutile car le temps de charge et de décharge de la batterie n'est pas pris en compte;
l'autre programme prend en compte l'horodatage, c'est-à-dire que le temps est pris en compte.

