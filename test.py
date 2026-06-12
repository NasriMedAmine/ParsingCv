from algoTest5 import AlgoTest

Algo = AlgoTest()
<<<<<<< HEAD
result = Algo.hedhiFixPdfFileLPointO("cvTest/cv2.pdf")
=======
result = Algo.hedhiFixPdfFileLPointO("cvTest/cv.pdf")
>>>>>>> 359960276af13563f2db7a9a3c46003bc5688046

if not result["success"]:
    print("Error:", result["error"])
    print("Message:", result["message"])
else:
    liste = Algo.hedhiTrajaaliCoorAsemiCle(result, Algo.SECTION_HEADERS)
    resultat = Algo.hedhiTrajaaliChildrenMotCle(result, liste,True)
<<<<<<< HEAD
    Algo.writeResultatJson(resultat)
=======
    Algo.writeResultatJson(resultat,"resultat")
>>>>>>> 359960276af13563f2db7a9a3c46003bc5688046






