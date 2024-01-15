from os import getcwd, path

WARFRAME_ITEMS_COLUMNS = [
    {"name": "name", "label": "Name", "field": "name"},
    {
        "name": "platinum_price",
        "label": "Platinum Price",
        "field": "platinum_price",
        "sortable": True,
    },
    {
        "name": "ducat_price",
        "label": "Ducat Price",
        "field": "ducat_price",
        "sortable": True,
    },
    {
        "name": "state",
        "label": "Item State",
        "field": "state",
        "sortable": True,
    },
]


PLAT_IMG_URL = path.join(getcwd(), "src/ui/static/plat-color.png")
DUCAT_IMG_URL = path.join(getcwd(), "src/ui/static/OrokinDucats.webp")
HEADER_IMG_URL = path.join(getcwd(), "src/ui/static/headerLogo.png")
