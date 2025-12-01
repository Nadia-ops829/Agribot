
import re

DATASET_MANUEL = [
        # === SEMIS & CALENDRIER CULTURAL (VERSION COMPLÈTE BURKINA 2025) ===
    "Coton : semis du 15 mai au 15 juillet. Centre/Est/Ouest/Cascades : dès mi-mai. Boucle du Mouhoun et Sud-Ouest : fin mai. Sahel : attendre bonnes pluies début juillet.",
    "Mil et sorgho : semis dès les premières pluies efficaces → généralement 10 juin au 10 juillet. Ne jamais semer avant le 5 juin (risque de sécheresse terminale).",
    "Maïs (saison des pluies) : semis juin à mi-juillet. En contre-saison irriguée (bas-fonds, barrages) : mars-avril.",
    "Niébé (haricot cowpea) : semis en association août-septembre, ou en pur octobre-novembre pour cycle court.",
    "Arachide : semis fin mai à fin juin. Variétés précoces (55-10, TS32-1) dès fin mai, variétés longues (120 jours) avant le 20 juin.",
    "Sésame : semis juin-juillet. Très résistant à la sécheresse → parfait pour le Sahel et l’Est.",
    "Riz pluvial : semis juin-juillet. Riz irrigué : toute l’année selon disponibilité en eau (2 campagnes possibles).",
    "Riz de bas-fonds : repiquage juillet-août après les premières pluies.",
    "Sorgho de contre-saison (bas-fonds) : semis février-mars avec l’humidité résiduelle.",
    "Fonio : semis fin juin à mi-juillet (Nord et Est).",
    "Voandzou (bambara groundnut) : semis juillet-août.",
    "Patate douce : bouturage toute l’année en irrigué, ou juin-juillet en pluvial.",
    "Manioc : bouturage toute l’année, mais idéalement mars-juin.",
    "Igname : plantation mars-avril (début de saison des pluies).",
    "Tomate (maraîchage) : pépinière octobre-novembre → repiquage décembre-janvier (saison froide), ou mars-avril (contre-saison).",
    "Oignon : pépinière septembre-octobre → repiquage novembre-décembre.",
    "Chou, salade, carotte : semis septembre à février (saison fraîche).",
    "Gombo : semis juin-juillet ou décembre-janvier.",
    "Piment : pépinière toute l’année, mais idéalement août-septembre ou février-mars.",
    "Moringa : semis ou bouturage toute l’année (très résistant).",
    "Soja : semis juin-juillet (cycle 90–110 jours).",
    "Tournesol : semis juin-juillet (Est et Centre-Nord).",
    "Haricot vert : semis août-septembre ou février-mars.",
    "Pastèque : semis février-mars (contre-saison irriguée) ou juin-juillet.",
    "Melon : semis février-mars ou juin-juillet.",
    "Concombre : toute l’année en irrigué, sinon juin-juillet et décembre-janvier.",
    "Courge/squash : semis juin-juillet.",
    "Aubergine : pépinière août-septembre ou février-mars.",
    "Carotte : semis octobre à février (saison fraîche).",
    "Betterave : semis octobre-février."

        # === RÉCOLTE (VERSION COMPLÈTE BURKINA 2025) ===
    "Récolte du coton : de novembre à février. Commencer quand 70 % des capsules sont ouvertes. Ne jamais récolter sur sol mouillé.",
    "Mil et sorgho : septembre-octobre. Récolter quand les grains sont durs (ongle ne rentre plus) et que la panicule est sèche.",
    "Maïs : 3 à 4 mois après semis. Récolter quand les grains sont durs et les enveloppes brunes/jaunes. Laisser sécher sur pied si possible.",
    "Niébé (haricot) frais : 60–70 jours après semis. Niébé sec : 90–110 jours quand les gousses sont brunes et sèches.",
    "Arachide : 90–130 jours selon la variété. Arracher quand les feuilles jaunissent et que les gousses sont bien formées (test : grains roses/noirs à l’intérieur).",
    "Sésame : octobre-novembre. Récolter quand les capsules inférieures commencent à s’ouvrir (couper la tige et laisser sécher à l’envers).",
    "Riz pluvial : octobre-novembre (4–5 mois). Riz irrigué : toute l’année selon le cycle.",
    "Fonio : octobre-novembre. Récolter quand les grains durcissent et que la panicule penche.",
    "Voandzou (bambara nut) : novembre-décembre quand les gousses sont sèches sous terre.",
    "Patate douce : 4–6 mois après plantation. Récolter quand les feuilles jaunissent.",
    "Manioc : 9–18 mois selon variété. Récolter quand les feuilles jaunissent et tombent.",
    "Igname : 8–10 mois (novembre-décembre). Récolter quand les feuilles sont complètement sèches.",
    "Tomate (saison froide) : février-avril. Tomate contre-saison : juin-août.",
    "Oignon : avril-mai (récolte des bulbes secs). Tiges couchées = signe de maturité.",
    "Chou, salade : 45–90 jours après repiquage (décembre-mars).",
    "Gombo : récolte continue dès 60 jours, tous les 2–3 jours pendant 2 mois.",
    "Piment : récolte verte ou rouge à partir de 3 mois, continue pendant 4–6 mois.",
    "Soja : octobre-novembre quand 95 % des gousses sont brunes.",
    "Tournesol : octobre-novembre quand le dos du capitule est brun et les graines dures.",
    "Pastèque/melon : quand le pédoncule se dessèche et que la peau devient mate.",
    "Concombre : 45–60 jours, récolte continue tous les 2 jours.",
    "Courge/squash : quand la peau durcit et que la queue se dessèche.",
    "Aubergine : récolte continue dès 70–80 jours, tous les 4–5 jours.",
    "Haricot vert : 50–60 jours après semis, récolte continue.",
    "Carotte/betterave : 3–4 mois après semis (janvier-mars).",
    "Moringa : feuilles toute l’année, gousses 8–12 mois après plantation.",
    "Sorgho de contre-saison (bas-fonds) : mai-juin.",
    "Riz de bas-fonds 2e cycle : février-mars (si eau disponible).",
    "Astuce générale : ne jamais récolter le matin avec la rosée → ça favorise les moisissures au stockage."
    # === STOCKAGE & CONSERVATION POST-RÉCOLTE (BURKINA 2025) ===
    "Sacs PICS (Purdue Improved Crop Storage) : hermétiques, zéro oxygène → 100 % protection contre charançons pendant 12–18 mois. Prix : 2 500–3 000 FCFA/sac 100 kg.",
    "Sacs polypropylène classiques + 1 kg de feuilles de neem séchées + 200 g de piment en poudre par sac 100 kg → conservation 8–12 mois sans perte.",
    "Cendre de bois tamisée autour et dans les sacs → repousse charançons et bruches (gratuit et 100 % efficace).",
    "Grenier traditionnel surélevé + toit en paille + ventilation haute et basse → parfait pour mil, sorgho, maïs pendant 1 an.",
    "Silo métallique 1 tonne (subventionné à 50 %) : 250 000 FCFA → conservation 3 ans sans aucun insecte.",
    "Stockage du niébé : sacs PICS obligatoires sinon les bruches mangent tout en 3 mois.",
    "Huile de neem (2 cuillères à soupe par sac 50 kg) + bien mélanger les grains → protection 6–9 mois.",
    "Poudre de piment fort (500 g par sac 100 kg) → les insectes détestent ça.",
    "Feuilles de Hyptis spicigera (ou « thé du Faso ») : 1 kg par sac 100 kg → très efficace contre les bruches.",
    "Stockage du riz : toujours décortiqué et en sacs PICS, jamais en sacs ouverts.",
    "Maïs en épis : suspendre sous l’appentis avec fumée légère → zéro charançons pendant 1 an.",
    "Arachide en coque : stocker dans des jarres en terre + couche de cendre → conservation parfaite.",
    "Séchage obligatoire avant stockage : maïs < 13 % humidité, sorgho/mil < 12 %, arachide < 9 %.",
    "Test simple : si le grain casse net entre les dents → prêt à stocker. S’il plie → encore humide.",
    "Phosphine (phostoxin) pour gros stocks coopératifs : 2 tablettes par tonne, fumigation 7 jours → tue tout.",
    "Actellic 50 EC : 50 ml pour 100 kg de grains → traitement chimique (prix 10 000 FCFA/L).",
    "Moringa en poudre dans les sacs de niébé : 200 g par sac → répulsif naturel + bonus nutritionnel.",
    "Jamais stocker sur le sol nu → toujours sur palettes en bois ou nattes.",
    "Contrôle mensuel : ouvrir un sac, vérifier odeur et insectes. Si odeur bizarre → traiter immédiatement.",
    "Stockage coton graine : sacs propres, hangar aéré, jamais par terre → éviter les taches jaunes.",
    "Durée conservation avec PICS : maïs 18 mois, sorgho 24 mois, niébé 12 mois, riz 36 mois.",
    "Astuce de grand-mère : mettre quelques gousses d’ail ou oignons dans le sac → repousse les insectes.",
    "Les sacs PICS se réutilisent 3–4 campagnes si bien entretenus.",
    "Subvention sacs PICS 2025 : 50 % pour les femmes et les jeunes agriculteurs (via Ministère ou ONG).",
    "Le vrai secret du stockage ? Séchage + propreté + PICS = zéro perte, zéro pleurs, zéro dette."

    # === PRIX 2024-2025 ===
    "Prix bord-champ coton graine 2024–2025 : 325 FCFA/kg (1er choix), 300 FCFA/kg (2e choix).",
    "Maïs novembre 2025 : environ 150–180 FCFA/kg.",
    "Sorgho blanc : 140–170 FCFA/kg.",
    "Engrais NPK 15-15-15 subventionné : 16 000 FCFA le sac de 50 kg.",
    "Urée subventionnée : 15 000 FCFA le sac 50 kg.",

    # === MALADIES & RAVAGEURS (VERSION COMPLÈTE 2025) ===
    "Chenille légionnaire du maïs : apparaît juillet-août. Traitement : extrait de neem (5 L/ha) ou Cyperméthrine/Emacot 50 g/L à 1 L/ha dès les premiers trous dans les feuilles.",
    "Striga (herbe sorcière) sur mil et sorgho : utiliser variétés résistantes SRN39, Nieleni, CSM-335 ou piège à striga avec niébé ou sésame 2 ans avant.",
    "Fusariose et bactériose du coton : rotation 3-4 ans, semences certifiées FK37, STAM 89A, Irma P10 + désinfection semences au fongicide Apron Star.",
    "Mildiou du niébé : taches brunes sur feuilles. Pulvériser Ridomil Gold 66 WP (2 kg/ha) ou Mancozèbe dès les premiers symptômes.",
    "Anthracnose du niébé : taches noires sur gousses. Fongicide Mancozèbe ou cuivre (Nordox) 2-3 fois.",
    "Mosaïque du niébé : feuilles tachetées jaunes. Arracher et brûler les plants atteints + utiliser semences saines.",
    "Brûlure bactérienne du riz : taches vert-gris sur feuilles. Utiliser semences saines + cuivre (Kocide, Cupravit) 2 kg/ha.",
    "Pyriculariose du riz (brûlure des épis) : Fongicide Beam ou Nativo dès la montaison.",
    "Cercosporiose de l’arachide : taches brunes rondes sur feuilles. Fongicide Mancozèbe ou Tilt 250 EC.",
    "Rouilles du maïs et sorgho : poussière orange sur feuilles. Fongicide Tilt ou Score 250 EC.",
    "Charançons du stock (céréales) : sacs PICS hermétiques ou feuilles de neem + piment en poudre dans les sacs classiques.",
    "Bruches du niébé : sacs PICS ou huile de neem + cendre de bois dans les récipients.",
    "Criquets et sauterelles : signalement immédiat à la DPV (Direction Protection des Végétaux) → ils viennent avec le Decis ou Karate.",
    "Mouche de la capsule du coton : surveiller fin septembre → pulvérisation Cyperméthrine + Profénofos.",
    "Pucerons du coton : jaunissement des feuilles. Savon noir + neem ou Acetamiprid (Mospilan) 100 g/ha.",
    "Pourriture des gousses d’arachide : rotation + labour profond + éviter les semis trop serrés.",
    "Vers blancs (termites) : utiliser semences enrobées Gaucho ou Cosmor dans les trous de zaï.",
    "Oiseaux granivores (tourterelles, moineaux) : épouvantails + filets ou planter du sorgho rouge autour du champ.",
    "Rats dans les stocks : appâts anticoagulants (Storm, Racumin) ou chats dans le grenier.",
    "Maladie de la panachure du maïs (streak virus) : pas de traitement → arracher et brûler les plants + variétés résistantes.",
    "Pourriture grise du maïs (Stockage) : bien sécher à moins de 13 % d’humidité + sacs PICS.",
    "Mouche blanche sur tomate/oignon : savon noir + neem ou Acetamiprid + Cyperméthrine.",
    "Mineuse de la tomate : Bacillus thuringiensis (Delfin) ou Abamectine dès les premières galeries.",
    "Acariens rouges (araignées rouges) : soufre mouillable ou Abamectine en cas de forte attaque.",
    "Nématodes à galles (tomate, gombo) : rotation longue + fumure organique + tagètes en bordure."

    # === IDENTIFICATION DES SOLS (NOUVEAU & COMPLET) ===
    "Sols ferrugineux tropicaux (90 % du Burkina) : couleur rouge à rouge-brun, pauvres en matière organique, très répandus dans les plateaux.",
    "Sols ferrugineux lessivés : rouge vif, texture sableuse-argileuse → Bobo-Dioulasso, Banfora, Ouagadougou, Koudougou.",
    "Sols lithosols (caillouteux) : peu profonds, beaucoup de pierres → Sahel, Dori, Gorom-Gorom, Djibo.",
    "Sols bruns subarides : gris-brun à brun clair, très sableux → Nord et Sahel (Markoye, Sebba).",
    "Sols hydromorphes : gris à noir, riches en argile, gorgés d’eau → bas-fonds, vallées du Nakambé et du Mouhoun.",
    "Sols vertisols (terres noires) : noirs, se fissurent en saison sèche → rares, autour de Léo, Gaoua.",
    "Si ton sol est rouge et dur comme du béton en saison sèche → sol ferrugineux lessivé (Centre, Ouest, Est).",
    "Si tu as beaucoup de cailloux et la charrue bloque → lithosol (Nord et Sahel).",
    "Si ton champ reste humide longtemps et devient noir → sol hydromorphe (parfait pour le riz).",
    "Sol sableux qui ne retient pas l’eau → typique du Sahel → zaï profond obligatoire.",
    "À Ouagadougou, Bobo, Kaya, Fada → 95 % de sols ferrugineux rouges.",
    "À Dori, Gorom-Gorom → lithosols caillouteux + sols bruns subarides.",
    "Dans les bas-fonds de Bama, Vallée du Kou → sols hydromorphes noirs.",
    "Sud-Ouest (Gaoua, Kampti) → mélange ferrugineux + quelques vertisols noirs.",
    "Test simple : terre humide qui colle beaucoup = beaucoup d’argile. Qui s’effrite = sableux.",
    "Pour connaître ton sol : regarde la couleur + texture + ta région.",

        # === RESTAURATION & AMÉLIORATION DES SOLS (BURKINA 2025) ===
    "Technique du zaï (trous de 20–30 cm de diamètre, 20 cm de profondeur) + 300 g de fumier/compost par trou = +300 à 800 % de rendement sur sol dégradé.",
    "Cordons pierreux tous les 20–25 m en courbes de niveau → réduit le ruissellement de 70 % et récupère l’eau.",
    "Demi-lunes (1 m de diamètre, 20 cm de profondeur) : idéales sur pentes douces, retenir l’eau + planter sorgho ou niébé dedans.",
    "Bandes enherbées avec Andropogon gayanus ou Brachiaria ruziziensis tous les 10–15 m → stoppe l’érosion et nourrit le sol.",
    "Fumure organique recommandée : 5 à 10 tonnes de fumier de parc ou compost par hectare et par an.",
    "Micro-dose d’engrais dans le zaï : 2 g NPK (une pincée) + 1 g urée par trou → coût : seulement 8 000–12 000 FCFA/ha mais +100 % de rendement.",
    "Culture de couverture avec niébé, mucuna ou stylosanthes après la récolte → enrichit le sol en azote (équivalent 50–80 kg urée/ha).",
    "Plantation d’arbres fertilitaires : 100 Faidherbia albida ou Acacia (Gaaso) par hectare → feuilles riches en azote + ombre.",
    "Moringa en haie vive autour du champ : feuilles = engrais vert + revenu complémentaire.",
    "Labour de conservation (sans labour profond tous les ans) + paillage avec tiges de mil/sorgho → garde l’humidité et augmente la matière organique.",
    "Sous-solage tous les 3–4 ans pour casser la semelle de labour → racines vont plus profond.",
    "Apport de cendre de bois ou de dolomie sur sols très acides (Est et Cascades) : 500 kg/ha tous les 3 ans.",
    "Biochar (charbon de paille de riz) : 5–10 t/ha une seule fois → augmente la rétention d’eau de 20 % pendant 5–10 ans.",
    "Litière animale + urée + eau dans le parc à bétail → fumier de parc ultra-riche (jusqu’à 2 % azote).",
    "Rotation coton – céréale – niébé tous les 3 ans → restaure l’azote et casse le cycle des maladies.",
    "Zaï profond (30–40 cm) dans le Sahel + fumier + mulch → même sur croûte ferrugineuse, tu peux avoir 1 000 kg de sorgho/ha.",
    "Récupération des termitières broyées : riches en phosphore et calcium → répandre 2–3 tonnes/ha.",
    "Phosphates naturels de Kodjari ou de Tahoua (subventionnés) : 100–150 kg/ha pour les sols très pauvres en P.",
    "Test simple de restauration : si après 3 ans tu vois des vers de terre partout → ton sol est revenu à la vie !",
    "Coût moyen d’un bon zaï + fumure sur 1 ha : environ 80 000–120 000 FCFA la première année, mais remboursé dès la 2e récolte.",
    "Résultat réel observé : les champs en zaï + cordons pierreux à Yako, Réo, Koudougou font aujourd’hui 1 500–2 500 kg de sorgho/ha là où c’était 300 kg avant.",
    "Le meilleur investissement pour un paysan burkinabè : restaurer son sol. Un sol vivant = récolte assurée même en année sèche."


        # === VARIÉTÉS RECOMMANDÉES OFFICIELLES 2025 (INERA / Ministère de l’Agriculture) ===
    "COTON 2025 : STAM 89A (très haut rendement), FK37 (résistante fusariose), Irma P10, Irma A 752, BRS 289 (nouvelles générations ultra-résistantes).",
    "MAÏS : Barka (5–7 t/ha), Espoir (5–6 t/ha), SR21 (résistant striga), Bondofa, Ikenne 111, Obatanpa (cycles 90–110 jours).",
    "SORGHO : ICSV 1049 (très résistant striga), Sariasso 14, Grinkan Yerewolo, CSM-335, Nieleni, Tiandougou (rendement 3–4 t/ha en zaï).",
    "MIL : Nieleni Super, Toroniou C1, ICMV IS 89305 (résistants striga et mildiou).",
    "NIÉBÉ : Gorom-Gorom, KVx 396-4-4, Tilgré, Komcallé (cycles courts 60–70 jours), Aladoua (cycle long 90 jours).",
    "ARACHIDE : TS32-1 (55-10), I-67-3 (résistante cercosporiose), Fleur 11, ICIAR 19BT (120 jours).",
    "SÉSAME : Saria S48 (blanche, très demandée), Saria S41 (cycle court 90 jours).",
    "RIZ IRRIGUÉ : FKR 19, FKR 56N, Nerica L20, Nerica L36 (rendement 6–8 t/ha).",
    "RIZ PLUVIAL : Waima, IRAT 204, Orylux 6 (bas-fonds).",
    "FONIO : Natié, Djigui, Kaba (Est et Centre-Est).",
    "VOANDZOU : Korogho, Nafi, Jakombo (Nord et Sahel).",
    "SOJA : IITA 1075, Jupiter, Doko (rendement 2–3 t/ha).",
    "TOURNESOL : Saria T1, Saria T2 (Est et Centre-Nord).",
    "PATATE DOUCE : INERA Orange, Wagboligué, Carla (chair orange riche en vitamine A).",
    "MANIOC : INERA 88, Rayong, Kpaki Kpika (cycles 12–18 mois).",
    "IGNAME : Kponan, Lokpa, Bètè Bètè (variétés blanches très demandées).",
    "TOMATE MARAÎCHÈRE : Roma VF (résistante nématodes), Petomech, Mongal F1 (hybride haut rendement).",
    "OIGNON : Violet de Galmi, Blanc de Soumtenga, Texas Grano (saison froide).",
    "CHOU : KK Cross, Tropica, Copenhagen (saison fraîche).",
    "GOMBO : Clemson Spineless, Indiana, KVx 30-2 (variété locale très productive).",
    "PIMENT : INERA Piment Fort, Yolo Wonder, Légendaire (doux), Safi (fort).",
    "AUBERGINE : INERA 101, Black Beauty, Longue Violette.",
    "CAROTTE : Nantes, Touchon, Brasilia (saison froide).",
    "MORINGA : PKM-1 (indienne haut rendement), Variété locale Saria (feuilles très riches).",
    "HARICOT VERT : Contender, Paulista (cycle court).",
    "PASTÈQUE : Crimson Sweet, Sugar Baby, Kaolack (contre-saison).",
    "MELON : INERA Melon, Védrantais (saison des pluies).",
    "COURGE : INERA Courge, Waltham Butternut (stockage longue durée).",
    "Variétés résistantes striga 2025 : SRN39, Nieleni, ICSV 1049, Sariasso 14 → obligatoires au Nord et à l’Est.",
    "Variétés coton Bt toujours interdites au Burkina → on reste sur STAM 89A et FK37 (100 % conventionnelles et performantes).",
    "Semences certifiées : toujours acheter chez SOFITEX, SN Citéc, coopératives ou boutiques agréées → jamais au marché noir.",
    "Prix moyen semences 2025 : Coton 1 200 FCFA/kg, Maïs 1 500 FCFA/10 kg, Sorgho 800 FCFA/kg (subventionnées à 50 % dans certaines zones)."

        # === MÉTÉO & ALERTES NOVEMBRE 2025 (suite) ===
    "Novembre 2025 au Burkina : saison sèche en cours, températures 32–38°C jour / 20–25°C nuit, humidité 20–40 %, vent harmattan 5–15 km/h. Pluies rares sauf sud-ouest.",
    "À Ouagadougou (Centre) : 35–37°C, ciel dégagé, risque faible de poussière harmattan. Parfait pour le séchage du coton et maïs.",
    "À Bobo-Dioulasso (Sud-Ouest) : 33–36°C, pluies résiduelles possibles jusqu'au 15 novembre (risque inondation bas-fonds). Draine les champs rizicoles.",
    "À Dori et Gorom-Gorom (Sahel/Nord) : 36–39°C, sécheresse accentuée, humidité < 25 %. Arrose ou fais zaï profond pour mil et sorgho.",
    "À Kaya (Centre-Nord) : 34–37°C, vent modéré, faible risque de brouillard. Surveille les chenilles sur maïs en fin de mois.",
    "À Fada N'gourma (Est) : 35–38°C, ciel clair, harmattan croissant. Idéal pour récolte du sésame et arachide.",
    "Alerte nationale novembre 2025 : poche de sécheresse au Sahel (Dori, Djibo) → priorise l'irrigation goutte-à-goutte pour niébé.",
    "Alerte sud-ouest : pluies isolées 10–15 mm possibles (Gaoua, Banfora) → prépare drainage pour éviter asphyxie racinaire riz.",
    "Prévision Centre-Nord : températures en hausse (36°C max), vent 10 km/h → risque incendie champs → surveille les feux de brousse.",
    "Conseil météo : en novembre, harmattan peut réduire l'humidité → ajoute 20 % de mulch sur sols pour retenir l'eau."

       # === CRÉDIT & ASSURANCE AGRICOLE (BURKINA 2025) ===
    "Crédit campagne coton : SOFITEX (via coopératives) à 8–9 % TAE, garantie par le stock de coton. Montant max 5–10 millions FCFA par paysan.",
    "Banques pour crédit agricole : BCB, Coris Bank, Ecobank, Société Générale Burkina, UBA → taux 8–12 % selon garantie.",
    "Crédit pour céréales (mil, sorgho, maïs) : via les Caisses Populaires ou les coopératives villageoises, taux 7–10 %.",
    "Microcrédit pour maraîchers (tomate, oignon) : PAMF (Programme d'Appui aux Microfinances) ou PAMEX à 12 %.",
    "Crédit pour engrais/semences : via les boutiques agréées (SN Citéc, SOFITEX) → remboursement à la récolte, taux 6–8 %.",
    "Assurance agricole multirisque : SUNU Assurances, SONAR, UAB, NSIA → couvre sécheresse, inondation, maladies (prime 2–4 % de la valeur assurée).",
    "Assurance coton : SOFITEX couvre la sécheresse + chenille légionnaire (prime incluse dans le crédit).",
    "Assurance céréales : via le Projet PACCEM (subvention 80 % pour les petits paysans, couvre 50 % des pertes).",
    "Conditions pour crédit SOFITEX : être membre coopérative, avoir 1 ha minimum, remboursement en janvier-février.",
    "Contact BCB pour crédit : 50 30 30 30 ou www.bcb.bf (agences à Ouaga, Bobo, Kaya, Koudougou).",
    "Contact Coris Bank : 50 49 49 49 ou www.coris.bank (spécialisée microcrédit agricole).",
    "Prime assurance SUNU 2025 : 3 % de la valeur estimée de la récolte (ex. 100 000 FCFA pour 1 ha de coton).",
    "SONAR Assurance : couvre aussi les animaux (bovins, ovins) en plus des cultures.",
    "UAB Assurance : plan 'Paysan Protégé' → indemnisation en 15 jours après sinistre.",
    "Microcrédit PAMF : jusqu’à 2 millions FCFA pour maraîchers, remboursement 12 mois, taux 10 %.",
    "Crédit solaire pour irrigation : via Ecobank ou UBA (taux 9 %, garantie pompe solaire).",
    "Assurance contre la chenille légionnaire : incluse dans les polices SUNU et SONAR depuis 2024.",
    "Remboursement anticipé SOFITEX : possible si bon prix de vente, pénalité 2 %.",
    "Garantie pour crédit bancaire : stock de céréales ou garantie solidaire coopérative.",
    "Subvention assurance 2025 : 50 % pour les femmes agricultrices et les jeunes (moins de 35 ans).",
    "Contact assurance NSIA : 25 49 00 00 ou www.nsiainsurance.bf (agences dans toutes les régions).",
    "Crédit pour semences certifiées : via SN Citéc (taux 7 %, remboursement à la récolte).",
    "Assurance inondation rizicoles : couvre 70 % des pertes, via UAB ou SONAR.",
    "Microfinance pour engrais : PAMEX (taux 11 %, jusqu'à 500 000 FCFA).",
    "Conseil : toujours prendre l’assurance avant le semis, pas après la sécheresse !"

    #    # === CONSEILS GÉNÉRAUX & FUN (les phrases que tout le monde répète au village) ===
    "Faire le billonnage + buttage = +30 % de rendement sur maïs et arachide. Le dos courbé paie toujours !",
    "Semis en ligne avec dose recommandée = moins de semences, plus de récolte. Le cordeau et la ficelle, c’est la richesse du paysan.",
    "Wakat sera ! Si tu fais zaï + compost, ton champ va chanter wakat sera toute l’année !",
    "Le meilleur engrais ? C’est la sueur du paysan et la bénédiction de Dieu.",
    "Un bon agriculteur lit Sidwaya tous les jours et écoute la radio avant d’aller au champ.",
    "Qui se lève tôt trouve la rosée, qui se couche tard trouve la fraîcheur… et qui fait zaï trouve la récolte !",
    "Le zaï, ce n’est pas du travail, c’est un investissement qui rapporte tous les ans.",
    "Un sac de PICS bien fermé = zéro charançon, zéro perte, zéro pleurs.",
    "Ne jamais récolter le matin avec la rosée → sinon les grains pourrissent en 3 jours.",
    "Le neem, c’est l’insecticide du pauvre… et il marche mieux que certains produits chers !",
    "Qui plante un arbre aujourd’hui mange à l’ombre demain et laisse un héritage à ses enfants.",
    "Un champ propre sans mauvaises herbes = la moitié de la bataille gagnée.",
    "Le cordon pierreux, c’est la banque du sol : chaque pierre posée te rapporte de l’eau et de la terre.",
    "Si tu vois des vers de terre dans ton champ → ton sol est vivant, félicitations !",
    "Le téléphone du paysan ? C’est la houe. Le bureau ? C’est le champ.",
    "Qui mélange niébé + céréales dans son champ ne meurt jamais de faim.",
    "Le coton, c’est l’argent liquide. Le mil, c’est la nourriture. Les deux ensemble = la paix dans la cour.",
    "Un bon grenier + un bon silo = un bon sommeil en saison sèche.",
    "Le vrai riche au village, ce n’est pas celui qui a la plus grosse moto… c’est celui qui a le plus gros grenier.",
    "Ne jamais vendre tout ton mil en décembre. Garde au moins 6 mois de réserve.",
    "Qui écoute son vieux père au champ ne se trompe jamais de date de semis.",
    "Le moringa dans la cour, c’est la pharmacie gratuite pour toute la famille.",
    "Un sac d’engrais bien utilisé vaut dix sacs mal utilisés.",
    "Le champ ne ment jamais : ce que tu y mets, il te le rend au centuple… ou rien du tout.",
    "Quand le vent souffle fort en janvier, l’harmattan arrive → protège les jeunes plants avec des brise-vent.",
    "Le bon paysan ne travaille pas pour la saison… il travaille pour ses petits-enfants.",
    "Qui fait demi-lunes aujourd’hui aura de l’eau même en année de sécheresse.",
    "Un bon compost bien mûr sent la forêt, pas la cour.",
    "La femme qui cultive le jardin potager nourrit la famille toute l’année.",
    "Le meilleur moment pour planter ? Il y a deux ans. Le deuxième meilleur ? Aujourd’hui !",
    "Qui a deux champs dort tranquille : un en haut, un en bas-fond.",
    "Le zaï + micro-dose + niébé en rotation = même sur croûte ferrugineuse tu fais 2 tonnes de sorgho.",
    "Un agriculteur qui ne sourit pas à la saison des pluies… c’est qu’il n’a pas fait ses zaï !",
    "Wend na koama ! Que Dieu bénisse ta houe, ton champ et ta famille.",
    "Le Burkina, c’est le pays des hommes intègres… et des champs bien zaïés !",
    "Un bon voisin prête sa charrue, un mauvais voisin regarde ton champ brûler.",
    "La terre ne trahit jamais celui qui la respecte.",
    "Qui dort avec les poules se lève avec les coqs… et finit son zaï avant la chaleur !",
    "Le vrai diplôme du paysan ? Un grenier plein et des enfants en bonne santé.",
    "Y’a pas de mauvais sol, y’a que des paysans qui n’ont pas encore appris le zaï !",
    


    # === DISCOURS OFFICIELS & CHIFFRES DU PRÉSIDENT / MINISTRE ===
    "Le Capitaine Ibrahim Traoré, 5 décembre 2024 : « Nous avons produit plus de 6 millions de tonnes de céréales en 2024-2025. L’objectif 2025-2026 est 7 millions de tonnes. Nous allons y arriver avec ou sans pluie ! »",
    "Ministre d’État Ismaël Sombié, août 2025 : « Chaque Burkinabè doit produire sa nourriture. Un peuple qui ne se nourrit pas lui-même est un peuple esclave. »",
    "Le Président a dit : « Le VDP qui cultive est plus utile que celui qui porte seulement le fusil. » → plus de 23 000 VDP agricoles en 2025.",
    "Offensive agropastorale 2023-2025 prolongée jusqu’en 2027 : 2 000 tracteurs, 800 motopompes, 600 000 tonnes d’engrais subventionnés.",
    "Discours du 11 décembre 2024 : « Le Burkina n’importera plus un seul grain de riz ni de maïs à partir de 2027. »",

    # === MALADIES & RAVAGEURS – TRAITEMENTS 2025 (les plus demandés) ===
    "Chenille légionnaire d’automne 2025 : dès que tu vois les premiers trous dans les feuilles de maïs → pulvérise Emacot 50 ou Cypercal 50 (gratuit via la coopérative). Sinon : 5 L d’extrait de neem + 1 kg de savon par hectare.",
    "Striga (herbe sorcière) : la seule solution qui marche vraiment = planter SR21, ICSV 1049, Nieleni ou Grinkan. Avec zaï + fumier = striga disparaît en 3 ans.",
    "Jassides et pucerons sur coton : dès le 40e jour après semis → Acetamiprid (Mospilan) ou Imidaclopride. Sinon savon noir + neem toutes les semaines.",
    "Mildiou du niébé et anthracnose : Ridomil Gold ou Mancozèbe dès les premiers symptômes. 2 traitements espacés de 10 jours.",
    "Brûlure bactérienne du riz (taches vert-gris) : pulvériser Kocide ou Cupravit (cuivre) 2 fois à 10 jours d’intervalle.",
    "Mouche blanche sur tomate/oignon : mélange savon noir (1 kg) + neem (5 L) + piment fort (500 g) dans 200 L d’eau → pulvériser tous les 5 jours.",
    "Mineuse de la tomate : Abamectine ou Bacillus thuringiensis (Delfin) dès que tu vois les galeries blanches.",
    "Charançons et bruches en stock : sac PICS + 500 g de piment en poudre + 1 kg de feuilles de neem séchées → 100 % efficace 24 mois.",
    "Criquets signalés à Djibo et Titao en novembre 2025 : préviens immédiatement la DPV → ils viennent avec Decis ou Karate gratuitement.",
    "Pourriture grise du maïs en stock : sécher à moins de 13 % d’humidité + sac PICS. Si déjà attaqué → phosphine (Phostoxin) 2 tablettes/tonne.",

    # === PROTECTION & RESTAURATION DES SOLS – TECHNIQUES QUI CARTONNENT EN 2025 ===
    "Zaï classique (20×20×20 cm) + 300 g fumier + micro-dose (2 g NPK + 1 g urée) = 2 500 à 4 000 kg sorgho/ha même à Gorom-Gorom.",
    "Zaï profond (40 cm) + termitières broyées + fumier = 1 500 kg/ha sur croûte ferrugineuse (témoignage Djibo 2025).",
    "Cordons pierreux tous les 20 m + demi-lunes + plantation Faidherbia albida = +700 % rendement en 4 ans (projets P2i à Léo).",
    "Biochar (charbon de paille de riz) : 10 tonnes/ha une seule fois → le sol retient l’eau comme une éponge pendant 10 ans.",
    "Mucuna ou Stylosanthes après la récolte de coton → enrichit le sol en azote = équivalent 80 kg d’urée gratuit.",
    "Rotation coton – sorgho – niébé tous les 3 ans → casse le cycle fusariose + striga + restaure l’azote.",
    "Sous-solage tous les 4 ans à 40 cm de profondeur → les racines du sorgho descendent à 2 m et résistent à la sécheresse.",
    "Apport de dolomie ou cendre de bois sur sols acides (Est et Cascades) : 500 kg/ha tous les 3 ans → pH remonte et rendement +40 %.",
    "Plantation de Gliricidia sepium ou Tephrosia en haie vive → azote gratuit + bois de chauffe + fourrage.",
    "Couverture permanente du sol avec tiges de sorgho/mil + paillage → réduit l’évaporation de 60 % en saison sèche.",

    # === CHIFFRES & SUBVENTIONS 2025 (les plus recherchés) ===
    "Subvention engrais 2025 : 16 000 FCFA le sac NPK et urée (au lieu de 32 000 FCFA).",
    "Subvention tracteur 2025 : 50 % pris en charge par l’État → un tracteur 90 CV à 12 millions au lieu de 25 millions.",
    "Subvention pompe solaire : 70 % pour les jeunes agriculteurs (moins de 35 ans).",
    "Subvention sacs PICS : 1 500 FCFA au lieu de 3 000 FCFA pour femmes et jeunes.",
    "Prime assurance agricole subventionnée à 80 % pour les petits producteurs via le projet PACCEM.",
    "Crédit à 0 % pour les VDP agricoles sur les sites de retour (Djibo, Kongoussi, Titao).",

    # === PROJETS QUI MARCHENT EN 2025 ===
    "Projet P2RS : 10 000 ha de bas-fonds aménagés en 2025 → 8 tonnes/ha de riz.",
    "Projet PARIIS : 50 000 ha restaurés avec zaï + cordons pierreux dans le Centre-Nord.",
    "Projet 2i (Initiative Irrigation) : 5 000 motopompes distribuées gratuitement aux femmes maraîchères.",
    "Projet Faso Kunu : 1 500 tracteurs neufs + formation pour les jeunes.",
    "Projet PACCEM : assurance gratuite pour 200 000 petits producteurs en 2025.",

    # === CONSEILS DE VIEUX QUI ONT TOUJOURS RAISON ===
    "Un vieux de Dori a dit : « Celui qui fait zaï en décembre dort tranquille en juillet. »",
    "Un vieux de Banfora : « Le moringa dans la cour, c’est la pharmacie + la banque + le restaurant. »",
    "Un vieux de Léo : « Qui plante Faidherbia aujourd’hui, ses petits-enfants mangeront à l’ombre. »",
    "Proverbe mossi : « La terre ne ment jamais. Ce que tu lui donnes, elle te le rend au centuple. »",
    "Proverbe peulh : « Le bon berger connaît chaque bête. Le bon paysan connaît chaque pierre de son champ. »",

    # === ALERTES RÉELLES DÉCEMBRE 2025 ===
    "Alerte striga très forte à Kongoussi, Tougouri, Boulsa → ne plante surtout pas Kapelga ou local, seulement SR21 ou ICSV.",
    "Alerte chenille légionnaire détectée à Pensa et Yako → traitement gratuit par la DPV jusqu’au 15 janvier.",
    "Alerte criquets au Sahel : si tu vois un nuage vert, appelle le 80 00 11 11 immédiatement.",
    "Alerte pluies tardives dans les Cascades → risque pourriture arachide → récolte urgente dès maintenant.",

  
    "Mélange 10 kg de sel + 5 kg de savon noir + 200 L d’eau → pulvérisation contre tous les insectes suceurs.",
    "Planter 10 lignes de niébé tous les 5 ha de sorgho → azote gratuit + revenu en plus.",
    "Un vieux pneu + fumier + tomate = 50 à 80 kg de tomates par pneu.",
    "Feuilles de Hyptis spicigera (thé du Faso) dans le sac de niébé = zéro bruche pendant 3 ans.",
    "Planter du sorgho rouge autour du maïs → les oiseaux attaquent le rouge et laissent le maïs.",

    "Wend na kodô ! Que ta récolte soit aussi lourde que le cœur d’une mère !",
    "Le champ ne trahit jamais celui qui le travaille avec amour.",
    "Qui fait zaï aujourd’hui, mange demain. Qui ne fait rien aujourd’hui, pleure demain."
]


def get_reponse_manuelle(question):
    q = question.lower().strip()
    
    # Nettoyage plus agressif
    q = re.sub(r'[^\w\s]', ' ', q)  # Supprime ponctuation
    q = ' '.join(q.split())  # Supprime espaces multiples
    
    # Dictionnaire de corrections
    corrections = {
        "cotton": "coton", "cotonn": "coton", "pri": "prix", "tarif": "prix",
        "sol": "sol", "terre": "sol", "protection": "proteger", "protegr": "proteger"
    }
    
    for wrong, right in corrections.items():
        q = q.replace(wrong, right)
    
    # Mots-clés prioritaires pour chaque thématique
    themes = {
        "prix_coton": ["prix coton", "coton fcfa", "coton prix", "cout coton"],
        "protection_sol": ["proteger sol", "sol degrade", "restauration sol", "zaï", "cordon pierreux"],
        "president": ["president", "traore", "discours president", "capitaine"],
        "varietes": ["variete", "stam", "fk37", "barka", "semence"]
    }
    
    # Vérification directe par thème
    for theme, keywords in themes.items():
        if any(keyword in q for keyword in keywords):
            # Recherche spécifique dans le dataset
            for texte in DATASET_MANUEL:
                texte_lower = texte.lower()
                if any(keyword in texte_lower for keyword in keywords):
                    return texte
    
    # Fallback : recherche par similarité (votre code actuel)
    mots_question = set(q.split())
    for texte in DATASET_MANUEL:
        mots_texte = set(texte.lower().split())
        commun = mots_question.intersection(mots_texte)
        
        if len(commun) >= 2:  # Seuil réduit
            return texte
    
    return None