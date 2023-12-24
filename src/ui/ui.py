from nicegui import ui
from src.warframe_inventory import WarframeUserInventory
from src.ui.table import build_warframe_items_table
from os import path, getcwd

PLAT_IMG_URL = path.join(getcwd(), "src/ui/static/plat-color.png")
DUCAT_IMG_URL = path.join(getcwd(), "src/ui/static/OrokinDucats.webp")


def build_item_card(prod_dict: dict) -> None:
    with ui.card().tight().style("width: 300px; padding: 20px").classes(
        "col-12 col-md"
    ):
        ui.image(prod_dict["item_image_url"]).style("width: 100%; height: 100px")
        with ui.card_section():
            ui.label(text=prod_dict["name"]).classes(
                "text-subtitle2 absolute-top text-center"
            ).style("padding-top: 20px")

        with ui.card_section():
            with ui.row().style("padding-top: 5px"):
                ui.image(PLAT_IMG_URL).style("width: 20px")
                ui.label(text=prod_dict["platinum_price"])
                ui.image(DUCAT_IMG_URL).style("width: 20px")
                ui.label(text=prod_dict["ducat_price"])


@ui.page("/")
def follow_cephalon_products():
    wf_inv = WarframeUserInventory()
    wf_items = wf_inv.get_items_from_database()
    plat_price = wf_inv.inventory_plat_price()
    ducat_price = wf_inv.inventory_ducat_price()

    with ui.row().classes("w-full center-items"):
        with ui.card().tight().style("width: 50%").classes("col-12 col-md"):
            ui.image(PLAT_IMG_URL).style("width: 20%")
            ui.label(text=f"Inventory platinum value {plat_price}").classes(
                "text-h5 q-mt-sm q-mb-xs absolute-center text-center text-black text-bold"
            )
        with ui.card().tight().style("width: 50%").classes("col-12 col-md"):
            ui.image(DUCAT_IMG_URL).style("width: 20%")
            ui.label(text=f"Inventory ducat value {ducat_price}").classes(
                "text-h5 q-mt-sm q-mb-xs absolute-center text-center text-black text-bold"
            )

    with ui.dialog() as dialog, ui.card():
        ui.label(text="Configure your Warframe Market Credentials").classes(
            "text-bold"
        )
        ui.input("Email").style("width: 100%")
        ui.input("Password").style("width: 100%")
        ui.button("Connect to Warframe Market")
        ui.button("Close", on_click=dialog.close)

    ui.button(icon="settings", on_click=dialog.open).props("outline round").classes(
        "shadow-lg absolute-bottom-right"
    ).style("margin: 10px")

    build_warframe_items_table(ui, wf_items)


ui.run()
