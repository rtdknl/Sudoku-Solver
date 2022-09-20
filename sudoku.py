#Sudoku Solver
#put here the name of the file with the sudoku we want to solve
inputFile = "sudoku6.txt"

#define the column names, for row and squares we use numbers
startcolumns = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
options = [1,2,3,4,5,6,7,8,9]

#this function creates the cells and adds them to rows, columns, squares and cells
def start():
    #create a list for rows/columns/squares and a dictionary for the cells:
    global rows
    rows = []
    global columns
    columns =[]
    global squares
    squares = []
    global cells
    cells= {}
    #create for every cell a list in rows and squares
    for x in range(9):
        rows.append([])
        squares.append([])

    #create the cells and add to columns
    for column in startcolumns:
        new_column= [] #temp list for cell for each column
        for row in range(1,10): #create 9 rows numbered from 1 - 9

            #define which square belongs to the cell
            if column in ("A", "B", "C"):
                square = 1
            elif column in ("D", "E", "F"):
                square = 2
            else:
                square = 3

            if row > 3 and row <= 6:
                square = square + 3
            elif row > 6:
                square= square + 6

            #create cell name (column,row,square) without spaces
            cell = "{}{}{}"
            cell = cell.format(column,row,square)

            #add cells to rows, columns, squares and cells
            rows[row-1].append(cell) #-1 because index of list start with 0
            new_column.append(cell)
            squares[square-1].append(cell)
            cells[cell] = {"options":options, "eliminate": 0}

        columns.append(new_column) #add list with cells per column to columns


#execute function start
start()

#print text Sudoku with blue background
print("\n  \x1b[2;30;44m " +  "              SUDOKU             " + " \x1b[0m \n")

#function to show sudoku
def showSudoku():
    #loop through the rows
    for r in range(len(rows)):
        #start every line with a space
        printText = " "
        #get the cells
        for c in range(len(rows[r])):
            #a is the the text version of the value of each cell
            a = ""
            de = cells[rows[r][c]]["options"]
            #check if only one value in options and show it, else show a zero
            if len(de) == 1:
                number = str(de[0])
            else:
                number ="0"
            #gives the color and underline to the value
            a = '\x1b[4;30;44m ' +  number  + ' \x1b[0m'
            printText = printText + " " + a

        print(printText)


#funcion to read the file and add the given values to the cells
def openFile():
    f = open(inputFile)
    #for each row read a line
    for r in range(len(rows)):
        readlines = f.readline()

        i = 0 #index of cell in list
        #split the values in the lines
        for x in readlines.rsplit(","):
            lineValue = [] #create a new list to overide options
            value = int(x)

            if value > 0:
                lineValue.append(value)
                cells[rows[r][i]]["options"]=lineValue
            i +=1
    f.close()


#open the file and shows the Sudoku
openFile()
showSudoku()

#function to eliminate value from options for cells in the same row, column and square
def eliminateValue(e): #e= cellname
    one = cells[e]["options"] #get values for the initial cell
    newlist = []
    columnindex = startcolumns.index(e[0]) #get the letter out of cellname and return indexnumber of list

    #create a list with the corresponding cells
    for x in rows[int(e[1])-1]:
        newlist.append(x)

    for y in columns[columnindex]:
        if y not in newlist: newlist.append(y)

    for z in squares[int(e[2])-1]:
        if z not in newlist: newlist.append(z)

    newlist.remove(e) #remove the initial cell from list

    #check if initial cell has only one value
    if len(one) == 1:
        value = one[0]
        cells[e]["eliminate"] = 1 #set eliminate to status one

        #get values for corresponding cells
        for cell in newlist:
            celloptions = list(cells[cell]["options"])
            #check if there are two the same values in same row/column/square
            if len(celloptions) ==1 and celloptions[0]==value:
               raise Exception("ERROR!, propably a value in the file sudoku.txt is wrong.")

            if value in celloptions:
                celloptions.remove(value)

            #add the new options to corresponding cell
            cells[cell]["options"] = celloptions


#look for cells with a value and eliminate this value in the corresponding rows, columns and squares
def oneValue():
    for x in cells:
        eliminate_status = cells[x]["eliminate"]

        #skip if the cell already have been used for eliminating, prevent infinite loop
        if  eliminate_status == 1:
            continue

        eliminateValue(x)


#create dict with cell and options for area (row, column, or square)
def getData(number, arealist):

    datadict = {}
    for cell in arealist[number]:
        datalist = list(cells[cell]["options"])
        datadict[cell]=datalist

    return(datadict)


#check for each area if value is present in only one cell
def check1Value(area):
    areadata = {}

    #get for each row/column/square a datadict with cells and options
    for r in range(len(area)):
        areadata[r] = getData(r, area)

    for a in areadata:
        restart = False

        #run a loop from 1 till 9 to check if value in options
        for value in range(1,10):
            cell_list = []

            for cell, options in areadata[a].items():
                if value in options:
                    cell_list.append(cell)

                #skip this cell if options contains one value
                if len(options) == 1:
                    continue

            #if value is only in one cell, run again function oneValue
            if len(cell_list)==1:
                #skip if the cell already have been used for eliminating
                if cells[cell_list[0]]["eliminate"] == 1:
                    continue
                else:
                    #change options of cell to only this value
                    cells[cell_list[0]]["options"] = [value]
                    #run function oneValue
                    oneValue()
                    #restart this function again
                    restart = True

    return(restart)


#check for each area if the options of a cell with two options, is present in the options of one other cell
def check2Values(area):
    areadata = {}

    #get for each row/column/square a datadict with cells and options
    for r in range(len(area)):
        areadata[r] = getData(r, area)

    for a in areadata:

        cell_dict = {}
        for value in range(1,10):
            cell_list = []

            for cell, options in areadata[a].items():

                #skip this cell if options contains one value
                if len(options) == 1:
                    continue

                if value in options:
                    cell_list.append(cell)

            cell_dict[value]=cell_list

        #compare the keys(1-9) if the values(list of cells) match
        for value1 in range(len(cell_dict)):
            value1 +=1 #index in cell_dict starts with 1
            #loop again to compare key with other keys
            for value2 in range(len(cell_dict)):
                value2 +=1

                #only compare key if value contains two cells
                if value1 != value2 and len(cell_dict[value1])==2:
                    #check if cell list of the key match other cell list
                    if cell_dict[value1] == cell_dict[value2]:
                        keys = iter(cell_dict[value1])
                        key1 = next(keys)
                        key2 = next(keys)

                        #add the values to the cells
                        for cell in cell_dict[value1]:
                            cells[cell]["options"] = [value1,value2]

                        #loop dict again to remove values from other cells
                        for other_values in cell_dict:
                            #only get other values in dict which have the same cell/cells
                            if other_values != value1 and other_values != value2 and cell in cell_dict[other_values]:
                                #loop the other cells and get their options
                                for other_cell in cell_dict[other_values]:
                                    other_cell_values = cells[other_cell]["options"]
                                    #only remove value if the othercell contains multiple options, and not from the cells self
                                    if len(other_cell_values) > 1 and other_cell != key1 and other_cell != key2:
                                        if value1 in other_cell_values:
                                            cells[other_cell]["options"].remove(value1)
                                        if value2 in other_cell_values:
                                            cells[other-cell]["options"].remove(value2)

                        #run function to eliminate if cells now have one option left
                        oneOption()



def oneOption(): #check if cell has only one option left

    #start function again if something changed
    restart = True
    while restart:
        restart = False

        rowresult = check1Value(rows)
        columnresult = check1Value(columns)
        squareresult = check1Value(squares)

        if  rowresult == True or columnresult == True or squareresult == True:
            restart = True


#check if cell has two options left and the same options are present in one other cell
def twoOptions():
    check2Values(rows)
    check2Values(columns)
    check2Values(squares)


#try the two options if cell has only two left and options are present in more cells
def tryValue():

    #check every cell
    for x in range(len(rows)):
        for cell in rows[x]:
            values = cells[cell]["options"]
            #check if cell has only two options
            if len(values) == 2:
                #get both options
                v = iter(values)
                value1 = []
                value2 = []
                value1.append(next(v))
                value2.append(next(v))

                #try option one
                try:
                    cells[cell]["options"]=value1
                    oneValue()
                    oneOption()
                    twoOptions()

                #if option one fails try option two
                except:
                    start() #start over again, because dict is changed when trying option one
                    openFile()
                    cells[cell]["options"]=value2
                    oneValue()
                    oneOption()
                    twoOptions()

#print text solution, run the functions and show the sudoku
print("\n \n  \x1b[2;30;44m " +  "             SOLUTION            " + " \x1b[0m \n")
oneValue()
oneOption()
twoOptions()
tryValue()
showSudoku()
print("\n")

