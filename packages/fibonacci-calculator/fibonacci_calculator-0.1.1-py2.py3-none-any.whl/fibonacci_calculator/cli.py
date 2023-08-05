"""Console script for fibonacci_calculator."""
import sys
import click
# from fibonacci_calculator import FibonacciSequenceService



# @click.command()
# @click.option('--length', default=0, required=True, help='Set length of Fibonacci Sequence')
# def set_length(length):
#     """
#     Prints out sequence in
#     """
#     click.echo('Given input length: {0}'.format(length))
#     if length > 1:
#         sequence = FibonacciSequenceService()
#         sequence.increase_sequence_length(length)
#         click.echo(sequence.get_sequence())
#         return sequence.get_sequence()
#     else:
#         click.echo('Please give a number with a value of 2 or higher.')


@click.command()
def main(args=None):
    """Console script for fibonacci_calculator."""

    click.echo("Replace this message by putting your code into "
               "fibonacci_calculator.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/ \n\n")

    # print(set_length())

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
