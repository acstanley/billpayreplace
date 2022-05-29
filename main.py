import csv
import re
from datetime import datetime

# initiate account number dictionary, key is new account number, value is old account number.
accno_dict = {}

# populate accno_dict, setting new account number as key from RptAccountsList.csv column 1, and old account
#   number from column 3.

print(datetime.now(), "Reading account numbers from RptAccountsList.csv...")
with open("RptAccountsList.csv") as rptfile:
    rptarray = list(csv.reader(rptfile))
    for rptaccountline in rptarray:
        accno_dict[rptaccountline[0]] = rptaccountline[2]


# function to fetch new account number for given old account number:
def getNewAccountNumber(accountnumber):
    for newaccountnumber, oldaccountnumber in accno_dict.items():
        if oldaccountnumber == accountnumber:
            return newaccountnumber


print(datetime.now(), "Reading Billpay An post file.DAT into memory...")
with open("Billpay An post file.DAT") as billpayfile:
    billpaylines = billpayfile.readlines()


# initiate array to store lines that will be written to the new file
lines_to_write = []
print(datetime.now(), "Replacing old account numbers with new...")
account_number_regex = re.compile(r'00000\d\d\d\d\d\d')
line_counter = 0
for line in billpaylines:
    line_counter += 1
    #check if we have an account number line
    accno_regex_check = account_number_regex.search(line[24:35])

    # if we do, break line into chunks, chunk2 being the account number.
    if accno_regex_check:
        #line_chunk1 = line[0:24]

        # strip 0's from start of string to get account number
        line_account_number = line[24:35].lstrip('0')
        print(line_counter, line_account_number)

        # check if it's already a new account number
        if line_account_number.startswith("4") and len(line_account_number) == 6:
            # if it is a new account number, don't touch it, write direct to file
            lines_to_write.append(line)
        else:
            # if it's not a new account number, build new line from chunks

            # first chunk = first 24 characters before account number
            # second chunk = call function to get new account number, pad it with zeroes to length of 11
            # third chunk = 36th character to end of file

            # if this raises Exception AttributeError: 'NoneType' object has no attribute 'zfill'
            #  then there is probably no corresponding new account number in RptAccountsList.csv
            new_line = line[0:24] +\
                       getNewAccountNumber(line_account_number).zfill(11) +\
                       line[35:]
            lines_to_write.append(new_line)
    # if it's not an account line, don't touch it, write direct to file
    else:
        lines_to_write.append(line)

print(datetime.now(), "Writing lines to new file...")
with open("Billpay An post file_replaced.DAT","w") as billpay_replacedfile:
    for line in lines_to_write:
        billpay_replacedfile.write(line)

print(datetime.now(), "Finished!")