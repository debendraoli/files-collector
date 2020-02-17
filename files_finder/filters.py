from typing import Iterable, Generator

def get_extensions(allowed_extensions: Iterable, links: Iterable) -> Generator:
    """
    :param allowed_extensions:
    :type allowed_extensions:
    :param links:
    :type links: list
    :return: generator
    :rtype:
    """

    # convert to tuple so that it extension can be directly checked using built-in function
    allowed_extensions = tuple(allowed_extensions)
    for link in links:
        url_path = '/'.join(link.url.split('/')[3:]).lower()
        if url_path.endswith(allowed_extensions):
            yield link.url
            continue
        res = [element for element in allowed_extensions if element in url_path]

        # yield if result have valid files links
        if bool(res):
            yield link.url
