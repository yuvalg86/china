#!/usr/bin/python3
"""Usage: tonumbered.py [--input=<FILE> --output=<FILE>]

Process text file and saves it numbered in daniel's way.

Options:
  -h --help     prints this screen
  --input=<FILE>    input text to load [default: input.txt]
  --output=<FILE>   Output text file to save [default: output.txt]
"""


from docopt import docopt

KEY_FOR_MAX_VALUE = 'max'


def load_file(filename):
    """
    function that loads the text file.
    # assumption: for a line with k tabs, the line under it will have no more than k+1 tabs.
    :param filename: a text file in correct format.
    :return: list with file content
    """
    try:
        with open(filename) as f:
            return f.readlines()
    except Exception as e:
        print("error occurred while loading file...", e)
        exit(1)


def prepare_new_prefix(counters, num_of_tabs):
    """
    function that loads the text file.

    :param filename: a text file in correct format.
    :return: list with file content
    """
    prefix = ""
    number_str = str(counters[0])
    for i in range(num_of_tabs):
        prefix += "\t"
        number_str += '.' + str(counters[i + 1])
    number_str += ". "
    return prefix + number_str


def reset_counters_after_n(n, counters):
    """
    function that resets all the coutners after n.
    :param n: needed index to reset after it.
    :param counters: coutners of the tabs
    """
    for i in range(n, counters[KEY_FOR_MAX_VALUE]):
        # print("reset")
        counters[i + 1] = 0
    # print(counters)
    return counters


def get_tabs_from_line(line):
    """
    function that gets only tabs from a single line of the text.
    :param line: the needed line to process.
    """
    tabs = ''
    for word in line:
        if word == '\t':
            tabs += '\t'
        else:
            break
    return tabs


def process_line(line, counters):
    """
    function that processes a single line of the text.
    :param line: the needed line to process.
    :param counters: coutners of current tab status.
    """
    tabs = get_tabs_from_line(line)
    str_only = line.lstrip('\t')
    num_of_tabs = tabs.count('\t')
    try:
        counters[num_of_tabs] += 1
        counters = reset_counters_after_n(num_of_tabs, counters)
    except KeyError:
        counters[num_of_tabs] = 1
        counters[KEY_FOR_MAX_VALUE] = num_of_tabs
    prefix = prepare_new_prefix(counters, num_of_tabs)
    return prefix + str_only, counters


def process(data):
    """
    function that processes the data list to needed format.
    :param data: data containing text lines.
    """
    try:
        counters = {}
        new_data = []
        for line in data:
            if line.strip() == '':
                new_line = line
            else:
                new_line, counters = process_line(line, counters)
            print(new_line)
            new_data.append(new_line)
        return new_data
    except Exception as e:
        print("error while processing...", e)
        exit(1)


def save_file(data, filename):
    """
    function that saves the data to text file.
    :param data: text list to be written
    """
    try:
        with open(filename, 'w') as f:
            for line in data:
                f.write(line)

    except Exception as e:
        print("error occurred while saving csv...", e)
        exit(1)


def main():
    arguments = docopt(__doc__, version='tonumbered 0.1')
    text = load_file(arguments['--input'])
    new_text = process(text)
    save_file(new_text, arguments['--output'])


if __name__ == "__main__":
    main()
