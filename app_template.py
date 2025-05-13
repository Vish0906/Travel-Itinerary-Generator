import streamlit as st
import pandas as pd
import datetime
import geonamescache
import openai
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import PageBreak
from io import BytesIO
import os

st.set_page_config(layout="wide")
#openai.api_key = st.text_input('OpenAI Api Key')

#add_selectbox = st.sidebar.selectbox(
#    "How would you like to be contacted?",
#    ("Email", "Home phone", "Mobile phone")
#)

custom_css = """
<style>
/* Custom CSS for Streamlit app */
body {
    background-color: #FFFFFF; /* Background color */
    color: #262730; /* Text color */
    font-family: sans-serif; /* Font family */
}

/* You can define more custom styles here as needed */
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Using "with" notation
with st.sidebar:
    openai.api_key = st.text_input('OpenAI Api Key')


def geo_data():
   #  geonames_df = pd.read_csv('cities15000.txt', sep='\t', header=None, names=['geonameid', 'name', 'asciiname', 'alternatenames', 'latitude', 'longitude', 'feature class', 'feature code', 'country code', 'cc2', 'admin1 code', 'admin2 code', 'admin3 code', 'admin4 code', 'population', 'elevation', 'dem', 'timezone', 'modification date'])
    city_to_country_dict = {}
    gc = geonamescache.GeonamesCache()
    for i, j in gc.get_cities().items():
      if j['countrycode'] in gc.get_countries():
         if j['countrycode'] in city_to_country_dict:
               city_to_country_dict[j['countrycode']].append(j['name'])
         else:
               city_to_country_dict[j['countrycode']] = [j['name']]
    city_to_country_dict2 = {}
    tmp = gc.get_countries()
    for i,j in city_to_country_dict.items():
       if i in gc.get_countries():
          city_to_country_dict2[tmp[i]['name']] = j

    return city_to_country_dict2

def create_pdf_with_formatted_text(pdf_filename, text_content):
    pdf_buffer = BytesIO()

    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)

    elements = []

    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.textColor = colors.black
    text_content = text_content.replace("|", "")
    paragraphs = text_content.split('\n')

    for paragraph in paragraphs:
        if paragraph.strip():  # Skip empty lines
            elements.append(Paragraph(paragraph, style))
            elements.append(Spacer(1, 12))  # Add some space between paragraphs

    doc.build(elements)

    with open(pdf_filename, 'wb') as f:
        f.write(pdf_buffer.getvalue())


if 'response' not in st.session_state:
    st.session_state['response'] = 'No Itinerary Generated!'

#st.title('Welcome to TravelEase.ai!')

col1, col2 = st.columns(2)



# using form so that changing a data point does not rerun
# the entire script 


preference_dict = {
   "filter_1":"Outdoor Activities",
   "filter_2":"Socializing & Nightlife",
   "filter_3":"Arts & Culture",
   "filter_4":"Food",
   "filter_5":"Festivals and Events"

}

st.title('Welcome to Inciditenary!')
col1, col2 = st.columns(2)
preferences_list = []
col_exp1,col_exp2 = st.columns(2)


with st.form("my_form"):
   with col1:
      col3, col4 = st.columns(2)
      today = datetime.date.today()
      tomorrow = today + datetime.timedelta(days=1)
      with col3:
         start_date = st.date_input('Start date', value=today,min_value=today,max_value=today + datetime.timedelta(days=90))
      with col4:
         end_date = st.date_input('End date', value=tomorrow,min_value=tomorrow,max_value=start_date + datetime.timedelta(45))
      
      if start_date>end_date:
         st.error('Error: End date must fall after start date.')
      # start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
      # end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
      date_diff = (end_date-start_date).days
      y = st.slider('Mention Your Budget', min_value=0, max_value=10000, step=1000)
      st.write("Budget:",y)

   with col2:
      col5, col6 = st.columns(2)
      col7, col8 = st.columns(2)
      gc = geonamescache.GeonamesCache()
      list_countries = sorted(list(gc.get_countries_by_names().keys()))
      with col5:
         countryf = st.multiselect("From", options=list_countries,default=None,max_selections=1)
         if len(countryf) >= 1:
            with col6:
               list_cities = geo_data()
               list_cities = sorted(list_cities[countryf[0]])
               cityf = st.multiselect("City", options=list_cities,default=None, max_selections=1)
      with col7:
         country = st.multiselect("To", options=list_countries,default=None,max_selections=1)
         if len(country) >= 1:
            with col8:
               list_cities = geo_data()
               list_cities = sorted(list_cities[country[0]])
               city = st.multiselect("City", options=list_cities,default=None)
    
               #y = st.slider('Mention Your Budget', min_value=0, max_value=1000000)
               #st.write("Budget:",y)

   
   preferences_list = []
   col_exp1,col_exp2 = st.columns(2)
   
   with col_exp1:
      with st.expander("Select Activities"):
         filter_1 = st.checkbox('Outdoor Activities')
         filter_2 = st.checkbox('Socializing & Nightlife')
         filter_3 = st.checkbox('Arts & Culture')
         filter_4 = st.checkbox('Food')
         filter_5 = st.checkbox('Festivals and Events')
         
         for i in range(1,6):
            if(eval("filter_"+str(i))):
               preferences_list.append(preference_dict["filter_"+str(i)])
   who_filter = "Friends"
   with col_exp2:
      with st.expander("Who do you plan on travelling with"):
         who_filter = st.radio(
      "Who do you plan on travelling with",
      ["Solo", "Family", "Couple","Friends"],label_visibility="hidden")

   submit_button = st.form_submit_button('Submit')


def generate_response(sys_message, human_message):
#   llm = OpenAI(temperature=0.8,openai_api_key=openai.api_key)
#   st.info(llm(sys_message))

  chat = ChatOpenAI(temperature=0.2,openai_api_key=openai.api_key, model='gpt-3.5-turbo')
  return chat([
    SystemMessage(content=sys_message)
      ]).content



# ref = {"Art and culture":filter_3,
#        "Food":filter_4,
#        "Socializing and nightlife":filter_2,
#        "Outdoor Activities":filter_1,
#        "Pace of activities": filter_5          
# }

total_cost = 0
day_cost = 0

if submit_button:
   system_prompt = f"""
   You are a virtual travel planner, assisting users with their travel plans by providing information based on their inputs.
   Offer tailored recommendations based on the user's responses to help them have a memorable and enjoyable trip. Below is some more context on their responses.
   ###
   Context:
   1. You are planning a trip from {cityf}, {countryf} to {city}, {country} for {date_diff+1} days. 
   2. {preferences_list} is a list of activities that a user wants to be included in their travel plan.
      a. if the list contains 'Outdoor Activities', prioritise recommending outdoor activities like hiking etc.
      b. if the list contains 'Socializing & Nightlife', prioritise recommending social activies and clubs, dancing etc.
      c. if the list contains 'Arts & Culture', prioritise recommending museums, art galleries, etc.
      d. if the list contains 'Food', prioritise recommending good restaurants within the price of {y}.
      e. if the list contains one or more of these activities, mix and match the recommendations.       
   3. User will be travelling in a {who_filter} setting. So make sure you tailor your reccomendation based on this attribute, ie:
      a. if the value is couple, prioritise recommending romantic things to do.
      b. if the value is family, prioritise recommending more family oriented activities.
      c. if the value is friends, prioritise recommending suited to a friend group.
      d. if the value is solo, prioritise recommending good solo activities.
   4. Include the time duration range for each output on the intinerary, e.g. if you recommend the explore Louvre in Paris you should also give a time range like [30 minutes - 120 minutes]
   5. Strictly Mention atleast one restaurant per day even if the {preferences_list} does not contain 'Food'. If the list contains 'Food', mention a few more restaurants 
   6. At the end of all the recommendations , please provide the approximate total cost it takes per day to complete the whole itenary of that specific day.
   ###
   
   Recommend atleast three places to visit for each day.
   Be sure to include web links to the places that you recommend. e.g. if you recommend the Louvre in Paris, include a hyperlink to its website in your response.
   At the end of all the recommendations , please provide the approximate total cost it takes to complete the whole itenary for all the days.
   Include the trasnportation costs as well. If you dont know the transportation fares of that country, just mention "(excluding transportation costs)"

   
   Make sure you separate each day by a pipe delimeter i.e "|" 

   ###
   Format your response in the following format:
   Day 1
      Name of the place along with a description
        -Time [Approximate Time]
        -Cost [Approximate Cost]
   .
   .
   .
   .
   .
   .
   .
      
      The total cost for the day is: 

   |
   
   Day 2
      Name of the place along with a description
        -Time [Approximate Time]
        -Cost [Approximate Cost]
   .
   .
   .
   .
   .
   .
   .
      
      The total cost for the day is: 
    

   |
   and so on..
 
   ***
   The total sum of the costs of all the days is:
   ***
   ###

   
   
   Your response:
   """
   #total_cost += day_cost

   # prompt = PromptTemplate(template=system_prompt, input_variables=['start_date','end_date','country','city','filter_1','filter_2','filter_3','filter_4'])
   sys_message = system_prompt
   # sys_message = "You are a travel advising AI bot that helps the user in planning itinerary for a user. the user will also provide their preferences for the following attributes {} with a score in the range 0-5. Where an attribute with a low score should be given a very low priotiy in the itinerary and  an attribute with a high value like 5 should be given high priority while planning the itinerary ".format(list(ref.keys()))
   human_message = "Hi Can you plan a travel for me to {},{} from {} to {} given the following qualities and their scores".format(city,country,start_date,end_date)
   basic_sys_message = f"""
   Can you find the the values of the following variables for {city}:
   1. Currency
   2. Electricity port type
   3. Time zone
   4. Most popular mode of transport 
   5. Population of the city

   Give me the output of this query as a python dictionary, the keys should be the variables 
   as stated above and the values should be the response you come up with, 
   if you are not able to find an the value of a key the value should be None
   The returned dictionary should not have any text outside curly braces"""

   facts_message = f"""
   Can you Provide the top 10 unknown facts about {city}
   The facts should be in the form of a numbered list.
   If you cannot find 10, display only the facts which you have encountered.
   Do not display the facts of any other city.
   """

   #first llm call
   

   tab1, tab2, tab3, tab4, tab5 = st.tabs(["Trip ","Basic Information", "Tourist Attractions", "Restaurants", "Total"])
   with tab1:
      st.header("Trip Info")
      with st.spinner('Creating your itinerary...'):
         trip_response = generate_response(sys_message,human_message)
         st.session_state['response'] = trip_response
      
      # tmp = generate_response(sys_message,human_message)
      
      
      try:
         pipe_count = trip_response.count('|')  
         trip_response_list = trip_response.split("|")
         if(date_diff+1==pipe_count):
            trip_response_list = trip_response_list[:-1]
         for i in range(len(trip_response_list)):
            with st.expander("Day"+str(i+1)):
               st.write(trip_response_list[i])
         st.write(trip_response.split("***"))

      except Exception as e:
         print(e)
         st.write("No response")

   basic_information_response = generate_response(basic_sys_message,human_message)

   with tab2:
      st.header("Basic Information")
     
      try:   
         basic_info_dict = eval(basic_information_response)
         print(basic_info_dict)
         df_basic_info = pd.DataFrame(basic_info_dict,index = [0])
         st.table(df_basic_info)

         facts_message_response = generate_response(facts_message,human_message)
         facts_message_response = facts_message_response.split("\n")
         city_str = str(city)
         st.write('<span style="font-size: 16px; font-weight: bold;">Some Interesting Facts:</span>', unsafe_allow_html=True)
         for it in facts_message_response:
            st.markdown(it)
      except:
         st.write("No response")

   safety_guidlines  = f"""
   The User will be travelling to {country} and {city}, can you list out the most popular
   tourist attractions which are specific to that {country} or {city} that a visitor might not know.
   Provide these attractions in the form of a bulleted list. 
   Display the names of the attractions in bold text.
   """
   
   #third llm call

   with tab3:
      st.header("Popular Tourist Attractions")
      with st.spinner('Fetching good places to go...'):
         safety_guidlines_response = generate_response(safety_guidlines,human_message)
         safety_guidlines_response = safety_guidlines_response.split("\n")
         try:
            for it in safety_guidlines_response:
               st.markdown(it)
            # something
         except:
            st.write("Nothing to show here")

   rest_cafe  = f"""
   The User will be travelling to {country} and {city}, can you list out the most popular
   restaurants present in that {city} and are well known or recommended by many.
   Provide these restaurants along with their address and some basic description one under the other in the form of a bulleted list.
   Display the restaurant's name in bold text and the address in italic.
   """

   with tab4:
      st.header("Must Try Restaurants")
      with st.spinner('Fetching you good food...'):
         rest_cafe_response = generate_response(rest_cafe,human_message)
         rest_cafe_response = rest_cafe_response.split("\n")
         try:
            for it in rest_cafe_response:
               st.markdown(it)
            # something
         except:
            st.write("Nothing to show here")

   
   total_cost = f"""
   Calculate the total cost from the above mentioned itenary and display it in bold text.
   Also if the total cost is less tha the value of {y}, then give some extra tips for what to do in the {city}.
   """


   with tab5:
      st.header("Total Expenditure")
      with st.spinner('Fetching how much you spent..'):
         total_cost_response = generate_response(total_cost,human_message)
         #total_cost_response = total_cost_response.split("\n")
         try:
            st.write(total_cost_response)
            # something
         except:
            st.write("Nothing to show here")
