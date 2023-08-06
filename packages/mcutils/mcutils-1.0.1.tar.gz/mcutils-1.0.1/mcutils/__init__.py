import os
from datetime import datetime

from .input_validation import input_validation
from .logger import *
from .print_manager import *

"""Top-level package for mcutils."""

__author__ = """Matias Canepa Gonzalez"""
__email__ = 'macanepa@miuandes.cl'
__version__ = '1.0.1'

"""Main module."""

Log = LogManager(developer_mode=True)


def exit_application(text=None, enter_quit=False):
    if text is not None:
        mcprint(text=text, color=Color.YELLOW)

    Log.log("Exiting Application Code:0")
    if enter_quit:
        get_input(text="Press Enter to exit...")
    exit(0)


def register_error(error_string, print_error=False):
    message = "Error Encountered <{}>".format(error_string)
    if print_error:
        mcprint(text=message, color=Color.RED)
    Log.log(text=message, is_error=True)


def get_input(format_=">> ", text=None, can_exit=True, exit_input="exit", valid_options=None, return_type=str,
              validation_function=None, color=None):
    if text is not None:
        mcprint(text=text, color=color)

    while True:
        user_input = input(format_)

        # Emergency exit system
        if user_input == exit_input:
            if can_exit:
                exit_application()
            else:
                register_error("Can't exit application now")

        # This is the build-in validations system
        if validation_function is not None:
            validation = validation_function.__call__(user_input)

        # This is the external validation system
        else:
            # from input_validation import input_validation
            validation = input_validation(user_input=user_input, return_type=return_type, valid_options=valid_options)
        if validation:
            break

        register_error("Not Valid Entry")

    return user_input


def clear(n=3):
    print("\n" * n)


class Credits:
    def __init__(self,
                 authors=None,
                 company_name=None,
                 team_name=None,
                 github_account=None,
                 email_address=None,
                 github_repo=None):

        self.authors = authors
        self.company_name = company_name
        self.team_name = team_name
        self.github_account = github_account
        self.github_repo = github_repo
        self.email_address = email_address

    def print_credits(self):
        clear(100)
        mcprint(">> Credits <<")
        if self.company_name:
            mcprint("Company: {}".format(self.company_name))
        if self.team_name:
            mcprint("Developed by {}".format(self.team_name))
        if self.authors:
            mcprint("\nAuthors:")
            for author in self.authors:
                mcprint("\t-{}".format(author))
        print()
        if self.email_address:
            mcprint("Email: {}".format(self.email_address))
        if self.github_account:
            mcprint("GitHub: {}".format(self.github_account))
        if self.github_repo:
            mcprint("GitHub Repository: {}".format(self.github_repo))
        get_input(text="\nPress Enter to Continue...")


class MenuFunction:
    def __init__(self, title=None, function=None, **kwargs):
        self.function = function
        self.title = title
        self.kwargs = kwargs
        self.returned_value = None

    def print_function_info(self):
        mcprint("Function: %s" % self.function)

        for parameter in self.kwargs:
            mcprint(parameter)

    def get_unassigned_params(self):
        unassigned_parameters_list = []
        for parameter in self.function.func_code.co_varnames:
            if parameter not in self.kwargs:
                mcprint(parameter)
                unassigned_parameters_list.append(parameter)
        return unassigned_parameters_list

    def get_args(self):
        mcprint(self.kwargs)
        return self.kwargs

    def call_function(self):
        self.returned_value = self.function(**self.kwargs)
        return self.returned_value


class Menu:

    def __init__(self, title=None, subtitle=None, text=None, options=None, return_type=int, parent=None,
                 input_each=False,
                 previous_menu=None, back=True):
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.options = options
        self.return_type = return_type
        self.parent = parent
        self.input_each = input_each
        self.previous_menu = previous_menu
        self.back = back
        self.returned_value = None
        self.function_returned_value = None

    def set_parent(self, parent):
        self.parent = parent

    def set_previous_menu(self, previous_menu):
        self.previous_menu = previous_menu

    def get_selection(self):

        start_index = 1
        if self.back:
            start_index = 0

        # if there exist options it means user have to select one of them
        if (self.options.__len__() != 0) and (not self.input_each):

            while True:

                selection = get_input()

                if selection.__str__().isdigit():
                    if int(selection) in range(start_index, (self.options.__len__()) + 1):
                        if int(selection) != 0:
                            if isinstance(self.options[int(selection) - 1], MenuFunction):
                                function = self.options[int(selection) - 1]
                                self.function_returned_value = function.call_function()
                            elif isinstance(self.options[int(selection) - 1], Menu):
                                sub_menu = self.options[int(selection) - 1]
                                sub_menu.set_parent(self)
                                sub_menu.show()
                        else:
                            if self.parent is not None:
                                self.parent.set_previous_menu(self)
                                self.parent.show()
                        break
                    else:
                        register_error("Index not in range")

                else:
                    register_error("Entered must be int.")

        elif self.input_each:
            selection = {}
            for option in self.options:
                print(option)
                if isinstance(self.options, dict):
                    filter_criteria = self.options[option]
                    return_type = int
                    if filter_criteria[0] in [str, int]:
                        return_type = filter_criteria[0]
                        filter_criteria = filter_criteria[1:]
                    parameter_value = get_input(format_="{} >> ".format(option),
                                                valid_options=filter_criteria,
                                                return_type=return_type)
                else:
                    parameter_value = get_input("{} >> ".format(option))
                selection[option] = parameter_value

        # if there aren't any option it means user must input a string
        else:
            selection = get_input()

        self.returned_value = selection
        return selection

    def show(self):
        # if(self.previous_menu != None) and (self != self.previous_menu):
        #     del(self.previous_menu)
        clear()
        if self.title is not None:
            mcprint("=== %s " % self.title)
        if self.subtitle is not None:
            mcprint("- - %s" % self.subtitle)
        print()
        if self.text is not None:
            mcprint(self.text)

        # print "Parent:",self.parent
        if self.options and not self.input_each:
            for index, option in enumerate(self.options):
                if isinstance(option, MenuFunction):
                    print("%s. %s" % (str(index + 1), option.title))
                elif isinstance(option, Menu):
                    print("%s. %s" % (str(index + 1), option.title))
                else:
                    print("%s. %s" % (str(index + 1), option))
            if self.back:
                mcprint("0. Back")

        selected_option = self.get_selection()
        return selected_option


class DirectoryManager:
    class File:
        def __init__(self, path, name, extension, size, created_at):
            self.path = path
            self.name = name
            self.extension = extension
            self.size = size
            self.created_at = created_at

        def print_info(self):
            mcprint("Name: {}".format(self.name))
            mcprint("Path: {}".format(self.path))
            mcprint("Extension: {}".format(self.extension))
            mcprint("Size: {}".format(self.size))
            mcprint("Created at: {}".format(self.created_at))
            print()

        # Modify delete function
        def delete_file(self):
            mcprint("Deleting File <{}>".format(self.path), color=Color.RED)
            os.remove(self.path)

    def __init__(self, directories=None):
        self.directories = directories
        self.files = []
        self.selected_files = []
        self.get_files()

    def get_dirs(self):
        dirs_list = []
        for file in self.files:
            dirs_list.append(file.path)
        return dirs_list

    # Retrieves a list of Files in self.files
    def get_files(self):
        import os
        def create_file(directory_name, new_file_name=None):

            file_dir = directory_name
            if new_file_name is not None:
                file_dir = os.path.join(directory_name, new_file_name)
            else:
                new_file_name = file_dir.rsplit('\\', 1)[-1]

            created_at = datetime.datetime.fromtimestamp(os.path.getctime(file_dir)).strftime('%Y-%m-%d %H:%M:%S')
            file = self.File(file_dir, new_file_name, new_file_name.rsplit('.', 1)[-1],
                             os.path.getsize(file_dir), created_at)
            self.files.append(file)

        for directory in self.directories:
            if os.path.isdir(directory):
                if os.path.exists(directory):
                    for file_name in os.listdir(directory):
                        create_file(directory, file_name)
                else:
                    register_error("Path \"{}\" doesn't exists".format(directory))
            elif os.path.isfile(directory):
                create_file(directory_name=directory)
            else:
                register_error("Path \"{}\" not found".format(directory))

    def print_files_info(self):
        for file in self.files:
            file.print_info()

    def filter_format(self, extensions=None):
        new_files = []
        for file in self.files:
            if file.extension in extensions:
                new_files.append(file)
        self.files = new_files

    @staticmethod
    def create_directory(directory):
        import os
        try:
            os.makedirs(directory)
        except IsADirectoryError:
            register_error(error_string="Couldn't create the directory '{}'".format(directory))

    def open_file(self, file):
        import platform
        import os
        import subprocess
        current_os = platform.system()

        if isinstance(file, self.File):
            path = file.path
        elif isinstance(file, str):
            path = file
        else:
            raise NotADirectoryError

        if os.path.isfile(path):

            Log.log("Open File <{}> // current os {}".format(file, current_os))

            if current_os == 'Linux':
                subprocess.call(('xdg-open', path))
            elif current_os == 'Windows':
                os.startfile(path)
            elif current_os == "Darwin":
                subprocess.call(('open', path))
            else:
                register_error("OS not supported")

        else:
            register_error("File \"{}\" not found".format(path))

    def add_file_to_selection(self, *args):
        Log.log("Adding Files <{}> to Selection".format(args))
        files = None
        for arg in args:
            if isinstance(arg, self.File):
                files = [arg]
            elif isinstance(arg, list):
                files = list(arg)
            elif isinstance(arg, str):
                files = list(filter(lambda x: arg in x.name, self.files))
            if files is not None:
                self.selected_files += files
        return self.selected_files

    def clear_file_selection(self):
        self.selected_files.clear()
