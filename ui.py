import database_handler

db = database_handler.PokemonDB()

def menu():
    print("team) show team stats")
    print("type) show average stats by type")
    print("battle) simulate a battle between two Pokémon")
    print("add) add a pokemon to your team")
    print("remove) remove a pokemon from your team")
    print("fill) fill the rest of your team with random pokemon")
    print("top pokemon) displays top pokemon by stat")
    print("most specialized) displays the most specialized pokemon for each stat")
    print("clear) empty your team")
    print("quit) quit Pokémon App")

def team_stats():
    db.team_stats()

def average_stats_by_type():
    db.average_stats_by_type()

def battle():
    name1 = input("Enter the name of the first Pokémon: ")
    name1 = name1.capitalize()
    name2 = input("Enter the name of the second Pokémon: ")
    name2 = name2.capitalize()
    db.battle(name1, name2)

quit = False
print("\nWELCOME TO POKÉMON APP\n\n")
menu()

while not quit:
    choice = input("\n\nchoice: ")
    if choice == "team":
        team_stats()
    elif choice == "type":
        average_stats_by_type()
    elif choice == "battle":
        battle()
    elif choice == "add":
        pokemon = input("Which pokemon do you want to add? ")
        pokemon = pokemon.capitalize()
        db.add_to_team(pokemon)
    elif choice == "remove":
        pokemon = input("Which pokemon would you like to remove? ")
        pokemon = pokemon.capitalize()
        db.remove_from_team(pokemon)
    elif choice == "fill":
        db.fill_team()
    elif choice == "most specialized":
        db.most_specialized_pokemon_by_stat()
    elif choice == "clear":
        db.clear_team()
    elif choice == "top pokemon":
        db.top_pokemon_by_stat()
    elif choice == "menu":
        menu()
    elif choice == "quit":
        quit = True
    else:
        print("### Enter a valid choice ###\n")
