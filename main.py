from BottonUp import BUParser
from TopDown import TDParser
from Grammar import Grammar
import os

def case_1():
    print("=======================================")
    print("You selected 1")
    print("Select an option:")
    print("1. Process string")
    print("2. First and follow")
    print("3. Gramatic is LL(1)")
    print("=======================================\n")
    
    option = input("Enter an option: ")
    if option.isdigit():
        selected = int(option)
        funciones_LL1(selected)
    else:
        pass

def case_2():
    print("You selected 2")
    print("=======================================")
    print("You selected 1")
    print("Select an option:")
    print("1. Process string")
    print("2. First and follow")
    print("3. Gramatic is LR(0)")
    print("4. Automata")
    print("=======================================\n")
    
    option = input("Enter an option: ")
    selected = int(option)
    funciones_LR0(selected)

def default_case():
    print("Invalid option")

def funciones_LL1(num): #Procesar cadena / Sacar first y follow
    if num == 1:
        print("You selected 1") 
        pass    #Procesar una cadena 
    elif num == 2:
        print("You selected 2")
        pass    #Fisrt y follow
    elif num == 3:
        print("You selected 3")
        pass    #Gramatica LL(1)
    else:
        default_case()

def funciones_LR0(num): #Procesar cadena / Sacar first y follow
    if num == 1:
        print("You selected 1") 
        pass    #Procesar una cadena 
    elif num == 2:
        print("You selected 2")
        pass    #Fisrt y follow
    elif num == 3:
        print("You selected 3")
        pass    #Gramatica lR(0)
    elif num == 4:
        print("You selected 4")
        pass    #Automata
    else:
        default_case()

if __name__ == '__main__':
    while True:
        try:
            print("=======================================")
            print("Enter the number of the gramatic")
            print("Enter 0 for termin the program")
            print("=======================================")
            number = input("Enter the number of the gramatic: ")

            option = input("Enter an option: ")
            if option == 0:
                break
            selected = int(option)
            gramatica = Grammar()
            grammarPath = "Tests\\Gramatica" + str(number)  + ".txt"
            gramatica.from_file(grammarPath)
            os.system('cls' if os.name == 'nt' else 'clear')

            parser = TDParser(gramatica.from_file())
            print()
            
            print("=======================================")
            print("Select an option:")
            print("1. LL(1)")
            print("2. LR(0)")
            print("3. Exit")
            print("=======================================\n")

        except:
            pass