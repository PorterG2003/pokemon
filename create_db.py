import sqlite3
import tables
import os
import pandas as pd

# Read CSV files
abilities_df = pd.read_csv('raw/abilities.csv')
master_df = pd.read_csv('raw/master.csv')
pokemon_game_stats_df = pd.read_csv('raw/pokemon-game-stats.csv')

# Create a SQLite connection and cursor
conn = sqlite3.connect('pokemon.db')
cursor = conn.cursor()

# Create tables
table_creates = [tables.abilities, tables.type_effectiveness, tables.types, tables.stats, tables.images, tables.pokemon]

for table in table_creates:
    cursor.execute(table)

# Insert data into the abilities table
for index, row in abilities_df.iterrows():
    for master_index, master_row in master_df.iterrows():
        if row["Name"] in master_row["abilities"]:
            cursor.execute("INSERT INTO abilities (pokedex_number, name, description, generation) VALUES (?, ?, ?, ?)",
                        (master_row["pokedex_number"], row['Name'], row['Description'], row['Generation']))

# Insert data into the type_effectiveness table
for index, row in master_df.iterrows():
    for type in ["against_bug","against_dark","against_dragon","against_electric","against_fairy","against_fight","against_fire","against_flying","against_ghost","against_grass","against_ground","against_ice","against_normal","against_poison","against_psychic","against_rock","against_steel","against_water"]:
        cursor.execute("INSERT INTO type_effectiveness (pokedex_number, against_type, effectiveness) VALUES (?, ?, ?)",
                    (row['pokedex_number'], type, row[type]))
    cursor.execute("INSERT INTO pokemon (pokedex_number, name, base_egg_steps, base_happiness, capture_rate, classification, experience_growth, height_m, weight_kg, generation, is_legendary) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (row['pokedex_number'], row['name'], row['base_egg_steps'], row["base_happiness"], row["capture_rate"], row["classification"], row["experience_growth"], row["height_m"], row["weight_kg"], row['generation'], row['is_legendary']))

# Insert data into the types, stats, and pokemon tables
prev_num = 0
for index, row in pokemon_game_stats_df.iterrows():
    cur_num = row["#"]
    if prev_num != cur_num:
        prev_num = cur_num
        cursor.execute("INSERT INTO types (pokedex_number, type1, type2) VALUES (?, ?, ?)",
                    (row['#'], row['Type 1'], row['Type 2']))
        cursor.execute("INSERT INTO stats (pokedex_number, base_total, hp, attack, defense, sp_attack, sp_defense, speed) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (row['#'], row['Total'], row['HP'], row['Attack'], row['Defense'], row['Sp. Atk'], row['Sp. Def'], row['Speed']))

#Function to read image files and insert them into the 'images' table
def insert_images(cursor, images_dir, master_df):
    for index, row in master_df.iterrows():
        pokedex_number = row["pokedex_number"]
        name = row["name"]
        image_path = os.path.join(images_dir, f"{name}.png")
        
        if os.path.exists(image_path):
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                cursor.execute(
                    "INSERT INTO images (pokedex_number, name, data) VALUES (?, ?, ?)",
                    (pokedex_number, name, sqlite3.Binary(image_data)),
                )

# Load images into the 'images' table
images_directory = "./images"
insert_images(cursor, images_directory, master_df)


print("Data has been inserted into the tables.")

# Commit and close the connection
conn.commit()
conn.close()
