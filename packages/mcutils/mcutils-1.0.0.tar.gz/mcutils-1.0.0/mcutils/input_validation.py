from print_manager import mcprint, Color

def print_error(operators_list = None, contains_list = None, return_type=None):
    return
    if operators_list:
        for operator in operators_list:
            if return_type == int:
                mcprint(text="input must be {}".format(operator),
                        color=Color.RED)
            elif return_type == str:
                mcprint(text="input length must be {}".format(operator),
                        color=Color.RED)
    if contains_list:
        mcprint(text="input must be one of the following", color=Color.RED)
        for contains in contains_list:
            mcprint(text="\t{}".format(contains), color=Color.RED)

def input_validation(user_input, return_type, valid_options):

    if return_type == int:
        if not user_input.isnumeric():
            return False
        user_input = int(user_input)

    # Contains validation
    if valid_options:

        operators_list = list(filter(lambda x: str(x).startswith(('<', '>', '==', '!=')), valid_options))
        contains_list = list(set(valid_options) - set(operators_list))

        # Complex validation
        # Special operators
        for operator in operators_list:
            if '<=' in operator:
                value = operator.replace('<=', '')
                if return_type == int:
                    if not user_input <= int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False
                elif return_type == str:
                    if not len(user_input) <= int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False

            elif '>=' in operator:
                value = operator.replace('>=', '')
                if return_type == int:
                    if not user_input >= int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False
                elif return_type == str:
                    if not len(user_input) >= int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False

            elif '<' in operator:
                value = operator.replace('<', '')
                if return_type == int:
                    if not user_input < int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False
                elif return_type == str:
                    if not len(user_input) < int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False

            elif '>' in operator:
                value = operator.replace('>', '')
                if return_type == int:
                    if not user_input > int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False
                elif return_type == str:
                    if not len(user_input) > int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False

            elif '==' in operator:
                value = operator.replace('==', '')
                if return_type == int:
                    if not user_input == int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False
                elif return_type == str:
                    if not len(user_input) == int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False
            elif '!=' in operator:
                value = operator.replace('!=', '')
                if return_type == int:
                    if not user_input != int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False
                elif return_type == str:
                    if not len(user_input) != int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False

        # if contains in valid options
        if len(contains_list) > 0:
            if user_input not in contains_list:
                return False

    return True
