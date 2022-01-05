"""my_validators.py - Functions I use for validating inputs and exits"""


def validate_exit():
    """This function asks the user to input either 'y' or 'n'.
    Inputting 'y' or a variant returns True.
    Inputting 'n' or a variant returns False.
    Inputting anything else is an invalid input and loops the function.

    Remember to use a main_loop function:

    def main_loop():
        exit = False
        while not exit:
            # EXECUTION
            exit = ve.validate_exit()"""

    yes_inputs = ("Y","y","Yes","yes","YES")
    no_inputs = ("N","n","No","no","NO")
    input_message = """\nDo you want to exit this program?
Input 'y' for yes and 'n' for no: """

    while True:
        user_input = input(input_message)

        if user_input in yes_inputs: return True
        elif user_input in no_inputs: return False
        else: print("\nInvalid input. Please try again.")


def validate_value( regex, value ):
    """This function takes a regex and an input.
    If the input matches the regex exactly, it returns True.
    Otherwise, it returns False.
    Remember to pass the regex with the "r" literal to make the string raw,"""

    import re
    return re.search( regex, value ) != None


def validate_input( regex, user_input_message, invalid_input_message ):
    import re
    while True:
        str_input = input(user_input_message)
        if validate_value( regex, str_input ): return str_input
        else: print(invalid_input_message)
