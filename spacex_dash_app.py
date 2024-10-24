# Import required libraries
import pandas as pd
import plotly.express as px

import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv('spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1('SpaceX Launch Records Dashboard',
                style={'textAlign': 'center', 'color': '#503D36',
                       'font-size': 40}),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        dcc.Dropdown(id='site-dropdown',
                     options=[
                         {'label': 'All Sites',
                          'value': 'ALL'},
                          {'label': 'LC-40',
                           'value': 'CCAFS LC-40'},
                           {'label': 'SLC-40',
                            'value': 'CCAFS SLC-40'},
                            {'label': 'LC-39A',
                             'value': 'KSC LC-39A'},
                             {'label': 'SLC-4E',
                              'value': 'VAFB SLC-4E'}
                              ],
                    value='ALL',
                    placeholder='place holder here',
                    searchable=True
                    ),
        html.Br(),
        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id='success-pie-chart')),
        html.Br(),
        html.P('Payload range (kg):'),
        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(
            id='payload-slider',
            min=0,
            max=10000,
            step=1000,
            marks={i: f"{i}" for i in range(0, 11000, 1000)},
            value=[min_payload, max_payload],  # Initial range from min to max
            tooltip={'all': 'Payload: {min:.0f} kg - {max:.0f} kg'}
            ),
        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(
            dcc.Graph(id='success-payload-scatter-chart'))
        ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value')
              )
def get_pie_chart(entered_site):
    filtered_df = spacex_df[
       spacex_df['Launch Site'] == entered_site if 
           entered_site != 'ALL' else spacex_df['class'] == 1
       ]['class' if entered_site != 'ALL' else 'Launch Site'].value_counts()
    
    fig = px.pie(filtered_df, 
                 names = filtered_df.index if entered_site == 'ALL' else ['Failed', 'Success'], 
                 values = filtered_df.values, 
                 title = 'Total Success Launches by Site' if 
                     entered_site =="ALL" else f'Total Launches for site {entered_site}')
    
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(
        component_id='success-payload-scatter-chart',
        component_property='figure'),
    [Input(component_id='site-dropdown',
           component_property='value'),
           Input(component_id='payload-slider',
                 component_property='value')
                 ])
def get_scatter_plot(selected_sites, payload_range):
  # Combine filtering logic
  filtered_df = spacex_df[
      (spacex_df['Launch Site']==selected_sites if selected_sites != 'ALL' else True) &
      (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
      (spacex_df['Payload Mass (kg)'] <= payload_range[1])
  ]
  # Create scatter plot with single logic
  fig = px.scatter(
      filtered_df,
      x='Payload Mass (kg)',
      y='class',
      labels={'class': selected_sites},
      color='Booster Version Category'
  )

  return fig


# Run the app
if __name__ == '__main__':
    app.run_server()