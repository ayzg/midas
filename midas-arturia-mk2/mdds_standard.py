from util.enum import Enum as enum

def byte(val):
    return bytes([val])

def nbyte(*values):
    return bytes(values)

class UIIDGeneratorKeyError(KeyError):
    """Exception raised when a key does not exist in the UIIDGenerator."""

    def __init__(self, key: int) -> None:
        self.key = key
        super().__init__(f"UIIDGeneratorKeyError: Key {key} does not exist.")


class UIIDGenerator:
    """
    A class that generates unique integer keys.

    Attributes:
        __key (int): The current key value.
        __used_keys (set): A set of keys that have been generated and used.

    Methods:
        generate_key: Generates a new unique key.
        pop_key: Removes a key from the set of used keys.
    """

    def __init__(self) -> None:
        self.__key = 0
        self.__used_keys = set()

    def generate_key(self) -> int:
        """
        Generates a new unique key.

        Returns:
            int: The generated key.
        """
        new_key = self.__key
        while new_key in self.__used_keys:
            new_key += 1
        self.__used_keys.add(new_key)
        self.__key += 1
        return new_key

    def pop_key(self, key: int) -> None:
        """
        Removes a key from the set of used keys.

        Args:
            key (int): The key to be removed.

        Raises:
            UIIDGeneratorKeyError: If the key is not found in the set of used keys.
        """
        if key not in self.__used_keys:
            raise UIIDGeneratorKeyError(key)
        else:
            self.__used_keys.remove(key)

    def __call__(self) -> int:
        return self.generate_key()

class Entry:
    '''
        An enumration-like object.
        Represents a value and its name.
    '''
    def __init__(self,name : str,value,value_type) -> None:
        self.name = name
        self.value = value

    def __str__(self) -> str:
        return f'{self.name}: {self.value}'

    def __call__(self):
        return self.value

class CommandEntry(Entry):
    def __init__(self,name:str, value) -> None:
        super().__init__(name,value,MDDSCommand)
    def __call__(self)->'MDDSCommand':
        return self.value


class eDefaultMidiStatus:
    note_on = nbyte(0x90)
    note_off = nbyte(0x80)
    control_change = nbyte(0xB0)
    program_change = nbyte(0xC0)
    pitch_bend = nbyte(0xE0)
    aftertouch = nbyte(0xA0)
    channel_aftertouch = nbyte(0xA0)
    system_exclusive = nbyte(0xF0)

class eStatus(enum):
    daw_to_midas = bytes([0x01])
    midas_to_daw = bytes([0x02])
    midas_to_device = bytes([0x03])
    device_to_midas =   bytes([0x04])
    daw_to_device = bytes([0x05])
    device_to_daw = bytes([0x06])
    device_to_device = bytes([0x07])

class eStatusType(enum):
    type1 = bytes([0x01])
    type2 = bytes([0x02])
    type3 = bytes([0x03])
    type4 =   bytes([0x04])
    type5 = bytes([0x05])
    type6 = bytes([0x06])
    type7 = bytes([0x07])

class eDestination(enum):
    all_ = byte(0x00)
    midas = byte(0x01)
    daw = byte(0x02)
    device = byte(0x03)

class eDaw(enum):
    all_ = nbyte(0x00,0x00,0x00,0x00)
    flstudio = nbyte(0x00,0x00,0x00,0x01)

class eDevice(enum):
    all_ = nbyte(0x00,0x00,0x00,0x00)

class MDDSPayloadDescription:
    '''
        This class is used to describe the payload of a MDDS command.
        A payload may have multiple loads, the amount of loads is described by load_count.
        Each load has a size, the size of each load is described by load_sizes.
        The size is in bytes.
        Accepted values for load_count are 0-255. 0 means an infinite amount of loads.
        Accepted values for a load size in load_size is 0-255. 0 means an infinite amount of bytes.
    '''
    def __init__(self, load_count : bytes = b'0x00', load_sizes : 'list[bytes]' = [b'0x00']):
        self.load_count = load_count
        self.load_sizes = load_sizes

    def to_bytes(self):
        # load count is the first byte
        payload_description = self.load_count
        # load sizes are the following bytes
        for load_size in self.load_sizes:
            payload += load_size

        return payload_description
    def __str__(self) -> str:
        return f'load_count: {self.load_count}, load_sizes: {self.load_sizes}'


class MDDSCommand:
    def __init__(self, status_id : bytes, command_id : bytes, payload_description : MDDSPayloadDescription):
        self.status_id = status_id
        self.command_id = command_id
        self.payload_description = payload_description

    def to_bytes(self):
        '''
            Returns the command as bytes.
            The command is structured as follows:
            0. Status               (1 byte)
            1. Command ID           (4 bytes)
            2. Payload description  (1 + n bytes)
        '''
        # status is the first byte
        command = self.status_id
        # command id is the next 4 bytes
        command = self.command_id
        # followed by the payload description
        command += self.payload_description.to_bytes()

class eType1CommandId(enum):
    script_init = nbyte(0x00,0x00,0x00,0x00)
    script_exit = nbyte(0x00,0x00,0x00,0x01)

class eType6CommandId(enum):
    ''' device to daw '''
    midi_message = nbyte(0x00,0x00,0x00,0x00)
    sysex_message = nbyte(0x00,0x00,0x00,0x01)

class eType6PayloadDescription(enum):
    midi_message = MDDSPayloadDescription(byte(0x01), nbyte(0x04)) # 4 bytes of midi data: status, port, data1(note), data2(value)
    sysex_message = MDDSPayloadDescription(byte(0x01), nbyte(0x00)) # N bytes of sysex data

class eType7CommandId(enum):
    ''' device to device '''
    pressed = nbyte(0x00,0x00,0x00,0x00)
    released = nbyte(0x00,0x00,0x00,0x01)
    moved_x = nbyte(0x00,0x00,0x00,0x02)
    moved_y = nbyte(0x00,0x00,0x00,0x03)
    moved_z = nbyte(0x00,0x00,0x00,0x04)
    held_x = nbyte(0x00,0x00,0x00,0x05)
    held_y = nbyte(0x00,0x00,0x00,0x06)
    held_z = nbyte(0x00,0x00,0x00,0x07)
    bent = nbyte(0x00,0x00,0x00,0x08)

class eType7PayloadDescription(enum):
    pressed = MDDSPayloadDescription(byte(0x01), nbyte(0x04,0x01,0x01,0x01,0x01)) # 4 bytes of data for the control identifier,4 bytes for the channel,note and value1 value2
    released = MDDSPayloadDescription(byte(0x01), nbyte(0x04,0x01,0x01,0x01,0x01))
    moved_x = MDDSPayloadDescription(byte(0x01), nbyte(0x04,0x01,0x01,0x01,0x01))
    moved_y = MDDSPayloadDescription(byte(0x01), nbyte(0x04,0x01,0x01,0x01,0x01))
    moved_z = MDDSPayloadDescription(byte(0x01), nbyte(0x04,0x01,0x01,0x01,0x01))
    held_x = MDDSPayloadDescription(byte(0x01), nbyte(0x04,0x01,0x01,0x01,0x01))
    held_y = MDDSPayloadDescription(byte(0x01), nbyte(0x04,0x01,0x01,0x01,0x01))
    held_z = MDDSPayloadDescription(byte(0x01), nbyte(0x04,0x01,0x01,0x01,0x01))
    bent = MDDSPayloadDescription(byte(0x01), nbyte(0x04,0x01,0x02)) # 4 bytes of data for the control identifier,1 bytes for the channel,2 for the value

class eCommandName:
    script_init = 'script_init'
    script_exit = 'script_exit'
    midi_message = 'midi_message'
    sysex_message = 'sysex_message'
    pressed = 'pressed'
    released = 'released'
    moved_x = 'moved_x'
    moved_y = 'moved_y'
    moved_z = 'moved_z'
    held_x = 'held_x'
    held_y = 'held_y'
    held_z = 'held_z'
    bent = 'bent'


class eCommand():
    script_init = Entry('script_init',MDDSCommand(eStatus.daw_to_midas.value,eType1CommandId.script_init.value, MDDSPayloadDescription(byte(0x01), [byte(0x00)])),MDDSCommand)
    script_exit = Entry('script_exit',MDDSCommand(eStatus.daw_to_midas.value,eType1CommandId.script_exit.value, MDDSPayloadDescription(byte(0x01), [byte(0x00)])),MDDSCommand)

# device to daw commands
# These are standardized midi and sysex commands which devices can output to the daw or other devices. To indicated they are device protable they are called Device to Device commands.
    midi_message = MDDSCommand(eStatusType.type6,eType6CommandId.midi_message.value, eType6PayloadDescription.midi_message.value )
    sysex_message = MDDSCommand(eStatusType.type6,eType6CommandId.sysex_message.value, eType6PayloadDescription.sysex_message.value )

# These are a subset of the midi and sysex commands, used for filtering and converting midi messages to MDDS. Some are not part of the midi standard, but are a MDDS extension.
# For example, upon receiving a midi note on message, midas can convert it to a MDDS pressed command.
# Upon outputting a MDDS pressed command, midas can convert it to a midi note on message. or choose to send a MDDS message instead.
# The same goes for the other midi messages.
# Keep in mind that the midi messages are not converted to MDDS messages by default. The user has to enable this in the MDDS script.
# Outputted MDDS are disguised as custom sysex messages, so they can be filtered by the MDDS script.
# There will be one script instance per device, all scripts will be linked to one daw instance.
# The daw instance will be linked to one midas instance per device.
# The midas instance will be able to communicate with other instances of itself through dispatch of MDDS messages converted to sysex messages.
    pressed = CommandEntry('pressed',MDDSCommand(eStatusType.type7.value,eType7CommandId.pressed.value, eType7PayloadDescription.pressed.value))
    released = MDDSCommand(eStatusType.type7.value,eType7CommandId.released.value, eType7PayloadDescription.released.value)
    moved_x = MDDSCommand(eStatusType.type7.value,eType7CommandId.moved_x.value, eType7PayloadDescription.moved_x.value)
    moved_y = MDDSCommand(eStatusType.type7.value,eType7CommandId.moved_y.value, eType7PayloadDescription.moved_y.value)
    moved_z = MDDSCommand(eStatusType.type7.value,eType7CommandId.moved_z.value, eType7PayloadDescription.moved_z.value)
    held_x = MDDSCommand(eStatusType.type7.value,eType7CommandId.held_x.value, eType7PayloadDescription.held_x.value)
    held_y = MDDSCommand(eStatusType.type7.value,eType7CommandId.held_y.value, eType7PayloadDescription.held_y.value)
    held_z = MDDSCommand(eStatusType.type7.value,eType7CommandId.held_z.value, eType7PayloadDescription.held_z.value)
    bent = MDDSCommand(eStatusType.type7.value,eType7CommandId.bent.value, eType7PayloadDescription.bent.value)
