import click
import validators
from extraction_benchmark.globals import *


@click.command(name='fetch')
@click.option('-s', '--source', help='source to extract from' ,type=click.Choice([*SOURCES]), default='gdelt')
@click.option('-d','--domain', help='domain of news we want to extract', default='')
@click.option('-k','--keyword', help='keyword of news we want to extract (works with gdelt source)', default='')
@click.option('-l','--language', help='language of news we want to extract (works with gdelt source)', default='english')
@click.option('-t','--timespan', help='time span of news we want to extract (works with gdelt source)', default='1weeks')
@click.option('-m', '--mode', help='choose mode of output (works with gdelt source)', type=click.Choice([*MODES]), default='ArtList')
def fetch(source, domain, keyword, language, mode, timespan):
    """
    Fetch URLs from various sources
    """

    if not source:
        click.echo('No sources selected.', err=True)
        return

    if source == 'gdelt':
        if timespan[0].isnumeric():
            if timespan[1:] not in ['days', 'weeks', 'months', 'years']:
                click.echo('Invalid timespan. Must be in the format "Xdays", "Xweeks", "Xmonths" or "Xyears".', err=True)
                return
    
    if source == 'npbuild':
        if not domain:
            click.echo('Domain must be provided for npbuild source.', err=True)
            exit()
        elif not validators.url(domain):
            click.echo('Domain must be a valid url', err=True)
            exit()
    '''
    if source == 'newsplease':
        if not domain:
            click.echo('Domain must be provided for newsplease source.', err=True)
            exit()
        elif not validators.url(domain):
            click.echo('Domain must be a valid url', err=True)
            exit()
    '''



    from extraction_benchmark.fetch_urls import fetch_urls
    fetch_urls(source, domain, keyword, language, mode, timespan)