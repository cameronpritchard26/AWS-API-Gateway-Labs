# AWS-API-Gateway-Labs

This file has cmds and notes used to work this lab - [AWS API Gateway Tutorial](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway-tutorial.html).

The goal of this repo is:
- Deploy an API method to API Gateway. The method will call a python Lambda function.
- Use AWS SSO login using a custom login created via AWS Organizations. Use this to access the console and CLI for these labs.
- Deploy an additional method to the first API (api.devcam.click)
- Setup HTML client to test API call


## Files
These are the files in the repo:
| Old File | New File |
|-----------------|-----------------|
| make_external_internet_api_call.py | src/get_stock_quote.py |
| test_make_external_internet_api_call.py | test/test_get_stock_quote.py |
| README.md | README.md 
| client/testApiCall.html | client/StockQuotes.html

## Steps

1. Create repo - include a README and a .gitignore for python
1. Create a virtual environment in the new repo -`python -m venv venv`
1. Copy and rename files
1. Scale down `README.md`
1. Ensure `src/get_stock_quote.py` is working
    - set up env var for API key -`export MARKETSTACK_API_KEY=[YOUR_KEY_HERE]`
1. Figure out how to handle requests. 
    - create a `deploy` folder 
    - install it there `pip install --target ./deploy requests`
    - copy the most recent copy of .py to ./deploy folder
1. Create the .zip
    - Zip up the *contents only* of the `deploy` folder (_while inside the folder - don't just zip the folder_)
1. Deploy it as a new Lambda - _delete the AWS resources from my old lab and create this again using this new repo._
    - Ensure the env var is setup
1. Test the Lambda. Create shared HappyPath and SadPath tests.
1. Wire up API Gateway as a new endpoint. Enable CORS so we can call it from other domains. Test using `curl` statements.
1. Update the HTML page so the textbox is the stock symbols and call the new API.
1. Test the HTML page. Locally first (c:\...\StockQuotese.html). Then deploy to IONOS and test via https://campritchard.com/StockQuotes.html
1. (Optional) Get the test to work. Update file names / locations, etc.
1. (Optional) Update `.gitignore` to ignore the `deploy` folder
1. (Optional) Write a shell script `deploy.sh`
    - copy current `scr/get_stock_quotes.py` file to `/deploy` folder
    - `cd deploy` to switch to the `deploy` folder
    - `zip ???` to zip up the contents of the folder into a file called `get_stock_objects.zip` in the root folder
    - `aws lambda update-function-code...` to update AWS. This would assume you are already logged in via `aws configure sso`

```
pip install --target ./deploy requests

aws lambda create-function --function-name GetStockQuote --zip-file fileb://get_stock_quote.zip --handler get_stock_quote.lambda_handler --runtime python3.12 --role arn:aws:iam::475530815984:role/service-role/lambda-apigateway-role --profile AdministratorAccess-475530815984

aws lambda update-function-code --function-name GetStockQuote --zip-file fileb://get_stock_quote.zip --profile AdministratorAccess-475530815984

curl -v -X OPTIONS https://6w3qds3iu8.execute-api.us-east-1.amazonaws.com/test/GetStockQuote
curl -v -X POST https://6w3qds3iu8.execute-api.us-east-1.amazonaws.com/test/GetStockQuote -d '{"data":{"symbols": "vz"}}'
curl -v -X POST https://api.devcam.click/GetStockQuote -d '{"data":{"symbols": "aapl"}}'

https://campritchard.com/labs/StockQuotes.html
```

### CSS to make the website look better
This [site](https://www.free-css.com/free-css-templates/page294/hirevac) has free CSS themes for websits. These will give us "resources" to help make the page look better.
I've stood up a copy of that template [here](http://absolutehero.com/csstest/). 
- By viewing the source, we can see stuff to cut/page into other pages.
- By using the Browser Developer Tools (F12), we can see how various items are marked up. Then we can update our test page to use similar tags.
=======
curl -v -X OPTIONS https://6w3qds3iu8.execute-api.us-east-1.amazonaws.com/test/HtmlJsService
curl -v -X POST https://6w3qds3iu8.execute-api.us-east-1.amazonaws.com/test/HtmlJsService -d '{"data":{"operation": "read","payload": {"Key": {"id": "5678EFGH"}}}}'
curl -v -X POST https://api.devcam.click/HtmlJsService -d '{"data":{"operation": "read","payload": {"Key": {"id": "5678EFGH"}}}}'
```


