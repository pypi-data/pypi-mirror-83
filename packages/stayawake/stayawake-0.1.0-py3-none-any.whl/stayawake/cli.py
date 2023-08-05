# -*- coding: utf-8 -*-

import click
import logging
from stayawake import move_cursor

@click.command()
@click.option('--interval', '-i', type=int, default=10)
def main(interval):
    click.echo(f'Move the cursor every {interval} seconds')
    click.echo('Press ctl-c to quit.')
    move_cursor(interval)

    
if __name__ == "__main__":
    main()
