from dash import html


# ===================================================================
# Define layout
# ===================================================================
layout = html.Div(
    children=[
        html.Div(
            [
                html.H1(
                    children="Förskrivning av ADHD-medicin till 0-17-åringar i Sverige",
                    className="startpage-title"
                ),
            ],
            className="startpage-title-wrapper"
        ),
        html.Div(
            children=[
                html.P(
                    children=[
                        (
                            "På de här sidorna beskrivs... "
                        ),
                    ],
                    className='startpage-intro'
                ),
            ],
            className='startpage-intro-wrapper'
        ),
    ],
    className="startpage-container"
)