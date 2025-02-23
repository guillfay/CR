## IA hybride pour le raisonnement "musical" incertain

### Analyse et prise de décision collective dans le choix d’un genre musical

Alice, Bob, Charlie et Dora doivent sélectionner un genre musical pour un événement commun. Les préférences de chacun sont exprimées sous forme d’une évaluation chiffrée :

**Genre musical**| Alice | Bob | Charlie | Dora |
--- | --- | --- | --- | --- |
pop | 14 | 18 | 13 | 5 |
jazz | 16 | 5 | 15 | 15 |
electro | 6 | 16 | 13 | 16 |
classique | 18 | 7 | 17 | 10 |
rock | 9 | 20 | 8 | 16 |
hip-hop | 11 | 17 | 17 | 6 |
blues | 17 | 11 | 7 | 16 |

L’objectif est de déterminer un choix collectif respectant certains principes fondamentaux de justice et d’efficacité.

### Réorganisation des préférences et symétrie

Afin d’assurer une prise en compte équitable des opinions, les évaluations sont réorganisées dans un ordre croissant pour chaque genre musical :

**Genre musical**| 👤1 | 👤2 | 👤3 | 👤4 |
--- | --- | --- | --- | --- |
p↑ | 5 | 13 | 14 | 18 |
j↑ | 5 | 15 | 15 | 16 |
e↑ | 6 | 13 | 16 | 16 |
c↑ | 7 | 10 | 17 | 18 |
r↑ | 8 | 9 | 16 | 20 |
h↑ | 6 | 11 | 17 | 17 |
b↑ | 7 | 11 | 16 | 17 |

Cette transformation permet d’examiner les disparités et d’évaluer la cohérence de la sélection finale avec les principes de redistribution et d’égalité.

### Dominance de Lorenz

Le critère de dominance de Lorenz est utilisé pour comparer les genres musicaux en fonction de leurs performances redistribuées. Un genre musical est dit dominant sur un autre s’il possède de meilleures sommes cumulées à chaque étape de classement.

#### Exemple : Comparaison entre jazz et hip-hop

- Jazz : (5, 15, 15, 16)
- Hip-hop : (6, 11, 17, 17)

Sommes cumulées :
- Jazz : 5, 20, 35, 51
- Hip-hop : 6, 17, 34, 51

On observe que j↑ ≽ h↑ car à chaque étape, la somme cumulée de jazz est supérieure ou égale à celle du hip-hop.
Dans ce cas, on a les dominances suivantes :  
jazz↑ $\succsim_L$ ​pop↑, electro↑ $\succsim_L$ ​pop↑, electro↑ $\succsim_L$ hip-hop↑, classique↑ $\succsim_L$ ​hip-hop↑, blues↑ $\succsim_L$ ​pop↑, blues↑ $\succsim_L$ ​classique↑, blues↑ $\succsim_L$ ​hip-hop↑

### Raisonnement redistributif

Un raisonnement redistributif permet d’ajuster les évaluations afin de garantir une meilleure équité. Un transfert de Pigou-Dalton peut être appliqué pour redistribuer une partie de l’utilité des plus favorisés vers les moins favorisés.

#### Exemple : Redistribution pour le jazz
- Avant : (5, 15, 15, 16)
- Après transfert : (6, 14, 15, 16)

Ce transfert améliore l’équité sans altérer la somme totale des évaluations.

Comparaison des poids OWA

On définit les jeux de paramètres suivants :


Poids $\omega$| 👤1 | 👤2 | 👤3 | 👤4 |
--- | --- | --- | --- | --- |
$\omega^1$ | 1 | 0 | 0 | 0 |
$\omega^2$ | 0 | 1 | 0 | 0 |
$\omega^3$ | 0 | 0 | 0 | 1 |
$\omega^4$ | 1 | 0 | 0 | 1 |
$\omega^5$ | 1 | -1 | -1 | 1 |
$\omega^6$ | 1 | 1 | 1 | 1 |
$\omega^7$ | 4 | 2 | 3 | 4 |

Les relations obtenues selon ces poids peuvent être analysées afin de déterminer lesquelles satisfont les propriétés suivantes :

- (s) Symétrie,
- (e) Efficacité,
- (r) Redistributivité,
- (t) Transitivité.

#### Résultats et implications

Certains jeux de poids, comme $\omega^6$ (égalité parfaite) et $\omega^7$ (privilégiant les plus favorisés), respectent la dominance de Lorenz et garantissent des résultats équitables.

Les poids comme $\omega^5$ introduisent des effets non désirables en inversant certaines préférences et ne respectent pas toujours la transitivité.

Le sous-ensemble $\Omega$ des poids garantissant toutes les propriétés précédentes comprend principalement les poids équilibrés ($\omega^6$ et $\omega^7$).

#### Comparaison avec la dominance de Lorenz

Lorsqu’un poids OWA appartient à $\Omega$, la relation de préférence induite par OWA est compatible avec la dominance de Lorenz. Cela signifie qu’un choix optimisé selon $\succsim_\omega$ respectera les principes de redistribution et garantira un choix collectif plus équitable.

### Critère OWA (Ordered Weighted Average)

L’OWA est une méthode de pondération qui permet d’affecter plus d’importance aux individus les moins satisfaits. En appliquant des coefficients pondérés, nous pouvons obtenir des décisions plus justes.

#### Calcul OWA avec poids (1,2,3,4)

- Jazz : 5x1 + 15x2 + 15x3 + 16x4 = 144
- Hip-hop : 6x1 + 11x2 + 17x3 + 17x4 = 147

Avec cette pondération, le hip-hop serait préféré.

### Incomplétude du raisonnement redistributif

L’application des transferts de Pigou-Dalton et du critère de dominance de Lorenz peut ne pas toujours suffire pour établir une hiérarchie complète entre les genres musicaux. Certaines comparaisons peuvent nécessiter un cadre plus large de prise de décision.

#### Exemple d’incomplétude
Si deux genres possèdent des évaluations très proches et des distributions symétriques, les outils précédents ne permettent pas de trancher de manière définitive. Une approche mixte combinant OWA et dominance peut être nécessaire.

### Conclusion

L’application des concepts de dominance de Lorenz, de raisonnement redistributif et d’OWA permet d’obtenir une approche rigoureuse et équitable pour la prise de décision collective. Toutefois, certaines comparaisons peuvent rester indécidables et nécessiter des méthodes complémentaires pour assurer une prise de décision robuste.

