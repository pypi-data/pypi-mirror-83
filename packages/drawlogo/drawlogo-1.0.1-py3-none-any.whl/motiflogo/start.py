"""

Usage:
    drawlogo <input-file> [-O <path> | --output <path>] [--words-count <int>] [-r | --revcomp]
    drawlogo -h | --help

Arguments:
    <input-file>     Path to input pcm or ppm matrix
    <path>           Path to output svg file or directory
    <int>            Any positive integer


Options:
    -h, --help                      Show this.
    -O <path>, --output <path>      Output directory or file path. [default: ./]
    --words-count <int>             Words count for ppm matrix representation. [default: 100]
    -r, --revcomp                   If true draw revcomp motif
"""

from docopt import docopt
from schema import Schema, And, Const, Use, SchemaError
from svgutils import transform
import numpy as np
from math import lgamma
import os
import pathlib

script_path = os.path.join(pathlib.Path(__file__).parent.absolute())


def get_letter_svg_by_name(name):
    return os.path.join(script_path, 'letters', '{}.svg'.format(name)),


get_revcomp = {
    'A': 'T',
    'T': 'A',
    'C': 'G',
    'G': 'C',
}

nucleotides = ['A', 'C', 'G', 'T']

visible_cut_tr = 0.01

unit_width = 300
unit_height = 600


def get_KDIC(counts, N):
    return 1 / (N * np.log(0.25)) * (
                lgamma(N + 1) + sum([x * np.log(0.25) - lgamma(x + 1) for x in counts]))


def get_heights(pcm_file, mode='freq', words=100):
    heights = []
    lines = []
    with open(pcm_file) as f:
        for line in f:
            if line.startswith('>'):
                continue
            try:
                lines.append(list(map(float, line.strip('\n').split('\t'))))
            except ValueError:
                lines.append(list(map(float, line.strip('\n').split(' '))))
    m = len(lines)
    for counts in lines:
        N = sum(counts)
        if mode == 'freq':
            KDIC = get_KDIC([x*100 for x in counts], words)
            heights.append(sorted(list(zip(nucleotides, [(x / N) * KDIC for x in counts])),
                                  key=lambda x: x[1], reverse=True))
        elif mode == 'KDIC':
            KDIC = get_KDIC(counts, N)
            heights.append(sorted(list(zip(nucleotides, [(x / N) * KDIC for x in counts])),
                                  key=lambda x: x[1], reverse=True))

    return m, heights


def place_letter_on_svg(figure, letter_svg, x, y, h):
    letter_object = transform.fromfile(letter_svg)
    letter_root = letter_object.getroot()
    # 13.229 and 26.458 are letter svg view box w and h
    letter_root.scale_xy(unit_width/13.229, h/26.458)
    letter_root.moveto(x, y)
    figure.append(letter_root)


def renorm(position):
    letters, heights = zip(*position)
    total_height = sum(heights)
    new_total_height = 0
    new_heights = []
    for height in heights:
        if height < visible_cut_tr * total_height:
            new_heights.append(0)
        else:
            new_total_height += height
            new_heights.append(height)
    new_heights = [x * new_total_height / total_height for x in new_heights]
    return zip(letters, new_heights)


def draw_logo(file_path, out_path, revcomp=False, words=100):
    if file_path.endswith('.pcm'):
        mode = 'KDIC'
    elif file_path.endswith('.ppm'):
        mode = 'freq'
    else:
        raise ValueError(file_path, ' should ends with ".pcm" or ".ppm"')
    if os.path.isdir(out_path):
        out_path = os.path.join(out_path, '{}{}.svg'.format(
                                os.path.splitext(os.path.basename(file_path))[0],
                                '_revcomp' if revcomp else ''))
    m, heights = get_heights(file_path, mode=mode, words=words)
    fig = transform.SVGFigure("{}px".format(m * unit_width), "{}px".format(unit_height))

    for pos, pack in enumerate(heights[::-1] if revcomp else heights):
        current_height = 0
        for letter, height in renorm(pack):
            # Draw letter with offset of pos*unit_width, current_height*unit_height and height of height*unit_height
            place_letter_on_svg(fig, get_letter_svg_by_name(get_revcomp[letter] if revcomp else letter),
                                pos*unit_width, (1-current_height - height)*unit_height, height*unit_height)
            current_height += height

    fig.save(out_path)


def main():
    args = docopt(__doc__)
    schema = Schema({
        '<input-file>': And(
            Const(os.path.exists, error='Input file should exist'),
            Use(open, error='Input file should be readable')
        ),
        '--output': And(
            Const(os.path.exists, error='Output path should exist'),
            Const(lambda x: os.access(x, os.W_OK), error='No write permissions')
        ),
        '--words-count': Use(int, error='Number of words must be positive integer'),
        str: bool
    })
    try:
        args = schema.validate(args)
    except SchemaError as e:
        print(__doc__)
        exit('Error: {}'.format(e))

    matrix_path = args['<input-file>']
    out_path = args['--output']
    is_revcomp = args['--revcomp']
    n_words = args['--words-count']
    draw_logo(matrix_path, out_path=out_path, revcomp=is_revcomp, words=n_words)
