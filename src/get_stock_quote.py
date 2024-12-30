import requests, json, os, time
import logging

if len(logging.getLogger().handlers) > 0:
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)

def callMarketStackApi(symbols):
  # result is an object that contains values from the API call
  result = {}
  result["error"] = ""

    # Enter your API key here
  api_key = os.environ['MARKETSTACK_API_KEY']
  
  # base_url variable to store url - GET https://api.marketstack.com/v2/eod?access_key=YOUR_ACCESS_KEY&symbols=AAPL
  base_url = "https://api.marketstack.com/v2/eod?"
  
  # complete_url variable to store
  # complete url address
  complete_url = base_url + "access_key=" + api_key + "&symbols=" + symbols
  print(complete_url)
  
  # get method of requests module
  # return response object
  response = requests.get(complete_url)
  result["http_status_code"] = response.status_code
  # check for errors
  if response.status_code != 200:
      # logging.error("Error: ", response.status_code)
      # logging.error("Message: ", response.json()['error']['message'])
      result["error"] = "Error: " + str(response.status_code) + " Message: " + str(response.json()['error']['message'])

      return result

  # we got a valid response, let's parse it
  resp = response.json()

  # Ensure we have some data
  if resp["data"][0]["date"] > "":
      result["vopen"] = resp["data"][0]["open"]
      result["vclose"] = resp["data"][0]["close"]
      result["vlow"] = resp["data"][0]["low"]
      result["vhigh"] = resp["data"][0]["high"]
      result["vdate"] = resp["data"][0]["date"]
    
      # print following values
      # logging.info(" Open = " +
      #                 str(result["vopen"]) +
      #       "\n Close = " +
      #                 str(result["vclose"]) +
      #       "\n High = " +
      #                 str(result["vhigh"]) +
      #       "\n Low = " +
      #                 str(result["vlow"]) +
      #       "\n Date = " +
      #                 str(result["vdate"]))
  
  else:
      result["error"] = "Could not parse response. response data = " + resp["data"]

  return result

def lambda_handler(event, context):
    '''Provide an event that contains the following keys:
      - operation: one of the operations in the operations dict below
      - payload: a JSON object containing parameters to pass to the 
        operation being performed
    '''
    logging.info("lambda_handler started")
    logging.info(event)

    data = event['data']

    symbols = data['symbols']
    result = callMarketStackApi(symbols)


    if result["error"] == "":
        # return the timestamp as part of the response
        timestamp = time.time()
        timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

        returnVal = json.dumps(result) + " at " + timestamp_str + " using a payload of " + str(symbols)

        return returnVal
        
    else:
        raise ValueError(f'Unrecognized operation "{result["error"]}"')
    
if __name__ == "__main__":
  logging.info("running locally")
  event = {
  "data": {
    "symbols": "AAPL"
  }
}
  context = []
  logging.info("final results from handler is: " + lambda_handler(event, context))
