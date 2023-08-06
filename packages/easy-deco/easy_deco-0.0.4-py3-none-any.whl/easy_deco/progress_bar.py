from tqdm import tqdm
from .core import decorator

@decorator
def progress_bar(func, *args, **kwargs):
    """
    This decorator allows to you add a progress bar in any function where you want to process any iterable object

    ___
    **Parameters**

    * **desc:** key word argument (kwargs) (str) Progress bar description
    * **unit:** key word argument (kwargs) (str) unit measurement, if you reading a list of files so you can use *Files*
    so you will get in the progress bar 'Files/s' when it is charging

    ___

    ## Snippet code

    ```python
    >>> from easy_deco import progress_bar
    >>> @progress_bar(desc='Loading files...', unit='files')
    >>> def read_files(self, filenames):

            read_file(filenames)

    ```
    """
    defaultOptions = {'desc': 'Reading files',
                      'unit': 'Files'}

    Options = {key: kwargs[key] if key in list(kwargs.keys()) else defaultOptions[key] for key in
               list(defaultOptions.keys())}

    (self, iterableObject) = args[0]

    if not hasattr(iterableObject, '__iter__'):

        raise ValueError('You must provide an iterableObject in {}'.format(func.__name__))

    for i in tqdm(range(len(iterableObject)), desc=Options['desc'], unit=Options['unit']):

        result = func(self, iterableObject[i])

    return result