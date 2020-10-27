
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import date
import pandas as pd
import numpy as np
import dash_table
import plotly
import plotly.graph_objects as go
import plotly.express as px
import json
import requests
import json
import pandas as pd
import datetime

app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = True
app.title = 'COVID-19'


CDC_BASE_URL = 'https://clinicaltrials.gov/api/query/study_fields?expr=COVID-19&min_rnk=1&max_rnk=1000&fmt=json'
CDC_BASE_URL1 = 'https://clinicaltrials.gov/api/query/study_fields?expr=COVID-19&min_rnk=1001&max_rnk=2000&fmt=json'
CDC_BASE_URL2 = 'https://clinicaltrials.gov/api/query/study_fields?expr=COVID-19&min_rnk=2001&max_rnk=3000&fmt=json'
CDC_BASE_URL3 = 'https://clinicaltrials.gov/api/query/study_fields?expr=COVID-19&min_rnk=3001&max_rnk=4000&fmt=json'

cdc_extract_fields = [
    'LocationCountry',
    'NCTId',
    'DesignPrimaryPurpose',
    'Phase',
    'EnrollmentCount',
    'CompletionDate',
    'LocationStatus',
    'LeadSponsorName',
    'CollaboratorName'
    
]
query_url = f'{CDC_BASE_URL}&fields={",".join(cdc_extract_fields)}'
    
query_url1 = f'{CDC_BASE_URL1}&fields={",".join(cdc_extract_fields)}'
    
query_url2 = f'{CDC_BASE_URL2}&fields={",".join(cdc_extract_fields)}'
    
query_url3 = f'{CDC_BASE_URL3}&fields={",".join(cdc_extract_fields)}'
    
r = requests.get(query_url)
r1 = requests.get(query_url1)
r2 = requests.get(query_url2)
r3 = requests.get(query_url3)

j = json.loads(r.content)
j1 = json.loads(r1.content)
j2 = json.loads(r2.content)
j3 = json.loads(r3.content)

df = pd.DataFrame(j['StudyFieldsResponse']['StudyFields'])
df1 = pd.DataFrame(j1['StudyFieldsResponse']['StudyFields'])
df2 = pd.DataFrame(j2['StudyFieldsResponse']['StudyFields'])
df3 = pd.DataFrame(j3['StudyFieldsResponse']['StudyFields'])

g=pd.concat([df, df1, df2,df3], ignore_index=True)

# Some of the fields are single-item lists which can be cleaned
def de_list(input_field):
    if isinstance(input_field, list):
        if len(input_field) == 0:
            return None
        else:
          return input_field[0]
        
    else:
        return input_field
    
    
for c in g.columns:
    g[c] = g[c].apply(de_list)
    
g["Phase"].replace({"Not Applicable": "Unknown"}, inplace=True)
g["Phase"].fillna("Unknown", inplace = True)
g.replace(to_replace=[None], value=np.nan, inplace=True)
g["DesignPrimaryPurpose"].fillna("Generic", inplace = True)
g["LocationStatus"].fillna("Unknown", inplace = True)
g["CollaboratorName"].fillna("Not Applicable", inplace = True)
g["LocationCountry"].fillna("N.A", inplace = True)
g['CompletionDate']=pd.to_datetime(g['CompletionDate']).dt.date
today = datetime.datetime(2020, 10, 1)
today1=pd.to_datetime(today)

g.sort_values(by=['CompletionDate'],ascending=True,inplace=True)


dj=g[['NCTId','LeadSponsorName','CollaboratorName','DesignPrimaryPurpose','Phase','EnrollmentCount','CompletionDate','LocationCountry','LocationStatus']]
    
dj.to_csv("C:/Users/Akash Deep/Downloads/covid-19-master/covid-19-master/data/worldwide.csv",index=False)

t=dj[dj['LocationCountry']=='United States']
t.to_csv("C:/Users/Akash Deep/Downloads/covid-19-master/covid-19-master/data/usa.csv",index=False)
t=dj[dj['LocationCountry']=='China']
t.to_csv("C:/Users/Akash Deep/Downloads/covid-19-master/covid-19-master/data/china.csv",index=False)    
t=dj[dj['LocationCountry']=='Belgium']
t.to_csv("C:/Users/Akash Deep/Downloads/covid-19-master/covid-19-master/data/europe.csv",index=False)
pfz=dj[dj['CollaboratorName']=='Pfizer']
pfz1=dj[dj['LeadSponsorName']=='Pfizer']
pfz2=pd.concat([pfz,pfz1],ignore_index=True)
pfz2.sort_values(by=['CompletionDate'],inplace=True)
pfz2.to_csv("C:/Users/Akash Deep/Downloads/covid-19-master/covid-19-master/data/pfizer.csv",index=False)
usb=t.query("LocationCountry == 'United States' & LeadSponsorName == 'Janssen Vaccines & Prevention B.V.'")
usb1=dj.query("LocationCountry == 'United States' & LeadSponsorName == 'Janssen Research & Development, LLC'")
usb2=dj.query("LocationCountry == 'United States' & LeadSponsorName == 'Janssen Pharmaceutica N.V., Belgium'")
usb3=dj.query("LocationCountry == 'United States' & LeadSponsorName == 'Novartis Pharmaceuticals'")
usb4=dj.query("LocationCountry == 'United States' & LeadSponsorName == 'AstraZeneca'")
usb5=dj.query("LocationCountry == 'United States' & LeadSponsorName == 'ModernaTX, Inc.'")
usb7=dj.query("LocationCountry == 'United States' & LeadSponsorName == 'Pfizer'")
usb8=dj.query("LocationCountry == 'United States' & CollaboratorName == 'Pfizer'")
usb10=dj.query("LocationCountry == 'United States' & LeadSponsorName == 'Eli Lilly and Company'")
usb11=dj.query("LocationCountry == 'United States' & CollaboratorName == 'Eli Lilly and Company'")
usb12=dj.query("LocationCountry == 'United States' & LeadSponsorName == 'Regeneron Pharmaceuticals'")


usb6 = pd.concat([usb,usb1,usb2,usb3,usb4,usb5,usb10,usb11,usb12],ignore_index=True)
usb6.sort_values(by=['CompletionDate'],inplace=True)
usb6.to_csv("C:/Users/Akash Deep/Downloads/covid-19-master/covid-19-master/data/colaborator.csv",index=False)
usb9 = pd.concat([usb,usb1,usb2,usb3,usb4,usb5,usb7,usb8,usb10,usb11,usb12],ignore_index=True)
usb9.sort_values(by=['CompletionDate'],inplace=True)
usb9.to_csv("C:/Users/Akash Deep/Downloads/covid-19-master/covid-19-master/data/pfizer1.csv",index=False)





dash_colors = {
    'background': 'black',
    'text': 'white',
    'grid': '#333333',
    'red': '#BF0000',
    'blue': '#466fc2',
    'green': '#5bc246'
}

df_worldwide = pd.read_csv('data/df_worldwide.csv')
df_worldwide1 = pd.read_csv('data/worldwide.csv')
df_worldwide1['CompletionDate']=pd.to_datetime(df_worldwide1['CompletionDate']).dt.date
t21=df_worldwide1[df_worldwide1['CompletionDate']>today1]

df_worldwide2 = pd.read_csv('data/map.csv')
df_enrollment = pd.read_csv('data/enrollment_count.csv')
df_usa = pd.read_csv('data/usa.csv')
df_china1 = pd.read_csv('data/china.csv')
df_belgium = pd.read_csv('data/europe.csv')
df_pfizer = pd.read_csv('data/pfizer.csv')
df_colaborator = pd.read_csv('data/colaborator.csv')
df_pfizer1 = pd.read_csv('data/pfizer1.csv')
df_worldwide['percentage'] = df_worldwide['percentage'].astype(str)
df_worldwide['date'] = pd.to_datetime(df_worldwide['date'])




# selects the "data last updated" date
today = date.today()
g=today.strftime('%B %d, %Y')


available_countries = sorted(df_worldwide['Country/Region'].unique())



df_us = pd.read_csv('data/df_us.csv')
df_us['percentage'] = df_us['percentage'].astype(str)
df_us['date'] = pd.to_datetime(df_us['date'])

df_eu = pd.read_csv('data/df_eu.csv')
df_eu['percentage'] = df_eu['percentage'].astype(str)
df_eu['date'] = pd.to_datetime(df_eu['date'])

df_china = pd.read_csv('data/df_china.csv')
df_china['percentage'] = df_china['percentage'].astype(str)
df_china['date'] = pd.to_datetime(df_china['date'])

df_us_counties = pd.read_csv('data/df_us_county.csv')
df_us_counties['percentage'] = df_us_counties['percentage'].astype(str)
df_us_counties['Country/Region'] = df_us_counties['Country/Region'].astype(str)
df_us_counties['date'] = pd.to_datetime(df_us_counties['date'])

@app.callback(
    [Output('filter-query-input', 'style'),
     Output('filter-query-output', 'style')],
    [Input('filter-query-read-write', 'value')]
)
def query_input_output(val):
    input_style = {'width': '100%'}
    output_style = {}
    if val == 'read':
        input_style.update(display='none')
        output_style.update(display='inline-block')
    else:
        input_style.update(display='inline-block')
        output_style.update(display='none')
    return input_style, output_style


@app.callback(
    Output('datatable-advanced-filtering', 'filter_query'),
    [Input('filter-query-input', 'value')]
)
def write_query(query):
    if query is None:
        return ''
    return query


@app.callback(
    Output('filter-query-output', 'children'),
    [Input('datatable-advanced-filtering', 'filter_query')]
)
def read_query(query):
    if query is None:
        return "No filter query"
    return dcc.Markdown('`filter_query = "{}"`'.format(query))


@app.callback(
    Output('datatable-query-structure', 'children'),
    [Input('datatable-advanced-filtering', 'derived_filter_query_structure')]
)
def display_query(query):
    if query is None:
        return ''
    return html.Details([
        html.Summary('Derived filter query structure'),
        html.Div(dcc.Markdown('''```json
{}
```'''.format(json.dumps(query, indent=4))))
    ])





@app.callback(
    Output('active_ind', 'figure'),
    [Input('global_format', 'value')])
def active(view):
    '''
    creates the CURRENTLY ACTIVE indicator
    '''
    if view == 'Worldwide':
        df = df_worldwide1
    elif view == 'United States':
        df = df_usa
    elif view == 'Europe':
        df = df_belgium
    elif view == 'China':
        df = df_china1
    elif view == 'Pfizer':
        df = df_pfizer
    elif view == 'Competitor':
        df = df_colaborator
    elif view == 'Pfizer&Comp':
        df = df_pfizer1
    else:
        df = df_worldwide1

    value = len(df)
    return {
            'data': [{'type': 'indicator',
                    'mode': 'number',
                    'value': value,
                    
                    'number': {'valueformat': ',',
                              'font': {'size': 50}},
                    'domain': {'y': [0, 1], 'x': [0, 1]}}],
            'layout': go.Layout(
                title={'text': "Total Drugs"},
                font=dict(color=dash_colors['red']),
                paper_bgcolor=dash_colors['background'],
                plot_bgcolor=dash_colors['background'],
                height=200
                )
            }



@app.callback(
    Output('deaths_ind', 'figure'),
    [Input('global_format', 'value')])
def deaths(view):
    '''
    creates the DEATHS TO DATE indicator
    '''
    if view == 'Worldwide':
        df = df_worldwide1
    elif view == 'United States':
        df = df_usa
    elif view == 'Europe':
        df = df_belgium
    elif view == 'China':
        df = df_china1
    elif view == 'Pfizer':
        df = df_pfizer
    elif view == 'Competitor':
        df = df_colaborator
    elif view == 'Pfizer&Comp':
        df = df_pfizer1
    else:
        df = df_worldwide1

    value = len(df[df['DesignPrimaryPurpose']=='Prevention'])
    return {
            'data': [{'type': 'indicator',
                    'mode': 'number',
                    'value': value,
                    
                    'number': {'valueformat': ',',
                              'font': {'size': 50}},
                    'domain': {'y': [0, 1], 'x': [0, 1]}}],
            'layout': go.Layout(
                title={'text': "No Of Vaccines"},
                font=dict(color=dash_colors['red']),
                paper_bgcolor=dash_colors['background'],
                plot_bgcolor=dash_colors['background'],
                height=200
                )
            }
@app.callback(
    Output('worldwide_trend', 'figure'),
    [Input('global_format', 'value'),
     ])
def worldwide_trend(view):
    '''
    creates the upper-left chart (aggregated stats for the view)
    '''
    if view == 'Worldwide':
        df = df_worldwide1
    elif view == 'United States':
        df = df_usa
        
    elif view == 'Europe':
        df = df_belgium
    elif view == 'China':
        df = df_china1
    elif view == 'Pfizer':
        df = df_pfizer
    elif view == 'Competitor':
        df = df_colaborator
    elif view == 'Pfizer&Comp':
        df = df_pfizer1
    else:
        df = df_worldwide
    title_suffix = ''
    
    t=df['Phase'].value_counts().sort_index()
    j=pd.DataFrame(t)

    traces = [go.Bar(
                    x=j.index,
                    y=j['Phase'],
                    text=j['Phase'],
                    textposition='auto',

                    ),
        
        
        
                ]
    return {
            'data': traces,
            'layout': go.Layout(
                title="{} Specific Phase wise drugs{}".format(view, title_suffix),
                xaxis_title="Phases",
                yaxis_title="Number of drugs",
                font=dict(color=dash_colors['text']),
                paper_bgcolor=dash_colors['background'],
                plot_bgcolor=dash_colors['background'],
                xaxis=dict(gridcolor=dash_colors['grid']),
                yaxis=dict(gridcolor=dash_colors['grid'])
                )
            }



@app.callback(
    Output('confirmed_ind', 'figure'),
    [Input('global_format', 'value')])
def confirmed(view):
    '''
    creates the CUMULATIVE CONFIRMED indicator
    '''
    if view == 'Worldwide':
        df = df_worldwide1
    elif view == 'United States':
        df = df_usa
    elif view == 'Europe':
        df = df_belgium
    elif view == 'China':
        df = df_china1
    elif view == 'Pfizer':
        df = df_pfizer
    elif view == 'Competitor':
        df = df_colaborator
    elif view == 'Pfizer&Comp':
        df = df_pfizer1
    else:
        df = df_worldwide

    value = df['EnrollmentCount'].sum()
    
    return {
            'data': [{'type': 'indicator',
                    'mode': 'number',
                    
                    'value': value,
                    
                    'number': {'valueformat': ',',
                              'font': {'size': 50}},
                    'domain': {'y': [0, 1], 'x': [0, 1]}}],
            'layout': go.Layout(
                title={'text': "Total Enrollments"},
                font=dict(color=dash_colors['red']),
                paper_bgcolor=dash_colors['background'],
                plot_bgcolor=dash_colors['background'],
                height=200
                )
            }

@app.callback(
    Output('active_countries', 'figure'),
    [Input('global_format', 'value'),
     
     
     ])
def active_countries(view):
    '''
    creates the upper-right chart (sub-region analysis)
    '''
    if view == 'Worldwide':
        df = df_worldwide1
    elif view == 'United States':
        df = df_usa
    elif view == 'Europe':
        df = df_belgium
    elif view == 'China':
        df = df_china1
    elif view == 'Pfizer':
        df = df_pfizer
    elif view == 'Competitor':
        df = df_colaborator
    elif view == 'Pfizer&Comp':
        df = df_pfizer1
    else:
        df = df_worldwide
    title_suffix=''



    traces = [go.Pie(
                    labels=df['DesignPrimaryPurpose'],hole=.5
                    
                    
                    
                    
                    ),
                ]
    
    return {
            'data': traces,
            'layout': go.Layout(
                    title="{} Specific Primary Purpose{}".format(view, title_suffix),
                    xaxis_title="Primary purpose",
                    yaxis_title="Primary purpose type count",
                    font=dict(color=dash_colors['text']),
                    paper_bgcolor=dash_colors['background'],
                    plot_bgcolor=dash_colors['background'],
                    xaxis=dict(gridcolor=dash_colors['grid']),
                    yaxis=dict(gridcolor=dash_colors['grid']),
                    hovermode='closest'
                )
            }

@app.callback(
    Output('worldwide_trend1', 'figure'),
    [Input('global_format', 'value')
     ])
def worldwide_trend1(view):
    '''
    creates the upper-left chart (aggregated stats for the view)
    '''
    if view == 'Worldwide':
        df = df_worldwide1
    elif view == 'United States':
        df = df_usa
        
    elif view == 'Europe':
        df = df_belgium
    elif view == 'China':
        df = df_china1
    elif view == 'Pfizer':
        df = df_pfizer
    elif view == 'Competitor':
        df = df_colaborator
    elif view == 'Pfizer&Comp':
        df = df_pfizer1
    else:
        df = df_worldwide
    title_suffix=''
    

    traces = [go.Pie(
                    labels=df['LocationStatus'],
                    ),
        
        
        
                ]
    return {
            'data': traces,
            'layout': go.Layout(
                title="{} Specific Recruitment Status{}".format(view, title_suffix),
                xaxis_title="Phases",
                yaxis_title="Number of drug",
                font=dict(color=dash_colors['text']),
                paper_bgcolor=dash_colors['background'],
                plot_bgcolor=dash_colors['background'],
                xaxis=dict(gridcolor=dash_colors['grid']),
                yaxis=dict(gridcolor=dash_colors['grid'])
                )
            }
@app.callback(
    Output('worldwide_trend2', 'figure'),
    [Input('global_format', 'value')
     ])
def worldwide_trend2(view):
    '''
    creates the upper-left chart (aggregated stats for the view)
    '''
    if view == 'Worldwide':
        df1 = df_worldwide1
    elif view == 'United States':
        df1 = df_usa
        
    elif view == 'Europe':
        df1 = df_belgium
    elif view == 'China':
        df1 = df_china1
    elif view == 'Pfizer':
        df1 = df_pfizer
    elif view == 'Competitor':
        df1 = df_colaborator
    elif view == 'Pfizer&Comp':
        df1 = df_pfizer1
    else:
        df1 = df_worldwide
    title_suffix=''
    df1['CompletionDate']=pd.to_datetime(df1['CompletionDate']).dt.date
    
    t1=df1[df1['CompletionDate']>today1]
    t2=t1.head(10)
    k=[]
    for i in range(len(t2)):
        j=t2['CollaboratorName'].iloc[i]
        lk=t2['EnrollmentCount'].iloc[i]
        lk1=t2['LocationCountry'].iloc[i]
        lk2=t2['LeadSponsorName'].iloc[i]
        k.append(f"Collaborator:{j}\n,Enrollment:{lk}\n, Country:{lk1}\n,Sponsor:{lk2}")
    traces = [go.Scatter(x=t2['CompletionDate'], y=t2['NCTId'],text=k,hovertemplate = "<b>%{text}</b><br><br>"),]
    return {
            'data': traces,
            'layout': go.Layout(
                title="{} Specific Top 10 Completion date of the project{}".format(view, title_suffix),
                xaxis_title="Completion Date",
                
                font=dict(color=dash_colors['text']),
                paper_bgcolor=dash_colors['background'],
                plot_bgcolor=dash_colors['background'],
                xaxis=dict(gridcolor=dash_colors['grid']),
                yaxis=dict(gridcolor=dash_colors['grid'],
                )
                )
            }

@app.callback(
    Output('worldwide_trend3', 'figure'),
    [Input('global_format', 'value')
     ])
def worldwide_trend3(view):
    '''
    creates the upper-left chart (aggregated stats for the view)
    '''
    if view == 'Worldwide':
        df1 = df_worldwide1
    elif view == 'United States':
        df1 = df_usa
        
    elif view == 'Europe':
        df1 = df_belgium
    elif view == 'China':
        df1 = df_china1
    elif view == 'Pfizer':
        df1 = df_pfizer
    elif view == 'Competitor':
        df1 = df_colaborator
    elif view == 'Pfizer&Comp':
        df1 = df_pfizer1
    else:
        df1 = df_worldwide
    title_suffix=''
    df1['CompletionDate']=pd.to_datetime(df1['CompletionDate']).dt.date
    t1=df1[df1['CompletionDate']>today1]
    
    
    
    traces = [go.Table(
    header=dict(values=['<b>NCTId<b>','<b>SponsorName<b>','<b>Collab.Name<b>','<b>Primary<br>Purpose<b>','<b>Phase<b>','<b>Enrollment<br>Count<b>','<b>Completion<br>Date<b>','<b>Country<b>','<b>Location<br>Status<b>',],
                fill_color='#A52A2A',
                line_color='white',
                align='left',
                font=dict(color='white', size=13),
                height=40),
                
    cells=dict(values=[t1.NCTId,t1.LeadSponsorName,t1.CollaboratorName, t1.DesignPrimaryPurpose, t1.Phase, t1.EnrollmentCount,t1.CompletionDate, t1.LocationCountry,t1.LocationStatus],
               fill_color='#A52A2A',
               line_color='darkslategray',
               align='left'))
        
        
        
                ]
    return {
            'data': traces,
            'layout': go.Layout(
                title="{} Data Summary{}".format(view, title_suffix),
                height=800,
            
                font=dict(color='white'),
                paper_bgcolor='black',
                plot_bgcolor='black',
                xaxis=dict(gridcolor=dash_colors['grid']),
                yaxis=dict(gridcolor=dash_colors['grid'])
                )
            }
@app.callback(
    Output('worldwide_trend9', 'figure'),
    [Input('global_format', 'value')
     ])
def worldwide_trend9(view):
    '''
    creates the upper-left chart (aggregated stats for the view)
    '''
    if view == 'Worldwide':
        df1 = df_enrollment
    elif view == 'United States':
        df1 = df_enrollment
        
    elif view == 'Europe':
        df1 = df_enrollment
    elif view == 'China':
        df1 = df_enrollment
    elif view == 'Pfizer':
        df1 = df_enrollment
    elif view == 'Competitor':
        df1 = df_enrollment
    elif view == 'Pfizer&Comp':
        df1 = df_enrollment
    else:
        df1 = df_enrollment
    
    
    
    
    
    traces = [go.Table(
    header=dict(values=['<b>date<b>','<b>NCT04381962<b>','<b>NCT04412252<b>','<b>NCT04469114<b>','<b>NCT04535167<b>','<b>NCT04575610<b>','<b>NCT04366050<b>','<b>NCT04588480<b>','<b>NCT04368728<b>',],
                fill_color='#A52A2A',
                line_color='white',
                align='left',
                font=dict(color='white', size=13),
                height=40),
                
    cells=dict(values=[df1.date,df1.NCT04381962,df1.NCT04412252, df1.NCT04469114, df1.NCT04535167, df1.NCT04575610,df1.NCT04366050, df1.NCT04588480,df1.NCT04368728],
               fill_color='#A52A2A',
               line_color='darkslategray',
               align='left'))
        
        
        
                ]
    return {
            'data': traces,
            'layout': go.Layout(
                title="PFIZER Enrollment count details from OCT 14th",
                height=400,
            
                font=dict(color='white'),
                paper_bgcolor='black',
                plot_bgcolor='black',
                xaxis=dict(gridcolor=dash_colors['grid']),
                yaxis=dict(gridcolor=dash_colors['grid'])
                )
            }
@app.callback(
    Output('world_map', 'figure'),
    [Input('global_format', 'value')
     ])
def world_map(view):
    '''
    creates the lower-left chart (map)
    '''
    if view == 'Worldwide':
        df = df_worldwide2
        scope = 'world'
        projection_type = 'natural earth'
        sizeref = 10
    elif view == 'United States':
        scope = 'usa'
        projection_type = 'albers usa'
        df = df_worldwide2
        sizeref = 7
    elif view == 'Europe':
        df = df_worldwide2
        scope = 'europe'
        projection_type = 'natural earth'
        sizeref = 15
    elif view == 'China':
        df = df_worldwide2
        scope = 'asia'
        projection_type = 'natural earth'
        sizeref = 3
    elif view == 'Pfizer':
        scope = 'usa'
        projection_type = 'albers usa'
        df = df_worldwide2
        sizeref = 7
        df = df_worldwide2
    elif view == 'Competitor':
        scope = 'usa'
        projection_type = 'albers usa'
        df = df_worldwide2
        sizeref = 7
        df = df_worldwide2
    elif view == 'Pfizer&Comp':
        scope = 'usa'
        projection_type = 'albers usa'
        df = df_worldwide2
        sizeref = 7
        df = df_worldwide2
    else:
        df = df_worldwide2
        scope = 'world'
        projection_type = 'natural earth',
        sizeref = 10
    g = df
    return {
            'data': [
                go.Scattergeo(
                    lon = g['Longitude'],
                    lat = g['Latitude'],
                    text = g['text'],
                    hoverinfo = 'text',
                    
                    mode = 'markers',
                    marker = dict(reversescale = False,
                        autocolorscale = False,
                        symbol = 'circle',
                        
                        sizeref = sizeref,
                        sizemin = 0,
                        line = dict(width=.5, color='rgba(0, 0, 0)'),
                        colorscale = 'Reds',
                        cmin = 0,
                        
                        
                        )
                    
                    )
            ],
            'layout': go.Layout(
                title ='Clinical Trial Information<br>(Hover for country count)',
                geo=dict(scope=scope,
                        projection_type=projection_type,
                        showland = True,
                        landcolor = "rgb(100, 125, 100)",
                        showocean = True,
                        oceancolor = "rgb(80, 150, 250)",
                        showcountries=True,
                        showlakes=True),
                        height=650,
                
                font=dict(color=dash_colors['text']),
                paper_bgcolor=dash_colors['background'],
                plot_bgcolor=dash_colors['background']
            )
        }







app.layout = html.Div(style={'backgroundColor': dash_colors['background']}, children=[
    html.H1(children='COVID-19(Clinical Trials/Drugs)',
        style={
            'textAlign': 'center',
            'color': dash_colors['text']
            }
        ),
    html.Div(children='Data last updated {}'.format(g), style={
        'textAlign': 'center',
        'color': dash_colors['text']
        }),
    
    html.Div(children='Select focus for the dashboard:', style={
        'textAlign': 'center',
        'color': dash_colors['text']
        }),
    

    html.Div(dcc.RadioItems(id='global_format',
            options=[{'label': i, 'value': i} for i in ['Worldwide', 'United States', 'Europe', 'China','Pfizer','Competitor','Pfizer&Comp']],
            value='Worldwide',
            labelStyle={'float': 'center', 'display': 'inline-block'}
            ), style={'textAlign': 'center',
                'color': dash_colors['text'],
                'width': '100%',
                'float': 'center',
                'display': 'inline-block'
            }
        ),

    
    html.Div(dcc.Graph(id='active_ind'),
        style={
            'textAlign': 'center',
            'color': dash_colors['red'],
            'width': '33%',
            'float': 'left',
            'display': 'inline-block'
            }
        ),
    html.Div(dcc.Graph(id='deaths_ind'),
        style={
            'textAlign': 'center',
            'color': dash_colors['red'],
            'width': '33%',
            'float': 'left',
            'display': 'inline-block'
            }
        ),
    html.Div(dcc.Graph(id='confirmed_ind'),
        style={
            'textAlign': 'center',
            'color': dash_colors['red'],
            'width': '33%',
            'float': 'center',
            'display': 'inline-block'
            }
        ),
    

    

    html.H2(dcc.Markdown('Display Clinical Trial Breakdowns:'),
        style={
            'textAlign': 'center',
            'color': dash_colors['text'],
            'width': '100%',
            'float': 'center',
            'display': 'inline-block'}),

    

    html.Div(  # worldwide_trend and active_countries
        [
            html.Div(
                dcc.Graph(id='worldwide_trend'),
                style={'width': '50%', 'float': 'left', 'display': 'inline-block'}
                ),
            html.Div([
                dcc.Graph(id='active_countries'),
                html.Div(
                    style={'width': '50%', 'float': 'center', 'display': 'inline-block'})
                ],
                style={'width': '50%', 'float': 'right', 'vertical-align': 'bottom'}
            )],
        style={'width': '98%', 'float': 'center', 'vertical-align': 'bottom'}
        ),
    html.Div(  # worldwide_trend and active_countries
        [
            html.Div(
                dcc.Graph(id='worldwide_trend1'),
                style={'width': '50%', 'float': 'left', 'display': 'inline-block'}
                ),
            html.Div([
                dcc.Graph(id='worldwide_trend2'),
                html.Div(
                    style={'width': '50%', 'float': 'center', 'display': 'inline-block'})
                ],
                style={'width': '50%', 'float': 'right', 'vertical-align': 'bottom'}
            )],
        style={'width': '98%', 'float': 'center', 'vertical-align': 'bottom'}
        ),
    html.Div(  # worldwide_trend and active_countries
        
            html.Div(
                dcc.Graph(id='worldwide_trend3'),
                style={'width': '100%', 'float': 'left', 'display': 'inline-block'}
                )
        ),
    html.Div(  # worldwide_trend and active_countries
        
            html.Div(
                dcc.Graph(id='worldwide_trend9'),
                style={'width': '100%', 'float': 'left', 'display': 'inline-block'}
                )
        ),
    html.Div(  # worldwide_trend and active_countries
        
            html.Div(
                dcc.Graph(id='world_map'),
                style={'width': '100%', 'float': 'center', 'display': 'inline-block'}
                )
            
        
        ),
    
    


    

    html.Div(dcc.Markdown(' '),
        style={
            'textAlign': 'center',
            'color': dash_colors['text'],
            'width': '100%',
            'float': 'center',
            'display': 'inline-block'}),
    html.H1(children='Data Summary',
        style={
            'textAlign': 'center',
            'color': dash_colors['text']
            }
        ),
    
    

    

    
    
     
    html.Div([

    dcc.RadioItems(
        id='filter-query-read-write',
        options=[
            {'label': 'Read filter_query', 'value': 'read'},{'label': 'Write to filter_query', 'value': 'write'}
        ],
        value='read',
        style={'textAlign': 'center',
                            'color': dash_colors['text'],
                            'width': '100%',
                            'float': 'right',
                            'display': 'inline-block'
                            }
    ),

    html.Br(),

    dcc.Input(id='filter-query-input', placeholder='Enter filter query'),

    html.Div(id='filter-query-output'),

    html.Hr(),
    
    
    dash_table.DataTable(
        id='datatable-advanced-filtering',
        columns=[
            {'name': i, 'id': i, 'deletable': False} for i in t21.columns
            # omit the id column
            if i != 'id'
        ],
        data=t21.to_dict('records'),
        
        
        style_cell={
            'backgroundColor': '#A52A2A',
            'color': 'white     ',
            'fontWeight':'bold',
            'fontSize':15,
            'font-family':'Lucida Sans Unicode',
            'minWidth': 95, 'maxWidth': 95, 'width': 95,
            'whiteSpace': 'normal',
            
            
    
        },
        
        style_table={
        
        'overflowX': 'auto'
    },
        style_data={ 'border': '1px solid black' },
        style_header={ 'border': '2px solid black','backgroundColor': '#A52A2A' },
        
        editable=False,
        page_action='native',
        page_size=10,
        filter_action="native",
        page_current=0,
        
        
    
        
    ),

    
    html.Hr(),
    html.Div(id='datatable-query-structure', style={'whitespace': 'pre'})
]),
    html.Div(dcc.Markdown('''
            &nbsp;  
            &nbsp;  
            Built For Pfizer  
            Source data: https://clinicaltrials.gov/  
              
            '''),
            style={
                'textAlign': 'center',
                'color': dash_colors['text'],
                'width': '100%',
                'float': 'center',
                'display': 'inline-block'}
            )
        ])


if __name__ == '__main__':
    app.run_server(debug=True)
