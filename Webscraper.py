import requests
from bs4 import BeautifulSoup

from requests_html import HTMLSession

import pprint
import random

import json

import os


SLEEP_VALUE = 0#5

pokeList = {"Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard", "Squirtle", "Wartortle", "Blastoise", "Caterpie", "Metapod", "Butterfree", "Weedle", "Kakuna", "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot", "Rattata", "Raticate", "Spearow", "Fearow", "Ekans", "Arbok", "Pikachu", "Raichu", "Sandshrew", "Sandslash", "Nidoran♀", "Nidorina", "Nidoqueen", "Nidoran♂", "Nidorino", "Nidoking", "Clefairy", "Clefable", "Vulpix", "Ninetales", "Jigglypuff", "Wigglytuff", "Zubat", "Golbat", "Oddish", "Gloom", "Vileplume", "Paras", "Parasect", "Venonat", "Venomoth", "Diglett", "Dugtrio", "Meowth", "Persian", "Psyduck", "Golduck", "Mankey", "Primeape", "Growlithe", "Arcanine", "Poliwag", "Poliwhirl", "Poliwrath", "Abra", "Kadabra", "Alakazam", "Machop", "Machoke", "Machamp", "Bellsprout", "Weepinbell", "Victreebel", "Tentacool", "Tentacruel", "Geodude", "Graveler", "Golem", "Ponyta", "Rapidash", "Slowpoke", "Slowbro", "Magnemite", "Magneton", "Farfetch’d", "Doduo", "Dodrio", "Seel", "Dewgong", "Grimer", "Muk", "Shellder", "Cloyster", "Gastly", "Haunter", "Gengar", "Onix", "Drowzee", "Hypno", "Krabby", "Kingler", "Voltorb", "Electrode", "Exeggcute", "Exeggutor", "Cubone", "Marowak", "Hitmonlee", "Hitmonchan", "Lickitung", "Koffing", "Weezing", "Rhyhorn", "Rhydon", "Chansey", "Tangela", "Kangaskhan", "Horsea", "Seadra", "Goldeen", "Seaking", "Staryu", "Starmie", "Mr. Mime", "Scyther", "Jynx", "Electabuzz", "Magmar", "Pinsir", "Tauros", "Magikarp", "Gyarados", "Lapras", "Ditto", "Eevee", "Vaporeon", "Jolteon", "Flareon", "Porygon", "Omanyte", "Omastar", "Kabuto", "Kabutops", "Aerodactyl", "Snorlax", "Articuno", "Zapdos", "Moltres", "Dratini", "Dragonair", "Dragonite", "Mewtwo", "Mew", "Chikorita", "Bayleef", "Meganium", "Cyndaquil", "Quilava", "Typhlosion", "Totodile", "Croconaw", "Feraligatr", "Sentret", "Furret", "Hoothoot", "Noctowl", "Ledyba", "Ledian", "Spinarak", "Ariados", "Crobat", "Chinchou", "Lanturn", "Pichu", "Cleffa", "Igglybuff", "Togepi", "Togetic", "Natu", "Xatu", "Mareep", "Flaaffy", "Ampharos", "Bellossom", "Marill", "Azumarill", "Sudowoodo", "Politoed", "Hoppip", "Skiploom", "Jumpluff", "Aipom", "Sunkern", "Sunflora", "Yanma", "Wooper", "Quagsire", "Espeon", "Umbreon", "Murkrow", "Slowking", "Misdreavus", "Unown", "Wobbuffet", "Girafarig", "Pineco", "Forretress", "Dunsparce", "Gligar", "Steelix", "Snubbull", "Granbull", "Qwilfish", "Scizor", "Shuckle", "Heracross", "Sneasel", "Teddiursa", "Ursaring", "Slugma", "Magcargo", "Swinub", "Piloswine", "Corsola", "Remoraid", "Octillery", "Delibird", "Mantine", "Skarmory", "Houndour", "Houndoom", "Kingdra", "Phanpy", "Donphan", "Porygon2", "Stantler", "Smeargle", "Tyrogue", "Hitmontop", "Smoochum", "Elekid", "Magby", "Miltank", "Blissey", "Raikou", "Entei", "Suicune", "Larvitar", "Pupitar", "Tyranitar", "Lugia", "Ho-Oh", "Celebi", "Treecko", "Grovyle", "Sceptile", "Torchic", "Combusken", "Blaziken", "Mudkip", "Marshtomp", "Swampert", "Poochyena", "Mightyena", "Zigzagoon", "Linoone", "Wurmple", "Silcoon", "Beautifly", "Cascoon", "Dustox", "Lotad", "Lombre", "Ludicolo", "Seedot", "Nuzleaf", "Shiftry", "Taillow", "Swellow", "Wingull", "Pelipper", "Ralts", "Kirlia", "Gardevoir", "Surskit", "Masquerain", "Shroomish", "Breloom", "Slakoth", "Vigoroth", "Slaking", "Nincada", "Ninjask", "Shedinja", "Whismur", "Loudred", "Exploud", "Makuhita", "Hariyama", "Azurill", "Nosepass", "Skitty", "Delcatty", "Sableye", "Mawile", "Aron", "Lairon", "Aggron", "Meditite", "Medicham", "Electrike", "Manectric", "Plusle", "Minun", "Volbeat", "Illumise", "Roselia", "Gulpin", "Swalot", "Carvanha", "Sharpedo", "Wailmer", "Wailord", "Numel", "Camerupt", "Torkoal", "Spoink", "Grumpig", "Spinda", "Trapinch", "Vibrava", "Flygon", "Cacnea", "Cacturne", "Swablu", "Altaria", "Zangoose", "Seviper", "Lunatone", "Solrock", "Barboach", "Whiscash", "Corphish", "Crawdaunt", "Baltoy", "Claydol", "Lileep", "Cradily", "Anorith", "Armaldo", "Feebas", "Milotic", "Castform", "Kecleon", "Shuppet", "Banette", "Duskull", "Dusclops", "Tropius", "Chimecho", "Absol", "Wynaut", "Snorunt", "Glalie", "Spheal", "Sealeo", "Walrein", "Clamperl", "Huntail", "Gorebyss", "Relicanth", "Luvdisc", "Bagon", "Shelgon", "Salamence", "Beldum", "Metang", "Metagross", "Regirock", "Regice", "Registeel", "Latias", "Latios", "Kyogre", "Groudon", "Rayquaza", "Jirachi", "Deoxys", "Turtwig", "Grotle", "Torterra", "Chimchar", "Monferno", "Infernape", "Piplup", "Prinplup", "Empoleon", "Starly", "Staravia", "Staraptor", "Bidoof", "Bibarel", "Kricketot", "Kricketune", "Shinx", "Luxio", "Luxray", "Budew", "Roserade", "Cranidos", "Rampardos", "Shieldon", "Bastiodon", "Burmy", "Wormadam", "Mothim", "Combee", "Vespiquen", "Pachirisu", "Buizel", "Floatzel", "Cherubi", "Cherrim", "Shellos", "Gastrodon", "Ambipom", "Drifloon", "Drifblim", "Buneary", "Lopunny", "Mismagius", "Honchkrow", "Glameow", "Purugly", "Chingling", "Stunky", "Skuntank", "Bronzor", "Bronzong", "Bonsly", "Mime Jr.", "Happiny", "Chatot", "Spiritomb", "Gible", "Gabite", "Garchomp", "Munchlax", "Riolu", "Lucario", "Hippopotas", "Hippowdon", "Skorupi", "Drapion", "Croagunk", "Toxicroak", "Carnivine", "Finneon", "Lumineon", "Mantyke", "Snover", "Abomasnow", "Weavile", "Magnezone", "Lickilicky", "Rhyperior", "Tangrowth", "Electivire", "Magmortar", "Togekiss", "Yanmega", "Leafeon", "Glaceon", "Gliscor", "Mamoswine", "Porygon-Z", "Gallade", "Probopass", "Dusknoir", "Froslass", "Rotom", "Uxie", "Mesprit", "Azelf", "Dialga", "Palkia", "Heatran", "Regigigas", "Giratina", "Cresselia", "Phione", "Manaphy", "Darkrai", "Shaymin", "Arceus", "Victini", "Snivy", "Servine", "Serperior", "Tepig", "Pignite", "Emboar", "Oshawott", "Dewott", "Samurott", "Patrat", "Watchog", "Lillipup", "Herdier", "Stoutland", "Purrloin", "Liepard", "Pansage", "Simisage", "Pansear", "Simisear", "Panpour", "Simipour", "Munna", "Musharna", "Pidove", "Tranquill", "Unfezant", "Blitzle", "Zebstrika", "Roggenrola", "Boldore", "Gigalith", "Woobat", "Swoobat", "Drilbur", "Excadrill", "Audino", "Timburr", "Gurdurr", "Conkeldurr", "Tympole", "Palpitoad", "Seismitoad", "Throh", "Sawk", "Sewaddle", "Swadloon", "Leavanny", "Venipede", "Whirlipede", "Scolipede", "Cottonee", "Whimsicott", "Petilil", "Lilligant", "Basculin", "Sandile", "Krokorok", "Krookodile", "Darumaka", "Darmanitan", "Maractus", "Dwebble", "Crustle", "Scraggy", "Scrafty", "Sigilyph", "Yamask", "Cofagrigus", "Tirtouga", "Carracosta", "Archen", "Archeops", "Trubbish", "Garbodor", "Zorua", "Zoroark", "Minccino", "Cinccino", "Gothita", "Gothorita", "Gothitelle", "Solosis", "Duosion", "Reuniclus", "Ducklett", "Swanna", "Vanillite", "Vanillish", "Vanilluxe", "Deerling", "Sawsbuck", "Emolga", "Karrablast", "Escavalier", "Foongus", "Amoonguss", "Frillish", "Jellicent", "Alomomola", "Joltik", "Galvantula", "Ferroseed", "Ferrothorn", "Klink", "Klang", "Klinklang", "Tynamo", "Eelektrik", "Eelektross", "Elgyem", "Beheeyem", "Litwick", "Lampent", "Chandelure", "Axew", "Fraxure", "Haxorus", "Cubchoo", "Beartic", "Cryogonal", "Shelmet", "Accelgor", "Stunfisk", "Mienfoo", "Mienshao", "Druddigon", "Golett", "Golurk", "Pawniard", "Bisharp", "Bouffalant", "Rufflet", "Braviary", "Vullaby", "Mandibuzz", "Heatmor", "Durant", "Deino", "Zweilous", "Hydreigon", "Larvesta", "Volcarona", "Cobalion", "Terrakion", "Virizion", "Tornadus", "Thundurus", "Reshiram", "Zekrom", "Landorus", "Kyurem", "Keldeo", "Meloetta", "Genesect", "Chespin", "Quilladin", "Chesnaught", "Fennekin", "Braixen", "Delphox", "Froakie", "Frogadier", "Greninja", "Bunnelby", "Diggersby", "Fletchling", "Fletchinder", "Talonflame", "Scatterbug", "Spewpa", "Vivillon", "Litleo", "Pyroar", "Flabébé", "Floette", "Florges", "Skiddo", "Gogoat", "Pancham", "Pangoro", "Furfrou", "Espurr", "Meowstic", "Honedge", "Doublade", "Aegislash", "Spritzee", "Aromatisse", "Swirlix", "Slurpuff", "Inkay", "Malamar", "Binacle", "Barbaracle", "Skrelp", "Dragalge", "Clauncher", "Clawitzer", "Helioptile", "Heliolisk", "Tyrunt", "Tyrantrum", "Amaura", "Aurorus", "Sylveon", "Hawlucha", "Dedenne", "Carbink", "Goomy", "Sliggoo", "Goodra", "Klefki", "Phantump", "Trevenant", "Pumpkaboo", "Gourgeist", "Bergmite", "Avalugg", "Noibat", "Noivern", "Xerneas", "Yveltal", "Zygarde", "Diancie", "Hoopa", "Volcanion", "Rowlet", "Dartrix", "Decidueye", "Litten", "Torracat", "Incineroar", "Popplio", "Brionne", "Primarina", "Pikipek", "Trumbeak", "Toucannon", "Yungoos", "Gumshoos", "Grubbin", "Charjabug", "Vikavolt", "Crabrawler", "Crabominable", "Oricorio", "Cutiefly", "Ribombee", "Rockruff", "Lycanroc", "Wishiwashi", "Mareanie", "Toxapex", "Mudbray", "Mudsdale", "Dewpider", "Araquanid", "Fomantis", "Lurantis", "Morelull", "Shiinotic", "Salandit", "Salazzle", "Stufful", "Bewear", "Bounsweet", "Steenee", "Tsareena", "Comfey", "Oranguru", "Passimian", "Wimpod", "Golisopod", "Sandygast", "Palossand", "Pyukumuku", "Type: Null", "Silvally", "Minior", "Komala", "Turtonator", "Togedemaru", "Mimikyu", "Bruxish", "Drampa", "Dhelmise", "Jangmo-o", "Hakamo-o", "Kommo-o", "Tapu Koko", "Tapu Lele", "Tapu Bulu", "Tapu Fini", "Cosmog", "Cosmoem", "Solgaleo", "Lunala", "Nihilego", "Buzzwole", "Pheromosa", "Xurkitree", "Celesteela", "Kartana", "Guzzlord", "Necrozma", "Magearna", "Marshadow", "Poipole", "Naganadel", "Stakataka", "Blacephalon", "Zeraora"}
formatPreferenceOrder = ["OU", "UU", "RU", "NU", "PU", "LC", "Ubers", "Doubles"]

level = 100
natures = {
           "Hardy":   [1,   1,   1,   1,   1,   1],
           "Lonely":  [1, 1.1, 0.9,   1,   1,   1],
           "Brave":   [1, 1.1,   1,   1,   1, 0.9],
           "Adamant": [1, 1.1,   1, 0.9,   1,   1],
           "Naughty": [1, 1.1,   1,   1, 0.9,   1],

           "Bold":    [1, 0.9, 1.1,   1,   1,   1],
           "Docile":  [1,   1,   1,   1,   1,   1],
           "Relaxed": [1,   1, 1.1,   1,   1, 0.9],
           "Impish":  [1,   1, 1.1, 0.9,   1,   1],
           "Lax":     [1,   1, 1.1,   1, 0.9,   1],

           "Timid":   [1, 0.9,   1,   1,   1, 1.1],
           "Hasty":   [1,   1, 0.9,   1,   1, 1.1],
           "Serious": [1,   1,   1,   1,   1,   1],
           "Jolly":   [1,   1,   1, 0.9,   1, 1.1],
           "Naive":   [1,   1,   1,   1, 0.9, 1.1],

           "Modest":  [1, 0.9,   1, 1.1,   1,   1],
           "Mild":    [1,   1, 0.9, 1.1,   1,   1],
           "Quiet":   [1,   1,   1, 1.1,   1, 0.9],
           "Bashful": [1,   1,   1,   1,   1,   1],
           "Rash":    [1,   1,   1, 1.1, 0.9,   1],

           "Calm":    [1, 0.9,   1,   1, 1.1,   1],
           "Gentle":  [1,   1, 0.9,   1, 1.1,   1],
           "Sassy":   [1,   1,   1,   1, 1.1, 0.9],
           "Careful": [1,   1,   1, 0.9, 1.1,   1],
           "Quirky":  [1,   1,   1,   1,   1,   1]
          }


def makeFormListing(formData):
    summary = formData.find(".PokemonAltInfo-data")[0]

    listing = {"base stats": [int(elem) for elem in formData.find(".PokemonStats",         first=True).text.split('\n')[1::2]],
               "types":      summary. find(".PokemonSummary-types", first=True).text.split('\n'),
               "abilities":  summary. find(".AbilityList",          first=True).text.split('\n'),
               "tier":       summary. find(".FormatList",           first=True).text.split('\n')
               }
    return listing

def makeStrategyListing(strategy, formListings):
    build = strategy.find("div", "MovesetInfo")

    buildMoves = build.find("div", "MovesetInfo-moves")
    buildMisc  = build.find("div", "MovesetInfo-misc")

    moves = []
    for elem in buildMoves.findAll("td"):
        ul = elem.findAll("li")
        if len(ul) == 0:
            moves.append([elem.text])
        else:
            moves.append([li.text for li in ul])

    misc = []
    for elem in buildMisc.findAll("td"):
        ul = elem.findAll("li")
        if len(ul) == 0:
            misc.append([elem.text])
        else:
            misc.append([li.text for li in ul])

    # EVs
    evs = misc[3] = buildEvSpread(misc[3])

    # IVs
    if len(misc) == 4:
        misc.append([31,31,31,31,31,31])
    else:
        misc[4] = buildIvSpread(misc[4])
    ivs = misc[4]

    #
    # Final Stats
    #

    natureMod = natures[misc[2][0]]

    baseStats = [-255]*6
    type = []
    try:
        baseStats = formListings["Base"]["base stats"]
        type = formListings["Base"]["types"]

        if misc[0][0].endswith("ite") and not misc[0][0].endswith("Eviolite"):
            baseStats = formListings["Mega"]["base stats"]
            type = formListings["Mega"]["types"]
    except Exception as ex:
        baseStats = formListings["Base"]["base stats"]
        type = formListings["Base"]["types"]

        print('->> no proper form found for the below forms with item "', misc[0], '" going with base form')
        print('\t', ex)

    stats = [int(int((2*baseStats[i] + ivs[i] + int(evs[i]/4)) * (level / 100) + 5) * natureMod[i]) for i in range(6)]

    listing = {"name": strategy.find("h1").text,
               "stats": stats,
               "type": type,
               "usage": strategy.find("section").findAll("p")[2].text,
               "moves": moves,
               "item": misc[0],
               "ability": misc[1],
               "nature": misc[2],
               "ev spread": evs,
               "iv spread": ivs
               }

    return listing


def buildEvSpread(labeledList):
    return buildSpread(labeledList, 0)


def buildIvSpread(labeledList):
    return buildSpread(labeledList, 31)


def buildSpread(labeledList, default):

    spread = [default]*6

    for elem in labeledList:
        if elem.endswith("HP"):
            spread[0] = int(elem[:len(elem) - 3])
        if elem.endswith("Atk"):
            spread[1] = int(elem[:len(elem) - 4])
        if elem.endswith("Def"):
            spread[2] = int(elem[:len(elem) - 4])
        if elem.endswith("SpA"):
            spread[3] = int(elem[:len(elem) - 4])
        if elem.endswith("SpD"):
            spread[4] = int(elem[:len(elem) - 4])
        if elem.endswith("Spe"):
            spread[5] = int(elem[:len(elem) - 4])

    return spread


def randomSleepValue():
    randval = random.expovariate(lambd=1)+0.5
    randval = min(12, randval)
    return SLEEP_VALUE*(randval)


def makePokeListing(session):
    pokePage = session.get("https://www.smogon.com/dex/sm/pokemon/" + pokemon.lower() + "/").html
    pokePage.render(sleep=randomSleepValue())

    #
    # navigate to preferred format
    #
    formatsAvailable = [elem.text for elem in pokePage.find(".PokemonPage-StrategySelector", first=True).find("li")]
    format = None

    for f in formatPreferenceOrder:
        if f in formatsAvailable:
            format = f
            break

    if format is None:
        format = formatsAvailable[0]
    else:
        pokePage = session.get("https://www.smogon.com/dex/sm/pokemon/" + pokemon.lower() + "/" + format + "/").html
        pokePage.render(sleep=randomSleepValue())

    #
    # Make form listings
    #
    titles = [elem.text for elem in pokePage.find("h1")]
    formNames = titles[2: titles.index("Evolutions")]
    if len(formNames) == 0:
        formNames = ["Base"]

    formList = [makeFormListing(formData) for formData in pokePage.find(".PokemonAltInfo")]

    formListings = {}
    try:
        for i in range(len(formList)):
            formList[i].update({"form": formNames[i]})
            formListings.update({formNames[i] : formList[i]})
    except Exception as ex:
        print("->> mismatching form list lengths: num listings=", len(formList), " num names=", len(formNames))
        print('\t', ex)


    #
    # Find strategies
    #
    sel = "body > div > div.DexBody > main.DexContent > div > section"

    articleContainer = pokePage.find(sel)[0].find("section")[2]
    article = articleContainer.find("div")[2]

    articleSoup = BeautifulSoup(articleContainer.html, 'html.parser')
    articleSoup = articleSoup.findAll("div")[2]

    children = [child for child in articleSoup.children]
    childrenText = [child.text for child in children]

    strategies = children[3 : len(children)-3]
    stratListings = [makeStrategyListing(strat, formListings) for strat in strategies]

    counters = [counter.text for counter in children[len(children)-3].findAll("strong")]

    credits = [credit.text for credit in children[len(children)-1].findAll("li")]

    #
    # Stick all the information together in an envelope
    #
    pokeListing = {"name":               pokemon,
                   "forms":              formListings,
                   "overview":           children[2].text,
                   "strategies' format": format,
                   "strategies":         stratListings,
                   "counters":           counters,
                   "credits":            credits
                   }

    return pokeListing

print("-> Starting up...")

session = HTMLSession()
printer = pprint.PrettyPrinter(indent=4, width=120)
failedPokemon = {}

previousSuccesses = {item[:-5] for item in os.listdir("pokemonListings/")}
pokeList = pokeList - previousSuccesses
printer.pprint(pokeList)

print("-> Scrapecrawling...")

for pokemon in pokeList:
    try:
        pokeListing = makePokeListing(session)

        # printer.pprint(pokeListing)
        pokejson = json.dumps(pokeListing)
        f = open("pokemonListings/"+pokemon+".json", "w")
        f.write(pokejson)
        f.close()
        print("COMPLETE: ", pokemon)
    except Exception as ex:
        print("FAILURE:  ", pokemon)
        print("\t", ex)
        session = HTMLSession()
        failedPokemon.update({pokemon: ex})

printer.pprint(failedPokemon)
errorsjson = json.dumps(failedPokemon)
ef = open("runtimeErrors.json", "w")
ef.write(errorsjson)
ef.close()






