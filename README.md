# Shopping Cart API Server
Shopping Cart API Server is a RESTFUL API Server based on Flask and use sqlite as database.

## APIs
- Add item to cart (API)
- Checkout from current cart (API)

## Installation (Local)
```
pip install -r requirements.txt
```
### Run Server
```
# /bin/bash
# 1.move to project dir
cd project
# 2.create demo database
python init_db.py
# 3.run flask server
python app.py
```


## Installation (Docker)
### Run Server
```
sudo docker run --rm -d -p 8000:8000 --name shopping_cart rejectsgallery/demo:sc-1.0
```

### Swagger Docs URL
```
http://127.0.0.1:8000/apidocs/#/default
```
### API Table
![image](src/swagger_api_table.png)



### Test Flow (Swagger)
1. /account/login
![image](src/swagger_step1.png)
2. /cart/add
![image](src/swagger_step2.png)
3. /cart/checkout
![image](src/swagger_step3.png)

## File Layout
![image](src/file_layout.png)

## Pytest APIs & Functions
```
cd project
pytest
```
