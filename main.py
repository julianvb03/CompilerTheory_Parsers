from BottonUp import BUParser
from TopDown import TDParser
from Grammar import Grammar
import os

def funciones_LL1(num, parser): #Procesar cadena / Sacar first y follow
    if num == 1:
        print("You selected 1")
        str_p = str(input("Enter a string for analysis: "))
        if parser.analixer_word(str_p):
            print(f"Succesful process ({str_p}):", parser.analixer_word(str_p))
        else:
            print(f"Succesful process ({str_p}):", parser.analixer_word(str_p))

    elif num == 2:
        print("You selected 2")
        print(parser.__str__())

    elif num == 3:
        print("You selected 3")
        if parser.ll1_verification():
            print("Grammar is LL(1):", parser.ll1_verification())
        else:
            print("Grammar isn't LL(1):", parser.ll1_verification())

    else:
        default_case()

def funciones_LR0(num, parser): #Procesar cadena / Sacar first y follow
    if num == 1:
        print("You selected 1")
        str_p = str(input("Enter a string for analysis: "))
        if parser.analyce_word(str_p):
            print(f"Succesful process ({str_p}):", parser.analyce_word(str_p))
        else:
            print(f"Succesful process ({str_p}):", parser.analyce_word(str_p))

    elif num == 2:
        print("You selected 2")
        print(parser.__str__())

    elif num == 3:
        pass


    else:
        default_case()

def case_1(parser):
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
        funciones_LL1(selected, parser)
    else:
        default_case()

def case_2(parser):
    print("You selected 2")
    print("=======================================")
    print("You selected 1")
    print("Select an option:")
    print("1. Process string")
    print("2. First and follow")
    print("3. Gramatic is LR(0)")
    print("=======================================\n")
    
    option = input("Enter an option: ")
    if option.isdigit():
        selected = int(option)
        funciones_LR0(selected, parser)
    else:
        default_case()

def default_case():
    print("Invalid option")


if __name__ == '__main__':
    while True:
        try:
            print("=======================================")
            print("Enter the number of the gramatic")
            print("Enter 0 for termin the program")
            print("=======================================")
            number = input("Enter the number of the gramatic: ")
            if(number.isdigit()):
                number = int(number)
            else:                
                print("Enter a number...")
                continue

            if(number < 1 or number > 23):
                print("Invalid option.")
                break;
            else:
                gramatica = Grammar()
                ruta_actual = os.path.dirname(os.path.abspath(__file__))
                ruta_tests = os.path.join(ruta_actual, 'Tests')
                nombre_documento = "Gramatica" + str(number)  + ".txt"
                nombre_documento = str(nombre_documento)
                ruta_documento = os.path.join(ruta_tests, nombre_documento)
                
                gramatica.from_file(ruta_documento)

                os.system('cls' if os.name == 'nt' else 'clear')
                print()
            
            print("=======================================")
            print(nombre_documento)
            print("Select an option:")
            print("1. LL(1)")
            print("2. LR(0)")
            print("3. Exit")
            print("----------------------------------------")
            selected = input("Enter an option: ")

            if(selected.isdigit()):
                if (selected == '1'):
                    parser = TDParser(gramatica)
                    case_1(parser);
                    break
                elif(selected == '2'):
                    parser = BUParser(gramatica)
                    case_2(parser)
                    break;
                elif(selected == '3'):
                    print("Good bye... :)");
                    break;
                else:
                    default_case()
                    break;
            else:
                print("Enter a number...")
        except Exception as e:
            print("Problema:", str(e))
            