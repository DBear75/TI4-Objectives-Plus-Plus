import argparse
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
import textwrap
import numpy as np
import sys

parser = argparse.ArgumentParser(description='Generates objective cards for O++ project.')

parser.add_argument(
	"--input-file",
	type=str,
	help="The csv file that will be used to generate the objectives.",
	default=None
)

parser.add_argument(
    "--objective-type",
    type=str,
    help="The type of objective.",
    default=None
)

parser.add_argument("--tts-mode", action='store_true', default=False)

args = parser.parse_args()

if args.objective_type is None:
    sys.exit("No objective type provided.")

if args.input_file is None:
    args.input_file = args.objective_type+".csv"

# Read the input CSV file
data = pd.read_csv(args.input_file)

# Check if the objective_type folder exists
if not os.path.exists("generatedImages"):
    # Create the objective_type folder
    os.makedirs("generatedImages")

# Check if the objective_type folder exists
if not os.path.exists("generatedImages/"+args.objective_type):
    # Create the objective_type folder
    os.makedirs("generatedImages/"+args.objective_type)




background_image = Image.open(f"backgrounds/{args.objective_type}.png")
z = pd.Index(data).size
if not args.tts_mode:
    x_deck = int(np.ceil(np.sqrt(z*background_image.height / background_image.width )))
else:
    x_deck = 10


y_deck = int(np.ceil(z/x_deck))
deck = Image.new('RGB', (x_deck*background_image.width, y_deck*background_image.height))

# Iterate over each row in the CSV
for index, row in data.iterrows():
    # Get the name and objective from the current row
    if "stageless" == args.objective_type:
        name = row['Stage 1 Name']
        objective = row['Stage 1 Objective']
        objective2 = row['Stage 2 Objective']
    elif "stageless_secret" == args.objective_type:
        name = row['name']
        objective = row['objective']
        objective2 = row['objective2']
        phase2 = row['Phase2']
        if phase2.lower() == "action":
            color2 = (246, 11, 4)
        elif phase2.lower() == "agenda":
            color2 = (96, 96, 254)
        else:
            color2 = (255, 255, 255)
    else:
        name = row['name']
        objective = row['objective']
    
    phase = row['Phase']
    
    # Open the background image
    name_gradient = Image.open(f"gradients/{args.objective_type}.png")
    
    alpha = Image.new('L', name_gradient.size)
    draw_alpha = ImageDraw.Draw(alpha)
    
    # Create a new image with the same size as the background
    new_image = Image.new('RGB', background_image.size)
    
    # Paste the background image onto the new image
    new_image.paste(background_image, (0, 0))
    
    # Create a new image draw object
    draw = ImageDraw.Draw(new_image)
    if "stageless" in args.objective_type:
        font_size = 68
    else:
        font_size = 92
    # Set the font and font size for the text
    font = ImageFont.truetype("SliderTI-_.otf", font_size)
    temp_name = name.upper()
    # Calculate the width and height of the text
    _, _, text_width, text_height = draw.textbbox((0, 0), temp_name, font=font)

    name_wrap_width = 16

    wrapped = textwrap.wrap(name, width=name_wrap_width)
    # Draw the objective text on the image
    for i, line in enumerate(wrapped):
        _, _, text_width, text_height = draw.textbbox((0, 0), line.upper(), font=font)
    
        # Calculate the x and y coordinates to center the objective text at the bottom of the image
        text_x = (name_gradient.width - text_width) // 2
        if "stageless" in args.objective_type:
            text_y = name_gradient.height // 2
        else:
            text_y = name_gradient.height // 8
        draw_alpha.text(
            (text_x, text_y + ((i-len(wrapped)/2)*font_size)),
            line.upper(),
            font=font,
            fill='white'
        )

    name_gradient.putalpha(alpha)
    new_image.paste(name_gradient, name_gradient)
    
    if phase.lower() == "action":
        color = (246, 11, 4)
    elif phase.lower() == "agenda":
        color = (96, 96, 254)
    else:
        color = (255, 255, 255)

    if "stageless" in args.objective_type:
        font3_size = 48
        font3 = ImageFont.truetype("SliderTI-_.otf", font3_size)
        _, _, text_width, text_height = draw.textbbox((0, 0), phase.upper()+" PHASE", font=font3)
        text_x = (new_image.width - text_width) // 2
        text_y = new_image.height // 2 - 28

        phase_offset = 150

        # Upper Phase
        draw.text(
            (text_x, text_y - phase_offset),
            phase.upper()+" PHASE",
            font=font3,
            fill=color
        )

        if "stageless_secret" == args.objective_type:
            # Lower Phase
            draw.text(
                (text_x, text_y + phase_offset),
                phase2.upper()+" PHASE",
                font=font3,
                fill=color2
            )
        else:
            # Lower Phase
            draw.text(
                (text_x, text_y + phase_offset),
                phase.upper()+" PHASE",
                font=font3,
                fill=color
            )
    else:
        font3_size=72
        font3 = ImageFont.truetype("SliderTI-_.otf", font3_size)
        _, _, text_width, text_height = draw.textbbox((0, 0), phase.upper()+" PHASE", font=font3)
        text_x = (new_image.width - text_width) // 2
        text_y = new_image.height // 2 + 10

    if "stageless" in args.objective_type:

        font2_size = 60
        font2 = ImageFont.truetype("MYRIADPRO-SEMIBOLD.OTF", font2_size)
        temp_obj = ""
        wrap_width = 28

        pad = 10
        wrapped = textwrap.wrap(objective, width=wrap_width)
        # Draw the objective text on the image
        for i, line in enumerate(wrapped):
            _, _, objective_width, objective_height = draw.textbbox((0, 0), line, font=font2)
        
            # Calculate the x and y coordinates to center the objective text at the bottom of the image
            objective_x = (background_image.width - objective_width) // 2
            objective_y = background_image.height // 4 + 30
            draw.text(
                (objective_x, objective_y + ((i-len(wrapped)//2)*font2_size)),
                line,
                font=font2,
                fill=(255, 255, 255)
            )


        wrapped2 = textwrap.wrap(objective2, width=wrap_width)
        for i, line in enumerate(wrapped2):
            _, _, objective_width, objective_height = draw.textbbox((0, 0), line, font=font2)
        
            # Calculate the x and y coordinates to center the objective text at the bottom of the image
            objective_x = (background_image.width - objective_width) // 2
            objective_y = 6 * background_image.height // 8 - 60
            draw.text(
                (objective_x, objective_y + ((i-len(wrapped2)//2)*font2_size)),
                line,
                font=font2,
                fill=(255, 255, 255)
            )
    else:
        font2_size = 84
        font2 = ImageFont.truetype("MYRIADPRO-SEMIBOLD.OTF", font2_size)
        temp_obj = ""
        wrap_width = 22

        pad = 10
        wrapped = textwrap.wrap(objective, width=wrap_width)
        # Draw the objective text on the image
        for i, line in enumerate(wrapped):
            _, _, objective_width, objective_height = draw.textbbox((0, 0), line, font=font2)
        
            # Calculate the x and y coordinates to center the objective text at the bottom of the image
            objective_x = (background_image.width - objective_width) // 2
            objective_y = background_image.height // 2
            draw.text(
                (objective_x, objective_y + ((i-len(wrapped)//2)*font2_size)),
                line,
                font=font2,
                fill=(255, 255, 255)
            )

    # Save the new image with the name as the filename
    new_image.save(f"generatedImages/{args.objective_type}/{name}.png")
    deck.paste(
        new_image,
        (background_image.width*(index%x_deck), background_image.height*(index//x_deck))
    )


# Check if the objective_type folder exists
if not os.path.exists("generatedImages/decks"):
    # Create the objective_type folder
    os.makedirs("generatedImages/decks")

deck = deck.resize((deck.width//2, deck.height//2))
deck.save(f"generatedImages/decks/{args.objective_type}.jpg")

