from six import string_types


def hash_function(key):
    result = 5381
    multiplier = 33
    if isinstance(key, int):
        return key
    for char in key:
        result = multiplier * result + ord(char)
    return result


def raise_if_not_acceptable_key(key):
    if not isinstance(key, (string_types, int)):
        raise TypeError("Key should be int or string or unicode")


class HashTable(object):
    def __init__(self):
        self._size = 11
        self.__initial_size = self._size
        self._used_slots = 0
        self._dummy_slots = 0
        self._keys = [None] * self._size
        self._values = [None] * self._size
        self.hash = hash_function
        self._max_threshold = 0.70

    def should_expand(self):
        return (float(self._used_slots + self._dummy_slots) / self._size) >= self._max_threshold

    def _probing(self, current_position):
        return ((5 + current_position) + 1) % self._size

    def _set_item_at_pos(self, position, key, value):
        self._keys[position] = key
        self._values[position] = value
        self._used_slots += 1

    def _set_item(self, position, key, value):
        existing_key = self._keys[position]
        if existing_key is None or existing_key == key:
            self._set_item_at_pos(position, key, value)
        else:
            new_position = self._probing(position)
            self._set_item(new_position, key, value)

    def _reposition(self, keys, values):
        for (key, value) in zip(keys, values):
            if key is not None:
                hash_value = self.hash(key)
                position = self._calculate_position(hash_value)
                self._set_item(position, key, value)

    def _resize(self):
        old_keys = self._keys
        old_values = self._values
        self._size = self._size * 4  # Increased size
        self._keys = [None] * self._size
        self._values = [None] * self._size
        self._used_slots = 0
        self._dummy_slots = 0
        self._reposition(old_keys, old_values)  # Repositioning Existing Key Value Pairs

    def _calculate_position(self, hashvalue):
        return hashvalue % self._size

    def put(self, key, value):
        raise_if_not_acceptable_key(key)
        if self.should_expand():
            self._resize()
        position = self._calculate_position(self.hash(key))
        self._set_item(position, key, value)

    def _get_pos_recursively(self, position, key):
        new_position = self._probing(position)
        tmp_key = self._keys[new_position]
        if tmp_key is None:
            raise KeyError(u"{} key not found".format(key))
        elif tmp_key != key:
            return self._get_pos_recursively(new_position, key)
        else:
            return new_position

    def _get_pos(self, key):
        raise_if_not_acceptable_key(key)
        position = self._calculate_position(self.hash(key))
        tmp_key = self._keys[position]
        if tmp_key is None:
            raise KeyError("{} doesn't exist".format(key))
        elif tmp_key != key:
            return self._get_pos_recursively(position, key)
        else:
            return position

    def get(self, key):
        position = self._get_pos(key)
        if position is None:
            return None
        return self._values[position]

    def _delete_item(self, position):
        self._keys[position] = None
        self._values[position] = None
        self._dummy_slots += 1

    def delete(self, key):
        position = self._get_pos(key)
        if position is None:
            raise KeyError(key)
        self._delete_item(position)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.put(key, value)

    @property
    def keys(self):
        return self._keys

    @property
    def values(self):
        return self._values

    @property
    def used_slots(self):
        return self._used_slots

    @property
    def size(self):
        return self._size
