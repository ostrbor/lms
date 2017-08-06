# Cool auction

## INSTALLATION

**Requirements:**
- pipenv install fabric3 
- install docker
- install docker-compose

**Commands:**
1. git pull

2. fab build_dev

3. edit .env file

4. fab init_dev

Will be asked to create superuser

5. fab up_dev

6. fab down

To delete containers

7. fab test 

To run Unittests


## URLS SCHEMA
**1.Create user**

*api/v1/users/*

POST

Available to all visitors

**2.Get token**

*api/v1/tokens/*

POST

Base64 authorization required

**3.Create auction, view auctions**

*api/v1/auctions/*

POST, GET

Token authorization required. [Authorization: Token your-token]

**4.Auction details**

*api/v1/auctions/1/*

GET

Token authorization required. [Authorization: Token your-token]

**5.Make bid**

*api/v1/bids/*

POST

Token authorization required. [Authorization: Token your-token]
