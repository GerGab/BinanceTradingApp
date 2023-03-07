# PERSONAL BINANCE BOT SERVER (PBBS)

![GitHub last commit](https://img.shields.io/github/last-commit/GerGab/Personal-Binance-Bot-Server)
![GitHub](https://img.shields.io/github/license/GerGab/Personal-Binance-Bot-Server)


## DISCLAIMER

This flask server implements a trading bot with a simple strategy relying on MACD technical indicator. Personal Binace Bot Server is only meant to demonstrate a basic implementation of a flask server and the functionality of Python-Binance lib. **In no way is this bot considered a profitable or trustworthy strategy for trading. ***USE AT YOUR OWN RISK!*****

***
## ABOUT PBBS

PBBS can be run in several ways:

#### By creating a virtual environment and running a wsgi service
by default gunicorn is included in the requirements.txt:

    python -m venv venv
    pip install -r requirements.txt
    gunicorn :b :<PORT> -w 1 run:app

***NOTE :*** the amount of workers is set to 1 because the portfolioManager class is meant as a singleton, no testing has been done with more than one instance. It may cause duplication of buy and sell orders or misbehaviour. 

Even though this option is available, what still remains to be tested in order to have a reliable app is:
- A reverse proxy (Nginx for example) to loadbalance the app.
- In case the app crashes there is no watchdog implemented to started up again.
- Include a .env file with the necesary secrets.

#### By building a docker Container and run it as it is

**IMPORTANT :** 
Before pushing the Container to Docker repo keep in mind to create a ***.dockerignore*** file to avoid any sensitive information to be delivered publicly with your container.

    docker build . -t <USER>/<REPO>:<TAG>
    docker <USER>/<REPO>:<TAG> --push

Of course keep in mind the implementations that remains unhandled, reverse proxy, watchdog, and secrets.

### Runing the container on K8s or k3s cluster

In my case, I created a k3s sever on a raspberry pi cluster and run solved all the problems described above creating the adequate resources, such as Deployments, Secrets, PersistentVolumeClaims, Services and Ingress.
All this configuration is out of this git repo scope.

***
### PBBS CONFIGURATION

PPBS needs 6 main environment variables to run:

From a Binance account:

    API_KEY=<API_KEY>
    SECRET_KEY=<SECRET_KEY>

An admin username and password for login:

    ADMIN=<USERNAME>
    PASSWORD=<PASSWORD>

A secret for the JWT encoding:

    JWT_SECRET=<YOUR_SECRET>
    JWT_EXPIRE_TIME=<MINUTES> # optional but recommended

***
**NOTE** there are other optional secret environment variables

    MAIL_USER=<SENDER@EMAIL>
    MAIL_PASSWORD=<PASSWORD> # created through google API passwords
    MAIL_RECIPIENTS=<RECIPIENT@EMAIL>

This env variables will not play any role due to the fact that emailing is still not implemented. **Do not** set them unless you implement the SMTP service in the app/utils/emailSender.py file.

***IMPORTANT=>*** One last modification must be implemented. As a last safety mechanism this repo is configured to create mock orders. If you ever feel ready to invest for real replace the function ***"create_test_order()"*** with ***"create_order()"*** in the modules BuyOrders and SellOrders located in the path: 

> *./app/tradingApp/PortfolioManager/Orders*
***

### UNDER THE HOOD

Some minor explanation about how PBBS works.
Through apscheduler lib, every day a cronjob is performed at 00:00:00 am.

The PorfolioManager instance ask the TradingManager what's new in the market, and according to the algorithm especified responds with a dict of actions.

With this information the PortfolioManager sets sell and buy orders. For buy orders two extra steps take place; first ask RiskManager the amount to invest, in second place it filters through a balancer the amounts in case the total amount to invest is higher than the free amount of available USDT.

The RiskManager works on a basis of ATR technical indicator and support/resistances (estimated from historical data with k-means clusters) to determine how much may the value drop prior to make any profit. According to the risk established when the RiskManager gets instantiated it adjusts each amount accordingly.

***

### API REST

PBBS API REST works with the following Endpoints:

    -   server
    -   app

***Server*** endpoints are meant to bring information and control over the server. Functionalities such as login, start/pause the scheduler, get the logs file, etc.

#### Most significan endpoints

-   POST server/login 
> allows the admin to login and receive a JWT to act upon the other endpoints.
    
        BODY:
            {
            "username":<ADMIN>,
            "password":<PASSWORD>
            }
        
        =====
        response:
            {
            "Message": "access granted",
            "Result": "success",
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3ODAwODExOSwianRpIjoiMDkxOWZmOTgtNWViYy00NDUzLTg1OTItYWIwYTY1MDcwMzNkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imdlcm1hbmdnb256YWxleiIsIm5iZiI6MTY3ODAwODExOSwiZXhwIjoxNjc4MDA4NzE5fQ._ysT_jc66p5CdzVLCh5S4p_wENhCLSkFKDeIFpPLLRk"
            }
-   PUT server/start
> Including the JWT in the header as a bearer auth, allows the admin to start the scheduler on the server. By default the scheduler is initiated on server start up.
        
        HEADER:
            BEARER : <token>

        =====
        response:
            {
            "Message": "server succesfully started",
            "Result": "success"
            }
-   PUT server/pause
> Including the JWT in the header as a bearer auth, allows the admin to pause the scheduler on the server
        
        HEADER:
            BEARER : <token>

        =====
        response:
            {
            "Message": "server paused awaiting orders",
            "Result": "success"
            }

***app*** endpoints are available once a jwt is granted through the login endpoint. This endpoints are meant to work with the binance account and intervene in some of the possibilities the server provides.

#### Some functionalities described below:

-   GET app/balance
> The balance endpoint allows the admin to get an instant picture upon her/his spot wallet. There are three main fields: "inTokens" indicates the amount of assets, "liquid" the amount of USDT to trade, and "totalBalance" the approximate value of the wallet according to each asset market value.
        
        HEADER:
            BEARER : <token>

        =====
        response:
            {
            "Message": "Balance successfully recovered",
            "Result": "success",
            "data": {
                "inTokens": [
                {
                    "freeTokens": <string>,
                    "freeUSDT": <string>,
                    "lockedTokens": <string>,
                    "lockedUSDT": <string>,
                    "symbol": "ETHUSDT"
                },
                {
                    "freeTokens": <string>,
                    "freeUSDT": <string>,
                    "lockedTokens": <string>,
                    "lockedUSDT": <string>,
                    "symbol": "BNBUSDT"
                }
                ],
                "liquid": {
                "asset": "USDT",
                "free": <string>,
                "locked": <string>
                },
                "totalBalance": <string>
                }
            }

-   POST app/market
> market endpoint activates PortfolioManager's main function. It triggers the sequence mentioned before and places buy and sell orders accordingly. This is the main function triggered by the scheduler at midnight. The response is a dict of lists with the assets that need an specific action.

        HEADER:
            BEARER : <token>

        BODY:
            {} # for the moment it accepts any json object but no functionality is implemented around it.

        =====
        response:
            {
            "Message": "Market successfully verified",
            "Result": "success",
            "data": {
                "buy": [
                "BTCUSDT",
                "LTCUSDT",
                "ADAUSDT"
                ],
                "sell": [
                "ETHUSDT",
                "BNBUSDT",
                "XRPUSDT",
                "LINKUSDT",
                "MATICUSDT",
                "ATOMUSDT",
                "DOGEUSDT",
                "SOLUSDT",
                "DOTUSDT",
                "UNIUSDT",
                "AVAXUSDT",
                "SHIBUSDT"
                ]
            }
            }

Please feel free to check the other endpoints available at ./app/routes

***

### FUTURE THOUGHTS

As mentioned earlier this is just a beginner's project. It is far from being a professional app and needs major improvements.
Some ideas for future iterations:
    
- ***Implement a BNB holding controller***; this will allow the admin to automate the BNB amounts to hold in order to reduce the fees Binance apply by paying them with BNB tokens.
- ***Implement a stoploss controller***, this will allow the admin to set stoplosses according RiskManager's results. It can be done by utilizing the creation of a stoploss through Binance API or a local price watcher implementing a Binance websocket suscribed to the tokens in the wallet.
- ***Complete the SMTP service***, this will allow the admin to wrap functions with the service so its logs could be included in the body of an email to receive any news or errors that they believe are important.

***

### MAJOR DEPENDENCIES

- APScheduler==3.10.1
- Flask==2.2.3
- Flask-Cors==3.0.10
- Flask-JWT-Extended==4.4.4
- numpy==1.24.2
- pandas==1.5.3
- python-binance==1.0.17 -> https://python-binance.readthedocs.io/en/latest/
- scikit-learn==1.2.1

for the complete list check the ***requirements.txt*** file.



