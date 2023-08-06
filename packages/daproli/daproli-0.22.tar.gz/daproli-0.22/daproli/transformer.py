from joblib import Parallel, delayed
from tqdm import tqdm

from .processing import map, filter, split, expand, combine, join
from .manipulation import windowed, flatten


class BaseTransformer:
    '''
    The BaseTransformer defines a generic data transformation pattern that
    can be implemented with a number of data processing concepts.
    '''
    def transform(self, data, *args, **kwargs):
        raise NotImplementedError()


class Mapper(BaseTransformer):

    def __init__(self, func, ret_type=None, expand_args=True, n_jobs=1, verbose=0, **kwargs):
        '''
        dp.Mapper is the respective transformer for dp.map.

        Parameters
        -----------
        :param func: the mapping function
        :param ret_type: if provided the used return type, otherwise ret_type(data)
        :param expand_args: true if args should be expanded, false otherwise
        :param n_jobs: amount of used threads/processes
        :param verbose: verbosity level for tqdm / joblib
        :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
        '''
        self.func = func
        self.ret_type = ret_type
        self.expand_args = expand_args
        self.n_jobs = n_jobs
        self.verbose = verbose
        self.kwargs = kwargs

    def transform(self, data, *args, **kwargs):
        return map(self.func, data, self.ret_type, expand_args=self.expand_args, n_jobs=self.n_jobs,
                   verbose=self.verbose, **self.kwargs)


class Filter(BaseTransformer):

    def __init__(self, pred, ret_type=None, expand_args=True, n_jobs=1, verbose=0, **kwargs):
        '''
        dp.Filter is the respective transformer for dp.filter.

        Parameters
        -----------
        :param pred: the filter predicate
        :param ret_type: if provided the used return type, otherwise ret_type(data)
        :param expand_args: true if args should be expanded, false otherwise
        :param n_jobs: amount of used threads/processes
        :param verbose: verbosity level for tqdm / joblib
        :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
        '''
        self.pred = pred
        self.ret_type = ret_type
        self.expand_args = expand_args
        self.n_jobs = n_jobs
        self.verbose = verbose
        self.kwargs = kwargs

    def transform(self, data, *args, **kwargs):
        return filter(self.pred, data, ret_type=self.ret_type, expand_args=self.expand_args, n_jobs=self.n_jobs,
                      verbose=self.verbose, **self.kwargs)


class Splitter(BaseTransformer):

    def __init__(self, func, ret_type=None, return_labels=False, expand_args=True, n_jobs=1, verbose=0, **kwargs):
        '''
        dp.Splitter is the respective transformer for dp.split.

        Parameters
        -----------
        :param func: the discriminator function
        :param ret_type: if provided the used return type, otherwise ret_type(data)
        :param return_labels: true if the associated labels should be returned, false otherwise
        :param expand_args: true if args should be expanded, false otherwise
        :param n_jobs: amount of used threads/processes
        :param verbose: verbosity level for tqdm / joblib
        :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
        '''
        self.func = func
        self.ret_type = ret_type
        self.return_labels = return_labels
        self.expand_args = expand_args
        self.n_jobs = n_jobs
        self.verbose = verbose
        self.kwargs = kwargs

    def transform(self, data, *args, **kwargs):
        return split(self.func, data, ret_type=self.ret_type, return_labels=self.return_labels,
                     expand_args=self.expand_args, n_jobs=self.n_jobs, verbose=self.verbose, **self.kwargs)


class Expander(BaseTransformer):

    def __init__(self, func, ret_type=None, expand_args=True, n_jobs=1, verbose=0, **kwargs):
        '''
        dp.Expander is the respective transformer for dp.expand.

        Parameters
        -----------
        :param func: the expansion function
        :param ret_type: if provided the used return type, otherwise ret_type(data)
        :param expand_args: true if args should be expanded, false otherwise
        :param n_jobs: amount of used threads/processes
        :param verbose: verbosity level for tqdm / joblib
        :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
        '''
        self.func = func
        self.ret_type = ret_type
        self.expand_args = expand_args
        self.n_jobs = n_jobs
        self.verbose = verbose
        self.kwargs = kwargs

    def transform(self, data, *args, **kwargs):
        return expand(self.func, data, ret_type=self.ret_type, expand_args=self.expand_args, n_jons=self.n_jobs,
                      verbose=self.verbose, **self.kwargs)


class Combiner(BaseTransformer):

    def __init__(self, func, expand_args=True, n_jobs=1, verbose=0, **kwargs):
        '''
        dp.Combiner is the respective transformer for dp.combine.

        Parameters
        -----------
        :param func: the combination function
        :param expand_args: true if args should be expanded, false otherwise
        :param n_jobs: amount of used threads/processes
        :param verbose: verbosity level for tqdm / joblib
        :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
        '''
        self.func = func
        self.expand_args = expand_args
        self.n_jobs = n_jobs
        self.verbose = verbose
        self.kwargs = kwargs

    def transform(self, data, *args, **kwargs):
        return combine(self.func, *data, expand_args=self.expand_args, n_jobs=self.n_jobs, verbose=self.verbose, **self.kwargs)


class Joiner(BaseTransformer):

    def __init__(self, func, expand_args=True, n_jobs=1, verbose=0, **kwargs):
        '''
        dp.Joiner is the respective transformer for dp.join.

        Parameters
        -----------
        :param func: the join function
        :param expand_args: true if args should be expanded, false otherwise
        :param n_jobs: amount of used threads/processes
        :param verbose: verbosity level for tqdm / joblib
        :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
        '''
        self.func = func
        self.expand_args = expand_args
        self.n_jobs = n_jobs
        self.verbose = verbose
        self.kwargs = kwargs

    def transform(self, data, *args, **kwargs):
        return join(self.func, *data, expand_args=self.expand_args, n_jobs=self.n_jobs, verbose=self.verbose, **self.kwargs)


class Manipulator(BaseTransformer):

    def __init__(self, func, void=False, *args, **kwargs):
        '''
        dp.Manipulator is a transformer to manipulate the entire collection of data items.

        Parameters
        -----------
        :param func: the manipulation function
        :param void: if true the result is not returned
        :param args: additional args for func
        :param kwargs: additional kwargs for func
        '''
        self.func = func
        self.void = void
        self.args = args
        self.kwargs = kwargs

    def transform(self, data, *args, **kwargs):
        res = self.func(data, *self.args, **self.kwargs)
        return res if self.void is False else data


class Window(BaseTransformer):

    def __init__(self, size, step=1, ret_type=None):
        '''
        dp.Window is the respective transformer for dp.windowed.

        Parameters
        -----------
        :param data: an iterable collection of data
        :param size: the window size
        :param step: the window step
        :param ret_type: if provided the used return type, otherwise ret_type(data)
        '''
        self.size = size
        self.step = step
        self.ret_type = ret_type

    def transform(self, data, *args, **kwargs):
        return windowed(data, self.size, step=self.step, ret_type=self.ret_type)


class Flat(BaseTransformer):

    def __init__(self, ret_type=None):
        '''
        dp.Flat is the respective transformer for dp.flatten.

        Parameters
        -----------
        :param ret_type: if provided the used return type, otherwise ret_type(data)
        '''
        self.ret_type = ret_type

    def transform(self, data, *args, **kwargs):
        return flatten(data, ret_type=self.ret_type)


class Union(BaseTransformer):

    def __init__(self, *transformers, n_jobs=1, verbose=0, **kwargs):
        '''
        dp.Union is a construct to manipulate mutli-collections of data tiems.

        Parameters
        -----------
        :param transformers: the transformers for the respective collections of data items
        :param n_jobs: amount of used threads/processes
        :param verbose: verbosity level for tqdm / joblib
        :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
        '''
        self.transformers = transformers
        self.n_jobs = n_jobs
        self.verbose = verbose
        self.kwargs = kwargs

    def transform(self, data, *args, **kwargs):
        if self.n_jobs == 1:
            return [transformer.transform(items, *args, **kwargs)
                    for transformer, items in tqdm(zip(self.transformers, data), disable=self.verbose < 1)]

        return Parallel(n_jobs=self.n_jobs, verbose=self.verbose, **self.kwargs)(delayed(transformer.transform)
                (items, *args, **kwargs) for transformer, items in zip(self.transformers, data))


class Pipeline(BaseTransformer):

    def __init__(self, *transformers, verbose=0):
        '''
        dp.Pipeline is a construct to pipe a collection of transformers.

        Parameters
        -----------
        :param transformers: the transformer sequence to apply
        :param verbose: verbosity level for tqdm
        '''
        self.transformers = list(transformers)
        self.verbose = verbose

    def transform(self, data, *args, **kwargs):
        res = data

        for transformer in tqdm(self.transformers, disable=self.verbose < 1):
            res = transformer.transform(res, *args, **kwargs)

        return res
