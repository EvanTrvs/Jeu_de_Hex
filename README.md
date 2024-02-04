# Interface pour le jeu de HEX, Version Présentation

## Introduction
Ce projet vise à implémenter le jeu de société HEX pour une utilisation complète, en ajoutant diverses fonctionnalités telles que la sauvegarde des parties et l'intégration de stratégies de jeu.
Cette version simplifiée permet une utilisation restreinte du projet dans un contexte de démonstration pédagogique.

## Jeu de HEX
Le [jeu de Hex](https://fr.wikipedia.org/wiki/Hex) est un jeu de société de plateau pour deux joueurs se déroulant sur une grille hexagonale en forme de losange. Conçu par des mathématiciens dans les années 40, c'est un jeu de stratégie combinatoire abstrait, asynchrone (tour à tour), fini, à information parfaite, sans hasard et match nul. Avec des règles simples, il offre une grande profondeur stratégique et est étudié dans divers domaines mathématiques.

### Règles du jeu
- Nombre de joueurs : 2
- Matériel : Un plateau de jeu, des pions rouges et des pions bleues.
Le plateau du jeu de Hex est composé de cases hexagonales formant un 
losange. La taille du plateau peut varier (habituellement 6x6, 9x9 ou 11x11). 
Deux cotés opposés du losange sont rouges, les deux autres sont bleues.
- Préparation : Le plateau est vide
- Déroulement : Le joueur rouge commence. Les joueurs jouent chacun leur 
tour. À chaque tour, le joueur place un pion de sa couleur sur une case libre 
du plateau. Il ne peut y avoir qu'un pion par case. Les pions posés le sont 
définitivement, ils ne peuvent être ni retirés, ni déplacés.
- Objectif : Le premier joueur qui réussit à relier ses deux bords par un chemin 
de pions contigus de sa couleur a gagné.

![illustration plateau de jeu avec victoire](https://media.discordapp.net/attachments/1087514695268847656/1203760499402215534/image.png?ex=65d24453&is=65bfcf53&hm=85e037d4cbebf64f18080f56f104628da083317fb863f38199e0e9bdf441ea51&=&format=webp&quality=lossless)

## Installation éxécutable
Téléchargement du dossier [Jeu Hex executable](https://github.com/EvanTrvs/Jeu_de_Hex/tree/Pr%C3%A9sentation-format/Jeu%20Hex%20executable) et extraction des deux archives.
Ensuite éxécution de `Hex.exe`, nécessite d'être dans un dossier accompagné de `graphismes` et `Jeu_Hex`.

## Installation code source
Téléchargement de toutes les sources de [Jeu Hex sources](https://github.com/EvanTrvs/Jeu_de_Hex/tree/Pr%C3%A9sentation-format/Jeu%20Hex%20sources).

Ce projet nécessite [Python 3.x](https://www.python.org/downloads/) pour être exécuté. Des librairies sont requise, pour les installer aisément, nous conseillons l'utilisation d'[Anaconda](https://www.anaconda.com) ou autres IDE python.
  ```bash
  pip install numpy
  pip install tk
  pip install pillow
  ```
Le fichier à exécuter est `jeu.py`.
  ```bash
  python jeu.py
  ```

### Illustration
![illustration accueil](https://media.discordapp.net/attachments/1087514695268847656/1203768380478201947/image.png?ex=65d24baa&is=65bfd6aa&hm=770c0515f1f99fc760780f904622661b0e303266fd250351cc2d15fd247e39d4&=&format=webp&quality=lossless)
![illustration jeu](https://media.discordapp.net/attachments/1087514695268847656/1203768755461689404/image.png?ex=65d24c04&is=65bfd704&hm=4a53d0f0c2d26ca6da45e5151cc4022fca8172895809f03dc0c4e09d4c2d14b2&=&format=webp&quality=lossless)

## Configurations Possibles
- Mode Joueur contre Joueur : les joueurs placent des pions à tour de rôle en utilisant la souris.
- Mode Joueur contre Ordinateur : le joueur rouge est un utilisateur qui place des pions à la souris, tandis que le joueur bleu est contrôlé par l'ordinateur.
- Mode Ordinateur contre Ordinateur : une partie est jouée automatiquement entre deux joueurs ordinateurs.

### Démonstration
Le programme permet de choisir entre 3 modes de jeu, configurer la taille de l'application et mettre en plein écran (touche F11).
De telle sorte que la personne qui lance le programme peux lancer soit un mode Joueur/Joueur(chacun son tour) ou Joueur/Ordinateur(un peu difficile) ou Ordinateur/Ordinateur(démonstration de jeu).
Les modes sont préconfigurer, tous de taille de plateau 8x8, et une fois dans un mode, il est possible de relancer autant de partie que souhaité.


Ainsi, une fois un mode lancé, le jeu peu être jouer avec seulement la souris, et contraint en plein écran pour garantir de rester dans le mode (pour quitter: echap ou fermer la fenêtre).
Cela permet une utilisation robuste simple avec uniquement une souris et un écran, sans possibilité de fermeture ou de blocage, ce qui le rend idéal pour un accès libre à tous public.

### Fenêtre
- Taille de fenêtre (Bouton +/- en haut à droite de l'accueil)
- Plein écran (F11 ou Bouton en haut à droite de l'accueil)
- Echap pour revenir en arrière ou quitter

## Auteurs
[EvanTrvs](https://github.com/EvanTrvs) et Thibaud, projet 2022
[EvanTrvs](https://github.com/EvanTrvs), adaptation 2024
