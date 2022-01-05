###### IMPORTS ######
import my_validators as va
import random

###### CLASSES ######
class Die():

    def __init__(self,sides=6,color="white",polarity="+"):
        self.sides = sides
        self.color = color
        self.polarity = polarity

    def __str__(self): return "D"+str(self.sides)+" "+self.color+" ("+self.polarity+")"

    @property
    def sides(self): return self._sides

    @sides.setter
    def sides(self,sides):
    # Only integers equal or higher than 2 are allowed
        if va.validate_value( r"^(1[0-9]+|[2-9][0-9]*)$", str(sides) ): self._sides = int(sides)
        else: raise ValueError("A die's sides has to be an integer equal or higher than 2")

    @property
    def color(self): return self._color

    @color.setter
    # Always saved as a string, lowercase, w/o commas ','
    def color(self,color):
        if ',' in color: raise ValueError("A color name cannot contain commas (,)")
        else: self._color = str(color).lower()

    @property
    def polarity(self): return self._polarity

    @polarity.setter
    def polarity(self,polarity):
        # Polarity is only '+' or '-'
        if va.validate_value( r"^[\+\-]$", polarity ): self._polarity = polarity
        else: raise ValueError("The die's polarity can only be '+' or '-'")

    def throw(self):
        if self.polarity == '+': return random.randint(1,self.sides)
        elif self.polarity == '-': return -random.randint(1,self.sides)

class DiceSet():

    def __init__(self,name="default"):
        self.name = name
        self.dice_list = []

    def __str__(self):

        str_dice_list = "\nSet Name: " + self.name

        if self.dice_list == []:
            str_dice_list += "\n<< EMPTY >>"
            return str_dice_list

        i = 0
        for d in self.dice_list:
            str_dice_list += "\n" + str(i+1) + ". " + str(d)
            i += 1
        return str_dice_list

    def __iter__(self):
        for current_die in self.dice_list:
            yield current_die

    @property
    def name(self): return self._name

    @name.setter
    def name(self,name):
        # Can be any string w/o commas
        if ',' in name: raise ValueError("A set name cannot contain commas (,)")
        else: self._name = str(name)

    @property
    def dice_list(self): return self._dice_list

    @dice_list.setter
    def dice_list(self,dice_list):
        # A dice_list can only point to a List entirely made of Die objects
        if isinstance(dice_list,list):
            for element in dice_list:
                if not isinstance(element,Die):
                    raise ValueError("One element in the set is not a die.")
        else: raise ValueError("The dice list must be a list.")
        self._dice_list = dice_list

    def get_copy(self):
        copy_dice_set = DiceSet(self.name)
        copy_dice_set.dice_list = self.dice_list.copy()
        return copy_dice_set

    def add_die(self,die):
        if isinstance(die,Die): self.dice_list.append(die)
        else: raise ValueError("Only Dice can be added to a Dice Set.")

    def throw_dice(self):
        total = 0
        str_throws_sum = "\n\u2685 RESULTS \u2685"

        if self.dice_list == []: str_throws_sum += "\n<< EMPTY >>"

        for d in self.dice_list:

            current_throw = d.throw()
            total += current_throw

            if current_throw < 0:
                str_throws_sum += '\n- ' + str(abs(current_throw)) + ' (' + d.color + ')'
            else:
                str_throws_sum += '\n+ ' + str(current_throw) + ' (' + d.color + ')'

        str_throws_sum += "\n= " + str(total)

        return str_throws_sum

    def delete_dice(self,dice_to_delete):

        if isinstance(dice_to_delete,DiceSet):
            self.dice_list = [ d for d in self.dice_list if d not in dice_to_delete.dice_list ]
        else:
            raise ValueError("The parameter for this function should be a temporary Dice Set with the dice to be deleted.")

class DiceBox():

    def __init__(self): self.dice_sets_dict = {}

    def __str__(self):
        str_dice_box = "\n# # # YOUR DICE BOX # # #"

        if self.dice_sets_dict == {}:
            str_dice_box += "\n<< EMPTY >>"
            return str_dice_box

        i = 0
        for s in self.dice_sets_dict.values():
            str_dice_box += "\n- - - - - -" + str(s)
        return str_dice_box

    @property
    def dice_set_dict(self): return self._dice_sets_dict

    @dice_set_dict.setter
    def dice_set_dict(self,dice_sets_dict):
        # A dice_sets_list can only hold a List entirely made of Dice Sets
        if isinstance(dice_sets_dict,dict):
            for ds in dice_sets_dict.values():
                if not isinstance(ds,DiceSet):
                    raise ValueError("One element in the set is not a Dice Set.")
        else: raise ValueError("The Dice Sets Dictionary must be a dictionary.")
        self._dice_sets_dict = dice_sets_dict

    def is_empty(self): return self.dice_sets_dict == {}

    def dice_set_exists(self,dice_set_name): return dice_set_name in self.dice_sets_dict

    def get_dice_set_copy(self,dice_set_name): return self.dice_sets_dict[dice_set_name].get_copy()

    def add_die_to_dice_set(self,die,dice_set_name):
        if isinstance(die,Die):
            if dice_set_name in self.dice_sets_dict: self.dice_sets_dict[dice_set_name].add_die(die)
            else: raise ValueError("No Dice Set with that name exists.")
        else: raise ValueError("First paramenter should be a Die object.")

    def add_dice_set(self,dice_set):
        if isinstance(dice_set,DiceSet): self.dice_sets_dict[dice_set.name] = dice_set
        else: raise ValueError("Only Dice Sets can be added to a Dice Box.")

    def delete_dice_from_dice_set(self,dice_to_delete):
        if isinstance(dice_to_delete,DiceSet):
            self.dice_sets_dict[dice_to_delete.name].delete_dice(dice_to_delete)
        else: raise ValueError("The parameter for this function should be a Dice Set.")

    def delete_dice_set(self,dice_set_name):
        if isinstance(dice_set_name,str):
            if dice_set_name in self.dice_sets_dict.keys(): self.dice_sets_dict.pop(dice_set_name)
            else: raise ValueError("The indicated Dice Set name does not exist in this Dice Box.")
        else: raise ValueError("The parameter for this function should be a string with the name of the Dice Set to delete from the Dice Box.")

    def load_dice_box(self,filename):
        with open(filename) as dice_box_file:
            for line in dice_box_file:
                current_dice_set = DiceSet()
                current_dice_set_values = line.rstrip('\n').split(',')
                current_dice_set_length = len(current_dice_set_values)

                current_dice_set.name = current_dice_set_values[0]
                for i in range(1,current_dice_set_length,3):

                    this_die_sides = int(current_dice_set_values[i])
                    this_die_color = current_dice_set_values[i+1]
                    this_die_polarity = current_dice_set_values[i+2]

                    this_die = Die(this_die_sides,this_die_color,this_die_polarity)
                    current_dice_set.add_die(this_die)

                self.add_dice_set(current_dice_set)


    def save_dice_box(self,filename):
        with open(filename,"w") as dice_box_file:

            for current_dice_set in self.dice_sets_dict.values():
                current_file_line = ""
                current_file_line += current_dice_set.name + ','

                for current_die in current_dice_set:
                    s = str(current_die.sides)
                    c = current_die.color
                    p = current_die.polarity
                    current_file_line += s + ',' + c + ',' + p + ','

                current_file_line = current_file_line[:-1] + "\n"
                dice_box_file.write(current_file_line)

###### FUNCTIONS ######
def menu_selection():

    menu_input_msg = """\nWhat would you like to do?
1. Create new Dice (and Dice Sets)
2. See your Dice Sets
3. Delete Dice from a Dice Set
4. Delete Dice Sets
5. Throw dice!
6. Exit the program

Please input an option and press Enter: """
    invalid_menu_input_msg = "\nOnly an integer from 1 to 6 is allowed. Please try again."

    return int( va.validate_input(r"^[1-6]$",menu_input_msg,invalid_menu_input_msg) )

def create_new_dice_set_with_die(die):
    print("\nPlease create a Dice Set in where to store your new Die.")

    input_msg = "Input the name of the new Dice Set: "
    invalid_input_msg = "\nThe name cannot include commas (,). Please try again."
    new_dice_set_name = va.validate_input(r"^[^\,]+$",input_msg,invalid_input_msg)

    new_dice_set = DiceSet(new_dice_set_name)
    new_dice_set.add_die(die)
    return new_dice_set

def create_new_dice(dice_box):

    input_msg = "\nHow many dice do you want to create? (1 or more): "
    invalid_input_msg = "\nPlease input an integer higher than 1."
    quantity_of_dice = int( va.validate_input(r"^[1-9]+[0-9]*$",input_msg,invalid_input_msg) )

    for i in range(quantity_of_dice):

        input_msg = "\nHow many sides will the die #" + str(i+1) + " have? (2 or more): "
        invalid_input_msg = "\nPlease input an integer, 2 or higher."
        die_sides = int( va.validate_input(r"^(1[0-9]+|[2-9][0-9]*)$",input_msg,invalid_input_msg) )

        input_msg = "\nWhat is the color of die #" + str(i+1) + "? (Anything without commas (,) ): "
        invalid_input_msg = "\nPlease input a name without commas (,)."
        die_color = va.validate_input(r"^[^\,]+$",input_msg,invalid_input_msg)

        input_msg = "\nWill die #" + str(i+1) + " add (+) or reduce (-) points? (Input '+' or '-'): "
        invalid_input_msg = "\nPlease input only '+' or '-'."
        die_polarity = va.validate_input(r"^[\+\-]$",input_msg,invalid_input_msg)

        current_die = Die( die_sides, die_color, die_polarity )

        if dice_box.is_empty():
            new_dice_set = create_new_dice_set_with_die(current_die)
            dice_box.add_dice_set( new_dice_set )
        else:
            print("\nPlease select OR create a Dice Set in where to store your new Die.")
            input_msg = "Input 1 to select an existing Dice Set\nOr input 2 to create a new Dice Set: "
            invalid_input_msg = "\nYou can only choose 1 or 2. Please try again."
            option_selected = int( va.validate_input(r"^[1-2]+$",input_msg,invalid_input_msg) )

            if option_selected == 1:
                while True:
                    print("\nPlease select a Dice Set in where to store your new Die.")
                    print(dice_box)
                    input_msg = "\nInput the name of the Dice Set: "
                    invalid_input_msg = "\nThe name cannot include commas (,). Please try again."
                    selected_dice_set_name = va.validate_input(r"^[^\,]+$",input_msg,invalid_input_msg)

                    if dice_box.dice_set_exists(selected_dice_set_name):
                        dice_box.add_die_to_dice_set(current_die,selected_dice_set_name)
                        break
                    else: print("\nThat Dice Set name does not exist. Please try again.")
            elif option_selected == 2:
                new_dice_set = create_new_dice_set_with_die(current_die)
                dice_box.add_dice_set( new_dice_set )

def throw_dice(dice_box):

    if dice_box.is_empty(): print("\nThere are no Dice in your Dice Box! Create some Dice first.")
    else:
        while True:
            print("\nPlease select the Dice Set which you want to throw!")
            print(dice_box)
            input_msg = "\nInput the name of the Dice Set: "
            invalid_input_msg = "\nThe name cannot include commas (,). Please try again."
            selected_dice_set_name = va.validate_input(r"^[^\,]+$",input_msg,invalid_input_msg)

            if dice_box.dice_set_exists(selected_dice_set_name):
                selected_dice_set = dice_box.get_dice_set_copy(selected_dice_set_name)
                print( selected_dice_set.throw_dice() )
                break
            else: print("\nThat Dice Set name does not exist. Please try again.")

def delete_dice_from_dice_set(dice_box):

    if dice_box.is_empty(): print("\nThe Dice Box is empty. There are no Dice to delete.")
    else:
        while True:
            print("\nPlease select the Dice Set that you want to work with.")
            print(dice_box)
            input_msg = "\nInput the name of the Dice Set: "
            invalid_input_msg = "\nThe name cannot include commas (,). Please try again."
            selected_dice_set_name = va.validate_input(r"^[^\,]+$",input_msg,invalid_input_msg)

            if dice_box.dice_set_exists(selected_dice_set_name): break
            else: print("\nThat Dice Set name does not exist. Please try again.")

        dice_to_delete = DiceSet(selected_dice_set_name)
        dice_set_to_edit = dice_box.get_dice_set_copy(selected_dice_set_name)

        for current_die in dice_set_to_edit:
            print("\n" + str(current_die))
            input_msg = "Do you want to delete this Die? Please input yes (y) or no (n): "
            invalid_input_msg = "\nOnly yes (y) or no (n) are valid inputs. Please try again."
            option_selected = va.validate_input(r"^(yes|y|no|n)$",input_msg,invalid_input_msg)

            if option_selected in ("yes",'y'): dice_to_delete.add_die(current_die)

        dice_box.delete_dice_from_dice_set(dice_to_delete)

        print("\nThe Dice you selected have been succesfully deleted!")

def delete_dice_set(dice_box):
    if dice_box.is_empty(): print("\nThe Dice Box is empty. There are no Dice Sets to delete.")
    else:
        while True:
            print("\nPlease select the Dice Set that you want to delete.")
            print(dice_box)
            input_msg = "\nInput the name of the Dice Set: "
            invalid_input_msg = "\nThe name cannot include commas (,). Please try again."
            selected_dice_set_name = va.validate_input(r"^[^\,]+$",input_msg,invalid_input_msg)

            if dice_box.dice_set_exists(selected_dice_set_name): break
            else: print("\nThat Dice Set name does not exist. Please try again.")

        dice_box.delete_dice_set(selected_dice_set_name)
        print("\nThe Dice Set has been deleted succesfully!")

def main_loop():

    main_dice_box = DiceBox()
    main_dice_box.load_dice_box("dice_box.txt")

    exit = False
    while not exit:
        print("\n\u2680 \u2681 \u2682 DICE SIMULATOR \u2683 \u2684 \u2685")

        option_selected = menu_selection()

        if option_selected == 1: create_new_dice(main_dice_box)
        elif option_selected == 2: print(main_dice_box)
        elif option_selected == 3: delete_dice_from_dice_set(main_dice_box)
        elif option_selected == 4: delete_dice_set(main_dice_box)
        elif option_selected == 5: throw_dice(main_dice_box)
        elif option_selected == 6:
            print("\nThank you for using Dice Simulator! See you later :)")
            exit = True

        main_dice_box.save_dice_box("dice_box.txt")

###### EXECUTION ######
main_loop()
