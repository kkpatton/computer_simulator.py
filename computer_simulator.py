"""
Implements the computer simulator.
"""

import os


class ComputerSimulator():

    def __init__(self):
        """Initializes computer simulator.
        """
        self.keep_going = True
        # Menu Item Constants
        self.LOAD_PROGRAM_FROM_FILE = '1'
        self.ENTER_PROGRAM_FROM_KEYBOARD = '2'
        self.LOAD_DEMO_PROGRAM = '3'
        self.RUN_PROGRAM = '4'
        self.DUMP_MEMORY = '5'
        self.QUIT = '6'

        # memory
        self.memory = [0] * 100

        # accumulator
        self.accumulator = 0

        # program counter
        self.program_counter = 0

        # opcodes

        self.READ = 10
        self.WRITE = 11
        self.LOAD = 20
        self.STORE = 21
        self.ADD = 30
        self.SUB = 31
        self.MUL = 32
        self.DIV = 33
        self.BRANCH = 40
        self.BRANCHNEG = 41
        self.BRANCHZERO = 42
        self.HALT = 43
       

    def display_menu(self):
        print('\n\n')
        print('\t\t Computer Simulator Menu')
        print('\n')
        print('\t1. Load program from file')
        print('\t2. Enter program from keyboard')
        print('\t3. Load demo program')
        print('\t4. Run program')
        print('\t5. Dump memory')
        print('\t6. Quit')
        print()

    def process_menu_choice(self):
        """
        Processes and executes menu commands.
        """
        # Get menu selection from user
        user_input = input('Enter menu choice... ')
        print(f'You entered... {user_input}')

        if not user_input:
            user_input = '0'

        # If input is valid menu choice
        # execute menu item
        # else display error message
        # and repeat menu 

        match user_input[0]:
            case self.LOAD_PROGRAM_FROM_FILE: self.load_program_from_file()
            case self.ENTER_PROGRAM_FROM_KEYBOARD: self.enter_program_from_keyboard()
            case self.LOAD_DEMO_PROGRAM: self.load_demo_program()
            case self.RUN_PROGRAM: self.run_program()
            case self.DUMP_MEMORY: self.dump_memory()
            case self.QUIT: self.keep_going = False
            case _: print(f'Invalid menu choice... {user_input[0]}')


    def load_program_from_file(self):

        try:
            # Open named file
            file_name = input('Enter the name of the file you would like to open... ')
            
            # Open the file for reading
            with open(file_name, mode = "r") as f:

                # Read the contents of the file
                # contents = f.read()
                
                # Print the contents of the file    
                # print(contents)
                # read each line
                # lines = f.readlines()

                # and store in memory
                count = 0
                for instruction_string in f.readlines():
                    self.memory[count] = int(instruction_string)
                    count += 1
            
        except Exception as e:
            print(f'Problem loading program into memory... {e}')

    def enter_program_from_keyboard(self):
        print("Enter 'exit' when you would like to return to the main menu.")
        self.memory = {}
        count = 0
        keep_going = True

        while keep_going:
            try:
               instruction = input("Please enter an instruction: ")
               if instruction.lower() == 'exit':
                  keep_going = False
               else:
                  self.memory[count] = int(instruction)
                  count += 1
            except Exception as e:
               print(f"Invalid instruction. Please try again. {e}")

        return
                   
    def load_demo_program(self):
         print('Loading demo program...')
         self.memory[0] = 1007
         self.memory[1] = 1008
         self.memory[2] = 2007
         self.memory[3] = 3208
         self.memory[4] = 2109
         self.memory[5] = 1109
         self.memory[6] = 4010
         self.memory[10] = 4300


    def run_program(self):
         print('Running program...')

         self.run = True
         self.program_counter = 0

         while self.run:
            # decode instruction
            instruction = self.memory[self.program_counter]
            opcode = int(instruction / 100)
            operand = instruction % 100
            self.program_counter += 1

            if __debug__:
                print('-' * 15)
                print(f'opcode: {opcode}')
                print(f'operand: {operand}')
                print(f'accumulator: {self.accumulator}')
                input('Press any key to continue...')
                print('-' * 15)

            # Execute instruction
            match opcode:
                case self.READ: self.read(operand)
                case self.WRITE: self.write(operand)
                case self.LOAD: self.load(operand)
                case self.STORE: self.store(operand)
                case self.ADD: self.add(operand)
                case self.SUB: self.sub(operand)
                case self.MUL: self.mul(operand)
                case self.DIV: self.div(operand)
                case self.BRANCH: self.branch(operand)
                case self.BRANCHNEG: self.branch_neg(operand)
                case self.BRANCHZERO: self.branch_zero(operand)
                case self.HALT: self.halt()
                case _: self.halt()

    def dump_memory(self):
         counter = 0
         for instruction in self.memory:
             counter += 1
             if (counter % 11) == 0:
                 print()
                 counter = 0
             else:
                 print(f'{instruction:4} ', end='')


    def read(self, operand):
        """Reads numeric input from console and stores it in
        memory location indicated by operand.
        """
        user_input = input('Enter numeric value... ')

        try:
            # Convert string input to floating point numeric value
            # If conversion fails catch exception, warn user, and set value to zero.
            self.memory[operand] = float(user_input)
        except Exception as e:
            print('ERROR: Invalid numeric value entered. Setting value to 0.')
            self.memory[operand] = 0


    def write(self, operand):
        """Write contents of memory location indicated by operand
        to console.
        """
        print(f'{self.memory[operand]}')

    def load(self, operand):
        """Load contents of memory location indicated by operand
        into the accumulator.
        """
        self.accumulator = self.memory[operand]

    def store(self, operand):
        """Store contents of accumulator into memory location indicated
        by operand.
        """
        self.memory[operand] = self.accumulator

    def add(self, operand):
        self.accumulator += self.memory[operand]

    def sub(self, operand):
        self.accumulator -= self.memory[operand]

    def mul(self, operand):
        self.accumulator *= self.memory[operand]

    def div(self, operand):
        self.accumulator /= self.memory[operand]

    def branch(self, operand):
        self.program_counter = operand

    def branch_neg(self, operand):
        if self.accumulator < 0:
            self.program_counter = operand

    def branch_zero(self, operand):
        if self.accumulator == 0:
            self.program_counter = operand

    def halt(self):
        self.run = False

    def launch_application(self):
        while self.keep_going:
            self.display_menu()
            self.process_menu_choice()
