# Ahmet Yavuz Mutlu 2210356014
import sys

def reading_line_func(txtFile): 
    """This function reads the input file and decode it."""
    input_file = open(txtFile,"r")
    while input_file:
        currentLine = input_file.readline()
        if currentLine == "":
            break
        else:
            currentLineList = currentLine.rstrip("\n").split(" ")
            functionPart = currentLineList[0].lower()
            dataPart = currentLineList[1:]

            if functionPart == "createcategory" : createcategory(dataPart) 
            if functionPart == "sellticket" : sellticket(dataPart) 
            if functionPart == "cancelticket" : cancelticket(dataPart) 
            if functionPart == "balance" : balance(dataPart) 
            if functionPart == "showcategory" : showcategory(dataPart)
    input_file.close()

def createcategory(createDatas):
    """This function creates a category that size is given by the user """
    global allCategories, alphabet
    categoryName, categorySize = createDatas[0], {"rows" : int(createDatas[1].split("x")[0]), "columns" : int(createDatas[1].split("x")[1])}
    
    if categoryName not in allCategories:
        allCategories[categoryName] = dict()                               
        for rowCounter in range(categorySize["rows"]):
            allCategories[categoryName][alphabet[rowCounter]] = dict() 
            for columnCounter in range(categorySize["columns"]):
                allCategories[categoryName][alphabet[rowCounter]][columnCounter] = {"seatSituation" : "X"} 
        output_func(f"The category \'{categoryName}\' having {categorySize['rows']* categorySize['columns']} seats has been created\n")
    else:
        output_func(f"Warning: Cannot create the category for the second time. The stadium has already {categoryName}\n")

def existFunction(categoryName,row,column):
    """This function checks the seat taht is given by user is exist or not. """
    rowExist, columnExist = row in allCategories[categoryName], column in allCategories[categoryName]["A"]
    
    if (not rowExist) and (not columnExist):
        output_func(f"Error: The category ’{categoryName}’ has less row and column than the specified index {row}{column}!\n")
    elif not rowExist:
        output_func(f"Error: The category ’{categoryName}’ has less row than the specified index {row}{column}!\n")
    elif not columnExist:
        output_func(f"Error: The category ’{categoryName}’ has less column than the specified index {row}{column}!\n")
    else:
        return True
def sellticket(sellDatas):
    "This function sells the tickets to customer."
    global allCategories, allTickets
    customerName, categoryName, seats= sellDatas[0], sellDatas[2], sellDatas[3:]
    if sellDatas[1] == "full" : paymentType = "F"
    if sellDatas[1] == "student": paymentType = "S"
    if sellDatas[1] == "season" : paymentType = "T"

    for seatCounter in range(len(seats)):
        row, column = seats[seatCounter][0],seats[seatCounter][1:]
        
        if "-" in column:
            columnDownLimit,columnUpLimit =int(column.split("-")[0]), int(column.split("-")[1])+1
        else:
            columnDownLimit,columnUpLimit = int(column), (int(column)+1)

        if existFunction(categoryName, row, (columnUpLimit-1)) == True:
            for columnCounter in range (columnDownLimit,columnUpLimit):
                if allCategories[categoryName][row][columnCounter]["seatSituation"] != "X":
                    if ("-" in column):
                        output_func(f"Error: The seats {row}{columnDownLimit}-{columnUpLimit-1} cannot be sold to {customerName} due some of them have already been sold!\n")
                    else:
                        output_func(f"Warning: The seat {row}{columnDownLimit} cannot be sold to {customerName} since it was already sold\n")
                    break
                else:
                    allCategories[categoryName][row][columnCounter]["seatSituation"] = paymentType
                    allCategories[categoryName][row][columnCounter]["customerName"] = customerName
                    if ("-" in column) and (columnCounter == columnUpLimit -1):
                        output_func(f"Success: {customerName} has bought {row}{columnDownLimit}-{columnUpLimit-1} at {categoryName}\n")
                    elif (columnCounter == columnUpLimit -1):
                        output_func(f"Success: {customerName} has bought {row}{columnDownLimit} at {categoryName}\n")
            
def cancelticket(cancelDatas):
    """When the function calls, it cancels the ticket that given by user."""
    global allCategories, allTickets
    categoryName, seats = cancelDatas[0], cancelDatas[1:]
    for seatCounter in seats:
        row, column = seatCounter[0], int(seatCounter[1:])
        if existFunction(categoryName, row, column) == True:
            if "customerName" in allCategories[categoryName][row][column]:
                del allCategories[categoryName][row][column]["customerName"]
                allCategories[categoryName][row][column]["seatSituation"] = "X"
                output_func(f"Success: The seats {row}{column} at '{categoryName}' have been canceled and now ready to sell again\n")
            else:
                output_func(f"Error: The seat {row}{column} at '{categoryName}' has already been free! Nothing to cancel\n")

def balance(balanceDatas):
    """The function calculates a categories total balance """
    global allCategories, allTickets, alphabet
    categoryName = balanceDatas[0]
    sumOfStudents, sumOfFulls, sumOfSeasons = 0, 0, 0
    for rowCounter in allCategories[categoryName]:
        for columnCounter in allCategories[categoryName][rowCounter]:
            if allCategories[categoryName][rowCounter][columnCounter]["seatSituation"] == "F": 
                sumOfFulls += 1
            elif allCategories[categoryName][rowCounter][columnCounter]["seatSituation"] == "S": 
                sumOfStudents += 1
            elif allCategories[categoryName][rowCounter][columnCounter]["seatSituation"] == "T": 
                sumOfSeasons += 1

    revenues = 10*sumOfStudents + 20*sumOfFulls + 250*sumOfSeasons
    output_func(f"Category report of '{categoryName}'\n"+"-"*32+f"\nSum of students = {sumOfStudents},"+
    f" Sum of full pay = {sumOfFulls}, Sum of season ticket = {sumOfSeasons}, and Revenues = {revenues} Dollars\n")

def showcategory(showDatas):
    """It shows all seat situations in a category"""
    global allCategories, alphabet
    categoryName = showDatas[0]
    for rowCounter in alphabet[::-1]: #sorted(allCategories[categoryName],reverse =True)
        if rowCounter in allCategories[categoryName]:
            output_func(rowCounter+"  ")
            for columnCounter in allCategories[categoryName][rowCounter]:
                if columnCounter == len(allCategories[categoryName][rowCounter])-1: spaceAmount = 0
                else: spaceAmount = 2 
                output_func(allCategories[categoryName][rowCounter][columnCounter]["seatSituation"]+" "*spaceAmount)
            output_func("\n")

            if (alphabet.index(rowCounter)) == 0:
                output_func(" "*3)
                for columnCounter in range(len(allCategories[categoryName]["A"])):
                    if columnCounter == len(allCategories[categoryName]["A"])-1: spaceAmount = 0
                    elif columnCounter >= 9: spaceAmount = 1
                    else: spaceAmount = 2
                    output_func(f"{columnCounter}"+" "*spaceAmount)
                output_func("\n")              

def output_func(text):
    """This function takes a text as parameter and print it to the terminal and write it to the output file."""
    print(text, end="")
    output_file.write(text)

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
allCategories, allTickets = dict(), dict()
output_file = open("output.txt","w")
reading_line_func(sys.argv[1])
output_file.close()

