# ParsingCv


Pour exécuter ce projet :

Allez dans le fichier test.py et exécutez-le.




Algo = AlgoTest()

Cette classe contient toute la logique du projet.



result = Algo.hedhiFixPdfFileLPointO("cvTest/cv.pdf")

Cette fonction traite chaque page du CV comme un rectangle, applique un repère dont le centre est le point O(0,0), puis retourne une liste contenant les coordonnées du point O pour chaque page.



liste = Algo.hedhiTrajaaliCoorAsemiCle(result, Algo.SECTION_HEADERS)

Cette fonction prend en entrée :

result
Algo.SECTION_HEADERS (les mots-clés qui apparaissent généralement dans tous les CV, comme Experience, Formation, etc.)

Elle retourne une liste des coordonnées de ces mots-clés selon notre repère centré en O pour chaque page.

resultat = Algo.hedhiTrajaaliChildrenMotCle(result, liste, True)

Cette fonction prend en entrée :

result
liste
True : cela signifie qu'elle applique la logique récursive où chaque élément peut avoir ses propres enfants.

Elle retourne une liste contenant tous les mots-clés du CV ainsi que leurs éléments enfants associés.

Algo.writeResultatJson(resultat, "resultat")

Cette fonction écrit le résultat final dans un fichier JSON nommé resultat.
