# dash package
from dash import dcc
from dash import html

from app import app

_links = [
    dcc.Link('Startsida', href='/start-page'),
    dcc.Link('Karta', href='/karta'),
    dcc.Link('Histogram', href='/histogram')
]

_desktop_top_nav = html.Nav(
    _links,
    id="desktop-nav",
    className="nav top-nav desktop-nav"
)

_mobile_top_nav = html.Nav(
    html.Ul([html.Li(l) for l in _links]),
    id="mobile-nav",
    className="mobile-nav"
)

_top_header = html.Header(
    [
        _desktop_top_nav,
        html.A(
            html.Img(
                src=app.get_asset_url('img/hamburger-menu.svg'),
                alt=(
                    "En ikon bestående av tre linjer, "
                    "som indikerar att man kan aktivera navigationsmenyn här."
                )
            ),
            className="menu-toggle",
            id="menu-toggle"
        )
    ],
    id="top-header",
    className="top-header"
)

chief_div = html.Div([
    # the url bar isn't an actual DOM object, rather it's
    # an abstract representation of the URL bar, used for
    # forming links between 'views' in the app
    dcc.Location(id='url', refresh=False),
    _top_header,
    _mobile_top_nav,
    html.Div(id="mobile-nav-shadow", className="mobile-nav-shadow"),
    html.Div(id='page-content'),
])
