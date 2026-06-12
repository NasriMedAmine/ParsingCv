from algoTest5 import AlgoTest

Algo = AlgoTest()
result = Algo.hedhiFixPdfFileLPointO("cvTest/cv2.pdf")

if not result["success"]:
    print("Error:", result["error"])
    print("Message:", result["message"])
else:
    liste = Algo.hedhiTrajaaliCoorAsemiCle(result, Algo.SECTION_HEADERS)
    resultat = Algo.hedhiTrajaaliChildrenMotCle(result, liste,True)
    Algo.writeResultatJson(resultat)






