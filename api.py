import requests

url = "https://fast-currency-convertor.p.rapidapi.com/api/Fetch-Currency/"

querystring = {"amount": "100", "fromCurrency": "USD", "toCurrency": "AUD"}

headers = {
    "X-RapidAPI-Key": "f8815dad22mshce0f3b4c90be0d3p1724ffjsndf9ebcee49ad",
    "X-RapidAPI-Host": "fast-currency-convertor.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.text)
