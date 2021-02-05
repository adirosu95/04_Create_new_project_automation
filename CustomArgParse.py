import argparse
from operator import attrgetter


class CustomArgParse:
    """
    Use this class if you want to insert arguments from the command-line.

    Example of an input dictionary
    args_dict = {'arg1': ['a1', ' Argument 1 Description'],
                    'arg2': ['a2', 'Argument 2 Description'],
                     'arg3': ['a3', 'Argument 3 Description']}
    """

    def __init__(self, args_dict: dict):
        self.args_dict = args_dict
        self._parser = argparse.ArgumentParser(description='----------------> Execution Instructions <----------------',
                                               epilog='-------------> End of the Execution Instructions <-------------')
        for full_arg, (abbr_arg, info_arg) in args_dict.items():
            self._parser.add_argument('-{abbr_arg}'.format(abbr_arg=abbr_arg), '--{full_arg}'.format(full_arg=full_arg),
                                      help='{info_arg}'.format(info_arg=info_arg), action='store', default=False)
        self._args = self._parser.parse_args()

    def get_args(self):
        """
        Return a dictionary where the key is the name of an argument and dict value is the value provided.
        The dictionary has elements of type string
        """
        d1 = {}
        for arg in self.args_dict.keys():
            prop_arg = attrgetter(arg)
            d1[arg] = prop_arg(self._args)
        return d1


if __name__ == "__main__":
    raise SyntaxError("This is a module and must be imported!")
