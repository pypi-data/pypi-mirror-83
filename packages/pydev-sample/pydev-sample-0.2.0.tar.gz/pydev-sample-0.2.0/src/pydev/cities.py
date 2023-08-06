"""
Analysis of cities based on data from Wikipedia.

This module downloads Wikipedia descriptions of cities, which are then
encoded into vector representations using the Universal Sentence
Encoder from Tensorflow Hub. These vectors can then be compared to
get a quantitative estimate of how similar cities are based on their
Wikipedia text.

Use compare_cities to compare a reference city to a list of other
cities.
"""

import numpy as np
from scipy.spatial import distance
import pandas as pd
import wikipedia
import tensorflow_hub as hub


def load_use_model(version='standard'):
    """
    Load the univeral sentence encoder from Tensorflow Hub.

    Parameters
    ----------
    version : {'standard', 'lite'}
        Universal Sentence Encoder version to load.

    Returns
    -------
    model : callable
        Tensorflow model.
    """
    if version == 'standard':
        module_url = 'https://tfhub.dev/google/universal-sentence-encoder/4'
    elif version == 'lite':
        module_url = (
            'https://tfhub.dev/google/universal-sentence-encoder-lite/2')
    else:
        raise ValueError(f'Unknown version: {version}')

    model = hub.load(module_url)
    return model


def get_city_title(city_name):
    """
    Convert city name to Wikipedia page title.

    Parameters
    ----------
    city_name : str
        Short name of the city.

    Returns
    -------
        Full city name. Looks for the city in a fixed dictionary, then
        searches Wikipedia.

    Raises
    ------
    ValueError
        If the city title is not found.
    """
    names = {'Austin': 'Austin, Texas',
             'Boulder': 'Boulder, Colorado',
             'Nashville': 'Nashville, Tennessee',
             'New York': 'New York City'}
    if city_name in names:
        title = names[city_name]
    else:
        # look for an exact match
        results = wikipedia.search(city_name)
        if city_name in results:
            title = city_name
        else:
            print(f'No exact match for {city_name}. Search results:')
            for name in results:
                print(name)
            raise ValueError('City title not found.')
    return title


def city_summary(page_title, sentences=None):
    """
    Download a text summary of a city from Wikipedia.

    Parameters
    ----------
    page_title : str
        Title of a Wikipedia page.

    sentences : int
        Number of sentences to include from the summary.

    Returns
    -------
    summary : str
        Plain text summary.
    """
    summary = wikipedia.summary(page_title, sentences=sentences)
    return summary


def city_vector(name, model, sentences=None):
    """
    Get a vector corresponding to a city summary.

    Parameters
    ----------
    name : str
        Short name of a city.

    model : callable
        TensorFlow embedding model to run.

    sentences : int
        Number of sentences to include from the Wikipedia summary.

    Returns
    -------
    vector : numpy.array
        Vector representation of the city based on its Wikipedia
        summary.
    """
    title = get_city_title(name)
    summary = city_summary(title, sentences)
    vector = model([summary])
    return vector


def compare_cities(reference_city, comparison_cities, model=None,
                   model_version='standard', sentences=30):
    """
    Compare a reference city to a list of comparison cities.

    Parameters
    ----------
    reference_city : str
        Short name of city to compare others to.

    comparison_cities : list of str
        Cities to compare to the `reference_city`.

    model : callable, optional
        Embedding model to run on city text.

    model_version : {'standard', 'lite'}, optional
        If `model` not specified, this version of the Universal
        Sentence Encoder will be downloaded and used.

    sentences : int
        Number of sentences to use from each city's summary text.

    Returns
    -------
    results : pandas.Series
        Correlation between the reference city and each comparison
        city.
    """
    if model is None:
        model = load_use_model(model_version)
    reference = city_vector(reference_city, model, sentences).numpy()
    comparison = np.vstack([city_vector(name, model, sentences).numpy()
                            for name in comparison_cities])
    similarity = 1 - distance.cdist(reference, comparison, 'correlation')
    results = pd.Series(similarity[0], index=comparison_cities)
    return results
