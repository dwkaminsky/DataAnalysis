import os


def base_path():
    return {
        'Danny': 'C:/Users/DannyDell/Documents/DataAnalysis'
    }[os.environ.get('USER')]
