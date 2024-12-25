import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pprint
from dash import Dash, _dash_renderer, dcc, callback, Input, Output, State, html, page_container, get_relative_path

_dash_renderer._set_react_version("18.2.0")

app = Dash(external_stylesheets=dmc.styles.ALL, use_pages=True)

theme_toggle = dmc.ActionIcon(
    [
        dmc.Paper(DashIconify(icon="radix-icons:sun", width=25), darkHidden=True),
        dmc.Paper(DashIconify(icon="radix-icons:moon", width=25), lightHidden=True),
    ],
    variant="transparent",
    #color="yellow",
    id="color-scheme-toggle",
    style={"marginLeft": "auto"},
    size="lg",
   # ms="auto",
)

header = dmc.Group(
    [
        dmc.Burger(id="burger-button", opened=False, hiddenFrom="md"),
        dmc.Text(["Header"], size="xl", fw=700),
        theme_toggle
    ],
    justify="flex-start",
    h=70
)




def create_main_link(icon, label, href):
    return dmc.Anchor(
        dmc.Group(
            [
                DashIconify(
                    icon=icon,
                    width=23,
                ) if icon else None,
                dmc.Text(label, size="sm"),
            ]
        ),
        # use get_relative_path when hosting to services like
        # Dash Enterprise or pycafe that uses pathname prefixes.
        # See the dash docs for mor info
        href=get_relative_path(href),
        variant="text",
        mb=5,
        underline=False,
    )

navbar = dmc.Group(
            dmc.ScrollArea(
            [
                create_main_link(icon=None, label=page["name"], href=page["path"])
                for page in dash.page_registry.values()
                if page["module"] != "pages.not_found_404"
            ],
            offsetScrollbars=True,
            type="scroll",
            style={"height": "100%"},
        )
)


app_shell = dmc.AppShell(
    [
        dmc.AppShellHeader(header, px=25),
        dmc.AppShellNavbar(navbar, p=24),
        dmc.AppShellMain(page_container, p=0),
        dmc.AppShellFooter("Footer", h=50, ml=400)
    ],
    header={"height": 70},
    padding="xl",
    navbar={
        "width": 80,
        "breakpoint": "md",
        "collapsed": {"mobile": True},
    },
    aside={
        "width": 100,
        "breakpoint": "xl",
        "collapsed": {"desktop": False, "mobile": True},
    },
    footer={
        "width": 300,
        "breakpoint": "md",
        "collapsed": {"desktop": False, "mobile": True},
    },
    id="app-shell",
)

app.layout = dmc.MantineProvider(
    [
        dcc.Store(id="theme-store", storage_type="local", data="light"),
        app_shell
    ],
    id="mantine-provider",
    forceColorScheme="light",
)


@callback(
    Output("app-shell", "navbar"),
    Input("burger-button", "opened"),
    State("app-shell", "navbar"),
)
def navbar_is_open(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


@callback(
    Output("mantine-provider", "forceColorScheme"),
    Input("color-scheme-toggle", "n_clicks"),
    State("mantine-provider", "forceColorScheme"),
    prevent_initial_call=True,
)
def switch_theme(_, theme):
    new_theme = "dark" if theme == "light" else "light"
    new_icon = [
        dmc.Paper(DashIconify(icon="radix-icons:sun", width=25), darkHidden=(new_theme == "dark")),
        dmc.Paper(DashIconify(icon="radix-icons:moon", width=25), lightHidden=(new_theme == "light")),
    ]
    return new_theme, new_icon



if __name__ == "__main__":
    app.run_server(debug=True, port=6070)