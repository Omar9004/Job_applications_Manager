from pymongo import MongoClient
import pandas as pd
from datetime import datetime
from nanoid import generate
import argparse
import numpy as np
client = MongoClient("mongodb://localhost:27017/")

db = client["JADatabase"] # Job applications database
job = db["jobApplication"]

def add_job (args_dict):
    job.insert_one({"id":generate(size=4), "Position Name": args_dict['name'],"Company":args_dict['company'], 
                    "Location":args_dict['location'], "Technologies/Programming Languages":args_dict['tech'], 
                    "Application Date": args_dict['date'], "Position URL": args_dict['url'], "Status": args_dict['status']})
    
# View the content of the DB using Pandas
def viewDb():
    docs = list(job.find())
    df = pd.DataFrame(docs)
    df.index= np.arange(1, len(df) + 1) #Index strats from 1
    df.drop(columns=["_id"], errors="ignore",inplace=True)

    print(df)

def validDate(s):
    try:
        return datetime.strptime(s,"%Y-%m-%d, %H:%M:%S")
    except:
        raise argparse.ArgumentTypeError(f"Not a vaild Date: '{s}'. Expected format of: YYYY-MM-DD")
def delete (id):
    if job.find_one({"id":id }):
        job.delete_one({"id":id})
        print(f"id: {id} has been deleted!")
    else:
        print("Query doesn't exist in the collection!")
def main():
    parser = argparse.ArgumentParser(description="Job Application Manager")
    subparsers = parser.add_subparsers(dest="command")

    # --- Main Args ---
    parser.add_argument("-v", "--view",action="store_true", help="To view the content of the job applicaiton table")
    parser.add_argument("-i", "--insert", type=str , help="Insert detail about a new job!!")
    parser.add_argument("-d", "--delete", type=str, help="Delete a row using its id")
   
    # --- insertion and its subcommand --- 
    insert_parser = subparsers.add_parser("insert", help="Insert detail about a new job!!")
    insert_parser.add_argument("--name", type=str, required = True, help = "Position name")
    insert_parser.add_argument("--company", type=str, required = True, help = "Company name")
    insert_parser.add_argument("--location", type=str, default="Sweden", required = False, help = "location")
    insert_parser.add_argument("--tech", type=str, required = False, default=" ", help = "Technologies/Programing Languages")
    insert_parser.add_argument("--date", type=validDate,default = datetime.now().strftime("%Y-%m-%d, %H:%M:%S"),required = False, help = "Applcation Date")
    insert_parser.add_argument("-url", type=str,default=" ", required= False, help= "Link to the job announcement" )
    insert_parser.add_argument("-status", type=str,default = "Submitted" ,required= False, help= "Job application status" )





    args = parser.parse_args()

    args_dict = vars(args)
    if args.insert or args.command == "insert":
        add_job(args_dict)
    elif args.view:
        viewDb()
    elif args.delete:
        delete(args.delete)

if __name__ == "__main__":
    main()

    