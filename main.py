from hash_table import HashTable
from hash_table import hash_function
import sys

# noinspection PyPep8Naming
def initializeHash():
    return HashTable()


# noinspection PyPep8Naming
def insertAppDetails(ApplicationRecords, name, phone, member_reference, status):
    ApplicationRecords[name.strip()] = phone.strip() + "$$" + member_reference.strip() + "$$" + status.strip()
    outputFile = open("outputPS8.txt", 'w+')
    outputFile.write(
        "Successfully inserted " + str(ApplicationRecords.used_slots) + " applications into the system. \n")
    outputFile.close()


# noinspection PyPep8Naming
def updateAppDetails(ApplicationRecords, name, phone, member_reference, status):
    outputFile = open("outputPS8.txt", 'a+')
    try:
        existingValue = ApplicationRecords[name.strip()]
        updateValue = phone.strip() + "$$" + member_reference.strip() + "$$" + status.strip()
        ApplicationRecords[name.strip()] = updateValue
        columns = ["Phone Number", "Member Reference", "Application Status"]
        columnsChanged = []
        for i in range(0, len(existingValue.split("$$"))):
            if existingValue.split("$$")[i] != updateValue.split("$$")[i]:
                columnsChanged.append(columns[i])
        columnsChanged = ', '.join(map(str, columnsChanged))
        if len(columnsChanged)<1:
            columnsChanged = "No columns has been changed"
        outputFile.write("\nUpdated details of " + name.strip() + ". " + columnsChanged + " has been changed \n")
    except :
        outputFile.write("Updation Failed : User" + name.strip() + "not Exists.")
    outputFile.close()


# noinspection PyPep8Naming
def memRef(ApplicationRecords, memID):
    outputFile = open("outputPS8.txt", 'a+')
    outputFile.write("\n---------- Member reference by " + memID.strip() + " -----------\n")
    for name in ApplicationRecords.keys:
        if name is not None:
            if memID.strip() == ApplicationRecords[name].split("$$")[1]:
                outputFile.write(name + " / " + ApplicationRecords[name].split("$$")[0] + " / " +
                                 ApplicationRecords[name].split("$$")[2] + "\n")
    outputFile.write("------------------------------------------------" + "\n")
    outputFile.close()


# noinspection PyPep8Naming
def appStatus(ApplicationRecords):
    outputFile = open("outputPS8.txt", 'a+')
    outputFile.write("\n-------------- Application Status --------------\n")
    appliedCount = 0
    verifiedCount = 0
    approvedCount = 0
    applied = "Applied"
    verified = "Verified"
    approved = "Approved"
    for value in ApplicationRecords.values:
        if value is not None:
            record = value.split("$$")[2]
            if applied in record:
                appliedCount += 1
            elif verified in record:
                verifiedCount += 1
            elif approved in record:
                approvedCount += 1
    outputFile.write("Applied:" + str(appliedCount) + "\n")
    outputFile.write("Verified:" + str(verifiedCount) + "\n")
    outputFile.write("Approved:" + str(approvedCount) + "\n")
    outputFile.write("------------------------------------------------" + "\n")
    outputFile.close()


# noinspection PyPep8Naming
def HashId(key):
    return hash_function(key)


# noinspection PyPep8Naming
def readPromptsData(ApplicationRecords, promptsFile):
    promptsFile = open(promptsFile, 'r+')
    for record in promptsFile:
        if "Update" in record:
            record = record.split(':')[1].split('/')
            updateAppDetails(ApplicationRecords, record[0], record[1], record[2], record[3])
        if "memberRef" in record:
            record = record.split(':')[1]
            memRef(ApplicationRecords, record)
        if "appStatus" in record:
            appStatus(ApplicationRecords)


# noinspection PyPep8Naming
def fetchInputData(ApplicationRecords, inputFile):
    inputFile = open(inputFile, 'r+')
    for records in inputFile:
        record = records.strip('\n').split('/')
        insertAppDetails(ApplicationRecords, record[0], record[1], record[2], record[3])


def main(args):
    application_records = initializeHash()
    if len(args)-1 > 0:
        input_file, prompt_file = args[1], args[2]
    else:
        input_file, prompt_file = "inputPS8.txt", "promptsPS8.txt"
    fetchInputData(application_records, input_file)
    readPromptsData(application_records, prompt_file)


if __name__ == "__main__":
    main(sys.argv)
