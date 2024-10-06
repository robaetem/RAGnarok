from itertools import combinations
import numpy as np
import pandas as pd

test_cases = [
    {
        "question": "Hoeveel eet een kat per dag?",
        "relevant_texts": [
            "Een kat eet dan ook vaak kleine hapjes: zo'n vijftien à twintig keer per dag. De meeste katten krijgen maar twee keer per dag te eten. Dit betekent dat ze achttien uur per dag honger hebben! Sommige pechvogels krijgen zelfs maar eenmaal daags te eten. Een kat moet kunnen eten wanneer hij wil. Dat kan bijvoorbeeld door ervoor te zorgen dat er altijd brokjes klaarstaan.",
            "Voor een kat van 5 kilo heeft een kat gemiddeld 80 kilocalorieën (kcal) per dag nodig: Voor een kat van 5 kilo komt dat neer op 400 kcal. Een gemiddelde muis levert maar 30 kcal. Een kat van 5 kilo moet dan ook 13 muizen per dag eten om op gewicht te blijven! Dat zijn er 91 per week, en 4.745 per jaar."
        ],
        "irrelevant_texts": [
            "- Een kat die probleemgedrag vertoont heeft hulp nodig.",
            "Voor een kat is het een absolute must om zich vrijelijk terug te kunnen trekken op een plaats waar hij letterlijk geen andere katten, mensen of huisdieren kan zien.",
            "De komende dagen haalt u meerdere keren per dag voorzichtig een doekje over een wang van de nieuwe kat en laat dit ruiken aan de kat die u al heeft."
        ]
    },
    {
        "question": "Wat zijn de tekenen dat mijn kat gelukkig is?",
        "relevant_texts": [
            "Een gelukkige kat toont vaak speels gedrag, zoals het achtervolgen van speelgoed of het spelen met andere katten.",
            "Tevens kan je zien dat je kat gelukkig is als hij spint, zich uitstrekt, en zijn staart recht omhoog houdt.",
            "Katten die zich op hun rug draaien en hun buik tonen, voelen zich meestal veilig en gelukkig."
        ],
        "irrelevant_texts": [
            "Huisdieren hebben vaak behoefte aan sociale interactie.",
            "Het is belangrijk om regelmatig met je huisdier naar de dierenarts te gaan.",
            "Katten zijn van nature solitair, maar kunnen ook hechte banden vormen met hun baasjes."
        ]
    },
    {
        "question": "Welke vaccinaties zijn essentieel voor katten en wanneer moeten ze worden gegeven?",
        "relevant_texts": [
            "Essentiële vaccinaties voor katten zijn onder andere die tegen kattenziekte (panleukopenie), niesziekte (FHV-1 en FCV), en rabies.",
            "De eerste vaccinaties worden meestal gegeven als kittens tussen de 6 en 8 weken oud zijn, met herhalingen tot ongeveer 16 weken.",
            "Volwassen katten moeten jaarlijks of om de drie jaar gevaccineerd worden, afhankelijk van het type vaccin."
        ],
        "irrelevant_texts": [
            "Katten hebben ook behoefte aan voldoende beweging.",
            "Het kiezen van het juiste kattenvoer is cruciaal voor hun gezondheid.",
            "Een goede verzorging van de vacht voorkomt klitten en huidproblemen."
        ]
    },
    {
        "question": "Hoe herken ik of mijn kat ziek is?",
        "relevant_texts": [
            "Tekenen dat je kat ziek kan zijn zijn onder andere verlies van eetlust, lethargie, braken of diarree.",
            "Als je merkt dat je kat ongewoon veel slaapt of zich verstopt, kan dit ook een teken van ziekte zijn.",
            "Veranderingen in gedrag zoals agressie of angst kunnen ook wijzen op gezondheidsproblemen."
        ],
        "irrelevant_texts": [
            "Katten kunnen goed omgaan met stressvolle situaties als ze goed getraind zijn.",
            "Een goede socialisatie helpt bij het voorkomen van gedragsproblemen.",
            "Het gebruik van speeltjes stimuleert de mentale gezondheid van je kat."
        ]
    },
    {
        "question": "Wat zijn de meest voorkomende gezondheidsproblemen bij katten?",
        "relevant_texts": [
            "Veelvoorkomende gezondheidsproblemen bij katten zijn tandheelkundige aandoeningen, obesitas, en nierziekten.",
            "Katten kunnen ook last hebben van huidallergieën en parasieten zoals vlooien en teken.",
            "Daarnaast komen aandoeningen zoals diabetes en hyperthyreoïdie vaker voor bij oudere katten."
        ],
        "irrelevant_texts": [
            "Katten hebben verschillende soorten speelgoed nodig om actief te blijven.",
            "Het trainen van je kat kan helpen bij het verbeteren van hun gedrag.",
            "Katten hebben behoefte aan zowel mentale als fysieke stimulatie."
        ]
    },
    {
        "question": "Waarom krabt mijn kat aan meubels en hoe kan ik dit voorkomen?",
        "relevant_texts": [
            "Katten krabben om hun nagels scherp te houden, hun territorium af te bakenen, en om stress te verlichten.",
            "Om dit gedrag te voorkomen kun je krabpalen aanbieden en meubels beschermen met speciale sprays of hoezen.",
            "Het is belangrijk om je kat te belonen als hij de krabpaal gebruikt in plaats van de meubels."
        ],
        "irrelevant_texts": [
            "Het geven van traktaties kan helpen bij het trainen van je huisdier.",
            "Katten hebben behoefte aan voldoende schuilplaatsen in huis.",
            "Regelmatige dierenartscontroles zijn belangrijk voor de gezondheid van je kat."
        ]
    },
    {
        "question": "Hoe kan ik de relatie tussen mijn kat en andere huisdieren verbeteren?",
        "relevant_texts": [
            "Introduceer nieuwe huisdieren langzaam en zorg ervoor dat elke huisdier zijn eigen ruimte heeft.",
            "Gebruik positieve bekrachtiging om goed gedrag tussen huisdieren aan te moedigen.",
            "Zorg ervoor dat alle huisdieren voldoende aandacht krijgen om jaloezie te voorkomen."
        ],
        "irrelevant_texts": [
            "Het kiezen van het juiste voer is essentieel voor een goede gezondheid.",
            "Katten hebben vaak behoefte aan sociale interactie met hun baasjes.",
            "Het bieden van voldoende speelgoed helpt bij het verminderen van verveling."
        ]
    },
    {
        "question": "Hoe kan ik mijn kat leren om op het kattenbak te gaan?",
        "relevant_texts": [
            "Zorg ervoor dat de kattenbak schoon is en op een rustige plek staat waar je kat zich veilig voelt.",
            "Gebruik een fijne kattenbakvulling die aantrekkelijk is voor je kat.",
            "Als je kitten niet naar de bak gaat, neem hem dan voorzichtig naar de bak na het eten of slapen."
        ],
        "irrelevant_texts": [
            "Het gebruik van natuurlijke producten voor schoonmaken is beter voor huisdieren.",
            "Katten kunnen ook leren om trucjes uit te voeren met geduldige training.",
            "Een goede voeding draagt bij aan een gezonde spijsvertering."
        ]
    },
    {
        "question": "Zijn er bepaalde voedingsmiddelen die schadelijk zijn voor katten?",
        "relevant_texts": [
            "Chocolade, uien, knoflook, en druiven zijn zeer giftig voor katten.",
            "Ook alcohol en cafeïne moeten ten koste van alles vermeden worden bij katten.",
            "Het is belangrijk om alleen speciaal kattenvoer of goedgekeurde snacks aan je kat te geven."
        ],
        "irrelevant_texts": [
            "Katten hebben behoefte aan regelmatige lichaamsbeweging om gezond te blijven.",
            "Het creëren van een veilige omgeving helpt bij het welzijn van je huisdier.",
            "Vlooienbestrijding is essentieel voor de gezondheid van je kat."
        ]
    },
    {
        "question": "Is het mogelijk om een kat te trainen, en zo ja, welke technieken zijn effectief?",
        "relevant_texts": [
            "Ja, katten kunnen getraind worden met positieve bekrachtiging zoals beloningen en lof.",
            "Clickertraining is een populaire methode die effectief kan zijn bij het trainen van katten.",
            "Consistentie in training helpt bij het versterken van gewenst gedrag."
        ],
        "irrelevant_texts": [
            "Het kiezen van kwalitatief hoogwaardig voer is belangrijk voor hun gezondheid.",
            "Katten hebben verschillende soorten speelgoed nodig om actief te blijven.",
            "Regelmatige dierenartscontroles helpen bij het vroegtijdig opsporen van gezondheidsproblemen."
        ]
    },
    {
      "question": "Hoe vaak moet ik mijn kat borstelen en waarom is het belangrijk?",
      "relevant_texts": [
        "Kortharige katten hebben meestal genoeg aan een borstelbeurt per week, terwijl langharige katten dagelijks geborsteld moeten worden.",
        "Regelmatig borstelen helpt bij het verwijderen van losse haren en voorkomt haarballen.",
        "Borstelen stimuleert de bloedsomloop en verspreidt natuurlijke oliën door de vacht, wat resulteert in een gezonde, glanzende vacht.",
        "Het is een goede gelegenheid om de huid van je kat te controleren op eventuele problemen zoals vlooien of kale plekken.",
        "Borstelen kan een fijn moment van binding zijn tussen jou en je kat, mits je kat ervan geniet."
      ],
      "irrelevant_texts": [
        "Katten hebben behoefte aan vers drinkwater dat dagelijks ververst wordt.",
        "Een kattenbak moet regelmatig worden schoongemaakt om hygiënisch te blijven.",
        "Sommige katten houden van kattenkruid, wat hen kan stimuleren om te spelen."
      ]
    },
    {
      "question": "Wat is het beste dieet voor een oudere kat?",
      "relevant_texts": [
        "Oudere katten hebben vaak baat bij voeding met een lager caloriegehalte om gewichtstoename te voorkomen, aangezien ze minder actief worden.",
        "Voeding rijk aan hoogwaardige eiwitten helpt om spiermassa te behouden bij oudere katten.",
        "Omega-3 vetzuren kunnen helpen bij het ondersteunen van gewrichten en cognitieve functies bij oudere katten.",
        "Sommige oudere katten hebben baat bij voeding die gemakkelijker te verteren is of een aangepaste textuur heeft.",
        "Overleg altijd met je dierenarts voor een dieet op maat, vooral als je kat specifieke gezondheidsproblemen heeft."
      ],
      "irrelevant_texts": [
        "Kittens hebben juist voeding nodig met een hoog caloriegehalte om hun groei te ondersteunen.",
        "Sommige katten zijn dol op kattengras, wat kan helpen bij de spijsvertering.",
        "Het is belangrijk om katten niet te veel traktaties te geven, ongeacht hun leeftijd."
      ]
    },
    {
      "question": "Hoe kan ik mijn binnen- en buitenkat veilig laten samenleven?",
      "relevant_texts": [
        "Introduceer de katten langzaam aan elkaar, begin met geuruitwisseling door middel van dekens of speeltjes.",
        "Zorg voor voldoende verticale ruimtes en verstopplekken voor beide katten.",
        "Houd de buitenkat regelmatig onder controle op parasieten om de binnenkat te beschermen.",
        "Voer de katten apart om competitie en stress te voorkomen.",
        "Zorg dat de binnenkat voldoende stimulatie krijgt om jaloersheid te voorkomen."
      ],
      "irrelevant_texts": [
        "Katten hebben geen speciale diëten nodig om samen te kunnen leven.",
        "Het is niet nodig om katten van hetzelfde geslacht te hebben voor een goede samenwoning.",
        "De kleur van de kat heeft geen invloed op hoe goed ze met andere katten omgaan."
      ]
    },
    {
        "question": "Hoe vaak moet een kat naar de dierenarts?",
        "relevant_texts": [
            "Een kat moet minimaal één keer per jaar naar de dierenarts voor een check-up. Tijdens deze controle worden het gebit, de vacht, de oren, ogen en de algemene gezondheid van de kat gecontroleerd. Katten ouder dan zeven jaar moeten vaker worden gecontroleerd, vaak eens per zes maanden, omdat ze vatbaarder zijn voor ouderdomskwalen zoals nierproblemen en artrose.",
            "Vaccinaties zijn ook belangrijk voor de gezondheid van de kat. Kittens hebben meerdere vaccinaties nodig in hun eerste levensjaar en daarna jaarlijks of tweejaarlijks een herhalingsvaccinatie tegen ziektes zoals kattenziekte en niesziekte."
        ],
        "irrelevant_texts": [
            "Katten hebben een bijzonder scherpe reukzin die hen helpt bij het vinden van voedsel. Ze kunnen subtiele geursporen oppikken die mensen niet eens opmerken. Dit komt doordat hun reukorgaan veel gevoeliger is dan dat van ons.",
            "De kleur van de vacht van een kat kan variëren van zwart en wit tot rood en blauwgrijs. De kleur van de ogen van een kat kan ook sterk verschillen, van helder blauw tot diep amberkleurig."
        ]
    },
    {
        "question": "Hoe oud kan een kat worden?",
        "relevant_texts": [
            "Huiskatten kunnen gemiddeld tussen de 12 en 16 jaar oud worden, hoewel sommige katten de leeftijd van 20 jaar of zelfs ouder kunnen bereiken. Dit hangt af van verschillende factoren zoals voeding, verzorging, en genetica. Buitenkatten hebben vaak een kortere levensduur vanwege gevaren zoals verkeer, ziektes en gevechten met andere dieren.",
            "De oudste geregistreerde kat ter wereld, Creme Puff, werd maar liefst 38 jaar oud. Een goede verzorging en regelmatige medische controle kunnen bijdragen aan een langere levensduur voor katten."
        ],
        "irrelevant_texts": [
            "Katten staan bekend om hun behendigheid. Ze kunnen met gemak van grote hoogtes springen zonder zichzelf te bezeren, dankzij hun flexibele ruggengraat en sterke poten.",
            "De staart van een kat wordt gebruikt om balans te houden tijdens het lopen of springen, en helpt de kat ook om te communiceren met andere katten en mensen. Een opgerichte staart kan duiden op een gelukkige kat, terwijl een laag gehouden staart vaak een teken is van angst of onzekerheid."
        ]
    },
    {
        "question": "Waarom spinnen katten?",
        "relevant_texts": [
            "Katten spinnen vaak als ze tevreden of ontspannen zijn, maar het kan ook een manier zijn om zichzelf te kalmeren wanneer ze angstig of gewond zijn. De trillingen die bij het spinnen ontstaan, kunnen zelfs helpen bij het genezingsproces van botten en weefsels.",
            "Sommige katten spinnen ook om de aandacht van hun eigenaar te trekken, bijvoorbeeld wanneer ze honger hebben of geaaid willen worden. Het is een veelzijdig communicatiemiddel dat niet alleen voor plezier maar ook voor troost en herstel wordt gebruikt."
        ],
        "irrelevant_texts": [
            "Katten hebben scherpe klauwen die ze gebruiken om te jagen en zichzelf te verdedigen. Ze krabben aan objecten zoals meubels en bomen om hun klauwen scherp te houden en hun territorium te markeren.",
            "De gemiddelde kat slaapt ongeveer 16 uur per dag, waarbij de meeste slaapperiodes verspreid zijn over korte dutjes van enkele minuten tot een paar uur. Katten zijn van nature nachtdieren, wat betekent dat ze het meest actief zijn in de vroege ochtend- en avonduren."
        ]
    },
    {
        "question": "Hoe verzorg je de tanden van een kat?",
        "relevant_texts": [
            "Tandverzorging bij katten is essentieel om tandvleesontstekingen en tandverlies te voorkomen. Het wordt aanbevolen om de tanden van een kat regelmatig te poetsen met speciale kattentandpasta en een tandenborstel die geschikt is voor huisdieren. Een goede mondgezondheid kan ook worden ondersteund door speciale tandenreinigende snacks of brokken.",
            "Het is belangrijk om tekenen van tandproblemen, zoals slechte adem, overmatig speekselen of moeite met eten, serieus te nemen. Katten laten vaak pas in een laat stadium merken dat ze pijn hebben, dus regelmatige tandcontroles door een dierenarts zijn van groot belang."
        ],
        "irrelevant_texts": [
            "Katten zijn erg territoriaal en zullen vaak gevechten aangaan met andere katten om hun terrein te beschermen. Dit gedrag komt vaker voor bij ongecastreerde katers, maar ook poezen kunnen hun territorium fel verdedigen.",
            "Het spinnen van katten is een geluid dat wordt geproduceerd door snelle bewegingen van de spieren in de keel, die trilling veroorzaken. Dit geluid wordt meestal geassocieerd met tevredenheid, maar katten kunnen ook spinnen als ze bang of gestrest zijn."
        ]
    },
    {
        "question": "Wat voor voeding heeft een kitten nodig?",
        "relevant_texts": [
            "Kittens hebben een speciaal dieet nodig dat rijk is aan eiwitten en vetten om hun snelle groei te ondersteunen. Speciaal kittenvoer bevat vaak meer calorieën en essentiële voedingsstoffen zoals taurine, wat belangrijk is voor hun oog- en hartgezondheid. Kittens moeten ook vaker per dag eten krijgen, meestal drie tot vier keer, omdat hun kleine maagjes snel leeg zijn.",
            "Zolang een kitten nog bij de moeder is, moet het tot ongeveer 8 weken oud moedermelk drinken, wat essentieel is voor hun ontwikkeling. Daarna kan er langzaam worden overgeschakeld op vast voedsel, maar het is belangrijk dat het voer speciaal voor kittens is geformuleerd."
        ],
        "irrelevant_texts": [
            "Kittens zijn bijzonder speels en leren veel over hun omgeving door te spelen met hun broertjes en zusjes. Dit is essentieel voor hun sociale ontwikkeling en coördinatie.",
            "De ogen van een kitten zijn bij de geboorte blauw en veranderen pas later naar hun definitieve kleur. Dit proces kan enkele weken duren en is volledig afhankelijk van het pigment in de iris van het oog."
        ]
    },
    {
        "question": "Wat is het verschil tussen natvoer en droogvoer voor katten?",
        "relevant_texts": [
            "Natvoer bevat meer water en is vaak smakelijker voor katten, wat kan helpen om voldoende vocht binnen te krijgen, vooral voor katten die niet veel drinken. Het is ook zachter, wat het makkelijker maakt voor oudere katten met tandproblemen om te eten. Droogvoer daarentegen helpt bij het reinigen van de tanden en is vaak goedkoper en makkelijker op te slaan.",
            "Droogvoer heeft een langere houdbaarheid en bevat vaak meer geconcentreerde voedingsstoffen, maar het kan leiden tot uitdroging als de kat niet genoeg water drinkt. Sommige eigenaren kiezen ervoor om zowel nat- als droogvoer aan te bieden om een gebalanceerd dieet te creëren."
        ],
        "irrelevant_texts": [
            "Katten gebruiken hun snorharen om hun omgeving te verkennen en voelen subtiele veranderingen in luchtstromen. Deze gevoelige haren helpen hen navigeren, vooral in het donker of in nauwe ruimtes.",
            "Katten hebben vijf tenen aan hun voorpoten en vier aan hun achterpoten. Sommige katten hebben echter een genetische eigenaardigheid, polydactylie, waarbij ze extra tenen hebben. Dit wordt soms als een geluksteken beschouwd."
        ]
    },
    {
        "question": "Hoeveel water moet een kat per dag drinken?",
        "relevant_texts": [
            "Een kat moet gemiddeld 50 milliliter water per kilogram lichaamsgewicht per dag drinken. Voor een kat van 4 kilo komt dit neer op ongeveer 200 milliliter per dag. Katten die droogvoer krijgen, hebben meer water nodig omdat droogvoer minder vocht bevat dan natvoer.",
            "Veel katten drinken van nature niet veel water, daarom is het belangrijk om ze te stimuleren door meerdere waterbakjes in huis te plaatsen of te investeren in een waterfontein. Het geven van natvoer kan ook bijdragen aan een betere hydratatie."
        ],
        "irrelevant_texts": [
            "Katten communiceren vaak met hun staart. Een zwiepende staart kan duiden op irritatie, terwijl een rechte, trillende staart vaak een teken van vreugde is. Dit lichaamstaalgedrag helpt eigenaren om beter te begrijpen hoe hun kat zich voelt.",
            "Veel katten houden ervan om in hoge gebieden te zitten omdat dit hen een gevoel van veiligheid en overzicht geeft. Ze kunnen van bovenaf hun omgeving observeren en hebben het gevoel dat ze controle hebben over hun territorium."
        ]
    },
    {
        "question": "Kunnen katten vegetarisch eten?",
        "relevant_texts": [
            "Katten zijn obligate carnivoren, wat betekent dat ze dierlijke eiwitten nodig hebben om gezond te blijven. Ze hebben essentiële voedingsstoffen zoals taurine, arachidonzuur, en vitamine A nodig, die alleen in dierlijke producten voorkomen. Een vegetarisch dieet kan ernstige gezondheidsproblemen veroorzaken, zoals blindheid, hartproblemen en een verzwakt immuunsysteem.",
            "Er zijn geen wetenschappelijk bewezen veilige vegetarische diëten voor katten, en het wordt afgeraden om een kat een dieet te geven dat volledig vrij is van dierlijke producten. In plaats daarvan moet hun dieet altijd voldoende vlees of hoogwaardige eiwitbronnen bevatten."
        ],
        "irrelevant_texts": [
            "Katten kunnen uren besteden aan het verzorgen van hun vacht. Dit gedrag helpt hen om schoon te blijven en om hun geur te verspreiden, wat belangrijk is voor het markeren van hun territorium.",
            "De meeste katten houden niet van water, maar er zijn enkele rassen, zoals de Turkse Van, die er wel van genieten om in het water te spelen of zelfs te zwemmen."
        ]
    },
    {
        "question": "Wat zijn de gevolgen van overgewicht bij katten?",
        "relevant_texts": [
            "Overgewicht bij katten kan leiden tot een verhoogd risico op gezondheidsproblemen zoals diabetes, gewrichtsproblemen, en hartziekten. Obesitas kan ook de levensverwachting van een kat aanzienlijk verkorten. Katten met overgewicht hebben vaak moeite met bewegen, zijn minder actief, en kunnen problemen hebben met ademhalen.",
            "Een gezonde, evenwichtige voeding en voldoende beweging zijn essentieel om overgewicht te voorkomen. Het is belangrijk om de dagelijkse voedselinname van de kat te monitoren en indien nodig dieetvoer te gebruiken dat speciaal is ontwikkeld voor gewichtsbeheersing."
        ],
        "irrelevant_texts": [
            "Katten hebben een uitstekend gehoor en kunnen geluiden in een frequentiebereik horen dat veel hoger is dan dat van mensen. Dit helpt hen om kleine prooien, zoals muizen, te detecteren, zelfs als deze zich onder de grond bevinden.",
            "De ogen van katten reflecteren licht, wat hen een groot voordeel geeft bij het zien in het donker. Dit komt door een laag cellen, tapetum lucidum genaamd, die licht terugkaatst naar de retina."
        ]
    },
    {
        "question": "Waarom krabt een kat aan meubels?",
        "relevant_texts": [
            "Katten krabben aan meubels om hun klauwen te onderhouden en hun territorium te markeren. De geurklieren in hun poten laten geursporen achter die andere katten kunnen waarnemen. Daarnaast helpt het krabben om de dode buitenste laag van hun klauwen te verwijderen, waardoor ze scherp blijven.",
            "Om te voorkomen dat een kat aan meubels krabt, kan een krabpaal worden aangeschaft. Het plaatsen van meerdere krabpalen door het huis en het belonen van de kat wanneer hij deze gebruikt, kan helpen om ongewenst krabgedrag aan meubels te verminderen."
        ],
        "irrelevant_texts": [
            "De vacht van een kat helpt bij het reguleren van hun lichaamstemperatuur. Wanneer het koud is, zal een kat zijn vacht meer opzetten om warmte vast te houden. In de zomer verhaart de kat om overtollige vacht kwijt te raken.",
            "Katten hebben een sterk nachtzicht. Ze kunnen bij veel minder licht zien dan mensen, wat hen uitstekende jagers maakt in schemerige omstandigheden."
        ]
    },
    {
        "question": "Waarom sproeien sommige katten in huis?",
        "relevant_texts": [
            "Sproeien is een vorm van territorium markeren en komt vaker voor bij ongecastreerde katers, maar ook poezen kunnen dit gedrag vertonen. Het sproeien kan worden veroorzaakt door stress, veranderingen in de omgeving, of de aanwezigheid van andere katten. Het is belangrijk om eerst medische oorzaken uit te sluiten, zoals een blaasontsteking, voordat er wordt gekeken naar gedragsmatige oplossingen.",
            "Castratie of sterilisatie kan vaak helpen om sproeien te verminderen, vooral bij katers. Daarnaast kan het helpen om stressfactoren te identificeren en te verminderen, zoals het plaatsen van meerdere kattenbakken of het gebruik van feromonen om de kat te kalmeren."
        ],
        "irrelevant_texts": [
            "Katten kunnen grote sprongen maken, soms wel vijf tot zes keer hun lichaamslengte. Dit komt door de kracht in hun achterpoten en hun flexibele ruggengraat, die hen helpt om met precisie te landen.",
            "De snorharen van een kat zijn niet alleen decoratief, ze spelen een cruciale rol in de perceptie van hun omgeving. Katten gebruiken hun snorharen om afstanden in te schatten en obstakels te vermijden, vooral in donkere omstandigheden."
        ]
    },
    {
        "question": "Waarom is mijn kat agressief naar andere katten?",
        "relevant_texts": [
            "Agressie tussen katten kan worden veroorzaakt door territoriumdrang, angst, of een gebrek aan socialisatie. Katten die elkaar niet vanaf een jonge leeftijd hebben leren kennen, kunnen moeite hebben om samen te leven, vooral als er onvoldoende ruimte is om zich terug te trekken. Agressief gedrag kan zich uiten in blazen, grommen, of zelfs fysieke aanvallen.",
            "Om agressie te verminderen, is het belangrijk om katten langzaam aan elkaar te laten wennen, bijvoorbeeld door ze eerst van elkaar gescheiden te houden en hun geur uit te wisselen via doekjes. Feromoonproducten kunnen ook helpen om de stress te verminderen die agressief gedrag kan veroorzaken."
        ],
        "irrelevant_texts": [
            "Katten zijn van nature solitaire jagers, maar ze kunnen in sommige gevallen ook in groepen leven, zoals bij verwilderde kattenkolonies. In huiselijke omstandigheden is het echter vaak moeilijker voor katten om hun territorium te delen met andere katten.",
            "Een kat kan urenlang dutjes doen, maar tijdens hun slaap blijven ze alert voor plotselinge geluiden. Dit komt door hun instinct om snel te reageren op potentiële bedreigingen of prooi."
        ]
    },
    {
        "question": "Hoe voorkom je dat een kat ’s nachts miauwt?",
        "relevant_texts": [
            "Katten miauwen ’s nachts vaak uit verveling, honger of een verlangen naar aandacht. Het kan helpen om voor het slapengaan met de kat te spelen om hem moe te maken. Daarnaast is het belangrijk om ervoor te zorgen dat de kat voldoende te eten heeft voordat je naar bed gaat, zodat hij ’s nachts niet wakker wordt van de honger.",
            "Als een kat consequent miauwt om aandacht, is het belangrijk om dit gedrag te negeren. Het geven van aandacht, zelfs negatieve aandacht, kan het miauwen alleen maar versterken. In plaats daarvan kan het helpen om een vaste routine te creëren waarin de kat weet wat hij kan verwachten."
        ],
        "irrelevant_texts": [
            "Katten gebruiken hun staart om hun evenwicht te bewaren, vooral tijdens het springen en klauteren. Een kat met een opgerichte staart voelt zich zelfverzekerd en tevreden, terwijl een laag gehouden staart kan wijzen op angst of onzekerheid.",
            "Katten hebben scherpe zintuigen en kunnen zeer subtiele veranderingen in hun omgeving waarnemen, zoals nieuwe geuren of geluiden. Dit maakt hen alert op potentiële gevaren of prooien."
        ]
    },
    {
        "question": "Waarom plast mijn kat naast de kattenbak?",
        "relevant_texts": [
            "Wanneer een kat naast de kattenbak plast, kan dit verschillende oorzaken hebben, zoals stress, een medische aandoening zoals blaasproblemen, of ontevredenheid over de kattenbak. Katten zijn zeer kieskeurig over hun toiletgewoontes en zullen de kattenbak vermijden als deze niet schoon genoeg is, of als hij op een plek staat die de kat niet prettig vindt.",
            "Het is belangrijk om de kattenbak dagelijks schoon te maken en ervoor te zorgen dat er genoeg kattenbakken zijn voor het aantal katten in huis. Ook kan het helpen om verschillende soorten kattenbakvulling uit te proberen om te zien welke de voorkeur van de kat heeft."
        ],
        "irrelevant_texts": [
            "Katten hebben een uitzonderlijk reukvermogen dat hen helpt bij het vinden van voedsel en bij het herkennen van territoriumgrenzen. Ze gebruiken geuren om hun omgeving te verkennen en communiceren met andere katten via geursporen.",
            "Sommige katten kunnen leren om trucjes uit te voeren, zoals zitten, pootjes geven of zelfs apporteren. Dit vereist geduld en positieve bekrachtiging, zoals het belonen met snoepjes of speeltjes."
        ]
    },
    {
        "question": "Waarom eet mijn kat niet?",
        "relevant_texts": [
            "Als een kat niet eet, kan dit verschillende oorzaken hebben, waaronder stress, ziekte, of pijn. Een kat die plotseling stopt met eten, moet zo snel mogelijk door een dierenarts worden gecontroleerd, omdat het missen van maaltijden, vooral bij katten, kan leiden tot leververvetting, een ernstige aandoening.",
            "Soms eet een kat niet vanwege veranderingen in de omgeving, zoals een nieuwe kattenbak of ander voer. Het is belangrijk om veranderingen langzaam door te voeren en ervoor te zorgen dat de kat zich veilig voelt in zijn omgeving om eetproblemen te voorkomen."
        ],
        "irrelevant_texts": [
            "Katten kunnen soms heel kieskeurig zijn over hun voeding. Het kan nodig zijn om verschillende merken of smaken uit te proberen voordat een kat iets vindt wat hij lekker vindt. Sommige katten houden bijvoorbeeld van vis, terwijl andere katten juist meer van gevogelte houden.",
            "De communicatie tussen katten is subtiel. Ze gebruiken lichaamstaal, zoals het bewegen van de oren en de staart, en geluiden zoals spinnen of miauwen om met mensen en andere dieren te communiceren."
        ]
    },
    {
        "question": "Hoe introduceer je een nieuwe kat bij een andere kat?",
        "relevant_texts": [
            "Het is belangrijk om nieuwe katten langzaam en zorgvuldig aan elkaar te introduceren om stress en agressie te minimaliseren. Begin met het houden van de nieuwe kat in een aparte kamer, zodat de katten elkaar kunnen ruiken zonder direct contact. Wissel vervolgens geuren uit door bijvoorbeeld een doekje over beide katten te wrijven en deze aan elkaar te laten ruiken.",
            "Na een paar dagen kunnen de katten elkaar zien, bijvoorbeeld door een deur op een kier te zetten of via een kattenhek. Dit visuele contact helpt hen om aan elkaar te wennen voordat ze elkaar volledig kunnen ontmoeten."
        ],
        "irrelevant_texts": [
            "Katten zijn carnivoren en hun dieet moet voornamelijk uit dierlijke eiwitten bestaan. Droogvoer is vaak goedkoper en makkelijker te bewaren, maar natvoer kan helpen bij de hydratatie van de kat.",
            "De meeste katten zijn solitair en kunnen goed alleen jagen. Dit betekent echter niet dat ze geen gezelschap waarderen; veel katten vormen sterke banden met hun eigenaren en andere dieren in huis."
        ]
    },
    {
        "question": "Wat te doen als katten elkaar aanvallen tijdens de introductie?",
        "relevant_texts": [
            "Het is niet ongewoon dat katten agressief zijn naar elkaar tijdens de eerste ontmoetingen. Dit kan voorkomen als ze zich bedreigd voelen of hun territorium willen verdedigen. Als de katten vechten, is het belangrijk om ze onmiddellijk te scheiden en de introductie te vertragen. Geef ze meer tijd om aan elkaars geur en aanwezigheid te wennen voordat je ze weer samenbrengt.",
            "Het gebruik van feromonen, zoals Feliway, kan helpen om de stress te verminderen en de katten rustiger te maken. Ook is het belangrijk om ervoor te zorgen dat er genoeg middelen, zoals kattenbakken, slaapplaatsen en voerbakken, beschikbaar zijn, zodat de katten niet hoeven te concurreren."
        ],
        "irrelevant_texts": [
            "Katten hebben scherpe klauwen die ze gebruiken om te jagen en zichzelf te verdedigen. Het is normaal dat katten hun klauwen in en uit trekken als ze zich ontspannen voelen of zich voorbereiden op een sprong.",
            "Een kat die zich op zijn rug rolt, voelt zich meestal comfortabel en veilig. Dit is vaak een uitnodiging om geaaid te worden, hoewel sommige katten dit gedrag ook vertonen als speelse uitdaging."
        ]
    },
    {
        "question": "Hoe lang duurt het voordat katten aan elkaar gewend zijn?",
        "relevant_texts": [
            "Hoe lang het duurt voordat katten aan elkaar gewend zijn, verschilt per individu. Sommige katten kunnen binnen een paar dagen aan elkaar wennen, terwijl het bij anderen weken of zelfs maanden kan duren. Het is belangrijk om geduld te hebben en de katten niet te forceren om sneller contact te maken dan ze willen.",
            "Het observeren van de lichaamstaal van beide katten kan helpen om te bepalen of ze zich op hun gemak voelen bij elkaar. Blazen, grommen en rechtopstaande haren zijn tekenen dat ze nog niet klaar zijn voor direct contact, terwijl snuffelen en ontspannen gedrag wijzen op een succesvolle introductie."
        ],
        "irrelevant_texts": [
            "Katten kunnen tot wel 16 uur per dag slapen, met de meeste dutjes verspreid over de dag. Ze slapen in korte periodes, waardoor ze altijd alert kunnen zijn op veranderingen in hun omgeving.",
            "De ogen van een kat zijn ontworpen om goed te functioneren in het donker. Ze hebben een extra laag achter hun netvlies, het tapetum lucidum, dat licht terugkaatst en hen helpt beter te zien bij weinig licht."
        ]
    },
    {
        "question": "Wat als de katten elkaar na een lange tijd nog steeds niet accepteren?",
        "relevant_texts": [
            "Als katten elkaar na weken of maanden nog steeds niet accepteren, kan het helpen om professionele hulp van een kattengedragstherapeut in te schakelen. Deze experts kunnen helpen bij het identificeren van onderliggende problemen, zoals territoriale conflicten of angst, en een plan opstellen om de relatie tussen de katten te verbeteren.",
            "Soms kan het nodig zijn om permanente maatregelen te nemen, zoals het creëren van gescheiden ruimtes in huis, waar elke kat zijn eigen territorium heeft. Het is belangrijk om stress te verminderen door voldoende middelen beschikbaar te stellen en te zorgen voor voldoende mentale en fysieke stimulatie."
        ],
        "irrelevant_texts": [
            "De meeste katten zijn uitstekende jagers en kunnen zelfs kleine vogels of knaagdieren vangen, zelfs als ze binnenshuis leven. Dit jagersinstinct blijft sterk, zelfs als ze geen honger hebben.",
            "Sommige kattenrassen, zoals de Maine Coon en de Noorse Boskat, staan bekend om hun grote formaat en pluizige vacht. Deze katten zijn vaak sociaal en kunnen goed overweg met andere huisdieren en kinderen."
        ]
    },
    {
        "question": "Hoe kun je conflicten tussen katten verminderen?",
        "relevant_texts": [
            "Om conflicten tussen katten te verminderen, is het belangrijk om ervoor te zorgen dat er genoeg bronnen zoals voerbakken, waterbakken, kattenbakken en slaapplaatsen beschikbaar zijn. Dit vermindert de noodzaak voor katten om te concurreren. Plaats meerdere krabpalen en verhoogde zitplekken, zodat elke kat zijn eigen ruimte kan claimen.",
            "Het aanbieden van interactieve speeltjes en regelmatig spelen met elke kat afzonderlijk kan helpen om hun energie kwijt te raken en frustraties te verminderen. Het is ook belangrijk om de katten apart te voeden als ze neigen te vechten over voedsel."
        ],
        "irrelevant_texts": [
            "Katten gebruiken miauwen en spinnen om te communiceren met hun eigenaren. Sommige katten zijn spraakzamer dan andere, en dit hangt vaak af van het ras en de persoonlijkheid van de kat.",
            "Het is normaal dat katten af en toe haarballen opbraken, vooral als ze zichzelf veel verzorgen. Haarballen ontstaan doordat katten tijdens het wassen losse haren inslikken, die zich ophopen in hun maag."
        ]
    },
    {
        "question": "Hoe belangrijk is geur bij het wennen van katten aan elkaar?",
        "relevant_texts": [
            "Geur speelt een cruciale rol in hoe katten elkaar leren kennen. Katten herkennen elkaar aan hun geur, en het uitwisselen van geur door middel van doekjes of objecten kan helpen om de stress te verminderen wanneer ze aan een nieuwe kat worden geïntroduceerd. Het wrijven van een doekje over de kop van beide katten en deze in elkaars ruimte leggen kan hen helpen om zich veiliger te voelen.",
            "Door een kat na elke interactie met een nieuwe kat te belonen met een traktatie of positieve aandacht, kan de associatie met de geur van de nieuwe kat verbeteren. Dit kan een belangrijke stap zijn in het soepel laten verlopen van de introductie."
        ],
        "irrelevant_texts": [
            "Katten kunnen urenlang observeren vanuit een hoge plek, zoals een plank of vensterbank. Dit geeft hen een gevoel van veiligheid en controle over hun omgeving.",
            "De meeste katten houden van het gevoel van veiligheid dat een doos of gesloten ruimte biedt. Dit verklaart waarom veel katten graag in dozen zitten of in kleine, afgesloten ruimtes slapen."
        ]
    },
    {
        "question": "Hoeveel kost het om een kat te adopteren?",
        "relevant_texts": [
            "De kosten van het adopteren van een kat variëren afhankelijk van waar je de kat adopteert. Bij een dierenasiel kan de adoptieprijs variëren van €50 tot €150, afhankelijk van de leeftijd en het ras van de kat. Deze prijs dekt vaak de kosten voor vaccinaties, sterilisatie of castratie, en een gezondheidsonderzoek.",
            "Bij een fokker zijn de kosten voor een raskat vaak veel hoger en kunnen oplopen tot wel €1000 of meer, afhankelijk van het ras en de reputatie van de fokker. Het is belangrijk om rekening te houden met de langetermijnkosten van het verzorgen van een kat, naast de initiële adoptiekosten."
        ],
        "irrelevant_texts": [
            "Katten houden van routine en kunnen van streek raken door veranderingen in hun omgeving. Een nieuwe omgeving, zoals een verhuizing of de introductie van een nieuw huisdier, kan stress veroorzaken bij katten.",
            "Katten zijn van nature nieuwsgierig en verkennen hun omgeving met behulp van hun scherpe zintuigen. Ze gebruiken hun snorharen om te navigeren door smalle ruimtes en om objecten om hen heen te voelen."
        ]
    },
    {
        "question": "Hoeveel kost het om een kat te verzorgen?",
        "relevant_texts": [
            "De maandelijkse kosten voor het verzorgen van een kat kunnen variëren, maar gemiddeld moet je rekening houden met €20 tot €50 per maand voor voedsel, afhankelijk van het type voer dat je kiest. Daarnaast komen kosten voor kattenbakvulling, die gemiddeld tussen de €5 en €15 per maand kunnen liggen, afhankelijk van het type vulling.",
            "Regelmatige kosten zoals vaccinaties, ontworming en vlooienbehandelingen bedragen gemiddeld €100 tot €200 per jaar. Daarnaast is het belangrijk om een noodfonds te hebben voor onverwachte dierenartskosten, die in sommige gevallen hoog kunnen oplopen."
        ],
        "irrelevant_texts": [
            "Katten kunnen leren om hun omgeving te verkennen door middel van geur en zicht. Ze markeren hun territorium door te krabben of door geursporen achter te laten met hun klieren in de poten.",
            "Katten houden ervan om op hoge plaatsen te zitten omdat ze zich daar veiliger voelen. Het biedt hen een goed overzicht van hun omgeving, waardoor ze potentiële bedreigingen snel kunnen waarnemen."
        ]
    },
    {
        "question": "Zijn er extra kosten bij het houden van een kat binnenshuis?",
        "relevant_texts": [
            "Bij het houden van een kat binnenshuis zijn er extra kosten voor het creëren van een stimulerende omgeving. Dit kan inhouden het aanschaffen van krabpalen, speeltjes, en klimmeubels, wat kan variëren van €50 tot enkele honderden euro's, afhankelijk van de kwaliteit en het aantal items.",
            "Daarnaast kunnen binnenkatten vaker gezondheidszorg nodig hebben, zoals extra vaccinaties en regelmatige controles, om ervoor te zorgen dat ze gezond blijven zonder toegang tot de buitenwereld. Dit kan leiden tot hogere dierenartskosten op de lange termijn."
        ],
        "irrelevant_texts": [
            "Katten kunnen genieten van het kijken naar vogels en andere dieren buiten het raam. Het creëren van een 'kijkplek' voor je kat kan hen helpen om zich bezig te houden en te ontspannen.",
            "De meeste katten staan bekend om hun zelfredzaamheid, maar ze hebben nog steeds veel aandacht en zorg nodig. Ze kunnen een sterke band vormen met hun eigenaren en genieten van regelmatige speeltijd."
        ]
    },
    {
        "question": "Hoeveel kost een ziektekostenverzekering voor een kat?",
        "relevant_texts": [
            "De kosten van een ziektekostenverzekering voor een kat hangen af van de leeftijd, het ras en de gezondheid van de kat. Gemiddeld kost een verzekering tussen de €10 en €30 per maand. Sommige verzekeringen dekken routinezorg, zoals vaccinaties en jaarlijkse controles, terwijl andere alleen grote, onverwachte medische kosten dekken.",
            "Het is belangrijk om de polisvoorwaarden goed te controleren, omdat sommige verzekeringen bepaalde rassen uitsluiten of hogere premies vragen voor oudere katten. Het hebben van een ziektekostenverzekering kan helpen om dure behandelingen, zoals operaties of medicatie, te bekostigen zonder dat je voor onverwachte uitgaven komt te staan."
        ],
        "irrelevant_texts": [
            "Katten staan bekend om hun territoriale aard. Ze kunnen hun territorium markeren door te krabben of door geursporen achter te laten via klieren in hun wangen en poten.",
            "Sommige katten houden van water en vinden het leuk om met druppels of in een stromende kraan te spelen. Dit gedrag is echter niet bij alle katten gebruikelijk, en veel katten vermijden water liever."
        ]
    },
    {
        "question": "Wat zijn de jaarlijkse medische kosten voor een kat?",
        "relevant_texts": [
            "De jaarlijkse medische kosten voor een kat kunnen variëren, maar gemiddeld moet je rekening houden met ongeveer €100 tot €300 per jaar. Dit omvat kosten voor vaccinaties, jaarlijkse controles, ontworming en vlooienpreventie. Sommige dierenartsen bieden ook gezondheidsplannen aan waarmee je de jaarlijkse zorgkosten kunt spreiden.",
            "Onverwachte medische kosten, zoals voor ziekten of verwondingen, kunnen echter veel hoger uitvallen. In dergelijke gevallen kan een ziektekostenverzekering of een noodfonds helpen om de kosten te dekken."
        ],
        "irrelevant_texts": [
            "Katten zijn vaak erg schoon en besteden veel tijd aan het verzorgen van hun vacht. Het is echter ook belangrijk voor eigenaren om regelmatig te borstelen, vooral bij langharige katten, om klitten te voorkomen.",
            "Het spinnen van een kat wordt vaak geassocieerd met tevredenheid, maar katten kunnen ook spinnen als ze zich angstig of ongemakkelijk voelen. Het spinnen kan een manier zijn om zichzelf te kalmeren."
        ]
    },
    {
        "question": "Wat zijn de opstartkosten voor het nemen van een kat?",
        "relevant_texts": [
            "De opstartkosten voor het nemen van een kat kunnen variëren, maar over het algemeen moet je rekening houden met ongeveer €100 tot €300. Dit omvat essentiële items zoals een kattenbak (€10-€50), een voerbak (€5-€20), een krabpaal (€20-€100), en speelgoed (€5-€50). Daarnaast moet je voer aanschaffen, wat gemiddeld rond de €10 tot €30 per maand kost, afhankelijk van het merk en de kwaliteit.",
            "Verder moet je denken aan de kosten voor de eerste gezondheidszorg, zoals vaccinaties en een controle door de dierenarts, wat tussen de €50 en €150 kan kosten. Het is belangrijk om deze kosten in je budget op te nemen voordat je een kat adopteert."
        ],
        "irrelevant_texts": [
            "Katten hebben een natuurlijke drang om te jagen en besteden veel tijd aan het besluipen van speeltjes of andere objecten in huis. Dit gedrag is een overblijfsel van hun wilde voorouders.",
            "Katten gebruiken hun staart als een communicatiemiddel. Een opgerichte staart met een lichte krul aan het uiteinde wijst op tevredenheid, terwijl een laag hangende of zwiepende staart kan wijzen op frustratie of angst."
        ]
    }
]

def l2_distance(vec1, vec2):
    return np.linalg.norm(vec1 - vec2)

def create_similarity_tuples(data):
    question = data['question']
    relevant_texts = data['relevant_texts']
    irrelevant_texts = data['irrelevant_texts']
    
    similar_texts = []
    dissimilar_texts = []
    
    # Similar texts: question with each relevant text
    similar_texts.extend([(question, text) for text in relevant_texts])
    
    # Similar texts: all combinations of relevant texts
    similar_texts.extend(list(combinations(relevant_texts, 2)))
    
    # Dissimilar texts: question with each irrelevant text
    dissimilar_texts.extend([(question, text) for text in irrelevant_texts])
    
    return similar_texts, dissimilar_texts

def convert_test_cases_in_test_dataframe(test_cases):
    all_similar_texts = []
    all_dissimilar_texts = []
    for test_case in test_cases:
        similar_texts, dissimilar_texts = create_similarity_tuples(test_case)
        all_similar_texts.extend(similar_texts)
        all_dissimilar_texts.extend(dissimilar_texts)
    
    type_column = ['similar'] * len(all_similar_texts) + ['dissimilar'] * len(all_dissimilar_texts)
    text1_column = [text[0] for text in all_similar_texts] + [text[0] for text in all_dissimilar_texts]
    text2_column = [text[1] for text in all_similar_texts] + [text[1] for text in all_dissimilar_texts]

    return pd.DataFrame({
        "type": type_column,
        "text1": text1_column,
        "text2": text2_column
    })

def add_distances_to_test_dataframe(model, test_dataframe, save_path: None):
    test_dataframe_copy = test_dataframe.copy()
    distances = []
    for text1, text2 in zip(test_dataframe_copy["text1"], test_dataframe_copy["text2"]):
        embedding1 = model.embed(text1)
        embedding2 = model.embed(text2)
        distance = l2_distance(embedding1, embedding2)
        distances.append(distance)
    test_dataframe_copy["distance"] = distances
    if save_path:
        test_dataframe_copy.to_pickle(save_path)
    return test_dataframe_copy

def test_dataframe_to_ratio_score(test_dataframe):
    avg_similar_distance = np.mean(test_dataframe[test_dataframe.type == "similar"]["distance"])
    avg_dissimilar_distance = np.mean(test_dataframe[test_dataframe.type == "dissimilar"]["distance"])
    dissimilar_similar_ratio = avg_dissimilar_distance / avg_similar_distance
    return dissimilar_similar_ratio