import re
from typing import List, Dict, Set
from itertools import product

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px


def match_mask(pattern: str, string: str) -> bool:
    """Checks if a regex pattern matches a string."""

    pattern: re.Pattern = re.compile(pattern=rf"{pattern}")

    if re.match(pattern=pattern, string=string):
        return True

    return False


def apply_mask(pattern: str, strings: List[str]) -> Dict[str, bool]:
    """Checks if a regex pattern matches a list of strings, returning a dictionary."""

    results: Dict[str, bool] = {}

    for string in strings:
        results[string] = match_mask(pattern=pattern, string=string)

    return results


def generate_strings(alphabet: Set[str], size: int) -> List[str]:
    """Generate all possible strings of an alphabet with repetitions, up until a given size."""

    # list to hold all strings
    strings: List[str] = []

    # for each possible length (1, 2, 3, ..., n)
    for i in range(size):

        # for each subset of the cartesian product with repetitions
        for p in product(alphabet, repeat=i+1):

            # join all elements of the subset with an empty string
            current_string: str = ''.join(p)

            # add current string to the list of all strings
            strings.append(current_string)

    return strings


def string_heatmap(strings, title='', figsize=(800, 800), fontsize=14, filename=None):
    """Creates a heatmap to show all strings of a list, colorized by string length."""

    # ensure that the list of strings is squared, else add empty strings until squared
    dim = len(strings)**0.5

    while (dim - int(dim)) > 0:
        strings.append("")
        dim = len(strings)**0.5

    dim = int(dim)

    # sort strings by length and reshape to a 2D list
    strings = sorted(strings, key=len)
    strings = [[strings[i:i+dim][j] if i+j < len(strings) else None for j in range(dim)] for i in range(0, len(strings), dim)]

    # calculate the lengths of each string
    lengths = [[str(len(s)) for s in row] for row in strings]

    # create the heatmap
    heatmap = go.Heatmap(
        z=lengths,
        text=strings,
        colorscale=px.colors.sequential.Rainbow,
        colorbar={"title": "Tamanho"},
        showscale=True,
        texttemplate='%{text}',
        textfont=dict(family='monospace', size=fontsize)
    )

    # create the figure layout
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(heatmap)
    fig.update_layout(
        title=dict(text=title, x=0.5),
        xaxis=dict(showticklabels=False, showgrid=False),
        yaxis=dict(showticklabels=False, showgrid=False),
        width=figsize[0], height=figsize[1],
    )

    # save the figure as .svg file
    if filename:
        fig.write_image(filename)

    return fig