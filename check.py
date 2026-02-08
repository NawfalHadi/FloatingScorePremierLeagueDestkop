import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Data from the previous recommendation table
data = [
    # Head
    {"Submenu": "Head", "Layer": "Skeletal", "Option": "Skull", "Parameter": "Narrow <-> Widen", "Value": 7},
    {"Submenu": "Head", "Layer": "Skeletal", "Option": "Skull", "Parameter": "Down <-> Up", "Value": 6},
    {"Submenu": "Head", "Layer": "Skeletal", "Option": "Skull", "Parameter": "Neutral <-> Forward", "Value": 5},
    {"Submenu": "Head", "Layer": "Skeletal", "Option": "Skull", "Parameter": "Round <-> Angular", "Value": 2},
    {"Submenu": "Head", "Layer": "Skeletal", "Option": "Skull", "Parameter": "Shift Left <-> Shift Right", "Value": 5},
    {"Submenu": "Head", "Layer": "Skeletal", "Option": "Skull Crown", "Parameter": "Narrow <-> Widen", "Value": 6},
    {"Submenu": "Head", "Layer": "Skeletal", "Option": "Skull Crown", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Head", "Layer": "Skeletal", "Option": "Skull Crown", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Head", "Layer": "Skeletal", "Option": "Skull Back", "Parameter": "Narrow <-> Widen", "Value": 6},
    {"Submenu": "Head", "Layer": "Skeletal", "Option": "Skull Back", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Head", "Layer": "Skeletal", "Option": "Skull Back", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Head", "Layer": "Skeletal", "Option": "Skull Back", "Parameter": "Round <-> Angular", "Value": 2},
    {"Submenu": "Head", "Layer": "Skeletal", "Option": "Temples", "Parameter": "Narrow <-> Widen", "Value": 7},
    {"Submenu": "Head", "Layer": "Skeletal", "Option": "Temples", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Head", "Layer": "Skeletal", "Option": "Temples", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Head", "Layer": "Skeletal", "Option": "Temples", "Parameter": "Round <-> Angular", "Value": 2},
    {"Submenu": "Head", "Layer": "Flesh", "Option": "Temples", "Parameter": "Less <-> More", "Value": 7},

    # Forehead
    {"Submenu": "Forehead", "Layer": "Skeletal", "Option": "Upper Forehead", "Parameter": "Narrow <-> Widen", "Value": 6},
    {"Submenu": "Forehead", "Layer": "Skeletal", "Option": "Upper Forehead", "Parameter": "Up", "Value": 5},
    {"Submenu": "Forehead", "Layer": "Skeletal", "Option": "Upper Forehead", "Parameter": "Back <-> Forward", "Value": 4},
    {"Submenu": "Forehead", "Layer": "Skeletal", "Option": "Upper Forehead", "Parameter": "Round <-> Angular", "Value": 3},
    {"Submenu": "Forehead", "Layer": "Skeletal", "Option": "Upper Forehead", "Parameter": "Neutral", "Value": 5},
    {"Submenu": "Forehead", "Layer": "Skeletal", "Option": "Upper Forehead", "Parameter": "Shift Left <-> Shift Right", "Value": 5},
    {"Submenu": "Forehead", "Layer": "Skeletal", "Option": "Lower Forehead", "Parameter": "Narrow <-> Widen", "Value": 6},
    {"Submenu": "Forehead", "Layer": "Skeletal", "Option": "Lower Forehead", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Forehead", "Layer": "Skeletal", "Option": "Lower Forehead", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Forehead", "Layer": "Skeletal", "Option": "Lower Forehead", "Parameter": "Round <-> Angular", "Value": 3},
    {"Submenu": "Forehead", "Layer": "Fat", "Option": "Forehead Center", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Forehead", "Layer": "Fat", "Option": "Forehead Center", "Parameter": "Less <-> More", "Value": 7},
    {"Submenu": "Forehead", "Layer": "Fat", "Option": "Forehead Sides", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Forehead", "Layer": "Fat", "Option": "Forehead Sides", "Parameter": "Less <-> More", "Value": 7},

    # Brows
    {"Submenu": "Brows", "Layer": "Skeletal", "Option": "Eyebrows", "Parameter": "Narrow <-> Widen", "Value": 5},
    {"Submenu": "Brows", "Layer": "Skeletal", "Option": "Eyebrows", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Brows", "Layer": "Skeletal", "Option": "Eyebrows", "Parameter": "Back <-> Forward", "Value": 6},
    {"Submenu": "Brows", "Layer": "Skeletal", "Option": "Eyebrows", "Parameter": "Round <-> Angular", "Value": 3},
    {"Submenu": "Brows", "Layer": "Skeletal", "Option": "Eyebrows Center", "Parameter": "Narrow <-> Widen", "Value": 5},
    {"Submenu": "Brows", "Layer": "Skeletal", "Option": "Eyebrows Center", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Brows", "Layer": "Skeletal", "Option": "Eyebrows Center", "Parameter": "Back <-> Forward", "Value": 6},
    {"Submenu": "Brows", "Layer": "Skeletal", "Option": "Eyebrows Center", "Parameter": "Round <-> Angular", "Value": 3},
    {"Submenu": "Brows", "Layer": "Skeletal", "Option": "Eyebrows Center", "Parameter": "Shift Left <-> Shift Right", "Value": 5},
    {"Submenu": "Brows", "Layer": "Skeletal", "Option": "Eyebrows Outside Top", "Parameter": "Narrow <-> Widen", "Value": 5},
    {"Submenu": "Brows", "Layer": "Skeletal", "Option": "Eyebrows Outside Top", "Parameter": "Down <-> Up", "Value": 4},
    {"Submenu": "Brows", "Layer": "Skeletal", "Option": "Eyebrows Outside Top", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Brows", "Layer": "Skeletal", "Option": "Eyebrows Outside Top", "Parameter": "Round <-> Angular", "Value": 3},
    {"Submenu": "Brows", "Layer": "Flesh", "Option": "Eyebrows Center", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Brows", "Layer": "Flesh", "Option": "Eyebrows Center", "Parameter": "Less <-> More", "Value": 7},
    {"Submenu": "Brows", "Layer": "Flesh", "Option": "Eyebrow Gap", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Brows", "Layer": "Flesh", "Option": "Eyebrow Gap", "Parameter": "Less <-> More", "Value": 5},

    # Eyes
    {"Submenu": "Eyes", "Layer": "Skeletal", "Option": "Eyes", "Parameter": "Narrow <-> Widen", "Value": 5},
    {"Submenu": "Eyes", "Layer": "Skeletal", "Option": "Eyes", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Eyes", "Layer": "Skeletal", "Option": "Eyes", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Eyes", "Layer": "Skeletal", "Option": "Eyes", "Parameter": "Larger <-> Smaller", "Value": 4},
    {"Submenu": "Eyes", "Layer": "Skeletal", "Option": "Eye Sockets", "Parameter": "Narrow <-> Widen", "Value": 5},
    {"Submenu": "Eyes", "Layer": "Skeletal", "Option": "Eye Sockets", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Eyes", "Layer": "Skeletal", "Option": "Eye Sockets", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Eyes", "Layer": "Flesh", "Option": "Eyelid Fold Center", "Parameter": "Narrow <-> Widen", "Value": 5},
    {"Submenu": "Eyes", "Layer": "Flesh", "Option": "Eyelid Fold Center", "Parameter": "Up", "Value": 6},
    {"Submenu": "Eyes", "Layer": "Flesh", "Option": "Eyelid Fold Center", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Eyes", "Layer": "Flesh", "Option": "Eyelid Fold Center", "Parameter": "Larger <-> Smaller", "Value": 5},
    {"Submenu": "Eyes", "Layer": "Flesh", "Option": "Eyelid Fold Outer", "Parameter": "Down <-> Up", "Value": 4},
    {"Submenu": "Eyes", "Layer": "Flesh", "Option": "Eyelid Fold Outer", "Parameter": "Larger <-> Smaller", "Value": 5},
    {"Submenu": "Eyes", "Layer": "Flesh", "Option": "Eyelid Fold Inner", "Parameter": "Narrow <-> Widen", "Value": 5},
    {"Submenu": "Eyes", "Layer": "Flesh", "Option": "Eyelid Fold Inner", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Eyes", "Layer": "Fat", "Option": "Eyelid Upper", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Eyes", "Layer": "Fat", "Option": "Eyelid Upper", "Parameter": "Less <-> More", "Value": 6},
    {"Submenu": "Eyes", "Layer": "Fat", "Option": "Eyelid Lower", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Eyes", "Layer": "Fat", "Option": "Eyelid Lower", "Parameter": "Less <-> More", "Value": 7},
    {"Submenu": "Eyes", "Layer": "Fat", "Option": "Under-Eye Lower", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Eyes", "Layer": "Fat", "Option": "Under-Eye Lower", "Parameter": "Less <-> More", "Value": 8},

    # Ears
    {"Submenu": "Ears", "Layer": "Skeletal", "Option": "Ears", "Parameter": "Narrow <-> Widen", "Value": 5},
    {"Submenu": "Ears", "Layer": "Skeletal", "Option": "Ears", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Ears", "Layer": "Skeletal", "Option": "Ears", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Ears", "Layer": "Skeletal", "Option": "Ears", "Parameter": "Larger <-> Smaller", "Value": 5},
    {"Submenu": "Ears", "Layer": "Skeletal", "Option": "Ears", "Parameter": "Shift Left <-> Shift Right", "Value": 5},
    {"Submenu": "Ears", "Layer": "Flesh", "Option": "Ear Outside Top", "Parameter": "Narrow <-> Widen", "Value": 5},
    {"Submenu": "Ears", "Layer": "Flesh", "Option": "Ear Outside Top", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Ears", "Layer": "Flesh", "Option": "Ear Outside Top", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Ears", "Layer": "Flesh", "Option": "Ear Outside Middle", "Parameter": "Narrow <-> Widen", "Value": 5},
    {"Submenu": "Ears", "Layer": "Flesh", "Option": "Ear Outside Middle", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Ears", "Layer": "Flesh", "Option": "Ear Outside Middle", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Ears", "Layer": "Flesh", "Option": "Ear Outside Bottom", "Parameter": "Narrow <-> Widen", "Value": 6},
    {"Submenu": "Ears", "Layer": "Flesh", "Option": "Ear Outside Bottom", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Ears", "Layer": "Flesh", "Option": "Ear Outside Bottom", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Ears", "Layer": "Flesh", "Option": "Ear Inside Top", "Parameter": "Narrow <-> Widen", "Value": 5},
    {"Submenu": "Ears", "Layer": "Flesh", "Option": "Ear Inside Top", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Ears", "Layer": "Flesh", "Option": "Ear Inside Top", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Ears", "Layer": "Flesh", "Option": "Ear Inside Bottom", "Parameter": "Narrow <-> Widen", "Value": 5},
    {"Submenu": "Ears", "Layer": "Flesh", "Option": "Ear Inside Bottom", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Ears", "Layer": "Flesh", "Option": "Ear Inside Bottom", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Ears", "Layer": "Flesh", "Option": "Earlobe", "Parameter": "Narrow <-> Widen", "Value": 6},
    {"Submenu": "Ears", "Layer": "Flesh", "Option": "Earlobe", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Ears", "Layer": "Flesh", "Option": "Earlobe", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Ears", "Layer": "Flesh", "Option": "Ear Tragus", "Parameter": "Narrow <-> Widen", "Value": 5},
    {"Submenu": "Ears", "Layer": "Flesh", "Option": "Ear Tragus", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Ears", "Layer": "Flesh", "Option": "Ear Tragus", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Ears", "Layer": "Fat", "Option": "Ear Outside Top", "Parameter": "Less <-> More", "Value": 5},
    {"Submenu": "Ears", "Layer": "Fat", "Option": "Ear Outside Bottom", "Parameter": "Less <-> More", "Value": 6},

    # Nose
    {"Submenu": "Nose", "Layer": "Skeletal", "Option": "Nose", "Parameter": "Narrow <-> Widen", "Value": 7},
    {"Submenu": "Nose", "Layer": "Skeletal", "Option": "Nose", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Nose", "Layer": "Skeletal", "Option": "Nose", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Nose", "Layer": "Skeletal", "Option": "Nose", "Parameter": "Round <-> Angular", "Value": 2},
    {"Submenu": "Nose", "Layer": "Skeletal", "Option": "Nose", "Parameter": "Shift Left <-> Shift Right", "Value": 5},
    {"Submenu": "Nose", "Layer": "Skeletal", "Option": "Nose Bridge Sides", "Parameter": "Narrow <-> Widen", "Value": 7},
    {"Submenu": "Nose", "Layer": "Skeletal", "Option": "Nose Bridge Sides", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Nose", "Layer": "Skeletal", "Option": "Nose Bridge Sides", "Parameter": "Back <-> Forward", "Value": 4},
    {"Submenu": "Nose", "Layer": "Skeletal", "Option": "Nose Bridge Sides", "Parameter": "Round <-> Angular", "Value": 2},
    {"Submenu": "Nose", "Layer": "Skeletal", "Option": "Nose Bridge Center", "Parameter": "Narrow <-> Widen", "Value": 6},
    {"Submenu": "Nose", "Layer": "Skeletal", "Option": "Nose Bridge Center", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Nose", "Layer": "Skeletal", "Option": "Nose Bridge Center", "Parameter": "Back <-> Forward", "Value": 4},
    {"Submenu": "Nose", "Layer": "Skeletal", "Option": "Nose Bridge Center", "Parameter": "Round <-> Angular", "Value": 2},
    {"Submenu": "Nose", "Layer": "Skeletal", "Option": "Nose Bridge Center", "Parameter": "Shift Left <-> Shift Right", "Value": 5},
    {"Submenu": "Nose", "Layer": "Skeletal", "Option": "Nose Bridge Upper", "Parameter": "Narrow <-> Widen", "Value": 6},
    {"Submenu": "Nose", "Layer": "Skeletal", "Option": "Nose Bridge Upper", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Nose", "Layer": "Skeletal", "Option": "Nose Bridge Upper", "Parameter": "Back <-> Forward", "Value": 4},
    {"Submenu": "Nose", "Layer": "Skeletal", "Option": "Nose Bridge Upper", "Parameter": "Round <-> Angular", "Value": 2},
    {"Submenu": "Nose", "Layer": "Skeletal", "Option": "Nose Bridge Upper", "Parameter": "Shift Left <-> Shift Right", "Value": 5},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nostril Upper", "Parameter": "Narrow <-> Widen", "Value": 6},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nostril Upper", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nostril Upper", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nostril Upper Outer", "Parameter": "Narrow <-> Widen", "Value": 7},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nostril Upper Outer", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nostril Upper Outer", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nostril Upper Center", "Parameter": "Narrow <-> Widen", "Value": 5},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nostril Upper Center", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nostril Upper Center", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nostril Lower", "Parameter": "Narrow <-> Widen", "Value": 7},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nostril Lower", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nostril Lower", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nostril Lower", "Parameter": "Round <-> Angular", "Value": 2},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nostril Outside Outer", "Parameter": "Narrow <-> Widen", "Value": 7},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nostril Outside Outer", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nostril Outside Outer", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nostril Outside Outer", "Parameter": "Round <-> Angular", "Value": 2},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nostril Outside Center", "Parameter": "Narrow <-> Widen", "Value": 7},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nostril Outside Center", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nostril Outside Center", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nose Tip Upper", "Parameter": "Narrow <-> Widen", "Value": 8},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nose Tip Upper", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nose Tip Upper", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nose Tip Upper", "Parameter": "Round <-> Angular", "Value": 1},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nose Tip Upper", "Parameter": "Shift Left <-> Shift Right", "Value": 5},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nose Tip Under", "Parameter": "Narrow <-> Widen", "Value": 8},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nose Tip Under", "Parameter": "Down <-> Up", "Value": 4},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nose Tip Under", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nose Tip Under", "Parameter": "Round <-> Angular", "Value": 1},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nose Tip Under", "Parameter": "Shift Left <-> Shift Right", "Value": 5},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nose Tip Lower", "Parameter": "Narrow <-> Widen", "Value": 8},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nose Tip Lower", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nose Tip Lower", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nose Tip Lower", "Parameter": "Round <-> Angular", "Value": 1},
    {"Submenu": "Nose", "Layer": "Flesh", "Option": "Nose Tip Lower", "Parameter": "Shift Left <-> Shift Right", "Value": 5},
    {"Submenu": "Nose", "Layer": "Fat", "Option": "Nose", "Parameter": "Less <-> More", "Value": 8},

    # Cheeks
    {"Submenu": "Cheeks", "Layer": "Skeletal", "Option": "Cheeks", "Parameter": "Narrow <-> Widen", "Value": 8},
    {"Submenu": "Cheeks", "Layer": "Skeletal", "Option": "Cheeks", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Cheeks", "Layer": "Skeletal", "Option": "Cheeks", "Parameter": "Back <-> Forward", "Value": 6},
    {"Submenu": "Cheeks", "Layer": "Skeletal", "Option": "Cheeks", "Parameter": "Round <-> Angular", "Value": 2},
    {"Submenu": "Cheeks", "Layer": "Flesh", "Option": "Cheeks", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Cheeks", "Layer": "Flesh", "Option": "Cheeks", "Parameter": "Less <-> More", "Value": 9},
    {"Submenu": "Cheeks", "Layer": "Flesh", "Option": "Upper Outside Cheeks", "Parameter": "Less <-> More", "Value": 8},
    {"Submenu": "Cheeks", "Layer": "Flesh", "Option": "Upper Inside Eyes", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Cheeks", "Layer": "Flesh", "Option": "Upper Inside Eyes", "Parameter": "Less <-> More", "Value": 7},
    {"Submenu": "Cheeks", "Layer": "Flesh", "Option": "Upper Inside Cheeks", "Parameter": "Less <-> More", "Value": 8},
    {"Submenu": "Cheeks", "Layer": "Flesh", "Option": "Lower Outside Cheeks", "Parameter": "Neutral <-> Less", "Value": 5},
    {"Submenu": "Cheeks", "Layer": "Flesh", "Option": "Lower Inside Cheeks", "Parameter": "Neutral <-> Less", "Value": 5},
    {"Submenu": "Cheeks", "Layer": "Fat", "Option": "Upper Cheeks", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Cheeks", "Layer": "Fat", "Option": "Upper Cheeks", "Parameter": "Less <-> More", "Value": 8},
    {"Submenu": "Cheeks", "Layer": "Fat", "Option": "Lower Cheeks", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Cheeks", "Layer": "Fat", "Option": "Lower Cheeks", "Parameter": "Less <-> More", "Value": 9},
    {"Submenu": "Cheeks", "Layer": "Fat", "Option": "Jowl", "Parameter": "Down <-> Up", "Value": 4},
    {"Submenu": "Cheeks", "Layer": "Fat", "Option": "Jowl", "Parameter": "Less <-> More", "Value": 7},
    {"Submenu": "Cheeks", "Layer": "Fat", "Option": "Cheeks Inside Upper", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Cheeks", "Layer": "Fat", "Option": "Cheeks Inside Upper", "Parameter": "Less <-> More", "Value": 7},
    {"Submenu": "Cheeks", "Layer": "Fat", "Option": "Cheeks Inside Lower", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Cheeks", "Layer": "Fat", "Option": "Cheeks Inside Lower", "Parameter": "Less <-> More", "Value": 8},
    {"Submenu": "Cheeks", "Layer": "Fat", "Option": "Temples", "Parameter": "Up", "Value": 5},
    {"Submenu": "Cheeks", "Layer": "Fat", "Option": "Temples", "Parameter": "Less <-> More", "Value": 7},

    # Mouth
    {"Submenu": "Mouth", "Layer": "Skeletal", "Option": "Mouth", "Parameter": "Narrow <-> Widen", "Value": 6},
    {"Submenu": "Mouth", "Layer": "Skeletal", "Option": "Mouth", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Skeletal", "Option": "Mouth", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Skeletal", "Option": "Mouth", "Parameter": "Round <-> Angular", "Value": 2},
    {"Submenu": "Mouth", "Layer": "Skeletal", "Option": "Mouth", "Parameter": "Shift Left <-> Shift Right", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Skeletal", "Option": "Mouth Outside Top", "Parameter": "Narrow <-> Widen", "Value": 6},
    {"Submenu": "Mouth", "Layer": "Skeletal", "Option": "Mouth Outside Top", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Skeletal", "Option": "Mouth Outside Top", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Skeletal", "Option": "Mouth Outside Top", "Parameter": "Round <-> Angular", "Value": 2},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Mouth Corners", "Parameter": "Narrow <-> Widen", "Value": 6},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Mouth Corners", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Mouth Corners", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Mouth Corners", "Parameter": "Round <-> Angular", "Value": 2},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Lip Gap Center", "Parameter": "Narrow <-> Widen", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Lip Gap Center", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Lip Gap Center", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Lip Gap Center", "Parameter": "Round <-> Angular", "Value": 2},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Lip Gap Sides", "Parameter": "Narrow <-> Widen", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Lip Gap Sides", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Lip Gap Sides", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Lip Gap Sides", "Parameter": "Round <-> Angular", "Value": 2},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Upper Lip Top Center", "Parameter": "Narrow <-> Widen", "Value": 6},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Upper Lip Top Center", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Upper Lip Top Center", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Upper Lip Top Center", "Parameter": "Round <-> Angular", "Value": 2},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Upper Lip Top Center", "Parameter": "Shift Left <-> Shift Right", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Upper Lip Top Sides", "Parameter": "Narrow <-> Widen", "Value": 6},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Upper Lip Top Sides", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Upper Lip Top Sides", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Upper Lip Top Sides", "Parameter": "Round <-> Angular", "Value": 2},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Upper Lip Top Corners", "Parameter": "Narrow <-> Widen", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Upper Lip Top Corners", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Upper Lip Top Corners", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Upper Lip Top Corners", "Parameter": "Round <-> Angular", "Value": 2},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Upper Lip Bottom Center", "Parameter": "Narrow <-> Widen", "Value": 6},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Upper Lip Bottom Center", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Upper Lip Bottom Center", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Upper Lip Bottom Center", "Parameter": "Round <-> Angular", "Value": 2},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Upper Lip Bottom Center", "Parameter": "Shift Left <-> Shift Right", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Upper Lip Bottom Sides", "Parameter": "Narrow <-> Widen", "Value": 6},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Upper Lip Bottom Sides", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Upper Lip Bottom Sides", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Upper Lip Bottom Sides", "Parameter": "Round <-> Angular", "Value": 2},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Upper Lip Fullness", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Upper Lip Fullness", "Parameter": "Back <-> Forward", "Value": 6},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Philtrum", "Parameter": "Narrow <-> Widen", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Philtrum", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Philtrum", "Parameter": "Round <-> Angular", "Value": 2},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Philtrum", "Parameter": "Shift Left <-> Shift Right", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Lower Lip Fullness", "Parameter": "Narrow <-> Widen", "Value": 7},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Lower Lip Fullness", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Lower Lip Fullness", "Parameter": "Back <-> Forward", "Value": 7},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Lower Lip Top Center", "Parameter": "Narrow <-> Widen", "Value": 7},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Lower Lip Top Center", "Parameter": "Up", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Lower Lip Top Center", "Parameter": "Shift Left <-> Shift Right", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Lower Lip Top Sides", "Parameter": "Narrow <-> Widen", "Value": 7},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Lower Lip Top Sides", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Lower Lip Top Sides", "Parameter": "Back <-> Forward", "Value": 6},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Lower Lip Bottom Center", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Lower Lip Bottom Center", "Parameter": "Back <-> Forward", "Value": 6},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Lower Lip Bottom Center", "Parameter": "Shift Left <-> Shift Right", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Lower Lip Bottom Sides", "Parameter": "Narrow <-> Widen", "Value": 7},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Lower Lip Bottom Sides", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Lower Lip Bottom Sides", "Parameter": "Back <-> Forward", "Value": 6},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Lower Lip Bottom Corners", "Parameter": "Narrow <-> Widen", "Value": 6},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Lower Lip Bottom Corners", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Lower Lip Bottom Corners", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Flesh", "Option": "Mouth Corner Grooves", "Parameter": "Neutral <-> Less", "Value": 8},
    {"Submenu": "Mouth", "Layer": "Fat", "Option": "Mouth Sides", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Fat", "Option": "Mouth Sides", "Parameter": "Less <-> More", "Value": 8},
    {"Submenu": "Mouth", "Layer": "Fat", "Option": "Upper Lip", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Fat", "Option": "Upper Lip", "Parameter": "Less <-> More", "Value": 6},
    {"Submenu": "Mouth", "Layer": "Fat", "Option": "Lower Lip", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Mouth", "Layer": "Fat", "Option": "Lower Lip", "Parameter": "Less <-> More", "Value": 8},

    # Chin
    {"Submenu": "Chin", "Layer": "Skeletal", "Option": "Chin", "Parameter": "Narrow <-> Widen", "Value": 6},
    {"Submenu": "Chin", "Layer": "Skeletal", "Option": "Chin", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Chin", "Layer": "Skeletal", "Option": "Chin", "Parameter": "Back <-> Forward", "Value": 4},
    {"Submenu": "Chin", "Layer": "Skeletal", "Option": "Chin", "Parameter": "Round <-> Angular", "Value": 2},
    {"Submenu": "Chin", "Layer": "Skeletal", "Option": "Chin", "Parameter": "Shift Left <-> Shift Right", "Value": 5},
    {"Submenu": "Chin", "Layer": "Skeletal", "Option": "Upper Chin", "Parameter": "Narrow <-> Widen", "Value": 6},
    {"Submenu": "Chin", "Layer": "Skeletal", "Option": "Upper Chin", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Chin", "Layer": "Skeletal", "Option": "Upper Chin", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Chin", "Layer": "Skeletal", "Option": "Upper Chin", "Parameter": "Round <-> Angular", "Value": 2},
    {"Submenu": "Chin", "Layer": "Skeletal", "Option": "Upper Chin", "Parameter": "Shift Left <-> Shift Right", "Value": 5},
    {"Submenu": "Chin", "Layer": "Flesh", "Option": "Chin Cleft", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Chin", "Layer": "Flesh", "Option": "Chin Cleft", "Parameter": "Shift Left <-> Shift Right", "Value": 5},
    {"Submenu": "Chin", "Layer": "Flesh", "Option": "Chin Sides", "Parameter": "Neutral <-> Less", "Value": 5},
    {"Submenu": "Chin", "Layer": "Fat", "Option": "Chin", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Chin", "Layer": "Fat", "Option": "Chin", "Parameter": "Less <-> More", "Value": 7},
    {"Submenu": "Chin", "Layer": "Fat", "Option": "Under Chin", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Chin", "Layer": "Fat", "Option": "Under Chin", "Parameter": "Less <-> More", "Value": 7},

    # Jaw
    {"Submenu": "Jaw", "Layer": "Skeletal", "Option": "Jaw", "Parameter": "Narrow <-> Widen", "Value": 7},
    {"Submenu": "Jaw", "Layer": "Skeletal", "Option": "Jaw", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Jaw", "Layer": "Skeletal", "Option": "Jaw", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Jaw", "Layer": "Skeletal", "Option": "Jaw", "Parameter": "Round <-> Angular", "Value": 2},
    {"Submenu": "Jaw", "Layer": "Skeletal", "Option": "Inside Jaw Top", "Parameter": "Narrow <-> Widen", "Value": 7},
    {"Submenu": "Jaw", "Layer": "Skeletal", "Option": "Inside Jaw Top", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Jaw", "Layer": "Skeletal", "Option": "Inside Jaw Top", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Jaw", "Layer": "Skeletal", "Option": "Inside Jaw Top", "Parameter": "Round <-> Angular", "Value": 2},
    {"Submenu": "Jaw", "Layer": "Skeletal", "Option": "Inside Jaw Bottom", "Parameter": "Narrow <-> Widen", "Value": 7},
    {"Submenu": "Jaw", "Layer": "Skeletal", "Option": "Inside Jaw Bottom", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Jaw", "Layer": "Skeletal", "Option": "Inside Jaw Bottom", "Parameter": "Back <-> Forward", "Value": 5},
    {"Submenu": "Jaw", "Layer": "Skeletal", "Option": "Inside Jaw Bottom", "Parameter": "Round <-> Angular", "Value": 2},
    {"Submenu": "Jaw", "Layer": "Flesh", "Option": "Jaw", "Parameter": "Less <-> More", "Value": 8},
    {"Submenu": "Jaw", "Layer": "Fat", "Option": "Jaw", "Parameter": "Down <-> Up", "Value": 5},
    {"Submenu": "Jaw", "Layer": "Fat", "Option": "Jaw", "Parameter": "Less <-> More", "Value": 8},
]

df = pd.DataFrame(data)

# Create a consolidated plot using plotly subplots (one for each Submenu) or just a long chart
# Since it's for an HTML file, a single scrollable chart is good, or grouped by submenu.
# Let's create one big chart but colored by Submenu.

fig = px.bar(
    df,
    x="Value",
    y="Option", # Grouping by Option isn't enough because parameters differ
    color="Submenu",
    orientation="h",
    hover_data=["Layer", "Parameter"],
    range_x=[0, 10],
    title="Advanced Sculpting Values (0-10)",
    height=3000, # Make it tall enough
    facet_col="Submenu", # Separate charts per submenu might be cleaner? No, facet_col is wide.
    facet_col_wrap=1 # This will stack them? No facet_row would stack.
)

# Better approach: Use subplots to create "sections"
submenus = df["Submenu"].unique()
fig = make_subplots(
    rows=len(submenus),
    cols=1,
    subplot_titles=submenus,
    vertical_spacing=0.01,
    shared_xaxes=True
)

row_idx = 1
for submenu in submenus:
    submenu_df = df[df["Submenu"] == submenu]
    
    # Create a unique label for y-axis: Option + Parameter
    submenu_df["Label"] = submenu_df["Option"] + " (" + submenu_df["Parameter"] + ")"
    
    # Add trace
    fig.add_trace(
        go.Bar(
            x=submenu_df["Value"],
            y=submenu_df["Label"],
            orientation='h',
            name=submenu,
            text=submenu_df["Value"],
            textposition='auto',
            marker=dict(color=submenu_df["Value"], colorscale='Viridis', cmin=0, cmax=10)
        ),
        row=row_idx,
        col=1
    )
    row_idx += 1

fig.update_layout(
    height=4000, # Very tall to accommodate all rows
    title_text="Advanced Sculpting Parameters Visualization",
    showlegend=False
)

# Fix y-axes to show labels properly
for i in range(1, len(submenus) + 1):
    fig.update_yaxes(row=i, col=1, tickmode='linear', automargin=True)
    fig.update_xaxes(range=[0, 10], row=i, col=1)

# Save to HTML
output_file = "sculpting_values_graph.html"
fig.write_html(output_file)

print(f"HTML file created: {output_file}")