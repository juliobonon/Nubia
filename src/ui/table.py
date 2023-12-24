from nicegui.events import GenericEventArguments

def warframe_item_dialog(ui, msg: GenericEventArguments):
    with ui.dialog() as dialog:
        dialog.open()
        with ui.card():
            ui.label(f"Want to create a auction for {msg.args['key']}?").classes("text-bold")
            ui.input("Price")
            ui.input("Quantity")
            with ui.row():
                ui.button("Create auction")
                ui.button("Close", on_click=dialog.close)


def build_warframe_items_table(ui, wf_items: list):
    columns = [
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
    rows = [wf_item.to_dict() for wf_item in wf_items]
    table = ui.table(columns=columns, rows=rows, row_key="name").style("width: 100%")

    table.add_slot(
        "header",
        r"""
            <q-tr :props="props">
                <q-th auto-width />
                <q-th v-for="col in props.cols" :key="col.name" :props="props">
                    {{ col.label }}
                </q-th>
            </q-tr>
            """,
    )
    table.add_slot(
        "body",
        r"""
            <q-tr :props="props">
                 <q-td auto-width>
                    <q-btn size="sm" color="accent" round dense
                        @click="$parent.$emit('add_business', props)"
                        :icon="props.add_business ? 'remove' : 'add_business'" />
                </q-td>
                <q-td v-for="col in props.cols" :key="col.name" :props="props">
                    {{ col.value }}
                </q-td>
            </q-tr>
            </q-tr>
        """,
    )
    table.on("add_business", lambda msg: warframe_item_dialog(ui, msg))
