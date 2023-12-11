import sqlite3
import io
import os
import database_handler as dbh
import tkinter as tk
from PIL import Image, ImageDraw, ImageSequence, ImageTk, ImageFont

# ... (rest of the PokemonDB class code)

import math

def create_animation(pokemon_name_1, pokemon_name_2, winner_name):
    db = dbh.PokemonDB()
    image_data_1 = db.get_image_by_name(pokemon_name_1)
    image_data_2 = db.get_image_by_name(pokemon_name_2)

    if not image_data_1 or not image_data_2:
        print("One or both Pokemon images were not found.")
        return

    background = Image.open("background.jpg").resize((300, 200))
    pokemon_1 = Image.open(io.BytesIO(image_data_1)).convert("RGBA")
    pokemon_1 = pokemon_1.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)
    pokemon_2 = Image.open(io.BytesIO(image_data_2)).convert("RGBA")
    crown = Image.open("crown.jpg").convert("RGBA")

    num_frames = 40
    frames = []

    for i in range(num_frames):
        new_frame = Image.new("RGBA", (300, 200), (255, 255, 255, 255))
        new_frame.paste(background, (0, 0))

        t = i / (num_frames - 1)
        if i < num_frames / 4:
            t *= 4
        elif i < num_frames / 2:
            t = 2 - 4 * t
        elif i < 3 * num_frames / 4:
            t = 4 * t - 2
        else:
            t = 4 - 4 * t

        offset_x_1 = 30 + int(70 * t)
        offset_y_1 = 65 - int(50 * (t - t**2))
        offset_x_2 = 170 - int(70 * t)
        offset_y_2 = 65 - int(50 * (t - t**2))

        new_frame.paste(pokemon_1, (offset_x_1, offset_y_1), pokemon_1)
        new_frame.paste(pokemon_2, (offset_x_2, offset_y_2), pokemon_2)

        if i == num_frames - 1:
            if winner_name == "DRAW":
                draw_text = "DRAW"
                draw_font = ImageFont.truetype("arial.ttf", 24)
                draw = ImageDraw.Draw(new_frame)
                text_width, text_height = draw.textsize(draw_text, font=draw_font)
                draw.text(((300 - text_width) / 2, 20), draw_text, (0, 0, 0), font=draw_font)
            else:
                winner_pokemon = pokemon_1 if winner_name == pokemon_name_1 else pokemon_2
                crown_resized = crown.resize((int(winner_pokemon.width * 0.6), int(winner_pokemon.height * 0.6)), Image.Resampling.LANCZOS)
                crown_offset_x = offset_x_1 + int(0.2 * winner_pokemon.width) if winner_name == pokemon_name_1 else offset_x_2 + int(0.2 * winner_pokemon.width)
                crown_offset_y = 30 + offset_y_1 - int(0.6 * winner_pokemon.height) if winner_name == pokemon_name_1 else offset_y_2 - int(0.6 * winner_pokemon.height)
                new_frame.paste(crown_resized, (crown_offset_x, crown_offset_y), crown_resized)

        frames.append(new_frame)

    # Add last frame for 40 additional frames
    frames += [frames[-1]] * 40

    output_file = f"{pokemon_name_1}_vs_{pokemon_name_2}_animation.gif"
    frames[0].save(
        output_file,
        save_all=True,
        append_images=frames[1:],
        duration=200,
        loop=0,
    )
    print(f"Animation saved as {output_file}")
    return output_file

def display_gif(gif_path):
    root = tk.Tk()
    root.title("Pokemon Battle Animation")

    frames = []
    with Image.open(gif_path) as im:
        for frame in ImageSequence.Iterator(im):
            frames.append(ImageTk.PhotoImage(frame))

    label = tk.Label(root)
    label.pack()

    def update_gif(idx=0):
        frame = frames[idx]
        idx = (idx + 1) % len(frames)
        label.config(image=frame)
        root.after(200, update_gif, idx)

    update_gif()
    root.mainloop()


if __name__ == "__main__":
    pokemon_name_1 = input("Enter the first Pokemon name: ")
    pokemon_name_2 = input("Enter the second Pokemon name: ")
    winner_name = input("Enter the winner Pokemon name: ")
    display_gif(create_animation(pokemon_name_1, pokemon_name_2, winner_name))
