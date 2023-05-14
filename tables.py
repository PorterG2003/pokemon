# tables.py
abilities = '''
CREATE TABLE IF NOT EXISTS abilities (
    pokedex_number INTEGER,
    name TEXT NOT NULL,
    description TEXT,
    generation INTEGER,
    FOREIGN KEY (pokedex_number) REFERENCES type_effectiveness (pokedex_number),
    FOREIGN KEY (pokedex_number) REFERENCES types (pokedex_number),
    FOREIGN KEY (pokedex_number) REFERENCES stats (pokedex_number),
    FOREIGN KEY (pokedex_number) REFERENCES images (pokedex_number),
    FOREIGN KEY (pokedex_number) REFERENCES pokemon (pokedex_number)
);
'''

type_effectiveness = '''
CREATE TABLE IF NOT EXISTS type_effectiveness (
    pokedex_number INTEGER,
    against_type TEXT,
    effectiveness REAL,
    FOREIGN KEY (pokedex_number) REFERENCES abilities (pokedex_number),
    FOREIGN KEY (pokedex_number) REFERENCES types (pokedex_number),
    FOREIGN KEY (pokedex_number) REFERENCES stats (pokedex_number),
    FOREIGN KEY (pokedex_number) REFERENCES images (pokedex_number),
    FOREIGN KEY (pokedex_number) REFERENCES pokemon (pokedex_number)
);
'''

types = '''
CREATE TABLE IF NOT EXISTS types (
    pokedex_number INTEGER PRIMARY KEY AUTOINCREMENT,
    type1 TEXT NOT NULL,
    type2 TEXT,
    FOREIGN KEY (pokedex_number) REFERENCES type_effectiveness (pokedex_number),
    FOREIGN KEY (pokedex_number) REFERENCES abilities (pokedex_number),
    FOREIGN KEY (pokedex_number) REFERENCES stats (pokedex_number),
    FOREIGN KEY (pokedex_number) REFERENCES images (pokedex_number),
    FOREIGN KEY (pokedex_number) REFERENCES pokemon (pokedex_number)
);
'''

stats = '''
CREATE TABLE IF NOT EXISTS stats (
    pokedex_number INTEGER PRIMARY KEY,
    base_total INTEGER,
    hp INTEGER,
    attack INTEGER,
    defense INTEGER,
    sp_attack INTEGER,
    sp_defense INTEGER,
    speed INTEGER,
    FOREIGN KEY (pokedex_number) REFERENCES type_effectiveness (pokedex_number),
    FOREIGN KEY (pokedex_number) REFERENCES types (pokedex_number),
    FOREIGN KEY (pokedex_number) REFERENCES abilities (pokedex_number),
    FOREIGN KEY (pokedex_number) REFERENCES images (pokedex_number),
    FOREIGN KEY (pokedex_number) REFERENCES pokemon (pokedex_number)
);
'''

images = '''
CREATE TABLE IF NOT EXISTS images (
    pokedex_number INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    data BLOB NOT NULL,
    FOREIGN KEY (pokedex_number) REFERENCES type_effectiveness (pokedex_number),
    FOREIGN KEY (pokedex_number) REFERENCES types (pokedex_number),
    FOREIGN KEY (pokedex_number) REFERENCES stats (pokedex_number),
    FOREIGN KEY (pokedex_number) REFERENCES abilities (pokedex_number),
    FOREIGN KEY (pokedex_number) REFERENCES pokemon (pokedex_number)
);
'''

pokemon = '''
CREATE TABLE IF NOT EXISTS pokemon (
    pokedex_number INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    base_egg_steps INTEGER,
    base_happiness INTEGER,
    capture_rate INTEGER,
    classification TEXT,
    experience_growth INTEGER,
    height_m REAL,
    weight_kg REAL,
    generation INTEGER,
    is_legendary TEXT,
    FOREIGN KEY (pokedex_number) REFERENCES type_effectiveness (pokedex_number),
    FOREIGN KEY (pokedex_number) REFERENCES types (pokedex_number),
    FOREIGN KEY (pokedex_number) REFERENCES stats (pokedex_number),
    FOREIGN KEY (pokedex_number) REFERENCES images (pokedex_number),
    FOREIGN KEY (pokedex_number) REFERENCES abilities (pokedex_number)
);
'''