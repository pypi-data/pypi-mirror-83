import dash

app = dash.Dash(__name__, update_title='Running...')
app.config.suppress_callback_exceptions = True
