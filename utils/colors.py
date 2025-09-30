PALETTES = {
    "default": {
        "PRIMARY": "#4CAF50",
        "SECONDARY": "#81C784",
        "BACKGROUND": "#F5F5F5",
        "TEXT": "#333333",
    },
    "dark": {
        "PRIMARY": "#FF9800",
        "SECONDARY": "#FFB74D",
        "BACKGROUND": "#121212",
        "TEXT": "#FFFFFF",
    },
    "tree": {
        "PRIMARY": "#2E7D32",
        "SECONDARY": "#66BB6A",
        "BACKGROUND": "#E8F5E9",
        "TEXT": "#63c968",
    }
}

def get_palette(theme: str) -> dict:
    """Return color palette for a given theme."""
    return PALETTES.get(theme.lower(), PALETTES["default"])