
import dash_mantine_components as dmc
import dash
from dash_iconify import DashIconify
from dash import Dash, _dash_renderer, dcc, callback, Input, Output, State

_dash_renderer._set_react_version("18.2.0")

app = Dash(
    external_stylesheets=dmc.styles.ALL, 
    use_pages=True,
    
)


links = dmc.Stack(
    [
        dmc.Anchor(f"{page['name']}", href=page["relative_path"])
        for page in dash.page_registry.values()
        if page["module"] != "pages.not_found_404"
    ]
)

theme_toggle = dmc.ActionIcon(
    [
        dmc.Paper(DashIconify(icon="radix-icons:sun", width=25), darkHidden=True),
        dmc.Paper(DashIconify(icon="radix-icons:moon", width=25), lightHidden=True),
    ],
    variant="transparent",
    color="yellow",
    id="color-scheme-toggle",
    size="lg",
    ms="auto",
)

header = dmc.Group(
    [
        dmc.Burger(id="burger-button", opened=True, hiddenFrom="md"),
        dmc.Text("Spotify Music Analysis", size="lg",ta='center',c='blue', fw=700),
        theme_toggle
    ],
    justify="flex-start",
    h=70
)


# developing the side setup inside a variable 
navbar = dcc.Loading(
    dmc.ScrollArea(

[
      dmc.Stack(
                [
                    
                    links

                ]
            )
], offsetScrollbars=True,
type='scroll',
style={'height': '100%'}
    ),
)


app_shell = dmc.AppShell(
    [
        dmc.AppShellHeader(header, px=15),
        dmc.AppShellNavbar(navbar, p=19),
        dmc.AppShellMain(dash.page_container, py=60, pr=5),
        dmc.AppShellFooter(
            [
                dmc.Group(
                    [
                        dmc.NavLink(
                            label= 'Sources Code',
                            description='double Sources',
                            leftSection=dmc.Badge(
                                "2", size="xs", variant='filled', color='orange', w=16, h=16,p=0
                            ),
                            childrenOffset=28,
                            children=[
                                dmc.NavLink(label="GitHub", href='https://github.com/SmartDvi/Air_Pollution.git'),
                                dmc.NavLink(label="PY.CAFE", href='https://py.cafe/SmartDvi/plotly-global-air-quality')
                            ]

                        )
                    ], justify='lg'
                )
            ]
        )
    ],
    header={"height": 70},
    padding="xl",
    navbar={
        "width": 250,
        "breakpoint": "md",
        "collapsed": {"mobile": True},
    },
    aside={
        "width": 150,
        "breakpoint": "xs",
        "collapsed": {"desktop": False, "mobile": True},
    },
    id="app-shell",
)

app.layout = dmc.MantineProvider(
    [
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
    navbar["collapsed"] = {"mobile": opened}
    return navbar


@callback(
    Output("mantine-provider", "forceColorScheme"),
    Input("color-scheme-toggle", "n_clicks"),
    State("mantine-provider", "forceColorScheme"),
    prevent_initial_call=True,
)
def switch_theme(_, theme):
    return "dark" if theme == "light" else "light"



if __name__ == "__main__":
    app.run(debug=True, port=6040)