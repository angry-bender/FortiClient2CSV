# Fortinet Client to csv converter V0.1

## Contents

- [Fortinet Client to csv converter V0.1](#fortinet-client-to-csv-converter-v01)
  - [Contents](#contents)
    - [DESCRIPTION](#description)
    - [PRE-REQUISITES](#pre-requisites)
    - [Use](#use)
    - [Dev Notes](#dev-notes)


### DESCRIPTION

This script aims to parse the fortinet client logs from a Windows Client.

### PRE-REQUISITES

Nil

### Use

Extract the fclog.dat file from `%programfiles%\Fortinet\FortiClient\logs`

run the script with `python3 ./FortiClient2CSV.py <fclog.dat location>`


By default the file will name itself from from the last log entry in your fclog.dat file. However, you optionally specify an output location with `python3 ./FortiClient2CSV.py <fclog.dat location> --outfile <outfilename>`.

### Dev Notes

This script has been built with the following sqlite data structure in place

```
SQLite version 3.31.1 2020-01-27 19:55:54
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
sqlite> .open fclog.dat
sqlite> .tables
AEViolations   Alerts         FWViolations   RMAViolations  VirusInfo    
AVScanInfo     Alerts_copy    LogTable       UrlInfoEx      WFViolations 
sqlite> .schema LogTable
CREATE TABLE LogTable (Id INTEGER PRIMARY KEY, Source INTEGER, Type INTEGER, DateTime INTEGER, Text TEXT, Reserved1 INTEGER, Reserved2 INTEGER, Reserved3 INTEGER, Reserved4 INTEGER );
', ' '), 'GGER LogTable_on_log_insert_trim        AFTER INSERT ON LogTable        FOR EACH ROW        BEGIN        update LogTable         set Text = trim(replace(replace(replace(Text, '
', ' '), '  ', ' '))        where rowid = new.rowid;        END;
CREATE UNIQUE INDEX index_LogTable ON LogTable(Id);
CREATE INDEX index_LogTable_source ON LogTable(Source);
CREATE INDEX index_LogTable_DateTime ON LogTable(DateTime);
sqlite> .header on
sqlite> .mode column
sqlite> pragma table_info('LogTable');
cid         name        type        notnull     dflt_value  pk        
----------  ----------  ----------  ----------  ----------  ----------
0           Id          INTEGER     0                       1         
1           Source      INTEGER     0                       0         
2           Type        INTEGER     0                       0         
3           DateTime    INTEGER     0                       0         
4           Text        TEXT        0                       0         
5           Reserved1   INTEGER     0                       0         
6           Reserved2   INTEGER     0                       0         
7           Reserved3   INTEGER     0                       0         
8           Reserved4   INTEGER     0                       0         
```