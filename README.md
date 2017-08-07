# AUCTION

NOTE: currently enabled SessionAuthentication with TokenAuthentication
for easy testing in browser.

## INSTALLATION

**Requirements:**
- pipenv install fabric3 
- install docker
- install docker-compose

**Commands to set up environment:**

1. git pull

2. fab build_dev

3. edit .env file (set email settings)

4. fab init_dev (run twice if problems with container start order)

5. fab up_dev

6. fab down (delete containers)

7. fab test 

## URLS SCHEMA
Located by url *schema/*
