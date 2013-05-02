EasyCache 0.3.0,  est un logiciel de conversion de fichier Eclipse Aria 10 (RP.dcm) vers le format propriétaire EasyCut (.ecf).

Objectifs, atouts :
- Simplifier/fiabiliser la fabrication des caches.
- Plus de point de découpe (Eclipse 300pts / digitaliser 20pts)
- Précision dans les coordonnées (supprimer l’étage humaine digitaliser)

EasyCache :

 


EasyCut :

 


Procédure d’export Eclipse :

 


Principe simplifié d’utilisation :

<pre>
1)	Export du Cache RP.dcm via filtre export Eclispe (voir PrintSceen ci-dessus).
2)	Ouvrir EasyCache : 
  a.	[ Source ] Fichier_Eclipse.dcm
  b.	[Cible] Dossier_de_destination
  c.	[Process] Exécute la procédure de conversion « .dcm/.ecf »
3)	Copier le fichier créé par EasyCache sur une disquette.
4)	Insérer la disquette dans l’ordinateur EasyCut .
5)	Dans EasyCut, Ajouter au registre le FICHIER_EasyCache.ecf
6)	Appliquer la procédure normale de création de cache.
7)	Toujours penser à comparer le PrintScreen Eclipse et le cache finalisé par EasyCut.
</pre>

FAIT :
- Kernel de conversion .dcm>.ecf
- Squelette d’une GUI (interface utilisateur).
- Représentation graphique du cache
- PrintScreen pour procédure export eclispe.

A FAIRE :
- Visualisation du RP_.dicm initial dans la Gui principale
- Intégrer le coef agrandissement. (actuellement X9)
- Coder en GTK/QT une nouvelle GUI.
- Phase de test grandeur nature.
- Rédiger procédure finale.
- Tester avec utilisateurs.

