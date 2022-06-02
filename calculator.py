import  tkinter as tk
import operator
import re

#TODO: issue with negative numbers
#TODO: if empty after/before dot - works but does not add 0 after/before dot

def retrieve_input():
    input = inputText.get()
    return input

def clicked(number):
    currentInput = retrieve_input()
    inputText.delete(0,tk.END)
    inputText.insert(0,str(currentInput) + str(number))

def deleteAll():
    inputText.delete(0,tk.END)

def deleteOne():
    currentInput = retrieve_input()
    if not currentInput:
        return
    else:
        inputText.delete(0,tk.END)
        inputText.insert(0,str(currentInput[:-1]))

def dot():
    currentInput = retrieve_input()
    inputText.delete(0,tk.END)
    inputText.insert(0,str(currentInput) + '.')

def eval(operators, numbers):
    #eval
    operOrder = ['*/%','+-']
    operDict = { '*':operator.mul,
                '/':operator.truediv,
                '%':operator.mod,
                '+':operator.add,
                '-':operator.sub}

    for op in operOrder:
        while any(o in operators for o in op): #we check if the operator exists
            idx,oo = next((i,o) for i,o in enumerate(operators) if o in op) #Next operator with this precedence         
            operators.pop(idx) #remove this operator from the operator list
            values = map(float,numbers[idx:idx+2]) #float for everything
            value = operDict[oo](*values)
            numbers[idx:idx+2] = [value] #clear out those indices

    return (numbers[0])


def parse(currentInput):
    #parsed 
    searchOper = re.findall("[*+\/\-\%()]+", currentInput)

    if ')(' in searchOper: #make it work when )( are together - add )*(, or when number() - add number*()
        searchOper = ''.join(searchOper)
        searchOper = searchOper.replace(')(',')*(')
    numbers = ['0','1','2','3','4','5','6','7','8','9']
    for number in numbers:
        if (str(number+'(') in currentInput):
            currentInput = currentInput.replace(str(number+'('), str(number+'*'+'('))

    searchOper = list(''.join(searchOper)) #split because of the operator next to operator issue
    if searchOper:
        findBrack = re.findall("[()]+", currentInput) #seach if there is a bracket
        if (findBrack):
            numInBrack = []
            onlyNum = re.findall(r"\((.*?)\)", currentInput) #get all info in the bracket
            for everyBrack in onlyNum: #for each bracket do
                searchOperBrack = re.findall("[*+\/\-\%]+", everyBrack)

                if ')(' in searchOperBrack:  #make it work when )( are together - add )*(, or when number() - add number*()
                    searchOperBrack = ''.join(searchOperBrack)
                    searchOperBrack = searchOperBrack.replace(')(',')*(')
                for number in numbers:
                    if (str(number+'(') in everyBrack):
                        everyBrack = everyBrack.replace(str(number+'('), str(number+'*'+'('))
                
                searchOperBrack = list(''.join(searchOperBrack)) #split because of the operator next to operator issue
                everyBrack = re.split("[*+\/\-\%]+", everyBrack)
                numInBrack.append(float(eval(searchOperBrack, everyBrack))) #adds in an array all the solved ones :)
            numBrackets = 0
            for inBrack in onlyNum: #for each bracket that is solved

                if ')(' in currentInput:  #make it work when )( are together - add )*(, or when number() - add number*()
                    currentInput = currentInput.replace(')(',')*(')
                for number in numbers:
                    if (str(number+'(') in currentInput):
                        currentInput = currentInput.replace(str(number+'('), str(number+'*'+'('))

                currentInput = str(currentInput).replace(str(inBrack),str(numInBrack[numBrackets])) # example: (2+1)*(2-1) repaces with (3)*(1)
                numBrackets = numBrackets + 1
            withNoBrack = currentInput.replace('(','').replace(')','') #removes brackets example: (3)*(1) will be 3*1
            parse(withNoBrack) 


        else:
            onlyNum = re.split("[*+\/\-\%]+", currentInput)
            solved = eval(searchOper, onlyNum)
            inputText.delete(0,tk.END)
            inputText.insert(0,solved)


def equal():
    currentInput = retrieve_input()
    return parse(currentInput)

def keyPressed(event):
    input = event.char
    if input.isnumeric() or input in mathOperatorsArr:
        clicked(input)
    elif input == '.':
        dot()
    elif input == ',':
        currentInput = retrieve_input()
        currentInput.replace(',', '.') 
        dot()
    elif event.keysym == 'Return':
        equal()
    elif event.keysym == 'BackSpace':
        deleteOne()
    elif event.keysym == 'Delete':
        deleteAll()

win= tk.Tk()
win.title('Calculator')
win.geometry("301x336")

inputText = tk.Entry(win, font="Helvetica 20", justify='right')
inputText.grid(row=0, columnspan=3)

for i in (range(10)):
    tk.Button(win, text= str(abs(i-9)), font="Helvetica 17", relief='groove',bg="#edfbff", fg="#333333", borderwidth=1, command=lambda c=i: clicked(str(abs(c-9)))).grid(row=int(((i) / 3)+1), column=((i) % 3), sticky='nesw')

equalBtn = tk.Button(win, text='=', font="Helvetica 17", relief='groove', borderwidth=1,bg="#e3f9ff", fg="#333333", command = equal, highlightthickness=0).grid(row=7,column=2, sticky='nesw')
dotBtn = tk.Button(win, text='.', font="Helvetica 17", relief='groove', borderwidth=1,bg="#e3f9ff", fg="#333333", command = dot, highlightthickness=0).grid(row=7,column=1, sticky='nesw')
deleteAllBtn = tk.Button(win, text='C', font="Helvetica 17", relief='groove', borderwidth=1,bg="#ededed", fg="#333333", command = deleteAll, highlightthickness=0).grid(row=4,column=2, sticky='nesw')
deleteOneBtn = tk.Button(win, text='CE', font="Helvetica 17", relief='groove', borderwidth=1,bg="#ededed", fg="#333333", command = deleteOne, highlightthickness=0).grid(row=4,column=1, sticky='nesw')

mathOperatorsArr = ['+','-','/','*','(',')','%']
placeRow=5
place = 0
for operators in (mathOperatorsArr):
    tk.Button(win, text= str(operators), font="Helvetica 17", relief='groove', borderwidth=1, highlightthickness=0 ,bg="#edfbff", fg="#333333", command=lambda o=operators: clicked(o)).grid(row=int(((place) / 3)+placeRow), column=int(place % 3), sticky='nesw')
    place = place + 1

win.bind("<Key>", keyPressed) #bind keyboard keys to functions for button press

win.mainloop()