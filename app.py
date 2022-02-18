import altair as alt
from dash import Dash, html, dcc, Input, Output
import pandas as pd

alt.data_transformers.disable_max_rows()

olympic = pd.read_csv('./olympic_after_2000.csv')

dropdown_list = sorted(list(olympic['Year'].unique()))

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

app.layout = html.Div([
        dcc.Dropdown(
            id='year', value=2002,
            options=[{'label': i, 'value': i} for i in dropdown_list]),
        html.Iframe(
            id='barplot',
            style={'border-width': '0', 'width': '100%', 'height': '400px'},
            )])

# Set up callbacks/backend
@app.callback(
    Output('barplot', 'srcDoc'),
    Input('year', 'value'))

def plot_altair(year):
    colors = ['#d95f0e', '#fec44f', 'silver']

    bars = alt.Chart(olympic[olympic['Year'] == year], title="Medal Distribution by Gender in Olympics after 2000's").encode(x=alt.X('Sex', title= 'Gender'),
                                 y=alt.Y('count(Medal)', title='Count of medals won'),
                                 color = alt.Color('Medal', scale=alt.Scale(range=colors))).mark_bar()

    text = bars.mark_text(
        align='left',
        baseline='middle',
        dy=-3,  # Nudges text above so it doesn't appear on top of the bar
        color='black'
    ).encode(
        text='count(Medal):Q'
    )

    chart = (bars+text).properties(height=300, width=200).facet('Medal')    
    
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)