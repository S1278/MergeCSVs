Merge two or more CSV files on a common column “email” which is present in all the files. 
Example: 

CSV1:
email		Value 1  
a@b.com		1
x@y.com		2      

CSV2:  
email		Value 2  
a@b.com		2
x@y.com		3

Output CSV:
email		Value 1		Value 2
a@b.com		1		2
x@y.com		2		3

Pass names of the CSV files to be merged as command line arguments. The last argument should be the name 
of the output CSV file to be created.

Files csv1.csv and csv2.csv can be used for testing.