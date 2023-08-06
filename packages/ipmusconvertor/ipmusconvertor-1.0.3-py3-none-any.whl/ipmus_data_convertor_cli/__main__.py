import sys
import click

from ipmus_data_convertor_cli.convertor import read, createCodeFrame, decodeIpums

@click.group()
@click.version_option("1.0.0")
def main():
    pass

@main.command()
@click.argument('zipped_data_file', type=click.Path(exists=True))
@click.argument('txt_file', type=click.Path(exists=True))
@click.argument('inds', type=click.Path(exists=True))
@click.option('-o', '--output-file-name', default="ipums-decoded.csv.zip")
def convert(**kwargs):
    """
    -o=[output file] [zipped_file].csv.gz [txt_file].txt inds.txt
    """
    cd = createCodeFrame(kwargs.get('txt_file'), kwargs.get('inds'))
    df = read(kwargs.get('zipped_data_file'))

    data = decodeIpums(df, cd)

    compression_opts = dict(method='zip', archive_name=kwargs.get('output_file_name') + '.csv')
    data.to_csv(kwargs.get('output_file_name') + '.zip', index=False, compression=compression_opts)

if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("$ ipmusconvert convert -o=[output file] [zipped_file].csv.gz [txt_file].txt inds.txt")
    main()
