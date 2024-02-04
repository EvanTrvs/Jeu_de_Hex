# Développement d'une Interface complète pour le jeu de HEX

## Introduction
Ce projet consiste à l'implémentation d'un jeu de société appelé HEX, accompagné de multiples fonctionnalités complémentaires allant de la sauvegarde de parties aux stratégies de jeu.

## Jeu de HEX
Le jeu de Hex est un jeu de société de plateau pour deux joueurs se déroulant sur une grille hexagonale en forme de losange. Conçu par des mathématiciens dans les années 40, c'est un jeu de stratégie combinatoire abstrait, asynchrone (tour à tour), fini, à information parfaite, sans hasard et match nul. Avec des règles simples, il offre une grande profondeur stratégique et est étudié dans divers domaines mathématiques.

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

## Utilisation
### Installation
Téléchargement de toutes les sources du dépot [Jeu_de_Hex](https://github.com/EvanTrvs/Jeu_de_Hex).

### Dépendances
Ce projet necessite [Python 3.x](https://www.python.org/downloads/) pour être exécuté.
Des librairies sont requise, pour les installer aisément, nous conseillons l'utilisation d'[Anaconda](https://www.anaconda.com) ou autres IDE python.
  ```bash
  pip install numpy
  pip install tk
  pip install pillow
  ```
## Exécution
Le fichier à exécuter est jeu.py

## Configuration d'une partie
* Taille du plateau
* Mode de Jeu avec temps limité
* Sélection : Joueur contre Joueur - Joueur contre Bot - Bot contre Bot
* Sélection de la stratégie de jeu du Bot


## Sauvegardes
Possibilitées de Sauvegarde de partie, trois emplacements de sauvegarde disponible avec chargement et éditions de celles-ci.

### Auteurs
[EvanTrvs](https://github.com/EvanTrvs) et Thibaud
