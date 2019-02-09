from copy import deepcopy


class CallResults:
    def __init__(self, input_arguments, input_kwargs, output_arguments, output_kwargs, return_value):
        self.__input_arguments = input_arguments
        self.__input_kwargs = input_kwargs
        self.__output_arguments = output_arguments
        self.__output_kwargs = output_kwargs
        self.__return_value = return_value

    @property
    def input_arguments(self):
        return self.__input_arguments

    @property
    def input_kwargs(self):
        return self.__input_kwargs

    @property
    def output_arguments(self):
        return self.__output_arguments

    @property
    def output_kwargs(self):
        return self.__output_kwargs

    @property
    def return_value(self):
        return self.__return_value


def call_function(f, *args, **kwargs):
    input_args = deepcopy(args)
    input_kwargs = deepcopy(kwargs)
    output_args = deepcopy(args)
    output_kwargs = deepcopy(kwargs)
    return_value = f(*output_args, **output_kwargs)

    return CallResults(input_args, input_kwargs, output_args, output_kwargs, return_value)


