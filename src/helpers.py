import requests
from requests.adapters import HTTPAdapter, Retry

# Set keys to constants to avoid 'magic' strings,
# since these keys are used in multiple methods
# to iterate through the response JSON object
FEATURES = 'features'
PROPERTIES = 'properties'
TYPE= 'type'
PLACE = 'place'
TIME = 'time'
MAG = 'mag'
CODE = 'code'

# Retry policy for https requests
def get_session(*arg_http_codes, retry_count):
  """
  Get resilient session with retry
  policy for https requests
  Arguments:
    arg_http_codes: a collection
    retry_count: an integer
  Returns:
    Session
  """
  # If invalid retry_count, set to 3
  retry_count = retry_count if isinstance(retry_count, int) and retry_count >= 0 else 3
  arg_http_codes = [code for code in arg_http_codes if isinstance(code, int) and code > 0]
  retry_policy = Retry(total=retry_count, backoff_factor=1, status_forcelist=arg_http_codes)
  s = requests.Session() 
  s.mount("https://", HTTPAdapter(max_retries=retry_policy))
  return s



"""
Submenu to all input of a code to provide a user
with the correct URL for the detail geojson data set
Arguments:
  data: a dictionary (JSON object)
Returns:
  None
"""
def get_by_code(data):
  user_input = ''
  while(user_input != "r"):
    print("********************************************************************")
    print("Input 'r' at any time and press ENTER to return to MAIN MENU!")
    print("********************************************************************")
    user_input = input('To get URL from initial data set, input code and then press ENTER: ').strip().lower()
    if user_input == 'r':
      break;
    item = next(iter([quake for quake in data if (quake.get(PROPERTIES, {}).get(CODE, {}) or "") == user_input]), None)

    # If no user input
    if len(user_input.strip()) == 0:
      print(f"PLEASE ENTER VALID INPUT!")
      continue

    # If code matches user input
    if item:
      print(f"Detail geojson data set URL: {item.get(PROPERTIES, {}).get('detail')}")
    else:
      print(f"code '{user_input}' not found...\n")

  print("Exiting to main menu...\n")
