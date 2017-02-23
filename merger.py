import csv
import os
import sys

class CSV_File(object):
    def __init__(self, fileName):
        """
        fileName: string denoting a CSV file name. (without .csv extension)

        Initialises the object instance with following attributes:
        fileName: name of file.
        emailList: email ids contained in file.
        fieldList: list of all fields present.
        table: data contained in file.
        """
        if type(fileName) != type('abcd'):
            raise Exception("File names must be given as strings. (within quotes)")
        if len(fileName) >= 4:
            if fileName[-4] == ".":
                fileName = fileName[ :-4]
        self.fileName = fileName + ".csv"
        self.emailList = None
        self.fieldList = None
        self.table = None

    def setEmailList(self, emailList):
        self.emailList = emailList

    def setFieldList(self,fieldList):
        self.fieldList = fieldList

    def setTable(self, table):
        self.table = table

    def getFileName(self):
        return self.fileName

    def getEmailList(self):
        """
        Saves all emails contained in the file.

        returns: List of email ids in the file. ('emailList' attribute)
        """
        if self.emailList != None:
            return self.emailList
        try:
            self.emailList = []
            with open(self.getFileName()) as csvFile:
                reader = csv.DictReader(csvFile)
                for row in reader:
                    try:
                        self.emailList.append(row['email'])
                    except KeyError:
                        print "No field named " + "'email'" + " found in the CSV file " + "'" + self.getFileName() + "'"
                        csvFile.close()
                        return
            csvFile.close()
            return self.emailList
        except IOError:
            raise Exception('No file named ' + "'" + self.getFileName() + "'" + ' found.')

    def getFieldList(self):
        """
        Saves all fields contained in the file. (the first line in the CSV)

        returns: List of fields contained in file. ('fieldList' attribute)
        """
        if self.fieldList != None:
            return self.fieldList
        try:
            with open(self.getFileName()) as csvFile:
                reader = csv.DictReader(csvFile)
                self.fieldList = reader.fieldnames

            csvFile.close()
            return self.fieldList
        except IOError:
            raise Exception('No file named ' + "'" + self.getFileName() + "'" + ' found.')
        
    def getTable(self):
        """
        Saves data in a dictionary with email ids as keys.
        Each key refers to a row.

        returns: Data represented in a dictionary. ('table' attribute)
        """
        if self.table != None:
            return self.table
        try:
            self.table = {}
            with open(self.getFileName()) as csvFile:
                reader = csv.DictReader(csvFile)
                for row in reader:
                    try:
                        self.table[row['email']] = row
                    except KeyError:
                        print "No field named " + "'email'" + " found in the file" + self.getFileName()
                        csvFile.close()
                        return
            csvFile.close()
            return self.table
        except IOError:
            raise Exception('No file named ' + "'" + self.getFileName() + "'" + ' found.')

    def mergeTwoCSVdata(self, other):
        """
        self, other: CSV_File instances.

        Merges data in 'table' attribute of the two CSV_File instances into 'table' attribute of the first one.

        returns: None
        """
        table1 = self.getTable()
        table2 = other.getTable()
        emails1 = self.getEmailList()
        emails2 = other.getEmailList()
        fields1 = self.getFieldList()
        fields2 = other.getFieldList()
        newFields = fields2[1: ]
        delete = []
        for email in table1:
            try:
                temp = table2[email]
            except KeyError:
                delete.append(email)
                emails1.remove(email)
        for email in delete:
            table1.pop(email)
        for email in emails1:
            for  field in newFields:
                table1[email][field] = table2[email][field]
        fields1 += newFields
        return None

    def writeCSVfromTable(self):
        """
        Accesses data in the 'table' attribute of the object instance and writes it in CSV format.

        returns: None
        """
        if self.emailList == None or self.fieldList == None or self.table == None:
            raise Exception('Either of email list, field list and table not set.')
        with open(self.getFileName(), 'w') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames = self.getFieldList(), lineterminator = '\n')
            writer.writeheader()
            emailList = self.getEmailList()
            table = self.getTable()
            for email in emailList:
                writer.writerow(table[email])

        csvFile.close()
    

def mergeAllFiles(CSV_List, targetFileName):
    """
    CSV_List: A List containing file names as strings. (without .csv extension)
    targetFileName: The file to be created and/or written upon to store merged data.

    Merges data from all files in CSV_List and stores in a file with name passed in targetFileName.

    returns: None
    """
    try:
        CSV_List = list(CSV_List)
        samefile = False
        if targetFileName in CSV_List:
            samefile = True

        n = len(CSV_List)
        for i in range(n):
            CSV_List[i] = CSV_File(CSV_List[i])

        CSV_File_Objects = CSV_List

        csvMerged = CSV_File(targetFileName)
        if samefile == True:
            raise Exception("Cannot create a file with an existing file name in the directory.")

        csvMerged.setEmailList(CSV_File_Objects[0].getEmailList()[:])
        csvMerged.setFieldList(CSV_File_Objects[0].getFieldList()[:])
        csvMerged.setTable(CSV_File_Objects[0].getTable().copy())

        for i in range(1, n):
            csvMerged.mergeTwoCSVdata(CSV_File_Objects[i])

        csvMerged.writeCSVfromTable()
        os.system('start excel.exe ' + csvMerged.getFileName())

    except IndexError:
        raise Exception('Pass a non Empty list of file name strings.')

    except TypeError:
        raise Exception('Non iterable argument passed.')


def main():
    args = sys.argv
    mergeAllFiles(args[1: -1], args[-1])


main()
