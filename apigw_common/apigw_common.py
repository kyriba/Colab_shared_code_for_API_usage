from IPython.display import display
import ipywidgets as widgets
from ipywidgets import Layout, VBox, HBox, HTML as IPywidgetsHTML


SPECIAL_ENTRIES = {"ALL", "ALL PROD", "ALL PROD AND SANDBOX"}


def _build_platform_list():
    """
    Build the master list of platform hostnames with special entries at top.
    """
    platforms = [
        "ALL",
        "ALL PROD",
        "ALL PROD AND SANDBOX",
        "neo.proto.cloud.kyriba.com",
        "morpheus.proto.cloud.kyriba.com",
        "demo.kyriba.com",
        "ammolite-preprod.treasury-factory.com",
        "ammolite-sandbox.treasury-factory.com",
        "ammolite.treasury-factory.com",
        "aquamarine-sandbox.treasury-factory.com",
        "aquamarine.treasury-factory.com",
        "diamond-preprod.treasury-factory.com",
        "diamond-sandbox.treasury-factory.com",
        "diamond.treasury-factory.com",
        "emerald-preprod.treasury-factory.com",
        "emerald-sandbox.treasury-factory.com",
        "emerald.treasury-factory.com",
        "jade-sandbox.treasury-cloud.cn",
        "jade.treasury-cloud.cn",
        "onyx-sandbox.treasury-factory.com",
        "onyx.treasury-factory.com",
        "opal-preprod.treasury-factory.com",
        "opal-sandbox.treasury-factory.com",
        "opal.treasury-factory.com",
        "quartz-preprod.treasury-factory.com",
        "quartz-sandbox.treasury-factory.com",
        "quartz.treasury-factory.com",
        "ruby-preprod.treasury-factory.com",
        "ruby-sandbox.treasury-factory.com",
        "ruby.treasury-factory.com",
        "topaz-preprod.treasury-factory.com",
        "topaz-sandbox.treasury-factory.com",
        "topaz.treasury-factory.com",
    ]
    special = ["ALL", "ALL PROD", "ALL PROD AND SANDBOX"]
    regular = [p for p in platforms if p not in special]
    regular_sorted = sorted(regular, key=lambda x: x.lower())
    return special + regular_sorted


def create_platform_selector():

    platforms = _build_platform_list()

    header = IPywidgetsHTML("""
        <h2 style="text-align: center; color: #007ACC;">
            📌 Select Your Desired Platforms
        </h2>
    """)

    search_box = widgets.Text(
        value='',
        placeholder='🔍 Search platforms...',
        description='',
        disabled=False,
        layout=widgets.Layout(width='100%'),
        style={'description_width': 'initial'},
    )

    platforms_sel = widgets.SelectMultiple(
        options=platforms,
        value=("ALL",),
        rows=15,
        description='',
        disabled=False,
        style={'description_width': 'initial'},
        layout=Layout(width='100%', height='300px'),
    )

    select_all_checkbox = widgets.Checkbox(
        value=False,
        description='Select All Platforms',
        disabled=False,
        indent=False,
        style={'description_width': 'initial'},
        layout=Layout(width='200px'),
    )

    state = {"updating": False}

    def filter_platforms(search_text: str):
        if search_text:
            return [p for p in platforms if search_text.lower() in p.lower()]
        return platforms

    def on_select_all_change(change):
        if state["updating"]:
            return
        state["updating"] = True
        if change["new"]:
            platforms_sel.value = tuple(platforms_sel.options)
        else:
            platforms_sel.value = ()
        state["updating"] = False

    def on_search_change(change):
        current_selection = set(platforms_sel.value)
        filtered = filter_platforms(change["new"])
        platforms_sel.options = filtered
        platforms_sel.value = tuple(current_selection.intersection(filtered))

    def on_platforms_selected_change(change):
        if state["updating"]:
            return
        state["updating"] = True
        all_selected = set(platforms_sel.value) == set(platforms_sel.options)
        select_all_checkbox.value = all_selected
        state["updating"] = False

    select_all_checkbox.observe(on_select_all_change, names="value")
    search_box.observe(on_search_change, names="value")
    platforms_sel.observe(on_platforms_selected_change, names="value")

    search_and_select_all = HBox(
        [search_box, select_all_checkbox],
        layout=Layout(width='100%', justify_content='space-between'),
    )

    container = VBox(
        [header, search_and_select_all, platforms_sel],
        layout=Layout(
            border='2px solid #007ACC',
            border_radius='10px',
            padding='20px',
            width='800px',
            background_color='#f9f9f9',
        ),
    )

    return platforms_sel, platforms, container


def normalize_platform_selection(selected=None, platforms_list=None):

    if platforms_list is None:
        platforms_list = _build_platform_list()

    if selected is None:
        selected = []

    if not selected:
        return []

    selected = list(selected)

    if "ALL PROD" in selected:
        prod = [
            "ammolite.treasury-factory.com",
            "aquamarine.treasury-factory.com",
            "diamond.treasury-factory.com",
            "emerald.treasury-factory.com",
            "jade.treasury-cloud.cn",
            "onyx.treasury-factory.com",
            "opal.treasury-factory.com",
            "quartz.treasury-factory.com",
            "ruby.treasury-factory.com",
            "topaz.treasury-factory.com",
        ]
        selected = [p for p in selected if p != "ALL PROD"] + prod

    if "ALL PROD AND SANDBOX" in selected:
        prod_and_sandbox = [
            "ammolite.treasury-factory.com", "ammolite-sandbox.treasury-factory.com",
            "aquamarine.treasury-factory.com", "aquamarine-sandbox.treasury-factory.com",
            "diamond.treasury-factory.com", "diamond-sandbox.treasury-factory.com",
            "emerald.treasury-factory.com", "emerald-sandbox.treasury-factory.com",
            "jade.treasury-cloud.cn", "jade-sandbox.treasury-cloud.cn",
            "onyx.treasury-factory.com", "onyx-sandbox.treasury-factory.com",
            "opal.treasury-factory.com", "opal-sandbox.treasury-factory.com",
            "quartz.treasury-factory.com", "quartz-sandbox.treasury-factory.com",
            "ruby.treasury-factory.com", "ruby-sandbox.treasury-factory.com",
            "topaz.treasury-factory.com", "topaz-sandbox.treasury-factory.com",
        ]
        selected = [p for p in selected if p != "ALL PROD AND SANDBOX"] + prod_and_sandbox

    if "ALL" in selected:
        selected = [p for p in selected if p != "ALL"] + [
            p for p in platforms_list if p not in SPECIAL_ENTRIES
        ]

    seen = set()
    out = []
    for p in selected:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out