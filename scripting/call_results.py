from copy import deepcopy


class CallResults:
    def __init__(self, input_arguments, output_arguments, return_value):
        self.__input_arguments = input_arguments
        self.__output_arguments = output_arguments
        self.__return_value = return_value

    @property
    def input_arguments(self):
        return self.__input_arguments

    @property
    def output_arguments(self):
        return self.__output_arguments

    @property
    def return_value(self):
        return self.__return_value


def call_function(f, *args):
    input_args = deepcopy(args)
    output_args = deepcopy(args)
    return_value = f(*output_args)

    return CallResults(input_args, output_args, return_value)


