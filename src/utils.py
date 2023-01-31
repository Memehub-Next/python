from itertools import chain
from multiprocessing import Pool as MpPool
from multiprocessing import cpu_count as MpCpu_count
from multiprocessing.pool import Pool as mpPoolType
from typing import Any, Callable, Iterable, List, Optional, TypeVar, cast

from billiard import Pool, cpu_count  # type:ignore
from tqdm import tqdm

ReturnType = TypeVar("ReturnType")


def _get_filters(distinct: bool):
    def isNotNone(result: Optional[ReturnType]):
        return result is not None

    def wrapper(gen: Iterable[Optional[ReturnType]]):
        return list(cast(Iterable[ReturnType], filter(isNotNone, gen)))

    def distinct_wrapper(gen: Iterable[Optional[ReturnType]]) -> list[ReturnType]:
        return list(cast(Iterable[ReturnType], filter(isNotNone, set(gen))))
    return distinct_wrapper if distinct else wrapper


def _use_single_mapper(func: Callable[..., Optional[ReturnType]],
                       iterable: Iterable[Any],
                       *,
                       distinct: bool,
                       verbose: bool,
                       label: Optional[str],
                       total: Optional[int]):
    if verbose:
        return _get_filters(distinct)(tqdm((func(item) for item in iterable), desc=label, total=total))
    else:
        return _get_filters(distinct)((func(item) for item in iterable))


def _use_mp_mapper(func: Callable[..., Optional[ReturnType]],
                   iterable: Iterable[Any],
                   *,
                   distinct: bool,
                   verbose: bool = True,
                   use_billard: bool = False,
                   label: Optional[str] = None,
                   total: Optional[int] = None,
                   num_workers: Optional[int] = None):
    with cast(mpPoolType, Pool(num_workers or cpu_count())) if use_billard else MpPool(num_workers or MpCpu_count()) as workers:
        if verbose:
            if total:
                return _get_filters(distinct)(tqdm(workers.imap_unordered(func, iterable), desc=label, total=total))
            else:
                return _get_filters(distinct)(tqdm(workers.imap_unordered(func, iterable), desc=label))
        else:
            return _get_filters(distinct)(workers.imap_unordered(func, iterable))


def process(func: Callable[..., Optional[ReturnType]],
            iterable: Iterable[Any],
            *,
            multi: bool = True,
            verbose: bool = True,
            use_billard: bool = False,
            label: Optional[str] = None,
            total: Optional[int] = None,
            distinct: bool = False,
            num_workers: Optional[int] = None) -> List[ReturnType]:
    if not multi:
        return _use_single_mapper(func, iterable, distinct=distinct, verbose=verbose,  label=label, total=total)
    else:
        return _use_mp_mapper(func, iterable, distinct=distinct, verbose=verbose, use_billard=use_billard, label=label, total=total, num_workers=num_workers)


def process_from_iterable(func: Callable[..., Iterable[ReturnType]],
                          iterable: Iterable[Any],
                          *,
                          multi: bool = True,
                          verbose: bool = True,
                          use_billard: bool = False,
                          label: Optional[str] = None,
                          total: Optional[int] = None,
                          distinct: bool = False) -> List[ReturnType]:
    data = chain.from_iterable(process(func, iterable, multi=multi, verbose=verbose, distinct=False, use_billard=use_billard, label=label, total=total))
    return _get_filters(distinct)(data)
