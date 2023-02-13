from datetime import datetime
from pymongo import MongoClient
import dns
from src.settings.config import DB_USER_KEY, DB_PASS_KEY

cluster = MongoClient("mongodb+srv://alexndrev:alexndrev@cluster0.vgyfitw.mongodb.net/?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE", connect=False)
db = cluster[f"DATABASE"]  


async def add_userGlobal(user_id, full_name, username):
    date = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    db["global"].insert_one({
        "_id" : user_id,
        "full_name" : full_name,
		"username" : username,
        "joining_date" : str(date),     # Date when user joined to Bot
        "allowedRequests" : 1,          # Extra Request
        "currentTariff": "Non Paid",     # Limited / Unlimited
        "expiryDate" : " ",             # If tariff Unlimited
        "isPaid" : False,               # If you're using Extra Request eqauls False
        "totalRequested": 0,
        "userPosition" : 'User',
        "DATA" : 'global'
    })


async def get_userPosition(user_id):
    userPosition = db[f"global"].find_one({
        "_id": user_id
    })["userPosition"]
    return userPosition

async def get_joiningDateGlobal(user_id):
    joining_date = db[f"global"].find_one({
        "_id": user_id
    })["joining_date"]
    return joining_date

async def get_allowedRequests(user_id):
    allowedRequests = db[f"global"].find_one({
        "_id": user_id
    })["allowedRequests"]
    return allowedRequests

async def get_isPaid(user_id):
    isPaid = db[f"global"].find_one({
        "_id": user_id
    })["isPaid"]
    return isPaid

async def get_currentTariff(user_id):
    currentTariff = db[f"global"].find_one({
        "_id": user_id
    })["currentTariff"]
    return currentTariff
    
async def get_expiryDate(user_id):
    expiryDate = db[f"global"].find_one({
        "_id": user_id
    })["expiryDate"]
    return expiryDate

async def update_allowedRequests(user_id, index):
    db["global"].update_one({
        "_id" : user_id
        },
        {
            "$set" : {
                "allowedRequests" : index
                }
            }, upsert=False)


async def update_userPosition(user_id, index):
    db["global"].update_one({
        "_id" : user_id
        },
        {
            "$set" : {
                "userPosition" : f'{index}'
                }
            }, upsert=False)

async def update_allowedRequests2(user_id, index):
    db[f"global"].update_one({
        "_id" : user_id
        },
        {
            "$inc" : {
                "allowedRequests" : index
                }
            }, upsert=False)     

async def update_totalRequested(user_id, index):
    db[f"global"].update_one({
        "_id" : user_id
        },
        {
            "$inc" : {
                "totalRequested" : index
                }
            }, upsert=False)  


async def update_expiryDate(user_id, index):
    db["global"].update_one({
        "_id" : user_id
        },
        {
            "$set" : {
                "expiryDate" : f"{index}"
                }
            }, upsert=False)


async def update_currentTariff(user_id, index):
    db["global"].update_one({
        "_id" : user_id
        },
        {
            "$set" : {
                "currentTariff" : f"{index}"
                }
            }, upsert=False)


async def update_isPaid(user_id, index):
    db["global"].update_one({
        "_id" : user_id
        },
        {
            "$set" : {
                "isPaid" : index
                }
            }, upsert=False)


async def increment_allowedRequests(user_id):
    db[f"global"].update_one({
        "_id" : user_id
        },
        {
            "$inc" : {
                "allowedRequests" : -1
                }
            }, upsert=False)