
import pprint
import os
import json

printer = pprint.PrettyPrinter(indent=4, width=120)
failedPokemon = {}

files = os.listdir("pokemonListings/")

for file in files:
    try:
        f = open("pokemonListings/" + file, 'r')
        data = f.read()
        f.close()
        data = json.loads(data)

        f = open("pokemonListings/" + file, 'w')
        # pprint.pprint(data, stream=f, indent=4, width=120)
        json.dump(data, f, indent=4)
        f.close()
    except Exception as ex:
        print(ex)
        print("-> ", file)
