from pymongo import MongoClient
import pandas as pd
from datetime import datetime
from nanoid import generate
import argparse
import numpy as np

class JobApplicationDB:
    def __init__(self, collectionName = "jobApplication" ):
        client = MongoClient("mongodb://localhost:27017/")
        db = client["JADatabase"] # Job applications database
        self.job = db[collectionName]
        self.__argsParser()

    def aliases_index(key:str):
        """Aliases_index is helping with aliases of a column inside the MongoDB collection. 
        Since it doesn't support it."""

        FIELD_ALIASES = {
        "name": "Position Name",
        "company": "Company",
        "location": "Location",
        "tech": "Technologies/Programming Languages",
        "date": "Application Date",
        "url": "Position URL",
        "status": "Status"
        }
        return FIELD_ALIASES[key]
    def add_job (self, args_dict):
        self.job.insert_one({"id":generate(size=4), "Position Name": args_dict['name'],"Company":args_dict['company'], 
                        "Location":args_dict['location'], "Technologies/Programming Languages":args_dict['tech'], 
                        "Application Date": args_dict['date'], "Position URL": args_dict['url'], "Status": args_dict['status']})
        
    def update(self, args_dict):
        id = args_dict["id"]
        if self.job.find_one({"id":id}) and len(args_dict)>=1:
            keys = list(args_dict.keys())
            print(args_dict)
            for i in range(1, len(args_dict)): # Skip id arg
                column = keys[i] # Extract the key/column name from args_dict
                newValue = args_dict[column] # Get the value of this key from args_dict
                aliasedColumn = self.aliases_index(column)
                self.job.update_one({"id":id}, {'$set' : {aliasedColumn: newValue}})
        else:
            print(f"The give id: {id} is not exist!")
        
    # View the content of the DB using Pandas
    def viewDb(self):
        docs = list(self.job.find())
        df = pd.DataFrame(docs)
        df.index= np.arange(1, len(df) + 1) #Index strats from 1
        df.drop(columns=["_id"], errors="ignore",inplace=True)
        print(df)

    def delete (self,id):
        if self.job.find_one({"id":id }):
            self.job.delete_one({"id":id})
            print(f"id: {id} has been deleted!")
        else:
            print("Query doesn't exist in the collection!")

    def __validDate(sef,s):
        try:
            return datetime.strptime(s,"%Y-%m-%d, %H:%M:%S")
        except:
            raise argparse.ArgumentTypeError(f"Not a vaild Date: '{s}'. Expected format of: YYYY-MM-DD")
    def __argsParser(self):
        parser = argparse.ArgumentParser(description="Job Application Manager")
        subparsers = parser.add_subparsers(dest="command")

        # --- Main Args ---
        parser.add_argument("-v", "--view",action="store_true", help="To view the content of the job applicaiton table")
        parser.add_argument("-i", "--insert", type=str , help="Insert detail about a new job!!")
        parser.add_argument("-u", "--update", type=str , help="Update a certain job entity by providing its id and the targeted column name!!")
        parser.add_argument("-d", "--delete", type=str, help="Delete a row using its id")

        # --- insertion and its subcommand --- 
        insert_parser = subparsers.add_parser("insert", help="Insert detail about a new job!!")
        if parser.parse_args().insert or parser.parse_args().command == "insert":
            insert_parser.add_argument("--name", type=str, required = True, help = "Position name")
            insert_parser.add_argument("--company", type=str, required = True, help = "Company name")
            insert_parser.add_argument("--location", type=str, default="Sweden", required = False, help = "location")
            insert_parser.add_argument("--tech", type=str, required = False, default=" ", help = "Technologies/Programing Languages")
            insert_parser.add_argument("--date", type=self.__validDate,default = datetime.now().strftime("%Y-%m-%d, %H:%M:%S"),required = False, help = "Applcation Date")
            insert_parser.add_argument("--url", type=str,default=" ", required= False, help= "Link to the job announcement" )
            insert_parser.add_argument("--status", type=str,default = "Submitted" ,required= False, help= "Job application status" )

        # --- Update and its subcommand --- 
        update_parser = subparsers.add_parser("update", help="Insert detail about a new job!!")
        if parser.parse_args().update or parser.parse_args().command == "update":
            update_parser.add_argument("--id", type=str, required=True, help="Job id")
            update_parser.add_argument("--name", type=str, required = False, help = "Position name")
            update_parser.add_argument("--company", type=str, required = False, help = "Company name")
            update_parser.add_argument("--location", type=str, required = False, help = "location")
            update_parser.add_argument("--tech", type=str, required = False, help = "Technologies/Programing Languages")
            update_parser.add_argument("--url", type=str, required= False, help= "Link to the job announcement" )
            update_parser.add_argument("--status", type=str ,required= False, help= "Job application status" )



        args = parser.parse_args()
        args_dict = vars(args)

        if args.insert or args.command == "insert":
            self.add_job(args_dict)
        elif args.update or args.command == "update":
            update_dict = {k:v for k,v in args_dict.items() if (k not in ["command"] and k != "view") and v is not None}
            self.update(update_dict)
        elif args.view:
            self.viewDb()
        elif args.delete:
            self.delete(args.delete)
    
def main():
    JobApplicationDB()


if __name__ == "__main__":
    main()

    