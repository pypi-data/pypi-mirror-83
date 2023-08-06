import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from ucbshift.app import app
from ucbshift.apps import display

server = app.server

app.title = 'NMR-Predict'
app.layout = html.Div([
	dcc.Location(id='url', refresh=False),
	html.Div(id='page-content')
])

@app.callback(
	Output('page-content', 'children'),
	[Input('url', 'pathname')]
)
def display_page(pathname):
	return display.layout

if __name__ == '__main__':
	app.run_server(debug=True)
