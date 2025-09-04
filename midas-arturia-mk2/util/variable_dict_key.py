'''
    Variable Dictionary Key
    =======================
    A key for a variable dictionary. Can be one of four types:
        AKey : value must match exactly
        RKey : value must be within range
        OKey : value must be in list of options
        ROKey : value must be within one of the ranges

    - The VKey class is used to create a variable key for a dictionary.
    - You can also use a tuple of VKeys as a key for a dictionary.

'''
import itertools

class _AllVal:
    '''
        Value that returns true in all equality operations. Except false for not equal.
        Its value is equal to None.
        Its hash value is equal to hash(None)
    '''
    def __init__(self) -> None:
        self.value = None

    def __eq__(self, other):
        return True
    def __ne__(self, other):
        return False
    def __hash__(self) -> int:
        return hash(self.value)
    def __lt__(self, other):
        return False
    def __le__(self, other):
        return True
    def __gt__(self, other):
        return True
    def __ge__(self, other):
        return True
    def __bool__(self):
        return True
AllVal = _AllVal()

class AllKey:
    '''
        Key that matches all values.
    '''
    def __init__(self):
        self.value = AllVal

    def __eq__(self, other):
        return self.value == other

    def __hash__(self) -> int:
        return hash(self.value)

    def expand(self):
        '''
            Returns a list of all possible values.
            Always returns [AllVal].
        '''
        return [self.value]

class AKey:
    """
        Acts like a regular key, value must match exactly.
            key == key
    """
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        '''
            Is equal to other if other is the same type and value as self.value
        '''

        if isinstance(other,type(self.value)):
            return self.value == other
        return False

    def __hash__(self) -> int:
        return hash(self.value)

    def expand(self):
        '''
            Returns a list of all possible values.
            Always returns [self.value].
        '''
        return [self.value]

class RKey:
    """
        Defined by a min and max value. Returns true if key is within range.
            min >= key <= max
    """
    def __init__(self, min_, max_):
        self.value = (min_, max_)

    def __eq__(self, other):
        if isinstance(other,type(self.value[0])):
            return self.value[0] <= other <= self.value[1]
        elif isinstance(other, RKey):
            return self.value == other.value
        else:
            return False

    def __hash__(self) -> int:
        return hash(self.value)

    def expand(self):
        '''
            Returns a list of all possible values.
            Always returns a list of all values between min and max inclusive.
        '''
        return [i for i in range(self.value[0], self.value[1]+1)]

class OKey:
    """
        Defined by a tuple of options. Returns true if key is in list.
            key in options
    """
    def __init__(self, options):

        # assert that options is a tuple or list. Convert list to tuple.

        if not (isinstance(options, tuple) or isinstance(options, list)):
            raise TypeError("OKey options must be a tuple or list.")
        else:
            if isinstance(options, list):
                passed_options = tuple(options)
                print("Warning: OKey options list converted to tuple.")
            else:
                passed_options = options

        self.value = passed_options

    def __eq__(self, other):
        for o in self.value: # Check if the type is one of the option's types
            if isinstance(other, type(o)): # Return the first match
                return other in self.value
        return False

    def __hash__(self) -> int:
        return hash(self.value)

    def expand(self):
        '''
            Returns a list of all possible values.
            Always returns a list of all options.
        '''
        return self.value

class ROKey:
    """
        Defined by a tuple of ranges. Returns true if key is within one of the ranges.
            min >= key <= max
    """
    def __init__(self, ranges):

        # assert that ranges is a tuple.

        # if the ranges are a list convert to a tuple
        if isinstance(ranges, list):
            passed_ranges = tuple(ranges)
            print("Warning: ROKey range list converted to tuple.")
            self.value = passed_ranges
        elif isinstance(ranges, tuple):
            self.value = ranges
        else:
            raise TypeError("ROKey range list must be a tuple or list.")


    def __eq__(self, other):
        for i in range(len(self.value)): #pylint: disable=C0200
            if isinstance(other, type(self.value[i][0])):
                if self.value[i][0] <= other <= self.value[i][1]:
                    return True

    def __hash__(self) -> int:
        return hash(self.value)

    def expand(self):
        '''
            Returns a list of all possible values.
            Always returns a list of all values between min and max inclusive of each of the ranges.
        '''
        expanded = []
        for i in self.value:
            expanded += [j for j in range(i[0], i[1]+1)]
        return expanded

class VKey:
    """
        A key for a variable dictionary. Can be one of four types:
            AKey
            RKey
            OKey
            ROKey
    """
    def __init__(self, key):

        # Check that key is one of valid types:
        if not isinstance(key, (AKey, RKey, OKey, ROKey,AllKey)):
            raise ValueError("Key must be one of: AKey, RKey, OKey, ROKey")

        self.key = key

    def __eq__(self, other):
        return self.key == other

    def __hash__(self) -> int:
        return hash(self.key)

class VKeySet:
    """
        A set of VKeys.
    """

    def __init__(self, *args):
        self.variable_keys = args

    def __eq__(self, other):
        return self.variable_keys == other

    def __hash__(self) -> int:
        return hash(self.variable_keys)

    def expand(self):
        '''
            Returns a list of all possible values as a tuple.
            Expands each key and return the union of all expanded keys.
            As a dictionary pointing back to the original key.
            eg: ((1,2),(3,4,5)) -> 2 x 3 = 6 keys
            expanded:      {  (1,3) : key,
                            (1,4) : key,
                            (1,5) : key,
                            (2,3) : key,
                            (2,4) : key,
                            (2,5) : key }
        '''
        for i in self.variable_keys:
            if not isinstance(i, VKey):
                raise ValueError("VKeySet must contain only VKeys.")

        expanded = []
        for i in self.variable_keys:
            expanded.append(i.key.expand())
        return [tuple(i) for i in itertools.product(*expanded)]

class VDictKeyTypeError(KeyError):
    """
        Error raised when a key is not found in the VDict.
    """

class VDictKeyValueError(KeyError):
    """
        Error raised when a key is not found in the VDict.
    """

class VDict(dict):
    """
        A dictionary that can be indexed by a tuple of keys.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._expanded = dict()

        for k in self.keys():
            if not isinstance(k, (VKey, VKeySet)):
                raise VDictKeyTypeError
            elif isinstance(k,VKey): # expand the key into the expanded dict.
                if isinstance(k.key, AllKey):
                    # If the dict contains any other single value keys, raise an error.
                    for i in self._expanded:
                        if not isinstance(i,tuple):
                            raise VDictKeyValueError
                        if AllVal in self._expanded:
                            raise VDictKeyValueError
                    self._expanded[AllVal] = k
                else:
                    key_vals = k.key.expand()

                    for i in key_vals:
                        if i in self._expanded:
                            raise VDictKeyValueError

                    for i in key_vals:
                        self._expanded[i] = k
            elif isinstance(k,VKeySet):
                key_vals = k.expand()

                for i in key_vals:
                    if i in self._expanded:
                        raise VDictKeyValueError

                for i in key_vals:
                    self._expanded[i] = k


    def __getitem__(self, key):
        '''
            Get item by key from the expanded dictionary.
        '''
        if isinstance(key, tuple):
            try:
                return super().__getitem__(self._expanded[key])
            except KeyError as e: # pylint: disable=W0612
                # Exact match not found, try to find a match for an all key in one
                # of the tuple values that is the same element index
                # as the one of the non matching keys.
                #1. Get a list of all the keys that partially match the tuple key.
                    # get list of all tuples of equal length to the key with an 'all' value in them.
                    # get all tuple keys that have a None in them.
                for i in self._expanded: # pylint: disable=C0206
                    if isinstance(i,tuple):
                        if AllVal in i and len(i) == len(key):
                            match = True
                            for j in range(len(i)): # pylint: disable=C0200
                                if i[j] is not AllVal and i[j] != key[j]:
                                    match = False
                            if match:
                                return super().__getitem__(self._expanded[i])
        else:
            if AllVal in self._expanded:
                return super().__getitem__(self._expanded[AllVal])
            else:
                return super().__getitem__(self._expanded[key])

def reverse_dict(d):
    '''
        Reverse a dictionary. Keys become values and values become keys.
    '''
    return dict(zip(d.values(), d.keys()))

# # Key will be (status,port,note,value)
# DefaultMidi = dict({
#     144 : 'note_on',
#     128 : 'note_off',
#     176 : 'control_change',
#     160 : 'polyphonic_key_pressure',
#     192 : 'program_change',
#     208 : 'channel_aftertouch',
#     224 : 'pitch_wheel',
#     240 : 'sysex_start',
#     247 : 'sysex_end',
#     248 : 'timing_clock',
#     250 : 'start',
#     251 : 'continue',
#     252 : 'stop',
#     254 : 'active_sensing',
#     255 : 'reset',
#     'note_on' : 144,
#     'note_off' : 128,
#     'control_change' : 176,
#     'polyphonic_key_pressure' : 160,
#     'program_change' : 192,
#     'channel_aftertouch' : 208,
#     'pitch_wheel' : 224,
#     'sysex_start' : 240,
#     'sysex_end' : 247,
#     'timing_clock' : 248,
#     'start' : 250,
#     'continue' : 251,
#     'stop' : 252,
#     'active_sensing' : 254,
#     'reset' : 255
#   })

# ArturiaMidiDict = VDict({VKeySet(VKey(AKey(DefaultMidi['note_on'])), VKey(AKey(16)),VKey(RKey(0,15)),VKey(AllKey())) : 'pads_note_on',
#                    VKeySet(VKey(AKey(4)), VKey(AKey(16)),VKey(RKey(0,15)),VKey(AllKey())) : 'pads_note_off',
# })


# def processMidi(status,port,note,value,sysex):
#     '''
#         Process a midi message and return a string.
#     '''
#     try:
#         return ArturiaMidiDict[(status,port,note,value)]
#     except KeyError:
#         return DefaultMidi[status]

# def processSysex(sysex):
#     '''
#         Process a sysex message and return a string.
#     '''
#     # Given a sysex message, remove the starting byte.

#     # Attempt to decode the sysex message.

#     # 1. If the bytes following the starting byte are in the lookup table of known devices.
#     # Consume the bytes and return the device name.

#     # If the bytes following the starting byte are not in the lookup table of known devices.
#     # Ignore the message and return None.

#     # 2. If the bytes following the starting byte are in the lookup table of known commands.
#     # Consume the bytes and return the command name.

#     # 3. The following bytes are the command arguments, based on the information of the command in the lookup table.
#     # For each argument, consume the number of bytes and return the argument value.
#     # Continue until reaching the sysex end byte. or the end of length of the argument list.


# print(processMidi(144,16,0,127))