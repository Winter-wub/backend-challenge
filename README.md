# Backend-challenge

## Requirement 🐱

- pipenv
- docker & docker-compose

## Command 🐱‍🏍

- 🏗 Install dependencies `pipenv sync`
- 🐍 Development Server `pipenv run flask run`
- 🐳 Production (Docker, docker-compose) `docker-compose up --build -d` \*\*Note: Production require cert.json for firestore service

## Route map 🚞

- product/
  - GET (Get a product with parameter product id)
  - POST (Create product)
  - PUT (Update product)
- products/
  - GET (Get product by type)
- customers/
  - GET (Get customer account List by role)
- customer/
  - POST (Create customer account )
  - PUT (Update customer account by document id)
- orders/
  - GET (Get order list from customer by customer document id)
- order/
  - POST (Create order for customer )
  - PUT (Update order )
- login/
  - POST (Login for customer)
