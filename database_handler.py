import sqlite3
import time

import tables  # Assuming the new schema is stored in the 'tables' module
import battle

class PokemonDB:
    def __init__(self):
        self.connection = sqlite3.connect("pokemon.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA foreign_keys = 1;")

        self.team = []

        # Create tables if they don't exist
        self.cursor.execute(tables.abilities)
        self.cursor.execute(tables.type_effectiveness)
        self.cursor.execute(tables.types)
        self.cursor.execute(tables.stats)
        self.cursor.execute(tables.images)
        self.cursor.execute(tables.pokemon)

    # --------- BASICS -----------

    def insert_pokemon(self, pokemon_data):
        self.cursor.execute(
            "INSERT INTO pokemon (pokedex_number, name, base_egg_steps, base_happiness, capture_rate, "
            "classification, experience_growth, height_m, weight_kg, generation, is_legendary) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", pokemon_data)

        self.connection.commit()

    def insert_type(self, type_data):
        self.cursor.execute(
            "INSERT INTO types (pokedex_number, type1, type2) VALUES (?, ?, ?)", type_data)

        self.connection.commit()

    def insert_ability(self, ability_data):
        self.cursor.execute(
            "INSERT INTO abilities (pokedex_number, name, description, generation) VALUES (?, ?, ?, ?)",
            ability_data)

        self.connection.commit()

    def insert_ability_effectiveness(self, ability_effectiveness_data):
        self.cursor.execute(
            "INSERT INTO abilities_effectiveness (pokedex_number, against_type, effectiveness) VALUES (?, ?, ?)",
            ability_effectiveness_data)

        self.connection.commit()

    def insert_stat(self, stat_data):
        self.cursor.execute(
            "INSERT INTO stats (pokedex_number, base_total, hp, attack, defense, sp_attack, sp_defense, speed) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", stat_data)

        self.connection.commit()

    def insert_image(self, image_data):
        self.cursor.execute(
            "INSERT INTO images (pokedex_number, name, data) VALUES (?, ?, ?)", image_data)

        self.connection.commit()

    def get_pokemon_by_name(self, name):
        self.cursor.execute("SELECT * FROM pokemon WHERE name = ?", (name,))
        return self.cursor.fetchone()

    def get_pokemon_by_pokedex_number(self, pokedex_number):
        self.cursor.execute("SELECT * FROM pokemon WHERE pokedex_number = ?", (pokedex_number,))
        return self.cursor.fetchone()

    def get_pokemon_by_generation(self, generation):
        self.cursor.execute("SELECT * FROM pokemon WHERE generation = ?", (generation,))
        return self.cursor.fetchall()

    def get_pokemon_by_type(self, type_name):
        self.cursor.execute("SELECT * FROM types WHERE type1 = ? OR type2 = ?", (type_name, type_name))
        return self.cursor.fetchall()

    def get_pokemon_by_ability(self, ability_name):
        self.cursor.execute("SELECT * FROM abilities WHERE name = ?", (ability_name,))
        return self.cursor.fetchall()

    def drop_all(self):
        table_names = ["abilities", "abilities_effectiveness", "types", "stats", "images", "pokemon"]
        for table_name in reversed(table_names):
            query = "DROP TABLE IF EXISTS " + table_name + ";"
            self.cursor.execute(query)

        self.connection.commit()

    def pokemon_exists(self, name):
        query = "SELECT COUNT(*) FROM pokemon WHERE name = ?"
        self.cursor.execute(query, (name,))
        count = self.cursor.fetchone()[0]
        return count > 0

    def get_random_pokemon_name(self):
        query = "SELECT name FROM pokemon ORDER BY RANDOM() LIMIT 1"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def get_all_types(self):
        self.cursor.execute("SELECT DISTINCT type1 FROM types UNION SELECT DISTINCT type2 FROM types WHERE type2 IS NOT NULL")
        types = [row[0] for row in self.cursor.fetchall()]
        return types


    # ---------- BATTLE ------------

    def get_image_by_name(self, name):
        self.cursor.execute("SELECT data FROM images WHERE name = ?", (name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def battle(self, name1, name2):
        self.cursor.execute("SELECT stats.base_total FROM stats JOIN pokemon ON stats.pokedex_number = pokemon.pokedex_number WHERE pokemon.name = ?", (name1,))
        hp1 = self.cursor.fetchone()
        self.cursor.execute("SELECT stats.base_total FROM stats JOIN pokemon ON stats.pokedex_number = pokemon.pokedex_number WHERE pokemon.name = ?", (name2,))
        hp2 = self.cursor.fetchone()
        filename = ""
        if hp1 and hp2:
            if hp1 > hp2:
                filename = battle.create_animation(name1, name2, name1)
            elif hp2 < hp1:
                filename = battle.create_animation(name1, name2, name1)
            else:
                filename = battle.create_animation(name1, name2, "")
            battle.display_gif(filename)
        else:
            print("One or both pokemon were not found")

        

    # ------------ TEAM -------------

    def add_to_team(self, name):
        if not self.pokemon_exists(name):
            print("Pokemon is not in the database! Are you sure you typed it correctly?")
            return
        if len(self.team) >= 6:
            print("Team is full! Please remove a pokemon and try again!")
            return
        self.team.append(name)
        print(f"Added {name} successfully")
        
    def remove_from_team(self, name):
        if not name in self.team:
            print("Pokemon is not in the team! Are you sure you typed it correctly?")
            print(f"Current team is: {self.team}")
            return 
        self.team.remove(name)
        print(f"Removed {name} successfully")
        
    def fill_team(self):
        count = 0
        while len(self.team) < 6:
            count += 1
            self.team.append(self.get_random_pokemon_name())
        print(f"Filled the team with {count} pokemon.")
        print(f"New team: {self.team}")

    def clear_team(self):
        self.team = []
        print(f"Reset team to empty!")

    def team_stats(self):
        if not self.team:
            print("Your team is empty!")
            return

        headers = ['Name', 'Type', 'HP', 'Attack', 'Defense', 'Sp. Attack', 'Sp. Defense', 'Speed', 'Total']
        print("{:<15} {:<15} {:<5} {:<7} {:<7} {:<10} {:<10} {:<5} {:<5}".format(*headers))

        total_team_stats = [0, 0, 0, 0, 0, 0]

        for name in self.team:
            self.cursor.execute("SELECT * FROM stats JOIN pokemon ON stats.pokedex_number = pokemon.pokedex_number WHERE pokemon.name = ?", (name,))
            stats = self.cursor.fetchone()

            self.cursor.execute("SELECT type1, type2 FROM types WHERE pokedex_number = ?", (stats[0],))
            type1, type2 = self.cursor.fetchone()
            type_str = type1 + (f", {type2}" if type2 else "")

            stat_values = stats[3:]
            print("{:<15} {:<15} {:<5} {:<7} {:<7} {:<10} {:<10} {:<5}".format(name, type_str, *stat_values))

            for i in range(len(total_team_stats)):
                total_team_stats[i] += stat_values[i]

        print("-" * 75)
        print("{:<15} {:<15} {:<5} {:<7} {:<7} {:<10} {:<10} {:<5}".format("Total", "", *total_team_stats))

    def top_pokemon_by_stat(self):
        stats_list = ["hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]
        query_template = "SELECT pokemon.name, max({stat}) FROM stats JOIN pokemon ON stats.pokedex_number = pokemon.pokedex_number"
        
        # Print the header
        print("{:<12} {:<12} {:<12}".format("Stat", "Pokemon", "Value"))
        print("-" * 36)

        for stat in stats_list:
            query = query_template.format(stat=stat.lower())
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            
            # Print the formatted row
            print("{:<12} {:<12} {:<12}".format(stat, result[0], result[1]))

    # ----------- Other -----------
    def average_stats_by_type(self):
        types = self.get_all_types()

        headers = ['Type', 'Avg HP', 'Avg Attack', 'Avg Defense', 'Avg Sp. Attack', 'Avg Sp. Defense', 'Avg Speed', 'Avg Total']
        print("{:<15} {:<9} {:<11} {:<11} {:<13} {:<13} {:<9} {:<9}".format(*headers))

        for type_name in types:
            self.cursor.execute("""
                SELECT AVG(stats.hp), AVG(stats.attack), AVG(stats.defense), AVG(stats.sp_attack), AVG(stats.sp_defense), AVG(stats.speed), AVG(stats.base_total)
                FROM types
                INNER JOIN stats ON types.pokedex_number = stats.pokedex_number
                WHERE types.type1 = ? OR types.type2 = ?
            """, (type_name, type_name))

            average_stats = self.cursor.fetchone()
            average_stats = [round(avg, 2) for avg in average_stats]

            print("{:<15} {:<9} {:<11} {:<11} {:<13} {:<13} {:<9} {:<9}".format(type_name, *average_stats))

    def most_specialized_pokemon_by_stat(self):
        stats_list = ["HP", "Attack", "Defense", "Sp_attack", "Sp_defense", "Speed"]
        query_template = """
        SELECT
            pokemon.name,
            stats.{stat},
            (
                stats.hp - stats.{stat} +
                stats.attack - stats.{stat} +
                stats.defense - stats.{stat} +
                stats.sp_attack - stats.{stat} +
                stats.sp_defense - stats.{stat} +
                stats.speed - stats.{stat}
            ) / 5.0 AS avg_difference
        FROM
            stats
        JOIN pokemon ON stats.pokedex_number = pokemon.pokedex_number
        ORDER BY
            avg_difference ASC
        LIMIT 1;
        """

        # Print the header
        print("{:<12} {:<12} {:<12} {:<12}".format("Stat", "Pokemon", "Value", "Avg Difference"))
        print("-" * 48)

        for stat in stats_list:
            query = query_template.format(stat=stat.lower())
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            
            # Print the formatted row
            print("{:<12} {:<12} {:<12} {:<12.2f}".format(stat, result[0], result[1], abs(result[2])))


