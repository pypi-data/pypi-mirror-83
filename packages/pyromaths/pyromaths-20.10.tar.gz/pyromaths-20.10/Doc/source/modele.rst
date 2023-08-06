:title: Réaliser un modèle de document
:date: 2009-09-16 12:00
:category: contribuer
:author: Arnaud, modifié par Louis Paternault
:description: Réaliser un modèle de document

Personnaliser un modèle de document
===================================

A quoi ça sert ?
----------------

Chacun aime personnaliser les documents qu’il donnera aux élèves.
La nouvelle mouture de pyromaths permet désormais cela, à condition de s’y connaître un peu en LaTeX.

En effet, chacune des fiches créées par pyromaths l'est par le biais modèles (ou *templates*), c'est-à-dire de fichiers ayant une extension .tex (fichiers LaTeX) qui sont ensuite compilés sous forme de pdf, pour ceux le désirant.

Par conséquent, réaliser un modèle pour pyromaths revient à réaliser un modèle LaTeX, avec deux ou trois règles supplémentaires.

De plus vous pourrez contribuer à pyromaths en proposant votre modèle, et le partageant aux autres utilisateurs de pyromaths.
C’est l’avantage de la communauté du libre. Toute proposition sera la bienvenue :)

Par défaut, Pyromaths propose deux modèles, à savoir pyromaths.tex et evaluation.tex.

Comment ?
---------

Comme dit plus haut, il suffit presque seulement de réaliser un modèle LaTeX, qui sera ensuite passé à la moulinette du moteur `jinja2 <http://jinja.pocoo.org/>`_ (avec quelques modifications indiquées dans :ref:`une note <jinja2>` du tutoriel :ref:`ecrire`.

Quelques mots-clés sont donc remplacés par leurs valeurs lors de la réalisation des fiches.
Ces mots-clés correspondent soit aux options du programme, soit au contenu des exercices. 
Ils sont faciles à repérer en raison de leur syntaxe, c’est-à-dire délimités par ``(( variable ))``. Les principaux sont :

-  ``(( titre ))`` : titre de la page voulu dans les options ;
-  ``(( niveau ))`` : niveau précisé dans les options ;
- ``(( enonce ))`` et ``(( corrige ))`` : booléens indiquant s'il faut ou non générer, respectivement, l'énoncé et le corrigé des exercices ;
- ``(( exercices ))`` : liste des exercices.

Des structures de contrôles sont aussi disponibles. Par exemple, pour exécuter du code seulement si le corrigé est demandé, on pourra utiliser :

.. code-block:: latex

    (* if corrige *)
    Voici le corrigé des exercices.
    (* endif *)

Pour afficher chaque énoncé d'exercice suivi de son corrigé, on pourra utiliser :

.. code-block:: latex

    (* for exo in exercices *)
        (( exo.tex_statement() ))
        (( exo.tex_answer() ))
    (* endfor *)

Une fois le modèle fini, il faudra le placer dans le dossier :

-  **$HOME/.config/pyromaths/modeles** sous LINUX,
-  **C:\Documents and Settings\vous\Application Data\pyromaths\modeles** sous WINDOWS,
-  **~/Library/Application Support/Pyromaths/templates/** sur MAC OS X,

puis relancer Pyromaths, et votre modèle apparaitra automatiquement dans la liste des modèles dans l’onglet « Options ».

À titre d’exemple, vous pouvez consulter le modèle :download:`pyromaths.tex <../../pyromaths/data/templates/pyromaths.tex>`.
