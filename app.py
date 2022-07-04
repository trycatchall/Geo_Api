import time
from helpers import FEATURES, MAG, PLACE, PROPERTIES, TIME, TYPE, get_by_code, get_session

# Requirement: Allow querying ALL earthquakes over the past 7 days and from that data set,
# print the PLACE of all earthquakes with a magnitude over 4.5 for the last day in order
# of highest to lowest magnitude.
def query_7_days():
  """
  Gets all earthquakes over the past 7 days and prints
  the place of all earthquakes with a mag over 4.5 for
  the last day (24 hours) in order from highest to lowest
  mag.

  Arguments:
    None
  Returns:
    None
  """

  """ Retry for 502, 503, or 504 response codes """
  s = get_session(502, 503, 504, retry_count=4)
  data = s.get('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson').json()

  # If no data received, exit function
  if len(data) == 0:
    print("No data received from request")
    return

  """ Current GMT time - 24 hours in unix time """
  now = int(time.time_ns() / 1000000)
  last_day = now - (24 * 60 * 60 * 1000)

  # Use coercion when comparing the 'time' and 'mag' properties,
  # in case those properties do not exist for the object in focus.
  # IMPORTANT: filter by 'earthquake', as data can contain 'ice quake'
  # and 'quarry blast'
  earthquakes = [quake for quake in data.get(FEATURES, {})
                if (quake.get(PROPERTIES, {}).get(TIME, {}) or last_day ) > last_day
                and (quake.get(PROPERTIES, {}).get(MAG, {}) or 4.5) > 4.5
                and (quake.get(PROPERTIES, {}).get(TYPE, {}) or '') == 'earthquake']
  # Sort filtered earthquakes in place by magnitude in descending order
  earthquakes.sort(key=lambda x: x.get(PROPERTIES, {}) and x.get(PROPERTIES, {}).get(MAG, {}), reverse=True)

  # If no earthquakes found matching
  # parameters, print message
  if len(earthquakes) == 0:
    print("No data found in data set that matches 'time', 'mag' and 'type' parameters...\n")
  else:
    # Print earthquakes matching parameters
    print('****** PLACES WITH EARTHQUAKES OVER THE PAST 7 DAYS WITH A MAGNITUDE OF OVER 4.5 - SORTED BY MAG *****')
    for earthquake in earthquakes:
      print(f"{earthquake.get(PROPERTIES, {}).get(PLACE, {})}")
    print("******************************************************************************************************\n")

  # Proceed to submenu to get URL from
  # the *INITIAL* JSON dataset
  get_by_code(data.get(FEATURES))



# Requirement: Allow querying ALL earthquakes for the last 30 days and from that data set,
# print each state or country along with the number of earthquakes that occurred.
def query_30_days():
  """
  Query all earthquakes for last 30 days and print each
  state or country along with the earthquake count.

  Arguments:
    None
  Returns:
    None
  """

  """ Retry for 502, 503, or 504 response codes """
  s = get_session(502, 503, 504, retry_count=4)
  data = s.get('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson').json()

  # If no data received, exit function
  if len(data) == 0:
    print("No data received from request")
    return

  # map_data will store key, value of place and earthquake count
  map_data = {}
  # Make sure to filter for 'earthquakes' since 'ice quakes' and 'quary blast' also occur
  earthquakes = [quake for quake in data.get(FEATURES, {}) if (quake.get(PROPERTIES, {}).get(TYPE, {}) or '') == 'earthquake']
  for k in earthquakes:
    place = k.get(PROPERTIES, {}).get(PLACE, {})
    if place and len(place.strip()) > 0: # if place has valid data
      place = place.split(', ')[-1].strip() # get place from string
      map_data[place] = map_data[place] + 1 if map_data.get(place) else 1 # set earthquake count for place
    else:
      print('Place was not able to be retrieved during deserialization...')

  # It is possible that we received data from request, but have
  # no data that matches all keys (features, properties, and place)
  # or parameters
  if len(map_data) == 0:
    print("No data found in data set for the given parameters...\n")
  else:
    print("\n***************** EARTHQUAKE COUNT FOR STATES AND COUNTRIES FOR THE LAST 30 DAYS *********************")
    for k, v in map_data.items():
      print(f"{k}: {v}")
    print("******************************************************************************************************\n")

  # Proceed to submenu to get URL from
  # the *INITIAL* JSON dataset
  get_by_code(data.get(FEATURES))



# Submenu for 7-day and 30-day query methods
def match_input(user_input):
  """
  Run method based on user input.
  Arguments:
    user_input: a string
  Returns:
    None
  """
  user_input = user_input.lower()
  match user_input:
    case 's':
      query_7_days()

    case 't':
      query_30_days()
    
    case _:
      print("PLEASE CHOOSE A VALID OPTION!\n")


# Main menu for console application
menu = "\
******************************************** MAIN MENU ***********************************************\n\
'q'-Quit\n\
's'- Print all earthquakes for past (7) days\n\
't'- Print earthquake count for countries and states for past (30) days\n\
******************************************************************************************************\n"
userInput = ''
while(userInput != 'q'):
  print(menu)
  userInput = input("Enter your option, then press ENTER: ").strip().lower()
  print()
  if(userInput != 'q'):
    try:
      match_input(userInput)
    except:
      print("ERROR RUNNING QUERY...")
  else:
    print("Quitting...")