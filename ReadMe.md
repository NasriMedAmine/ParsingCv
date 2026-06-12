result = {
"pdf_file": "full/path/to/cv.pdf",

    "coordinate_system": "center_origin",

    "unit": "PDF point",

    "pages": [
        {
            "page": 1,

            "width": 595.28,
            "height": 841.89,

            "origin": {
                "name": "O",
                "x": 0.0,
                "y": 0.0,

                # old PDF position of the center
                "old_x": 297.64,
                "old_y": 420.94,
            },

            "rectangle": {
                # page limits in the new coordinate system
                "left": -297.64,
                "right": 297.64,
                "top": 420.94,
                "bottom": -420.94,
            },

            "lines": [
                {
                    "line_number": 1,
                    "page": 1,

                    "text": "Ahmed Ben Ali",

                    # text box limits in new coordinate system
                    "x0": -120.50,
                    "x1": 80.25,
                    "top": 350.12,
                    "bottom": 335.80,

                    # center of this text box
                    "x": -20.13,
                    "y": 342.96,

                    # aliases
                    "left": -120.50,
                    "right": 80.25,
                    "y_top": 350.12,
                    "y_bottom": 335.80,
                },

                {
                    "line_number": 2,
                    "page": 1,
                    "text": "Software Developer",
                    "x0": -90.10,
                    "x1": 95.60,
                    "top": 320.30,
                    "bottom": 306.10,
                    "x": 2.75,
                    "y": 313.20,
                    "left": -90.10,
                    "right": 95.60,
                    "y_top": 320.30,
                    "y_bottom": 306.10,
                },
            ],
        },

        {
            "page": 2,
            "width": 595.28,
            "height": 841.89,
            "origin": {...},
            "rectangle": {...}, a
            "lines": [...],
        },
    ],
}

w hedhi en general
result = {
"pdf_file": str,

    "coordinate_system": str,

    "unit": str,

    "pages": [
        {
            "page": int,

            "width": float,
            "height": float,

            "origin": {
                "name": str,
                "x": float,
                "y": float,
                "old_x": float,
                "old_y": float,
            },

            "rectangle": {
                "left": float,
                "right": float,
                "top": float,
                "bottom": float,
            },

            "lines": [
                {
                    "line_number": int,
                    "page": int,

                    "text": str,

                    "x0": float,
                    "x1": float,
                    "top": float,
                    "bottom": float,

                    "x": float,
                    "y": float,

                    "left": float,
                    "right": float,
                    "y_top": float,
                    "y_bottom": float,
                }
            ],
        }
    ],
}
























behy tao nheb methode trajaali liste esmha     hedhiTrajaaliCoorAsemiCle(x1,x2) x1 heya resultat adhika w x2 heya header


hedhi nhebha takra b kelma b kelma w tetcheki aala asemi mot cle ama shouf condition shniya , yelzem wakt talka kelma mot cle tabda mokhtalfa font size w color aala klem eli kablou moch ay kelma tetchakeha thotha yelzem tetaaked w taatini emplacement mtaaha par rapport point origine


w aandek class algo test hadher fih hedha deja  maaneha mattawedech haja maktouba deja ghadi


aatini code kemel




























behy  condition okhra , k detecti kelmet centres (mot cle ) aaref rak tesstana f  kelma baadha mot cle interet

bech tji f kelma wahda moch kelmtin kif tao maamalt
w hedhi tabaakha ala kol maathalan lkit f section kelma wahda experience khalik f kelma wahda experince Mot cle
lkit expériences professionnelles mot cle w enti tao detectit professionnelles  comme mot cle yelzmek kbalha bithabet f list mtaa klem elkol f instant adhika mdetecti deja kelmet expériences sinon tayechha w ahsbeha word*
lkit mathalan technical skills comme index f section w enti tao detectit technical  kbal matkayadha yelzemha f instant t+1 tkoun lkit kelmet skills bech tkaydha mot cle sinon tayech w ahsbeha word*

hani aaitek exemple b kbal w baaed bech tefhemn



aatini implemetation el bech nzidha a partir men code hedha

























behy tao aandek code hedha
hedha condtion 1L :  
ken detectit kelma mot cle shoufha f section one word wila alotwords ,
(nahki aala fard section)
condition loula 1 : heya kelma f section one word kahao , waktha ekhdem aadi
condition 2 : ken kelma f alotofword kahao kif exemple "centres d'interet" nofrdhou detecit kelmet centres aarfr eli heya f section "centres_interet" alotofwords , yelzmek baaed tetwakaa eli kelma jeya D'INTÉRÊT w khoudha k kelma wahda thnin moch kol wahda wahadha , wila exemple "parcours professionnel" enti hna detectit professionnel yelzem kbal t-1 enti deja mdetecti kelmet parcours bech thezhom thnin mot cle sinon tayech w ahsbeha word*
condtion 3 : ken lkelma mawjouda f thnin 1word w alotwords khoudh aala ases 1 word

w condition kbira 1L matemchi ela contion 2L temchi w eli heya :

bech tetdecti kelma lezem tkoun mokhtalfa aali kbal lkol (kbalha noskod word*) w lkol noksod - t klem eli sajaltou lkol moch kbal b x wila y

w lezem zeda tabda f ligne adhika mokhtlafa wahadha makifha had word*

ekhdem khedma dynamic moch just aala exemple eli aatithoulek khedma takhdem aala kol fard logiques w kasem les func aalekher iibara taamel f facotirsation




aatini code kemel



















aamel liste static feha awel element "&" , hedhi k yalkaha yahsebha kelma deja maaneha Formations & Certifications  yakrahom 3 kelmet moch wahdha , ama aamel lista khater momkon nzid hajet okhrin w zidha f code hseb mtaaha



























behy tao nheb ay kelma detectitha eli heya cle word , el klem eli iji baadou kol detectith aala ases children l mot cle adhika ama condition shniya

condition loula : nofrdhou f star detectit ken kelma barka mot cle , maaneha tao aandek ken mot cle wahda f star adheka , nofrdhou kelma aandha (x,y) just tahbet b ligne aal y  w ay kelma aadeya word* hotha f children l cle mot adhiak hata detecti kelma mot cle jdida taawed fard hesba


condition thenia : nordhou fard ligne detectit zouz kelmet mot cle , haka coord (x1,y1) w (x2,y2)
houma normalement aandhom nafs y , donc how chtaamel tao
ay kelma appartient [0 , x2-2unite[ hedhi hotha f children mtaa mot cle lawla
ay kelma appartient [x2-2unite hata l ekher safa X hedhi hotha f children mtaa mot cle thenia

aaleh x - 2unite bech nassuri eli mathalan fama symbole sghir kbal mot cle


condition 3 : nordhou fard ligne detectit 3 kelmet mot cle , haka coord (x1,y1) w (x2,y2) w (x3,y3)
houma normalement aandhom nafs y , donc how chtaamel tao
ay kelma appartient [0 , x2-2unite[ hedhi hotha f children mtaa mot cle lawla
ay kelma appartient [x2-2unite , x3 - 2unite[ hedhi hotha f children mtaa mot cle thenia
ay kelma appartient [x3-2unite hata l ekher safa X hedhi hotha f children mtaa mot cle theltha

aatini code haka b logique hedha w resultat killada json ,
aatini code kemel aala ases aandek deja test.py
just aatini code eli lezem nzidou mataawdlich eli aandi
hotli param eli najem nbadlhom mara okhra wahahdom men fok (kif -2unite)
w aamel hesbtek lkol aala ases point centre O w liste hedhi
liste = Algo.hedhiTrajaaliCoorAsemiCle(result, Algo.SECTION_HEADERS)




enta wakt detectit kelma mot cle mao tfahmna tahbet  w tabda thot f children a partir men COLUMN_OFFSET_X

ama zeda en parallel moch ay kelma toul tzidha dima lezmek dima tasti seaa ken kelma adhika mot cle w ila la
wila ken lkitha mot cle par exmple
tao detectit kelmet mot cle COMPÉTENCES w bdit tzid f children hata detectit 










behy tao nheb ay kelma detectitha eli heya cle word , el klem eli iji baadou kol detectith aala ases children l mot cle adhika ama condition shniya

condition loula : nofrdhou f star detectit ken kelma barka mot cle , maaneha tao aandek ken mot cle wahda f star adheka , nofrdhou kelma aandha (x,y) just tahbet b ligne aal y  w ay kelma aadeya word* hotha f children l cle mot adhiak hata detecti kelma mot cle jdida taawed fard hesba


condition thenia : nordhou fard ligne detectit zouz kelmet mot cle , haka coord (x1,y1) w (x2,y2)
houma normalement aandhom nafs y , donc how chtaamel tao
ay kelma appartient [0 , x2-2unite[ hedhi hotha f children mtaa mot cle lawla
ay kelma appartient [x2-2unite hata l ekher safa X hedhi hotha f children mtaa mot cle thenia

aaleh x - 2unite bech nassuri eli mathalan fama symbole sghir kbal mot cle


condition 3 : nordhou fard ligne detectit 3 kelmet mot cle , haka coord (x1,y1) w (x2,y2) w (x3,y3)
houma normalement aandhom nafs y , donc how chtaamel tao
ay kelma appartient [0 , x2-2unite[ hedhi hotha f children mtaa mot cle lawla
ay kelma appartient [x2-2unite , x3 - 2unite[ hedhi hotha f children mtaa mot cle thenia
ay kelma appartient [x3-2unite hata l ekher safa X hedhi hotha f children mtaa mot cle theltha

3 condition hedhom mayakhdmou ken ken condition 1F = false 


1F heya ken deja fama klem detectitou kbal mot cle wila (maneha yelzem aandek list taarf kadeh men kelma mot cle detectitha kbal w shniya heya )
ken la donc akhdemli b logique eli gotlek aalih 

tao ken deja detecit kelma mot cle w enti deja mdetecti deja kbalha eli fama mot cle

nodrdhou intervalle mtaa klem mot cle eli kbal que se soit wahed wila barcha houwa 
  xG < x < xF
x heya kool intevaller lkol eli tnajem mot cle wahdah wila barcha tkoun fihom f t adhika 
nofrdhou enti baadha detectit kelma mot cle 
condition loula : ken tao detectit kelma wahdha (x1,y1)  
ken x1 appartient intevall xG < x < xF tchouf anehi bithabet mot cle kdima eli appartient x1 liha heya , tnahiha w tabda thot f children l mot cle mtaa x1
w nafs hkeya ken thin w tletha 
dima shouf intervalle eli kbal w tchouf aneha mot cle eli jet baadha mot cle f intervalle mtaaha tnahiha maach taabi children w thot mot cle jdid section w tabda taabi f children



aatini code haka b logique hedha w resultat killada json ,
aatini code kemel aala ases aandek deja test.py
just aatini code eli lezem nzidou mataawdlich eli aandi
hotli param eli najem nbadlhom mara okhra wahahdom men fok (kif -2unite)
w aamel hesbtek lkol aala ases point centre O w liste hedhi
liste = Algo.hedhiTrajaaliCoorAsemiCle(result, Algo.SECTION_HEADERS)









































if (tao detectit kelam wahda mot cle )
detect A at xA
akhdem b logique mtaa detectit kelma wahdha f ligne wahed 


              if baaed detectit 1 words :
                detect B at xB 
                x3 = ekher kelma f ekher item f children A 
                x4 =  awel kelma f ekher item f children A
                if n'apparitent pas [x4-COLUMN_OFFSET_X , x3-COLUMN_OFFSET_X] :
                    kamel aamel children A w amel children B b fard logique houma zouz mot cle fard ligne
                fin if n'apparitent pas [x4-COLUMN_OFFSET_X , x3-COLUMN_OFFSET_X] : : 
                else if apparitent [x4-COLUMN_OFFSET_X , x3-COLUMN_OFFSET_X]
                    maach taamel children A w aamel tao children B b fard logique mtaa kelma wahdah mot cle f ligne
                fin else if apparitent [x4-COLUMN_OFFSET_X , x3-COLUMN_OFFSET_X]
              fin if baaed detectit 1 words :

              else if baaed detectit 2 words :
                hna menich khadem logique mtaaha khater siiba tji 

else if : tao detectit 2 kelmet mot cle 
    detect K at xK et L at xL
    akhdem b logique detectit 2 mot cle fard ligne 

    if baaed detectit 1 words :
        detectit kelma jdia S at xS
        xFK = ekher kelma f ekher item f children K -COLUMN_OFFSET_X
        xAK =  awel kelma f ekher item f children K -COLUMN_OFFSET_X

        xFL = ekher kelma f ekher item f children L  -COLUMN_OFFSET_X
        xAL =  awel kelma f ekher item f children L -COLUMN_OFFSET_X
        if ( xS appartient [ xAK - COLUMN_OFFSET_X , xFK - COLUMN_OFFSET_X]:
            habs aala aala K maach tzidou children w abda ahseb children l S 
            maa nafs logique 2 mot cle fard ligne L w S mara hedhi
        fin if ( xS appartient [ xAK - COLUMN_OFFSET_X , xFK - COLUMN_OFFSET_X]:
        else  if ( xS appartient [ xAL - COLUMN_OFFSET_X , xFL - COLUMN_OFFSET_X]:
            habs aala aala L maach tzidou children w abda ahseb children l S 
            maa nafs logique 2 mot cle fard ligne K w S mara hedhi
        fin else  if ( xS appartient [ xAL-COLUMN_OFFSET_X , xFL-COLUMN_OFFSET_X]:

        if xS n'appartient ni [ xAK-COLUMN_OFFSET_X , xFK-COLUMN_OFFSET_X] ni [ xAL-COLUMN_OFFSET_X , xFL-COLUMN_OFFSET_X] :
            ahsb mot cle w abda ahsbou b logique mtaa 3 mot cle fard ligne 
            K w L w S maahom 
    end if baaed detectit 1 words :
    
    
kif ngolek : xAK =  awel kelma f ekher item f children A 
moch maaneha xAK = "string" maaneha tjibli awel kelma noskod f X mtaaha abssice mtaaha w ekher kelma zeda 
















EXPÉRIENCES detected first time -> creates section experience
EXPÉRIENCES detected again -> reuses same experience section
children keep going in same section















behy tao bech taabi f children experiance 
behy houwa jetou children "x1"
puisque heya awel wahdou bech iwali children of experiance 
w baaed tjih x2 hna khedma 
yelzem icompari aal x1 ken x2 kifha bithabet nafs kolshay maa x1 kobr color size en gras kol shay iwali
fard level maa x2 ken kif exemple hedha x1 w x2 mokhtalfa twali x2 children l x1 
tao jet x3 yelzmou ikarenha maa 


dima valeur jdid detecté tetkarn maa kbalha w maa kbal kbalha w akeka ibara Un -1 w baaed tchouf rouha f ana level kif eli kifha w tahseb rouhha kifha
maaneha tahseb rouha +item f liste eli kif kif maaha

hata yekmlou kol children kol l section adhika 

{
"section": "formation",

"children": [
    [{"valeur :""x1",
     "children" : [{"x2"}]
    }]
]














