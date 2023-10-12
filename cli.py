import click

@click.group()
def cli():
    print("hello from cli!") # add this