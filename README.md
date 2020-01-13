# Augmented Reality SIFT Translator (Python)

## Tím
* **Peter Ličko** - *
* **Richard Záhumenský** - *
* **Dávid Gajdoš** - implementácia SIFTu s využitím OpenCV + Translate API

## Zadanie
* Implementujte real-time preklad textu cez Augmented Reality na štýl Google Translate 

## Štruktúra projektu
* Augmented_Reality_Translator.py + skripty 
* TranslatorOpenCV_v3.py -> OpenCV implementácia pre detekciu písmen pomocou SIFTu 

## Výsledky

* **Augmented_Reality_Translator.py**

Hlavny skript, v ktorom sa nastavuju parametre algoritmu sift.

Tiez je mozne pracovat bud s RGB obrazkom (cize sa pocita pyramida DoG pre vsetky spektra) alebo pre sedotonovy obrazok (jedna vrstva).

Z originalu obrazka sa robi tvrda kopia, ktora sa neskor zmensuje pre dalsie urovne pyramid.

Funkcia Gaussian_filter nam vrati gaussovsky filter pre vyuzitie v dalsom kroku.

Dalsim krokom je zavolanie funkcie Create_Octave_Pyramid, ktora nam vrati pyramidu oktav a pyramidu rozdielov gaussianov. (je dolezite si uvedomit, ze na ziskanie rozdielu gaussianov potrebujeme aspon 3 obrazky v jednej oktave - cize parameter blur_levels nemoze byt mensi ako 4, zo styroch stupnov rozmazania obrazka ziskame akurat 3 obrazky na oktave, cize akurat jednu diferenciu gaussianov).

Dalej volame funkciu Detect_Extremes, ktora zisti extremy nachadzajuce sa na diferenciach, co su vlastne keypoints.


**Octaves.py**

Skript okrem hlavnej funkcie Create_Octave_Pyramid spominanej vyssie, este obsahu funkciu na zmensene vstupneho obrazka na polovicu Downsize_img_to_half.
Gaussian_filter bola uz tiez spomenuta, a vracia gaussov filter rozmazania a funkcia Gaussian_Blur pouziva tento filter na rozmazanie.


**Keypoints.py**

Funkcia Detect_Extremes vola jednu z funkcii Extrema_DetectionX kde X je cislo 1 az 3. Skusali sme rozne formy tejto funkcie kvoli optimalizacii. Pre mensie obrazky je vhodna funkcia Extrema_Detection3 a pre vacsie Extrema_Detection1 (rekurzia).

![Default image](/result_images/default.png) 
<!-- .element height="30%" width="30%" -->


* **TranslatorOpenCV_v3.py**

Dependencies: 
* opencv-contrib-python==3.4.2.16 
* opencv-python==3.4.2.16

Skript TranslatorOpenCV_v3.py obsahuje komentáre k funkciám. 

Finálne parametre pre SIFT: SIFT_create(nfeatures = 0,
                            		nOctaveLayers = 5,
                            		contrastThreshold = 0.04,
                            		edgeThreshold = 10,
                            		sigma = 1.2 )
                                
Využité matchers pre keypointy : Brute-force matcher a FlannBasedMatcher (viď dokumentácia k OpenCV).

## Problémy

* **Implementácia bez využitia OpenCV**

* **OpenCV Implementácia**

Problémom pri tejto implementácii je párovanie Keypointov. Pri párovaní real-time videa s predlohou písmen nevie implementácia jednoznačne určiť všetky písmená. Problém je hlavne pri písmenách "O", "C", "G", ale aj pri iných písmenách.

## Záver

