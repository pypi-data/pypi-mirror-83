from collections import defaultdict
from dataclasses import dataclass, field
from pprint import pprint
from typing import Any, Dict, Generic, List, Set, Tuple, TypeVar, Union

T = TypeVar('T')


@dataclass(frozen=True)
class KeyStore(Generic[T]):
    keys: Union[Tuple[str], List[str]]
    objects: Union[List[T], Set[T]]

    # Internal cache used if same input kwargs are re-used.
    _cache: Dict = field(default_factory=lambda: defaultdict(list))

    # ------------------------ PUBLIC METHODS -------------------------------- #

    def get(self, **kwargs) -> List[T]:
        """Given a set of kwargs mapping attributes to values, return
        a list of items with attributes and value corresponding to the kwargs.
        """
        self._check_keys(**kwargs)
        return self._get(**kwargs)

    def get_one_or_none(self, **kwargs) -> T:
        """Given a set of kwargs mapping attributes to values, return a single item
        if it exists, or None if it does not. If multiple items match then raise
        an error."""
        self._check_keys(**kwargs)
        values = self._get(**kwargs)

        if len(values) == 0:
            return None
        elif len(values) > 1:
            print("\n\n\n**** CACHE: ")
            pprint(self._cache)
            raise RuntimeError(f"Expected one or no items matching {kwargs} got {len(values)}")
        return values[0]

    def get_one(self, **kwargs) -> T:
        """Given a set of kwargs mapping attributes to values, return a single item
        if it exists, if none or multiple exist then raise an error."""
        self._check_keys(**kwargs)
        values = self._get(**kwargs)

        if len(values) == 1:
            return values[0]
        else:
            raise RuntimeError(f"Expected one item matching {kwargs} got {len(values)}")

    # ----------------------- INTERNAL METHODS ------------------------------- #

    def _check_keys(self, **kwargs) -> None:
        """Check that the keys used to query for objects are valid keys
        that were provided in the input. If they were not then raise an error."""
        kwargs_not_in_keys = set(kwargs.keys()) - set(self.keys)
        if len(kwargs_not_in_keys) != 0:
            raise RuntimeError(
                f"Key store has filter keys {self.keys}, query has keys {kwargs_not_in_keys} which are invalid."
            )

    def _get(self, **kwargs) -> List[T]:
        """Internal method to get objects linked to a set of kwargs,
        checking first if the query has already been made and taking from the
        cache if so."""
        attr_dict = {k: None for k in self.keys}
        attr_dict.update(**kwargs)
        key = tuple(attr_dict.values())

        if key not in self._cache:
            for obj in self.objects:
                if self._all_keys_match(obj=obj, **kwargs):
                    self._cache[key].append(obj)

        return self._cache.get(key, [])

    def _all_keys_match(self, obj: Any, **kwargs) -> bool:
        """Check if all attribute / values in the input matches an object."""
        return all(
            self._equal(obj=obj, attr=attr, val=val)
            for attr, val in kwargs.items()
        )

    def _equal(self, obj: Union[object, Dict], attr: str, val: Any) -> bool:
        """Check if an attribute on an object is a given value."""
        if type(obj) == dict:
            return obj.get(attr) == val
        return getattr(obj, attr) == val

    def __getitem__(self, key: int) -> T:
        return self.objects[key]
