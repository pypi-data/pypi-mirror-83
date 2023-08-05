from lt_hist import main
import click


@click.command(name='compare')
@click.option('--lt-name', help='name of the lt as it is in s3 directory (eg: lt-account)')
@click.option('--days', default=7, help='the number of days to be compared')
def compare(lt_name, days):
    """Plot data from a given lt"""
    main.do(lt_name, days)