#!/usr/bin/python3
import argparse
from typing import Dict


class SSConverter(object):
    """
    Convert the dot-bracket format to a MrBayes readable format.
    """

    def __init__(self, sequence: str):
        self.__sequence = sequence
        self.__converter()

    def __converter(self) -> None:

        self.__stem_pair_list = []
        self.__loop_list = []

        stem_open_list = []
        stem_close_list = []
        dot_list = []
        loop_open = int()

        # Generate position of complementary parenthesis
        for i, SS in enumerate(self.__sequence):

            if SS == ')':
                stem_close_list.append(i+1)

            elif SS == '(':
                stem_open_list.append(i+1)

            else:
                dot_list.append(i+1)

        # Populate steam pairs
        for i, stem_close in enumerate(stem_close_list):
            for y, stem_open in enumerate(stem_open_list):
                if stem_close > stem_open:
                    continue
                else:
                    self.__stem_pair_list.append(
                        (stem_open_list[y-1], stem_close))
                    del stem_open_list[y-1]
                    break

        if len(stem_open_list) > 0:
            for i, stem_open in enumerate(stem_open_list):
                for y, stem_close in enumerate(stem_close_list):
                    self.__stem_pair_list.append(
                        (stem_open, stem_close_list[-(i+1)]))
                    break

        # Populate loops
        if len(dot_list) > 1:

            loop_open = dot_list[0]

            for i, position in enumerate(dot_list):

                if i == len(dot_list) - 1:
                    if position - dot_list[i-1] == 1 and loop_open < position:
                        self.__loop_list.append((loop_open, position))
                    else:
                        self.__loop_list.append((loop_open, loop_open))
                        self.__loop_list.append((position, position))

                elif position - dot_list[i-1] < 2 and position >= loop_open:
                    continue

                else:
                    if loop_open <= dot_list[i-1]:
                        self.__loop_list.append((loop_open, dot_list[i-1]))

                        loop_open = dot_list[i]

        self.__ss = {
            'stems': ' '.join('{} {}'.format(*pares) 
                for pares in sorted(self.__stem_pair_list)),
            
            'loops': ' '.join('{}-{}'.format(a, b) 
                if a != b else '{}'.format(a) 
                for a, b in sorted(self.__loop_list)),
            
            'pairs': ','.join('{}:{}'.format(*pares) 
                for pares in sorted(self.__stem_pair_list))
        }

    def get_ss(self) -> Dict:
        """
        Return a dict containing the secondary structure.
        """
        return self.__ss

    def print_ss(self) -> None:
        """
        Print the secondary structure in terminal.
        """

        print("\nstems =", ' '.join('{} {}'.format(*pares)
            for pares in sorted(self.__stem_pair_list)))
        
        print("\nloops =", ' '.join('{}-{}'.format(a, b) 
            if a != b else '{}'.format(a) 
            for a, b in sorted(self.__loop_list)))
        
        print("\npairs:", ','.join('{}:{}'.format(*pares)
            for pares in sorted(self.__stem_pair_list)))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Convert the dot-bracket format to MrBayes readable format.\n"
    )

    required = parser.add_argument_group('required arguments')

    required.add_argument(
        '-s',
        help="The dot-bracket string. "
            "Ex.: -s '.((((((((((((((((((((((...)))))))))))...))).))))))))....(((((....(.((.(((.((((...))))))).)))))))).'",
        required=True
    )

    args = parser.parse_args()
    ss = SSConverter(args.s)
    ss.print_ss()

