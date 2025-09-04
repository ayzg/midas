# name=MidasOS Test Script
# receiveFrom=MidasOS Test Script
from typing import Any
import mdds_standard as midasstd
import _struct as struct
import time
import device
import binascii

from util import enum

def print_bytes(b):
    bytelist = []
    for byte in b:
        bytelist.append(byte)
    return bytelist.__str__()

def check_types(list_of_values,list_of_types):
    if len(list_of_values) != len(list_of_types):
        raise ValueError("list_of_values and list_of_types must be of the same length.")
    for i in range(len(list_of_values)):
        if not isinstance(list_of_values[i],list_of_types[i]):
            raise TypeError(f"Value at index {i} must be of type {list_of_types[i]}")

def check_type(list_of_values,type_):
    for value in list_of_values:
        if not isinstance(value,type_):
            raise TypeError(f"Value {value} must be of type {type_}")

# Exceptions
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

# Message Types:
#  1. Signal: A signal carries with it a type, sender, a reciever, a command, and a payload.
#  2. Message: A sender, reciever and a command id.
#  3. TargetedMessage: A message with a target.
#  4. BoundMessage: A message with a target and arguments.
# Command Space Objects
class MidiModel:
    """
    Represents a midi command status.
    """
    def __init__(self,
                 status : int) -> None:
        self.status = status

    def target(self,channel : int = None,note : int = None,value : int = None):
        ''' Target the command to a channel and note. Return a TargetedMidiCommand object.
            Arguments may be None to target all channels and notes.
        '''
        return TargetedMidi(self,channel,note,value)
    def bind(self,channel,note,value):
        """
        Binds the midi command to channel, note and value.
            BoundMidiCommand: The bound midi command.
        """
        return BoundMidiMessage(self.status,channel,note,value)
    def match(self,status,channel = None,note = None,value = None):
        ''' Returns true if the values may potentially match this midi model. '''
        if status != self.status:
            return False
        else:
            return True
    def byte(self):
        ''' Returns the midi status data as a byte. '''
        return midasstd.byte(self.status)

class TargetedMidi:
    '''
        Represents a midi command that has been targeted to a specific channel and note.
        This is used to check if a midi message matches the targeted channel and note.
    '''
    def __init__(self, midi_model : MidiModel,port : int = None, note : int = None,value : int = None) -> None:
        self.model = midi_model
        self.status = midi_model.status
        self.port = port
        self.note = note
        self.value = value

    def match(self,status,port = None,note = None,value = None):
        ''' Returns true if the values may potentially match this midi model. '''
        if status != self.status:
            return False

        scan_port = True
        scan_note = True
        scan_value = True

        if port is None:
            scan_port = False
        if note is None:
            scan_note = False
        if value is None:
            scan_value = False

        if scan_port and scan_note and scan_value:
            if port == self.port and note == self.note and value == self.value:
                return True
            else:
                return False
        elif scan_port and scan_note:
            if port == self.port and note == self.note:
                return True
            else:
                return False
        elif scan_port and scan_value:
            if port == self.port and value == self.value:
                return True
            else:
                return False
        elif scan_note and scan_value:
            if note == self.note and value == self.value:
                return True
            else:
                return False
        elif scan_port:
            if port == self.port:
                return True
            else:
                return False
        elif scan_note:
            if note == self.note:
                return True
            else:
                return False
        elif scan_value:
            if value == self.value:
                return True
            else:
                return False
        else:
            return True

    def bytes_tuple(self):
        ''' Returns the midi message data as a tuple of bytes or None. '''
        return (self.status,self.port,self.note,self.value)

class BoundMidiMessage:
    '''
        Represents a midi command that has been targeted to a specific channel and note, with a specific value.
        This is used to send a midi message to the device. Or check if a midi message matches the targeted channel, note and value.

    '''
    def __init__(self, status,port,note,value) -> None:
        self.status = status
        self.port = port
        self.note = note
        self.value = value


class Entry:
    '''
        An enumration-like object.
        Represents a value and its name.
    '''
    def __init__(self,name : str,value : Any) -> None:
        self.name = name
        self.value = value

    def __str__(self) -> str:
        return f'{self.name}: {self.value}'

    def __call__(self) -> Any:
        return self.value

class eDefaultMidi():
    NOTE_ON = Entry('NOTE_ON',MidiModel(144))
    NOTE_OFF = Entry('NOTE_OFF',MidiModel(128))
    CONTROL_CHANGE = Entry('CONTROL_CHANGE',MidiModel(176))
    PROGRAM_CHANGE = Entry('PROGRAM_CHANGE',MidiModel(192))
    PITCH_BEND = Entry('PITCH_BEND',MidiModel(224))
    NOTE_PRESSURE = Entry('NOTE_PRESSURE',MidiModel(160))
    CHANNEL_PRESSURE = Entry('CHANNEL_PRESSURE',MidiModel(208))
    SYSTEM_EXCLUSIVE = Entry('SYSTEM_EXCLUSIVE',MidiModel(240))

class MDDS:
    '''
        Midas Daw Device Signal
    '''
    def __init__(self,timestamp : bytes,signal_type : bytes,source : bytes,destination : bytes,command_id : bytes,payload_description : bytes) -> None:

        if not isinstance(signal_type,bytes):
            raise TypeError("Signal type must be of type bytes.")
        if not isinstance(source,bytes):
            raise TypeError("source must be of type bytes.")
        if not isinstance(destination,bytes):
            raise TypeError("destination must be of type bytes.")
        if not isinstance(command_id,bytes):
            raise TypeError("command_id must be of type bytes.")


        self.timestamp = timestamp
        self.signal_type = signal_type
        self.source = source
        self.destination = destination
        self.command_id = command_id
        self.payload_description = payload_description
        self.payload = None

    def bind_payload(self,payload : bytes):
        if not isinstance(payload,bytes):
            raise TypeError("Payload must be of type bytes.")
        self.payload = payload
        return self

    def update_timestamp(self,time : float):
        digit , fraction = float_to_2int32(time.monotonic())
        self.timestamp = int32_to_bytes(digit) + int32_to_bytes(fraction)
        return self

    def __str__(self) -> str:
        return f'''
        [MDDS]
            timestamp: {print_bytes(self.timestamp)}
            signal_type: {print_bytes(self.signal_type)}
            source: {print_bytes(self.source)}
            destination: {print_bytes(self.destination)}
            command_id: {print_bytes(self.command_id)}
            payload_description: {self.payload_description}
            payload: {print_bytes(self.payload)}
        '''

    def __repr__(self) -> str:
        return self.__str__()


class MIDIMap:
    '''
        This class is used to describe the midi map of a device.
        The status, port, and note are used to identify the midi message key.
        The key is mapped to a MDDS command identifier and control identifier.
    '''
    def __init__(self) -> None:
        self.midi_map = {}

    def map_midi(self,
            status : bytes, # mandatory
            port : bytes = None, # optional, otherwise all ports accepted. set none to accept all ports.
            note : bytes = None, # optional, otherwise all notes accepted. set none to accept all notes.
            value : bytes = None, # optional, otherwise all values accepted. set none to accept all values.
            command_type: bytes = None,
            command_id : bytes = None,
            control_id : bytes = None):
        ''' Add a mapping from a midi message to a MDDS type, command and control identifier.'''

        if self.match(status,port,note,value):
            raise ValueError(f"Key already exists: {status,port,note,value}")

        scan_port = True
        scan_note = True
        scan_value = True

        if port is None:
            scan_port = False
        if note is None:
            scan_note = False
        if value is None:
            scan_value = False

        if scan_port and scan_note and scan_value:
            self.midi_map[status,port,note,value] = (command_type,command_id,control_id)
        elif scan_port and scan_note:
            self.midi_map[status,port,note] = (command_type,command_id,control_id)
        elif scan_port and scan_value:
            self.midi_map[status,port,value] = (command_type,command_id,control_id)
        elif scan_note and scan_value:
            self.midi_map[status,note,value] = (command_type,command_id,control_id)
        elif scan_port:
            self.midi_map[status,port] = (command_type,command_id,control_id)
        elif scan_note:
            self.midi_map[status,note] = (command_type,command_id,control_id)
        elif scan_value:
            self.midi_map[status,value] = (command_type,command_id,control_id)
        else:
            self.midi_map[status] = (command_type,command_id,control_id)

    def map_midi_list(self,list_of_midi : 'list[tuple[bytes,bytes,bytes,bytes]]',mdds_commands : 'list[midasstd.MDDSCommand]',control_id : bytes = None):
        '''
            Add a mapping from a list of midi messages to a MDDS command and control identifier.
            The midi messages must be a list of tuples of the form (status,port,note,value).
            The command must be a list of MDDS commands.
            The control identifier is the 4 byte identifier of the control for all the commands in the list.
        '''
        # check that the list of midi is a list of tuples.
        check_type(list_of_midi,tuple)
        # check that the list of mdds_commands is a list of MDDSCommands.
        check_type(mdds_commands,midasstd.MDDSCommand)

        # check that the length of the list of midi is the same as the length of the list of mdds commands.
        if len(list_of_midi) != len(mdds_commands):
            raise ValueError("The length of list_of_midi must be the same as the length of mdds_commands.")

        for i in range(len(list_of_midi)):
            self.map_midi(*list_of_midi[i],
                          mdds_commands[i].status_id,
                          mdds_commands[i].command_id,
                          control_id)

    def map_sysex(self,sysex : bytes,command_type: bytes = None,command_id : bytes = None,control_id : bytes = None):
        # if the key already exists then print a warning that you are overwriting the key.
        if sysex in self.midi_map.keys():
            print(f"Warning: Overwriting existing key: {sysex}")

        # check if sysex is a valid sysex message.
        # check the beggings and terminating byte.
        if sysex[0] != 0xF0:
            raise ValueError("Sysex message must begin with 0xF0")
        if sysex[-1] != 0xF7:
            raise ValueError("Sysex message must end with 0xF7")

        self.midi_map[sysex] = (command_type,command_id,control_id)


    def get(self,status : bytes,port : bytes = None,note : bytes = None,value : bytes = None):
        ''' Returns the MDDS type, command and control identifier of a midi message.
            Based on the status, port, note, and value of the midi message as a key.
            If the port, note, or value is not specified then it will not be part of the key.
        '''
        scan_port = True
        scan_note = True
        scan_value = True

        if port is None:
            scan_port = False
        if note is None:
            scan_note = False
        if value is None:
            scan_value = False

        if scan_port and scan_note and scan_value:
            return self.midi_map[status,port,note,value]
        elif scan_port and scan_note:
            return self.midi_map[status,port,note]
        elif scan_port and scan_value:
            return self.midi_map[status,port,value]
        elif scan_note and scan_value:
            return self.midi_map[status,note,value]
        elif scan_port:
            return self.midi_map[status,port]
        elif scan_note:
            return self.midi_map[status,note]
        elif scan_value:
            return self.midi_map[status,value]
        else:
            return self.midi_map[status]

    def match(self,status : bytes,port : bytes,note : bytes,value : bytes):
        ''' Returns true if the midi message matches the midi map.'''
        scan_port = True
        scan_note = True
        scan_value = True

        if port is None:
            scan_port = False
        if note is None:
            scan_note = False
        if value is None:
            scan_value = False

        if scan_port and scan_note and scan_value:
            return (status,port,note,value) in self.midi_map
        elif scan_port and scan_note:
            return (status,port,note) in self.midi_map
        elif scan_port and scan_value:
            return (status,port,value) in self.midi_map
        elif scan_note and scan_value:
            return (status,note,value) in self.midi_map
        elif scan_port:
            return (status,port) in self.midi_map
        elif scan_note:
            return (status,note) in self.midi_map
        elif scan_value:
            return (status,value) in self.midi_map
        else:
            return status in self.midi_map

Minilab2Map = MIDIMap()
Minilab2Map.map_midi(*(eDefaultMidi.NOTE_ON().target(15,0,None).bytes_tuple()),
                     midasstd.eCommand.pressed().status_id,
                     midasstd.eCommand.pressed().command_id,
                     bytes([0x00, 0x00, 0x00, 0x00])
                )

print(Minilab2Map.match(status=bytes([0x90]),port=bytes([0x0F]),note=bytes([0x00]),value=None))

def float_to_2int32(f):
    integer_part = int(f)
    fractional_part = int((f - integer_part) * 10**9)  # Adjusted for 4-byte int precision
    return integer_part, fractional_part

def int32_to_bytes(i):
    return struct.pack('i', i)

def monotonic_bytes():
    '''
        Returns a tuple of 2 32-bit integers as bytes representing the digit and fraction of the time in seconds.
    '''
    digit , fraction= float_to_2int32(time.monotonic())
    return int32_to_bytes(digit) + int32_to_bytes(fraction)

def get_script_device_id():
    return device.getDeviceID()

def process_MDDS(mdds : MDDS):
    print(mdds)
    if(mdds.command_id == midasstd.eCommand.script_init.value.command_id):
        print("Script Init")
        if(mdds.payload == get_script_device_id()):
            print("Script Init for this device")
            print("Script Init for device id: ",mdds.payload)
        else:
            print("Script Init for another device")
            print("Script Init for device id: ",mdds.payload)
    pass


def midi_to_mdds():
    '''
        Converts a midi message to an mdd signal.
        Returns a tuple of the mdds signal and the control id.
    '''





'''
    Midas Daw Device Protocol:

        Midas Daw Device Signal:
            - A signal is a midi message or sysex message, or a message from the DAW, or a combination of these.
            - A signal is a message that is sent from :
                1. The DAW to MidasOS.
                    | [INPUT EVENT] Cannot be sent by MidasOS, only received by MidasOS.
                    | Events such a script init, script deinit, dirty channel changes, meter update request, idling, value request replies, etc.
                2. The Device to MidasOS.
                    | [INPUT EVENT] Cannot be sent by MidasOS, only received by MidasOS.
                    | Events such as midi messages, sysex messages, device state changes, MPE/MCC messages etc.
                3. MidasOS to the DAW.
                    | [OUTPUT EVENT]
                    | Events such as setting values in the daw or requesting values from the daw.
                4. MidasOS to the Device.
                    | [OUTPUT EVENT]
                    | Events such as midi messages, sysex messages, device state changes, MPE/MCC messages output to the device.
                5. The DAW to the Device.
                    | [INPUT EVENT] Can be sent by the DAW or MidasOS.
                    | Events from the daw making a direct request or command to the device. Can be filtered by midasOS.
                6. The Device to the DAW.
                    | [INPUT EVENT] Can be sent by the Device or MidasOS.
                    | Events from the device directly to the daw. Usually replies to daw requests or master clock synchonization.
                7. Device to Device. (Dispatched by MidasOS through the DAW)
                    | [OUTPUT EVENT]
                    | Events which are requests or commands from one device to another. Dispatched by MidasOS through the DAW.
            - A signal will have a type, a source, and a destination.
                1. The type of the signal is the type of the message(out of the 7 options)
                2. The source of the signal is the device or the DAW unique identifier. If left empty then the command is anonymous(more on this further...).
                3. The destination of the signal is the device or the DAW unique identifier of the reciever. If left empty then command is sent to all recievers.
            - A signal will have a command unique identifier. This is a unique identifier for the command.
            - A signal will have a payload. This is the data of the signal. It can be a midi message, sysex message, or a combination of these.
            - A signal will have a timestamp. This is the timestamp of the signal. It is used to determine the order of the signals.
            - A signal with have a load description which is a list of the payload's description. This is used to extract the payload data from the signal.
                - Each load in the payload of the signal will have a list of argument types and their allowed parameters, and the parameter's byte size.
                    This is used to validate the signal.

            For example:
                1. A note_on midi message with channel 0, note 42 and value 69 from the device to the DAW.
                    - MDDS signal emission start byte
                    - Timestamp: 8 bytes, 2 32 bit integers representing the timestamp in seconds with
                                        the first being being the digits before the decimal point
                                        and the second being the digits after the decimal point.
                    - Type: 4
                    - Source: Device Unique Identifier
                    - Destination: DAW Unique Identifier
                    - Command Unique Identifier: Device Note On Byte Value
                    - Payload Description:
                        - Device Note On Byte Value
                            - Argument1(1 byte): Channel) : 0 to 255
                            - Argument2(1 byte): Note) : 0 to 255
                            - Argument3(1 byte): Value) : 0 to 255
                    - Payload: [int_to_byte(0),int_to_byte(42),int_to_byte(69)] (or use bytes like so: b'\x00\x2A\x45'))
                    - MDDS signal emission end byte

            Use of MDDS emissions:
                User is able to emit MDDS signals from the device to the DAW or from the DAW to the device.
                MidasOS takes care of converting the diffrent signal types into MDD signals.
                The user can also emit MDDS signals directly.
                These signals are re-interpreted by midasOS into custom sysex messages
                    which can be sent accross devices and to the DAW and respond to them all in one script.
                        example:
                            Emit custom MDDS signal to a another device, once recieved the device can respond with a custom MDDS signal.
                            These signals can be a custom command, existing midi message or sysex message, or a combination of these.
                            Once recieved the script may react to the signal in any way it sees fit.
                            Since the reciever and sender of the signal are the same script, the script will have knowledge of the signal's payload.
                            In case of seperate scripts, the reciever must define the payload description of the expected sender's signal.
                            All this can be done from one method in the script by checking the reciever and sender of the signal. Responding accordingly.
                            This allows for a more modular and flexible script.
                            Anonymous signals can also be used to send signals to all devices or the DAW.(Device and daw can choose to ignore or accept all anonymous signals)
'''

def OnInit():
    print("OnInit")
    mdds_input = MDDS(timestamp= monotonic_bytes(),
                      signal_type= midasstd.eCommand.script_init.value.status_id,
                      source=midasstd.eDaw.flstudio.value,
                      destination=midasstd.eDestination.all_.value,
                      command_id=midasstd.eCommand.script_init.value.command_id,
                      payload_description=midasstd.eCommand.script_init.value.payload_description)
    mdds_input.bind_payload(get_script_device_id())

    process_MDDS(mdds_input)

def OnDeInit():
    print("OnDeInit")

    mdds_input = MDDS(timestamp= monotonic_bytes(),
                      signal_type= midasstd.eStatus.daw_to_device.value,
                      source=midasstd.daw_id.flstudio.value,
                      destination=midasstd.eDestination.all_.value,
                      command_id=midasstd.eCommand.script_exit.value.command_id,
                      payload_description=midasstd.eCommand.script_init.value.payload_description)
    mdds_input.bind_payload(get_script_device_id())

def OnMidiMsg(eventData):
    # If the sysex data is None, then we need to set it to an empty byte string for type-safety.
    # NOTE:(It seems to always be none for midi commands)
    # TODO: Generate sysex from midi data.
    if eventData.sysex is None:
        actual_sysex_data = b''
    else:
        actual_sysex_data = eventData.sysex

    mdds_input = MDDS(timestamp= monotonic_bytes(),
                        signal_type= midasstd.eStatus.device_to_device.value,
                        source=get_script_device_id(),
                        destination=midasstd.eDestination.all_.value,
                        command_id=midasstd.eCommand.midi_message.value.command_id,
                        payload_description=midasstd.eCommand.midi_message.value.payload_description)
    mdds_input.bind_payload(bytes([eventData.midiId,eventData.midiChan,eventData.data1,eventData.data2]))

    process_MDDS(mdds_input)

    # filter midi messages to MDDS messages using default midi message protocol. Custom midi message protocol can be used instead.
        # "NOTE_ON",MidiMessage(144) Byte: 0x90
        # "NOTE_OFF",MidiMessage(128) Byte: 0x80
        # "CONTROL_CHANGE",MidiMessage(176) Byte: 0xB0
        # "PROGRAM_CHANGE",MidiMessage(192) Byte: 0xC0
        # "PITCH_BEND",MidiMessage(224) Byte: 0xE0
        # "NOTE_PRESSURE",MidiMessage(160) Byte: 0xA0
        # "CHANNEL_PRESSURE",MidiMessage(208) Byte: 0xD0

    # if the midi message is a note on message then convert it to a MDDS pressed command.
    # 4 bytes.
    # Given a device identifier, search for applicaple adapters in device adapter dictionary.
    # A device adapter describes the conversion of midi messages and sysex messages to MDDS messages.
    # A device adapter is a dictionary of midi messages and sysex messages and their corresponding MDDS messages.
    # Each midi message and sysex message is atrtributed to a device, this is described as the sender in the MDDS.


    if True: # TODO: test for controller identifier. for now assume all messages are from Arturia Minilab MKII.
        if eventData.midiId == 144: # note on
            if eventData.midiChan == 15: # pads channel
                if eventData.data1 == 0: # note 0 is pad 1
                    control_id = bytes([0x00, 0x00, 0x00, 0x00])
                    status = midasstd.eStatusType.type7.value
                    command = midasstd.eCommand.pressed.value
                    payload = control_id + bytes([eventData.midiChan,eventData.data1,eventData.data2])

        if eventData.midiId == 176: # cc
            if eventData.midiChan == 0: # pads channel
                if eventData.data1 == 18: # note 0 is pad 1
                    if eventData.data2 == 127:
                        control_id = bytes([0x00, 0x00, 0x00, 0x00])
                        status = midasstd.eStatusType.type7.value
                        command = midasstd.eCommand.pressed.value
                        payload = control_id + bytes([eventData.midiChan,eventData.data1,eventData.data2])

    # Now we can query control id and respond how we want.


    unique_controler_id = bytes([0x00, 0x00, 0x00, 0x00]) # NOTE: this is a temporary palceholder for the unique controller identifier.
    # FIXME: implement a unique controller identifier method for the MDDS protocol.
    #       Each controller will have a unique identifier which will be used to identify the physical controller.
    #       This will be 4 bytes long and is device dependant.


    if eventData.midiId == 144:
        mdds_input = MDDS(timestamp= monotonic_bytes(),
                          signal_type= midasstd.eStatus.device_to_device.value,
                          source=get_script_device_id(),
                          destination=midasstd.eDestination.all_.value,
                          command_id=midasstd.eCommand.pressed.value.command_id,
                          payload_description=midasstd.eCommand.pressed.value.payload_description)
        mdds_input.bind_payload(unique_controler_id + bytes([eventData.midiChan,eventData.data1,eventData.data2]))

        process_MDDS(mdds_input)
    # if the midi message is a note off message then convert it to a MDDS released command.
    elif eventData.midiId == 128:
        mdds_input = MDDS(timestamp= monotonic_bytes(),
                          signal_type= midasstd.eStatus.device_to_device.value,
                          source=get_script_device_id(),
                          destination=midasstd.eDestination.all_.value,
                          command_id=midasstd.eCommand.released.value.command_id,
                          payload_description=midasstd.eCommand.released.value.payload_description)
        mdds_input.bind_payload(unique_controler_id + bytes([eventData.midiChan,eventData.data1,eventData.data2]))

        process_MDDS(mdds_input)
    # if the midi message is a control change or key aftertouch message then convert it to a MDDS moved_x command.
    elif eventData.midiId == 176 or eventData.midiId == 160:
        mdds_input = MDDS(timestamp= monotonic_bytes(),
                          signal_type= midasstd.eStatus.device_to_device.value,
                          source=get_script_device_id(),
                          destination=midasstd.eDestination.all_.value,
                          command_id=midasstd.eCommand.moved_x.value.command_id,
                          payload_description=midasstd.eCommand.moved_x.value.payload_description)
        mdds_input.bind_payload(unique_controler_id + bytes([eventData.midiChan,eventData.data1,eventData.data2]))

        process_MDDS(mdds_input)
    # if the midi message is a channel aftertouch message then convert it to a MDDS held_x command.
    elif eventData.midiId == 208:
        mdds_input = MDDS(timestamp= monotonic_bytes(),
                          signal_type= midasstd.eStatus.device_to_device.value,
                          source=get_script_device_id(),
                          destination=midasstd.eDestination.all_.value,
                          command_id=midasstd.eCommand.held_x.value.command_id,
                          payload_description=midasstd.eCommand.held_x.value.payload_description)
        mdds_input.bind_payload(unique_controler_id + bytes([eventData.midiChan,eventData.data1,eventData.data2]))

        process_MDDS(mdds_input)
    # if the midi message is a pitch bend message then convert it to a MDDS bent command.
    elif eventData.midiId == 224:
        mdds_input = MDDS(timestamp= monotonic_bytes(),
                          signal_type= midasstd.eStatus.device_to_device.value,
                          source=get_script_device_id(),
                          destination=midasstd.eDestination.all_.value,
                          command_id=midasstd.eCommand.bent.value.command_id,
                          payload_description=midasstd.eCommand.bent.value.payload_description)
        mdds_input.bind_payload(unique_controler_id + bytes([eventData.midiChan,eventData.data1,eventData.data2]))

        process_MDDS(mdds_input)




    # Compare incoming status, port, and note agaisnt the current active adapter's command map and find a match.
    # Determine the command source type (Internal,Button, Knob(infinite abs controller), Fader(finite abs controller), Relative(infinite rel controller))
    # if there is a matcht then we bind the command to the event channel and note.
    # Use the targeted midi message to determine the source control of the command based on the device adapter command dictionary.
    # The adapter dictionary is a names and a device object model which contains info about the possible midi messages these buttons can send.
    # We will return a list of all buttons that can send this midi message. It will be implied that they are the sender of the command.
    # If there is no match then we ignore the event.
    # if this is a button command then initiate search for matching button in the active adapter's control dictionary.