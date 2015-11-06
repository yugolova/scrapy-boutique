# scrapy-boutique

Get information about each product in the online boutique shop by using

```
scrapy crawl oxygenboutique.com -o items.json -t json
```

example of item's dictionary:

```json
{"code": "Hiltrud-Shirt-with-Side-Panels",
"name": "Alexis Hiltrud Shirt with Side Panels",
"gbp_price": 147.5,
"usd_price": 225.68,
"eur_price": 206.5,
"sale_discount": 50.0,
"gender": "F",
"type": "A",
"stock_status": {"XS": 3, "S": 1, "M": 3, "L": 1},
"designer": "Alexis",
"link": "http://www.oxygenboutique.com/Hiltrud-Shirt-with-Side-Panels.aspx", 
"raw_color": "white", 
"images": ["http://www.oxygenboutique.com/GetImage/cT0xMDAmdz04MDAmaD02MDAmUEltZz04YjBjY2QxYi1lZjJlLTQ2MzItYTgyZi1lZTI2ZDg1OTdiZGEuanBn0.jpg", "http://www.oxygenboutique.com/GetImage/cT0xMDAmdz04MDAmaD02MDAmUEltZz0zNjIxNjhlMy00OTE5LTQ1Y2YtOTE5ZC0zODY2NGM4ZDQ5ZmEuanBn0.jpg"], 
"description": "Hiltrud Shirt with Side Panels by Alexis. Push aside your collared white shirts and make way for this cool, contemporary piece. A flattering V neckline is married with bell sleeves and side panels to match. "}
```
