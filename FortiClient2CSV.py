import sqlite3 as sql
import os
import csv
import argparse
import sqlite3
import datetime
import sys

def ReadSQLiteData(filename, tablename):
    
    print("Reading SQLite Data from " + filename + "...")

    #Connect to Database    
    con = sql.connect(filename)

    #Get Row Names
    con.row_factory = sqlite3.Row

    #Prepare the database cursor
    cur = con.cursor()

    #RetreiveData from logfile (See readme.md for db DESCRIBE)
    cur.execute(f'SELECT * from {tablename}')
    data = cur.fetchall()

    return data

def ReadLastSQLiteLine(filename, tablename, columnname):
    
    print("Reading Last Line of " + columnname + " from the " + tablename + " table using SQLite file " + filename + "...")

    #Connect to Database    
    con = sql.connect(filename)

    #Get Row Names
    con.row_factory = sqlite3.Row

    #Prepare the database cursor
    cur = con.cursor()

    #Retreive Last Line from logfile from a given column of interest (See readme.md for db DESCRIBE)
    cur.execute('SELECT * FROM %s ORDER BY %s DESC LIMIT 1;' % (tablename,columnname))
    lastline = cur.fetchone()

    return lastline

def FortiClientToCSV(db, filename):
    print("Exporting client logs to " + filename + ".....")
    with open(filename, "w") as csv_file:
        csv_writer = csv.writer(csv_file)
        
        #Create the Header
        names = ('Id', 'Source', 'Type', 'DateTime', 'Text')    
        csv_writer.writerow(names)

        #Bodge the utctime into the log on each row, as we don't want to modify the DB file.
        for row in db:
            epoch = row['DateTime']
            utctime = datetime.datetime.fromtimestamp(epoch).isoformat()
            values = (row['Id'], row['Source'], row['Type'], utctime, row['Text'])
            csv_writer.writerow(values)

try:    
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('filename', type=str, help="The fclog.dat filename to read from")
    arg_parser.add_argument('--outfile', type=str, default=("FortiClient.csv"), help="Specifies a custom output filename (Default is YYYY-MM-DDTHH:MM:SS_Forticlient.csv from last log)")

    args = arg_parser.parse_args()

    print("Fortinet client log converter V0.1 by Angry Bender \n \n")

    if args.filename:
        if os.path.exists(args.filename) == False:
            print("error: Invalid log file, please check the supplied directory and try again")
            sys.exit(1)
        else:
            
            try: 
                #Read the parsed in Log File using the Known FortiGate log table
                data = ReadSQLiteData(args.filename, 'LogTable')
            except sqlite3.Error as ex:
                print ("error: SQLITE Error - Check log file type, or See below for sqlite exception:")
                print (ex)
                sys.exit(2)
    try:
        if args.outfile == "FortiClient.csv":            
            #Read in the last line of the log file, by date, to get the most recent log from FortiGate Logs
            lastline = ReadLastSQLiteLine(args.filename, 'LogTable', 'DateTime')

            #Convert the fetched row(Tuple) to a string to add to the filename
            lastdate = str(datetime.datetime.fromtimestamp(lastline['DateTime']).isoformat()) 
            outfile = (lastdate + "_FortiClient.csv")
        else:
            outfile = args.outfile
    
        #Create the CSV
        FortiClientToCSV(data,outfile)
    except Exception as ex:
        print (ex)
        sys.exit(3)

except KeyboardInterrupt:
    print("ERROR:   User Requested keyboard interupt, Exiting now...")