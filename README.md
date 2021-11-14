# DatavizProject


### Etude du CSV 
Ce projet a pour but d'étudier différents CSV portant sur les valeurs foncières en France.
<br/>J'ai donc commencé par étudier les différents CSV afin de comprendre leurs colonnes, je me suis ensuite intéressé à l'étude du CSV 2020 en particulier et eu l'idée de plusieurs graphs que vous pourrez découvrir par vous-même.


### Réduction du temps de chargement
Etant donnée la taille du dataset, j'ai décidé d'en lire un sample de 500 000 lignes au départ afin d'exécuter mes tests plus rapidement. 
J'ai aussi supprimé les colonnes qui ne m'intéressaient pas commes les "lots" ou les "anciens code commune".
<br/>Pour accélerer le chargement du site, j'ai mis en dehors du main les différents graphiques et maps.

### Problème de taille du CSV
Le CSV étant trop volumineux, il ne pouvait pas être push sur Github. Il m'a fallu parser le CSV pour pouvoir l'utiliser.

### Autre problème
Streamlit share ne semblait pas posséder la librairie matplotlib, et il m'a fallu un moment pour trouver la solution et l'importer grâce au requirement.txt
