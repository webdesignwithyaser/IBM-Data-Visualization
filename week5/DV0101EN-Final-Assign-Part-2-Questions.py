import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# TASK 2.1: Create a Dash application and give it a meaningful title
app.title = "Automobile Sales Statistics Dashboard"

# Create the layout of the app
app.layout = html.Div([
    # TASK 2.1: Add title to the dashboard
    html.H1("Automobile Sales Statistics Dashboard", 
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),
    
    # TASK 2.2: Add drop-down menus
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            placeholder='Select a report type',
            value='Select Statistics',
            style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}
        )
    ]),
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in range(1980, 2024)],
            placeholder='Select-year',
            value='Select-year'
        )
    ]),
    
    # TASK 2.3: Add a division for output display
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex'})
])

# TASK 2.4: Callback to enable/disable the year dropdown
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics': 
        return False
    else: 
        return True

# TASK 2.5 & 2.6: Callback to update the output container (Plots)
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), 
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter data for recession periods
        recession_data = data[data['Recession'] == 1]
        
        # Plot 1: Automobile sales fluctuate over Recession Period (year wise)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', 
                             title="Average Automobile Sales Fluctuation Over Recession Period"))

        # Plot 2: Average number of vehicles sold by vehicle type
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()                           
        R_chart2 = dcc.Graph(figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales',
                             title="Average Vehicles Sold by Vehicle Type during Recessions"))
        
        # Plot 3: Total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(figure=px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type',
                             title="Total Advertising Expenditure Share by Vehicle Type"))

        # Plot 4: Effect of unemployment rate on vehicle type and sales
        unemp_data = recession_data.groupby(['Unemployment_Rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(figure=px.bar(unemp_data, x='Unemployment_Rate', y='Automobile_Sales', color='Vehicle_Type',
                             title='Effect of Unemployment Rate on Vehicle Type and Sales'))

        return [
            html.Div(className='chart-item', children=[R_chart1, R_chart2], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[R_chart3, R_chart4], style={'display': 'flex'})
        ]

    elif (input_year and selected_statistics == 'Yearly Statistics'):
        yearly_data = data[data['Year'] == input_year]
        
        # Plot 1: Yearly Automobile sales using line chart for the whole period
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales', 
                             title='Yearly Automobile Sales (Whole Period)'))
            
        # Plot 2: Total Monthly Automobile sales using line chart
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(mas, x='Month', y='Automobile_Sales', 
                             title='Total Monthly Automobile Sales in {}'.format(input_year)))

        # Plot 3: Bar chart for average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales',
                             title='Average Vehicles Sold by Vehicle Type in {}'.format(input_year)))

        # Plot 4: Total Advertisement Expenditure for each vehicle using pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type',
                             title='Total Advertisement Expenditure for Each Vehicle'))

        return [
            html.Div(className='chart-item', children=[Y_chart1, Y_chart2], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[Y_chart3, Y_chart4], style={'display': 'flex'})
        ]
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)