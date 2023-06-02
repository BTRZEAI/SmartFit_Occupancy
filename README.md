# SmartFit Occupancy Dashboard
A Python Streamlit Dashboard app which displays, through Folium Maps, the occupancy data in percentages during the day, for all Brazilian gym Smart Fit franchises.

## Demo
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/btrzeai/smartfit_occupancy/main/SmartFit_Occupancy.py)

## Screenshot
![(image)](./Screenshot.png?raw=true)

## How to run this app
```
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Author
Beatriz Santos Ramos de Jesus

## But why, Bia?

As a sedentary and procrastinating human being, I sometimes sabotage myself in my fitness journey with lame excuses. For this project, I sought to build a tool to help me with one of my biggest annoyances when going to the gym: the crowding.
I have a very dynamic routine. Sometimes I exercise in São Paulo, other times I train in parents' city,  and sometimes I go to a gym along my route home. Thus, I have access to *multiple units* of the Smart Fit network. Additionally, since I visit different gyms, I have noticed that the demographics of each unit *vary*. Some have more teenagers, others have more adults, and some have more seniors. Each of these groups has a certain *distribution of attendance throughout the day*, on average. However, somehow, I always seem to end up in the most crowded unit of all. If I could only discover which are the patterns for every gym to use this on my behalf... While studying the company's website, I came across a graph displaying the flow of people for each unit, as a percentage of maximum occupation, which is updated hourly.

The following dashboard is created from the database available on "data" archive, based on  SmartFit website crawling and scrapping end result. I would like to credit @mybrother for helping me with the HTML understanding, in such a short span of time, to accomplish this project.

As a possible future research direction, I would like to explore the possibility of merging the dashboard with real-time web crawling. This would enable me to analyze in real time which gym has the least occupancy, allowing me to choose the least crowded unit as close to "real time" as possible. 
Additional filters may be added, such as specific webcrawling per state or per municipality, the availability of air conditioning, hot showers, hair dryers, parking, and other unit-specific characteristics.

_P.s.: To be honest, I don't truly believe this research will get me to hit the gym more often. I just wanted to train myself on De-estructured Data and embark on some python adventure. Took me much more time than I have imagined and it is not as good as I wanted it to be, but I am happy to share my accomplishes so far, as a enthusiast of programming that most of the times is just curious enough to get there._
