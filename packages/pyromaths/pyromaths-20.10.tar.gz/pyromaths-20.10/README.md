[Pyromaths](http://pyromaths.org/) est un programme qui a pour but de créer des exercices type de mathématiques niveau collège et lycée ainsi que leur corrigé. C'est ce qu'on appelle parfois un exerciseur. Contrairement à de nombreux autres projets, Pyromaths a pour objectif de proposer une correction véritablement détaillée des exercices proposés et pas seulement une solution.

Il permet par exemple de proposer des devoirs maison aux élèves et de leur distribuer ensuite la correction. Il peut aussi servir à des familles afin qu'un élève puisse travailler un point du programme et se corriger ensuite.

Si vous voulez participer à la traduction, consultez [cette page](https://framagit.org/pyromaths/pyromaths/blob/develop/pyromaths/data/locale/TRADUIRE.md).

# Dépendances

Pour utiliser pyromaths, il faut :

* Python (version 3.5 ou supérieure) ;
* quelques bibliothèques python qui seront installées automatiquement avec pyromaths ;
* LaTeX (par exemple [TeXLive](https://tug.org/texlive/)), et de nombreux paquets, y compris le binaire ``latexmk`` (voir les instructions sur [le site web de Pyromaths](https://www.pyromaths.org/installer/)).

# Utiliser Pyromaths

Ce dépôt concerne la version en ligne de commandes. Vous cherchiez peut-être :

## Version en ligne

Il est possible d'utiliser Pyromaths sans l'installer, en utilisant [la version en ligne](http://enligne.pyromaths.org).

## Version de bureau

Pour GNU/Linux, Mac OS, Windows, visitez [la page d'installation](https://www.pyromaths.org/installer/).

## Version en ligne de commande

- Installation :

      pip install pyromaths

- Utilisation (par exemple, création d'une fiche d'exercice pour la spécialité math en terminale ES) :

      pyromaths generate EtatStableSysteme2 InterpolationMatrices

- Pour plus d'informations :

      pyromaths --help

# Développer Pyromaths

- Clonez le dépôt pour télécharger les sources.

        git clone https://framagit.org/pyromaths/pyromaths.git
        cd pyromaths

- Créer un virtualenv utilisant python3.

        virtualenv -ppython3 pyromaths-venv

- Installez les dépendances

        pip install -r requirements.txt

- Vous pouvez maintenant utiliser pyromaths, avec l'une ou l'autre des commandes suivantes.

        python -m pyromaths
        ./utils/pyromaths
