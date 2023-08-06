import requests
import ffmpeg
import click
import json
import os
from .resources import Meeting
from .composer import compose_lesson


@click.group()
def main():
    pass


@main.command()
@click.option("-i", "--input-url", type=str, prompt=True,
              help="The URL of the meeting to download.")
@click.option("-o", "--output-file", type=str, prompt=True,
              help="The file the video should be written to.")
@click.option("-O", "--overwrite", is_flag=True,
              help="Overwrite existing files instead of skipping them.")
@click.option("-v", "--verbose-ffmpeg", is_flag=True,
              help="Print ffmpeg info to stderr.")
def download(input_url, output_file, overwrite=False, verbose_ffmpeg=False):
    if not overwrite and os.path.exists(output_file):
        raise click.ClickException(f"Output file already exists: {output_file}")

    click.echo(f"Downloading: {input_url} -> {output_file}", err=True)

    meeting = Meeting.from_url(input_url)
    streams = compose_lesson(meeting)
    output = ffmpeg.output(*streams, output_file)

    output.run(quiet=not verbose_ffmpeg, overwrite_output=True)


@main.command()
@click.option("-f", "--file", type=click.File(),
              help="The JSON file containing the files to download.")
@click.option("-r", "--remote-file", type=str,
              help="The URL where the JSON file containing the files to download can be fetched.")
@click.option("-O", "--overwrite", is_flag=True,
              help="Overwrite existing files instead of skipping them.")
@click.option("-v", "--verbose-ffmpeg", is_flag=True,
              help="Print ffmpeg info to stderr.")
@click.pass_context
def sync(ctx: click.Context, file=None, remote_file=None, overwrite=False, verbose_ffmpeg=False):
    if file:
        click.echo(f"Syncing from local file: {file.name}", err=True)
        j = json.load(file)
    elif remote_file:
        click.echo(f"Syncing from remote file: {remote_file}", err=True)
        j = requests.get(remote_file).json()
    else:
        raise click.ClickException("No JSON file was specified.")

    for output_file, input_url in j.items():
        try:
            ctx.invoke(download, input_url=input_url, output_file=output_file, overwrite=overwrite, verbose_ffmpeg=verbose_ffmpeg)
        except click.ClickException:
            click.echo(f"Skipped: {input_url} -> {output_file}", err=True)


if __name__ == "__main__":
    main()
