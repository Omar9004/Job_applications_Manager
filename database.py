from pymongo import MongoClient
import argparse
client = MongoClient("mongodb://localhost:27017/")

db = client["JADatabase"] # Job applications database


def addColl(collName:str):
    if collName not in db.list_collection_names():
            db.create_collection(
                collName,
                validator = {
                    "$jsonSchema":{
                        "bsonType": "object",
                        "required":["id","Position Name", "Company", "Location", "Technologies/Programming Languages",
                                    "Application Date", "Position URL", "Status"],
                        "properties": {
                            "Position Name": {"bsonType": "string"},
                            "Company": {"bsonType": "string"},
                            "Location": {"bsonType": "string"},
                            "Technologies/Programming Languages": {"bsonType": "string"},
                            "Application Date": {"bsonType": "date", 
                                                "description":"must be a date in yyyy-mm-dd format"},
                            "Position URL": {"bsonType": "string"},
                            "Status": {"bsonType": "string"}
                        }
                        
                    }
                }
            )
            db.collName.create_index("id", unique=True)
            print("Collection created with schema validation!!")
    else:
        print("Collection already exists!")

    

def dropColl(collectionName):
    if collectionName not in db.list_collection_names():
        raise Exception(f"❌ Collection '{collectionName}' does not exist in database '{db.name}'")
    db.drop_collection(collectionName)

def viewColl():
    print(db.list_collection_names())   
        

def main():
    parser = argparse.ArgumentParser(description="Job Application Manager")
    parser.add_argument("-d", "--delete",type=str, help="Delete a collection from MangoDB collections")
    parser.add_argument("-v", "--view", action="store_true", help="View the collections inside the JADatabase")
    parser.add_argument("-a", "--add", type=str, help="Add a new collection to JADatabase!")

    args = parser.parse_args()

    if args.delete:
        dropColl(args.delete)
    elif args.view:
        viewColl()
    elif args.add:
        addColl(args.add)


if __name__ == "__main__":
    main()
