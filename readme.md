# Fortinet Client to csv converter V0.1

## Contents

- [Fortinet Client to csv converter V0.1](#fortinet-client-to-csv-converter-v01)
  - [Contents](#contents)
    - [DESCRIPTION](#description)
    - [PRE-REQUISITES](#pre-requisites)
    - [Use](#use)
    - [fclog.dat schema](#fclogdat-schema)
      - [tablelist](#tablelist)
      - [LogTable Types](#logtable-types)


### DESCRIPTION

This script aims to parse the fortinet client logs from a Windows Client.

### PRE-REQUISITES

Nil

### Use

Extract the fclog.dat file from `%programfiles%\Fortinet\FortiClient\logs`

run the script with `python3 ./FortiClient2CSV.py <fclog.dat location>`

By default the file will name itself from from the last log entry in your fclog.dat file. However, you optionally specify an output location with `python3 ./FortiClient2CSV.py <fclog.dat location> --outfile <outfilename>`.

### fclog.dat schema

This script has been built with the following sqlite data structure in place

#### tablelist

```
SQLite version 3.31.1 2020-01-27 19:55:54
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
sqlite> .open fclog.dat
sqlite> .tables
AEViolations   Alerts         FWViolations   RMAViolations  VirusInfo    
AVScanInfo     Alerts_copy    LogTable       UrlInfoEx      WFViolations 
```

#### LogTable Types

cid        | name       | type       | notnull    | dflt_value | pk        
---------- |----------  |----------  |----------  |----------  |----------
0          | Id         | INTEGER    | 0          |            | 1         
1          | Source     | INTEGER    | 0          |            | 0         
2          | Type       | INTEGER    | 0          |            | 0         
3          | DateTime   | INTEGER    | 0          |            | 0         
4          | Text       | TEXT       | 0          |            | 0         
5          | Reserved1  | INTEGER    | 0          |            | 0         
6          | Reserved2  | INTEGER    | 0          |            | 0         
7          | Reserved3  | INTEGER    | 0          |            | 0         
8          | Reserved4  | INTEGER    | 0          |            | 0         
