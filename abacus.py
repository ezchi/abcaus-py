#!/usr/bin/env python3

import logging
import random
import datetime
import argparse
import sys

def cmd_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="cmd")

    parser_mult = subparsers.add_parser("mult",
                                        help="Times table")
    parser_mult.add_argument("tables",
                             nargs="+",
                             help="List of tables for practice")
    parser_mult.add_argument("-r, --random",
                             dest="do_random",
                             action="store_true",
                             help="Randomize the sequence in times \
                             table")
    parser_plus = subparsers.add_parser("plus",
                                        help="Plus and Minus")
    parser_plus.add_argument("--questions",
                             type=int,
                             dest="questions",
                             default=30,
                             help="Number of questions")
    parser_plus.add_argument("--operands",
                             type=int,
                             dest="operands",
                             default=5,
                             help="Number of operands")
    parser_plus.add_argument("--repeat",
                             action="store_true",
                             default=False,
                             dest="repeat",
                             help="Repeat the question with wrong answer \
                             until get it right")
    args = parser.parse_args()

    if args.cmd is None:
        parser.print_help()
        sys.exit()
    return args


def gen_questions(num_operands, max_operand=100):
    """
    Generate abacus question with given number of operands
    """
    operand = 0
    sum = 0
    tmp_sum = 0
    operands = []

    for i in range(num_operands):
        get_operand = False
        while (not get_operand):
            operand = random.randint(-sum, max_operand-1)
            tmp_sum = sum + operand
            if tmp_sum in range(max_operand):
                get_operand = True
                operands.append(operand)
                sum = tmp_sum

    return operands, sum


def print_operands(operands):
    """
    Print the operands in formula format
    """
    for i in range(len(operands)):
        if (i == 0):
            print(operands[i], end="")
        else:
            if (operands[i] >= 0):
                print(" + ", end="")
                print(operands[i], end="")
            else:
                print(" - ", end="")
                print(-operands[i], end="")
    print(" = ")


def repr_operands(operands):
    """
    Covert the operands to formula format
    """
    rslt = []
    for i in range(len(operands)):
        if (i == 0):
            rslt.append("{0:>2}".format(operands[i]))
        else:
            if (operands[i] >= 0):
                rslt.append("+ {0:>2}".format(operands[i]))
            else:
                rslt.append("- {0:>2}".format(-operands[i]))
    rslt.append("= ")
    return " ".join(rslt)


def generate_table(strTable):
    """
    Generate table list from give table stings
    """
    timesTable = []
    for t in strTable:
        if '-' in t:
            items = t.split('-')
            timesTable += [x for x in range(int(items[0]), int(items[1])+1)]
        else:
            timesTable.append(int(t))

    if [x for x in timesTable if x > 12] or [x for x in timesTable if x < 1]:
        log = logging.getLogger(__name__)
        log.error("Found Illegel Table {}".format(timesTable))
        raise ValueError("Found Illegal Table {}".format(timesTable))
    return timesTable


def mult_questions(tables, do_random=False):
    """
    Generate questions for multiple
    """
    log = logging.getLogger(__name__)

    baseTable = [x for x in range(1, 13)]

    questions = []

    for t in tables:
        for a in baseTable:
            questions.append((a, t))

    log.debug("Questions before random : {}".format(questions))

    if do_random:
        random.shuffle(questions)
    log.debug("Questions after random : {}".format(questions))

    for a, b in questions:
        correct = False
        while not correct:
            log.debug("{} x {} = ".format(a, b))
            ans = input("{} x {} = ({})".format(a, b, a*b))
            log.debug("Answer = {}".format(ans))
            try:
                if (int(ans) == a * b):
                    correct = True
                else:
                    print("The answer is wrong, try again")
            except:
                print("Can't understand what do you mean, try it again")


def ShowReport():
    """
    Display report
    """
    log = logging.getLogger(__name__)
    log.warning("ShowReport function is not implemented yet")


def main():
    """
    Main function
    """
    args = cmd_parser()

    # Logging Configuration
    FORMAT = '%(asctime)s - %(levelname)-8s - %(message)s'
    #    logging.basicConfig(format=FORMAT, level=logging.INFO, filename="abacus.log")
    logging.basicConfig(format=FORMAT, level=logging.DEBUG, filename="abacus.log")
    log = logging.getLogger(__name__)

    startTime = datetime.datetime.now()
    log.info("Start Time: {}".format(startTime))

    log.debug("Command = {}".format(args.cmd))

    if args.cmd == "mult":
        tables = generate_table(args.tables)
        mult_questions(tables, args.do_random)
    elif args.cmd == "plus":
        num_questions = args.questions
        not_repeat = not args.repeat
        num_operands = args.operands

        total_mark = 0
        wrong_ans = []

        log_fname = "wrong_questions.txt"
        log_fhd   = open(log_fname, 'w')

        for i in range(num_questions):
            mark = 1
            operands, sum = gen_questions(num_operands)
            correct = False
            while not correct:
                ans = input(repr_operands(operands))
                if (ans.isdecimal()):
                    if (int(ans) == sum):
                        correct = True
                    else:
                        log_fhd.write(repr_operands(operands))
                        log_fhd.write(ans.strip())
                        log_fhd.write("\t" + "[{0:>2d}]".format(sum))
                        log_fhd.write("\n")
                        mark = 0
                        if (not_repeat):
                            correct = True
                        else:
                            print("The answer is wrong, try again")
                else:
                    print("Sorry, give me the answer please")
                    mark = 0
            total_mark += mark

        log_fhd.close()

    endTime = datetime.datetime.now()

    log.info("End   Time: {}".format(endTime))
    log.info("Total Time: {}".format(endTime - startTime))

    print("Total time:", endTime - startTime)
    ShowReport()


if __name__ == '__main__':
    main()
