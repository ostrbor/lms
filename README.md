# Cool auction
## INSTALLATION
**Requirements**:
- pipenv install fabric3 
- install docker
- install docker-compose

1. git pull

2. fab build_dev

3. edit .env file

4. fab init_dev
Will be asked to create superuser

5. fab up_dev

6. fab down
To delete containers

## URLS SCHEMA
1.
*api/v1/users/*
POST
Create user.
Available to all visitors. 
2.
*api/v1/tokens/*
POST
Get token.
Base64 authorization required.
3.
*api/v1/auctions/*
POST, GET
Create auction, view auctions.
Token authorization required. [Authorization: Token <your-token>].
4.
*api/v1/auctions/1/*
GET
Auction details.
Token authorization required. [Authorization: Token <your-token>].
5.
*api/v1/bids/*
POST
Make bid.
Token authorization required. [Authorization: Token <your-token>].
