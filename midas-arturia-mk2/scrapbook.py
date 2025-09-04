# FLSI : FL Studio Scripting Interface
FLSI_PME_FLAGS = {
    'PME_System': 2,
    'PME_System_Safe': 4,
    'PME_PreviewNote': 8,
    'PME_FromHost': 16,
    'PME_FromMIDI': 32
}

FLSI_ON_REFRESH_FLAGS = {
    ''' OnRefresh flags
            Parameter	                Value	Documentation
            HW_Dirty_Mixer_Sel	        1	mixer selection changed
            HW_Dirty_Mixer_Display	    2	mixer display changed
            HW_Dirty_Mixer_Controls	    4	mixer controls changed
            HW_Dirty_RemoteLinks	    16	remote links (linked controls) has been added/removed
            HW_Dirty_FocusedWindow	    32	channel selection changed
            HW_Dirty_Performance	    64	performance layout changed
            HW_Dirty_LEDs	            256	various changes in FL which require update of controller leds
                                            update status leds (play/stop/record/active window/.....) on this flag
            HW_Dirty_RemoteLinkValues	512	remote link (linked controls) value is changed
            HW_Dirty_Patterns	        1024	pattern changes
            HW_Dirty_Tracks	            2048	track changes
            HW_Dirty_ControlValues	    4096	plugin cotrol value changes
            HW_Dirty_Colors	            8192	plugin colors changes
            HW_Dirty_Names	            16384	plugin names changes
            HW_Dirty_ChannelRackGroup	32768	Channel rack group changes
            HW_ChannelEvent	            65536	channel changes
    '''
    'HW_Dirty_Mixer_Sel': 1,
    'HW_Dirty_Mixer_Display': 2,
    'HW_Dirty_Mixer_Controls': 4,
    'HW_Dirty_RemoteLinks': 16,
    'HW_Dirty_FocusedWindow': 32,
    'HW_Dirty_Performance': 64,
    'HW_Dirty_LEDs': 256,
    'HW_Dirty_RemoteLinkValues': 512,
    'HW_Dirty_Patterns': 1024,
    'HW_Dirty_Tracks': 2048,
    'HW_Dirty_ControlValues': 4096,
    'HW_Dirty_Colors': 8192,
    'HW_Dirty_Names': 16384,
    'HW_Dirty_ChannelRackGroup': 32768,
    'HW_ChannelEvent': 65536
}

# Exceptions
class ExcInvalidMidiByteValue(ValueError):
    """
    Exception raised when an invalid midi byte is encountered.
    """

# Utility functions for the MidasOS test script
def abstract_method(func):
    """
    Decorator for marking a method as abstract.

    Raises:
        NotImplementedError: If the decorated method is called directly.
    """
    def wrapper(*args, **kwargs):
        """abstract method wrapper"""
        raise NotImplementedError(f"Abstract method {func.__name__} called. Override required.")

    return wrapper

def check_type(value, expected_type):
    """
    Checks if the value is of the expected type.

    Args:
        value (any): The value to check.
        expected_type (type): The expected type.

    Raises:
        TypeError: If the value is not of the expected type.
    """
    if not isinstance(value, expected_type ):
        raise TypeError(f"Expected type {expected_type} but got {type(value)}.")
    else:
        return value

def check_value(value, expected_values):
    """
    Checks if the value is in the expected values.

    Args:
        value (any): The value to check.
        expected_values (list[any]): The expected values.

    Raises:
        ValueError: If the value is not in the expected values.
    """
    if value not in expected_values:
        raise ValueError(f"Expected one of {expected_values} but got {value}.")
    else:
        return value

def check_flags(value : int, flags):
    """
    Checks if the integer value is a valid combination of flags.

    Flags are a dictionary of flag names and their values.

    """
    set_flags = {name: bool(value & flag) for name, flag in flags.items()}
    return set_flags

def is_valid_midi_byte(byte : int):
    """
    Returns true if the byte is a valid midi byte.

    Args:
        byte (int): The byte to check.

    Returns:
        bool: True if the byte is a valid midi byte.
    """
    if byte >= 0 and byte <= 127:
        return True
    else:
        raise ExcInvalidMidiByteValue(f"Byte {byte} is not a valid midi byte.")

def iterate_nested_dict(d, parent_key=''):
    for k, v in d.items():
        new_key = f"{parent_key}.{k}" if parent_key else k
        if isinstance(v, dict):
            iterate_nested_dict(v, new_key)
        else:
            print(f"Key: {new_key}, Value: {v}")

# DAW Space Objects
class DawEventBase:
    name = ''
    nargs = 0

    def __init__(self, timestamp : float = 0) -> None:
        self.args = []
        self.timestamp = timestamp

    def set_args(self,args : list):
        if len(args) != self.nargs:
            raise ValueError(f"Expected {self.nargs} args but got {len(args)}.")
        self.args = args
        self._set_args(args)

    @staticmethod
    def make_daw_event(event_type,timestamp : float , args : list = []):

        event = event_type(timestamp)
        if args:
            event.set_args(args)
        return event

    @abstract_method
    def _set_args(self,args):
        pass

class DawEventScriptInit(DawEventBase):
    name = 'script_init'

class DawEventScriptDeInit(DawEventBase):
    name = 'script_deinit'

class DawEventDeviceMidiIn(DawEventBase):
    """
    PME flags
        Parameter	Value	Documentation
        PME_System	2	Can do system stuff (play/pause.. mostly safe things)
        PME_System_Safe	4	Can do critical system stuff (add markers.. things that can't be done when a modal window is shown)
        PME_PreviewNote	8	note trigger previews notes | controls stuff
        PME_FromHost	16	when the app is hosted
        PME_FromMIDI	32	coming from MIDI event


    """
    name = 'device_midi_in'
    nargs = 8
    def __init__(self,timestamp : float = 0) -> None:
        super().__init__(timestamp)

        self.handled : int
        self.timestamp : float
        self.status : int
        self.port : int
        self.note : int
        self.value : int
        self.port_exclusive: int
        self.sysex : bytes

    def _set_args(self, args):
        self.handled = check_type(args[0],int)
        self.timestamp = check_type(args[1],float)
        self.status = check_type(args[2],int)
        self.port = check_type(args[3],int)
        self.note = check_type(args[4],int)
        self.value = check_type(args[5],int)
        self.port_exclusive = check_type(args[6],int)
        self.sysex = check_type(args[7],bytes)

class DawEventDeviceSysexIn(DawEventBase):
    name = 'device_sysex_in'
    nargs = 1

    def __init__(self,timestamp : float = 0) -> None:
        super().__init__(timestamp)
        self.sysex : bytes

    def _set_args(self, args):
        self.sysex = check_type(args[0],bytes)

class DawEventDawMidiIn(DawEventBase):
    name = 'daw_midi_in'
    nargs = 8
    def __init__(self,timestamp : float = 0) -> None:
        super().__init__(timestamp)

        self.handled : int
        self.status : int
        self.data1 : int
        self.data2 : int
        self.port : int
        self.midiId : int
        self.midiChan : int
        self.midiChanEx : int

    def _set_args(self, args):
        self.handled = check_type(args[0],int)
        self.status = check_type(args[1],int)
        self.data1 = check_type(args[2],int)
        self.data2 = check_type(args[3],int)
        self.port = check_type(args[4],int)
        self.midiId = check_type(args[5],int)
        self.midiChan = check_type(args[6],int)
        self.midiChanEx = check_type(args[7],int)

class DawEventIdle(DawEventBase):
    name = 'idle'

class DawEventProjectLoaded(DawEventBase):
    """
        OnProjectLoad status (arg1)
            Parameter	    Value	Documentation
            PL_Start	    0	    Called when project loading start
            PL_LoadOk	    100	    Called when project was succesfully loaded
            PL_LoadError	101	    Called when project loading stopped because of error
    """
    name = 'project_loaded'
    nargs = 1

    def __init__(self,timestamp : float = 0) -> None:
        super().__init__(timestamp)

        self.status = None

    def _set_args(self, args):
        self.status = check_value(args[0],[0,100,101])

class DawEventRefresh(DawEventBase):
    """
    OnRefresh flags
        Parameter	Value	Documentation
        HW_Dirty_Mixer_Sel	1	mixer selection changed
        HW_Dirty_Mixer_Display	2	mixer display changed
        HW_Dirty_Mixer_Controls	4	mixer controls changed
        HW_Dirty_RemoteLinks	16	remote links (linked controls) has been added/removed
        HW_Dirty_FocusedWindow	32	channel selection changed
        HW_Dirty_Performance	64	performance layout changed
        HW_Dirty_LEDs	256	various changes in FL which require update of controller leds
        update status leds (play/stop/record/active window/.....) on this flag
        HW_Dirty_RemoteLinkValues	512	remote link (linked controls) value is changed
        HW_Dirty_Patterns	1024	pattern changes
        HW_Dirty_Tracks	2048	track changes
        HW_Dirty_ControlValues	4096	plugin cotrol value changes
        HW_Dirty_Colors	8192	plugin colors changes
        HW_Dirty_Names	16384	plugin names changes
        HW_Dirty_ChannelRackGroup	32768	Channel rack group changes
        HW_ChannelEvent	65536	channel changes

    """
    name = 'refresh'
    nargs = 1
    def __init__(self,timestamp : float = 0) -> None:
        super().__init__(timestamp)

        self.flags = None

    def _set_args(self, args):
        self.flags = check_type(args[0],int) # NOTE: Use check_flags(value, FLSI_ON_REFERESH_FLAGS) to retrieve the flags from the integer value.

class DawEventFullRefresh(DawEventBase):
    name = 'full_refresh'

class DawEventBeatIndicatorUpdate(DawEventBase):
    name = 'beat_indicator_update'
    nargs = 1
    def __init__(self,timestamp : float = 0) -> None:
        super().__init__(timestamp)
        self.value = None

    def _set_args(self, args):
        self.value = check_type(args[0],int)

class DawEventDisplayZoneUpdate(DawEventBase):
    name = 'display_zone_update'

class DawEventLiveModeUpdate(DawEventBase):
    name = 'live_mode_update'
    nargs = 1
    def __init__(self,timestamp : float = 0) -> None:
        super().__init__(timestamp)
        self.last_track = None

    def _set_args(self, args):
        self.last_track = check_type(args[0],int)

class DawEventMixerTrackChanged(DawEventBase):
    """
    	Called on mixer track(s) change, 'index' indicates track index of track that changed or -1 when all tracks changed
        collect info about 'dirty' tracks here but do not handle track(s) refresh, wait for OnRefresh event with HW_Dirty_Mixer_Controls flag

    """
    name = 'mixer_track_changed'
    nargs = 1
    def __init__(self,timestamp : float = 0) -> None:
        super().__init__(timestamp)
        self.index = None

    def _set_args(self, args):
        self.index = check_type(args[0],int)

class DawEventChannelChanged(DawEventBase):
    """
        Called on channel rack channel(s) change, 'index' indicates channel that changed or -1 when all channels changed
        collect info about 'dirty' channels here but do not handle channels(s) refresh, wait for OnRefresh event with HW_ChannelEvent flag

        OnDirtyChannel flags
        Parameter	Value	Documentation
        CE_New	0	new channel is added
        CE_Delete	1	channel deleted
        CE_Replace	2	channel replaced
        CE_Rename	3	channel renamed
        CE_Select	4	channel selection changed

    """
    name = 'channel_changed'
    nargs = 2
    def __init__(self,timestamp : float = 0) -> None:
        super().__init__(timestamp)
        self.index = None
        self.flags = None

    def _set_args(self, args):
        self.index = check_type(args[0],int)
        self.flags = check_value(args[1],[0,1,2,3,4])

class DawEventDeviceFirstConnect(DawEventBase):
    name = 'device_first_connect'

class DawEventRequestingUpdateMeters(DawEventBase):
    name = 'requesting_update_meters'

class DawEventRequestingInput(DawEventBase):
    name = 'requesting_input'

class DawEventSendingHintToDevice(DawEventBase):
    name = 'sending_hint_to_device'
    nargs = 2
    def __init__(self,timestamp : float = 0) -> None:
        super().__init__(timestamp)
        self.message = None
        self.duration = None

    def _set_args(self, args):
        self.message = check_type(args[0],str)
        self.duration = check_type(args[1],int)

# Command Space Objects
class MidiMessageBehavior:
    ''' A set of flags that describe how a midi message coming from the device should be interpreted.'''
    def __init__(self,is_offset_by_channel = False,
                 is_base_offset_by_channel = False,
                 is_offset_by_note = False,
                 is_base_offset_by_note = False,
                 base_channel_offset = 0,
                 base_note_offset = 0) -> None:
        # True if the code is additionally offset by the midi channel
        # eg. Status 148 Port 4 is status 144 Port 4. Status 148 Port 0 is status 148 Port 0.
        # status_actual = status_in - channel
        self.is_offset_by_channel = is_offset_by_channel

        # True if the code is offset by the midi channel
        # eg. Status 148 Port 4 is status 144 Port 4.
        #   Status 148 Port 0 is status 144 Port 0. (scans up to 16 channels)
        # for i in range(16):
        #   status_actual = status_in - i
        #   if status_actual == existing_status:
        #       channel = i
        #       return status_actual
        self.is_base_offset_by_channel = is_base_offset_by_channel

        # True if the code is additionally offset by the midi note eg.
        # Status 148 Note 4 is status 144 Note 4. Status 148 Note 0 is status 148 Note 0.
        # status_actual = status_in - note
        self.is_offset_by_note = is_offset_by_note

        # True if the code is offset by the midi note #NOTE: This is a rare case.
        # eg. Status 148 Port 4 is status 144 Port 4.
        #   Status 148 Port 0 is status 144 Port 0. (scans up to 127 notes)
        self.is_base_offset_by_note = is_base_offset_by_note
        # for i in range(127):
        #   status_actual = status_in - i
        #   if status_actual == existing_status:
        #       note = i
        #       return status_actual

        # The base offset of the midi channel for this code.
        # Eg. Status 148 Port 4 with base offset of 4 is status 148 port 8.
        self.base_channel_offset = base_channel_offset

        # The base offset of the note of this code.
        # Eg. Status 148 Note 4 with base offset of 4 is status 148 Note 8.
        self.base_note_offset = base_note_offset

    def __eq__(self, __value: object) -> bool:
        # equal if the status and behavior are equal.
        if isinstance(__value, MidiMessageBehavior):
            return self.is_offset_by_channel == __value.is_offset_by_channel \
                and self.is_base_offset_by_channel == __value.is_base_offset_by_channel \
                and self.is_offset_by_note == __value.is_offset_by_note \
                and self.is_base_offset_by_note == __value.is_base_offset_by_note \
                and self.base_channel_offset == __value.base_channel_offset \
                and self.base_note_offset == __value.base_note_offset
        else:
            return False

    def __hash__(self) -> int:
        return hash((self.is_offset_by_channel,self.is_base_offset_by_channel,self.is_offset_by_note,self.is_base_offset_by_note,self.base_channel_offset,self.base_note_offset))

    def __str__(self) -> str:
        return f"[MIDI_MESSAGE_BEHAVIOR] \nis_offset_by_channel: {self.is_offset_by_channel} \nis_base_offset_by_channel: {self.is_base_offset_by_channel} \nis_offset_by_note: {self.is_offset_by_note} \nis_base_offset_by_note: {self.is_base_offset_by_note} \nbase_channel_offset: {self.base_channel_offset} \nbase_note_offset: {self.base_note_offset} \n"

class MidiMessage:
    """
    Represents a midi command.

    EXAMPLE USE:

    DEFAULT_NOTE_ON_MIDI_COMMAND = MidiCommand(int_to_byte(144),
                                            MidiCommandBehavior(True,False,False,False,0,0),
                                            {'VELOCITY':MidiParameter([])})

    # TARGET Commands to check and compare against input commands.
    DEFAULT_NOTE_ON_MIDI_COMMAND_CH1_NOTE1 = DEFAULT_NOTE_ON_MIDI_COMMAND.target(1,1)

    # Bind Commands to send to the device with a value or check for a specific value.
    DEFAULT_NOTE_ON_MIDI_COMMAND_CH1_NOTE1_VELOCITY127 = DEFAULT_NOTE_ON_MIDI_COMMAND.bind(
                                                            1,1,{'VELOCITY':int_to_byte(127)})
    """
    def __init__(self,
                 status : int ,
                 behavior : MidiMessageBehavior = MidiMessageBehavior()) -> None:
        self.status = status
        self.behavior = behavior

    def get(self,status_in : int, channel : int,note : int):
        """
        Gets the actual status, channel and note given a status, channel and note based on the offset behavior.

        Args:
            status_in (int): The status to offset.
            channel (int): The channel to offset by.
            port (int): The port to offset by.

        Returns:
            bytes: The actual status.
        """
        status_actual = status_in
        channel_actual = channel
        note_actual = note

        # apply channel offset
        if self.behavior.is_offset_by_channel:
            status_actual = status_in - channel
            channel_actual = channel

        # apply base channel offset
        # Check if the status matches one of the offset by channel commands for up to 16 channel offsets
        # This is in case the port is always set to 0, but the status is offset by the channel.
        #       The range is a maximum of 16 channels.
        if self.behavior.is_base_offset_by_channel:
            for i in range(16):
                status_actual = status_in - i
                if status_actual == self.status:
                    channel_actual = i
                    break


        # apply note offset
        if self.behavior.is_offset_by_note:
            status_actual = status_in - channel
            channel_actual = channel

        # apply base note offset
        # Check if the status matches one of the offset by note commands for up to 127 offsets
        # This is in case the note is set  to 0, but the status is offset by the note.
        #       The range is a maximum of 127 notes.
        # NOTE: edge case. Rarely used.
        if self.behavior.is_base_offset_by_note:
            for i in range(17):
                status_actual = status_in - i
                if status_actual == self.status:
                    note_actual = i
                    break

        # apply base channel offset
        channel_actual += self.behavior.base_channel_offset

        # apply base note offset
        note_actual += self.behavior.base_note_offset

        return status_actual,channel_actual,note_actual

    def __eq__(self, __value: object) -> bool:
        # equal if the status and behavior are equal.
        if isinstance(__value, MidiMessage):
            return self.status == __value.status and self.behavior == __value.behavior
        else:
            return False

    def __hash__(self) -> int:
        return hash((self.status,self.behavior))

    def matches(self,status_in : int, channel : int,note : int):
        '''
            Returns a list of status codes that may possibly match with this command based on the behavior.

        '''
        astatus, *_  = self.get(status_in,channel,note)
        if astatus == self.status:
            return True
        else:
            return False

    def target(self,channel : int,note : int):
        '''Target the command to a channel and note. Return a TargetedMidiCommand object.'''

        # Validate the channel and note.
        if is_valid_midi_byte(channel) and is_valid_midi_byte(note):
            return TargetedMidiMessage(self,channel,note)
        else:
            raise ValueError(f"Channel {channel} and note {note} must be valid midi bytes.")

    def bind(self,channel,note,value):
        """
        Binds the midi command to channel, note and value.

        Args:
            parameters (dict[str,bytes]): The parameters to bind to the midi command.

        Returns:
            BoundMidiCommand: The bound midi command.
        """

        # Validate the channel and note.
        if is_valid_midi_byte(value):
            return BoundMidiMessage(TargetedMidiMessage(self,channel,note),value)
        else:
            raise ValueError(f"Channel {channel} and note {note} must be valid midi bytes.")

    def __str__(self) -> str:
        return f"[MIDI_MESSAGE] Status: {self.status} \n"

class TargetedMidiMessage(MidiMessage):
    '''
        Represents a midi command that has been targeted to a specific channel and note.
        This is used to check if a midi message matches the targeted channel and note.
    '''
    def __init__(self, midi_msg : MidiMessage,port : int, note : int) -> None:
        super().__init__(midi_msg.status, midi_msg.behavior)
        self.port = port
        self.note = note

    def get(self,status_in):
        return super().get(status_in,self.port,self.note)

    def bind(self,value) -> 'BoundMidiMessage':
        """
        Binds the midi command to channel, note and value.

        Args:
            parameters (dict[str,bytes]): The parameters to bind to the midi command.

        Returns:
            BoundMidiCommand: The bound midi command.
        """
        return super().bind(self.port,self.note,value)

    def target(self, channel: int, note: int):
        return super().target(channel, note)


    # def matches(self,status_in : int, channel : int,note : int):
    #     '''
    #         Returns a list of status codes that may possibly match with this command based on the behavior.

    #     '''
    #     astatus, *_  = self.get(status_in,channel,note)
    #     if astatus == self.status:
    #         return True
    #     else:
    #         return False

    def __str__(self) -> str:
        return "[TARGETED]" + super().__str__() + f"Port: {self.port} Note: {self.note}"

class BoundMidiMessage(TargetedMidiMessage):
    '''
        Represents a midi command that has been targeted to a specific channel and note, with a specific value.
        This is used to send a midi message to the device. Or check if a midi message matches the targeted channel, note and value.

    '''
    def __init__(self, targeted_midi_msg : TargetedMidiMessage,value) -> None:
        super().__init__(MidiMessage(targeted_midi_msg.status, targeted_midi_msg.behavior),targeted_midi_msg.port,targeted_midi_msg.note)
        self.value = value

    def __str__(self) -> str:
        return "[BOUND]" + super().__str__() + f" Value: {self.value}"



def int_to_byte(value : int) -> bytes:
    """
    Converts an int to a byte.

    Args:
        value (int): The value to convert.

    Returns:
        bytes: The converted value.
    """
    return bytes([value])

class SysexParameter:
    """
    Represents a sysex message parameter.
    """
    def __init__(self, size : int, options : 'list[bytes]') -> None:
        self.size = size # The number of bytes the parameter takes up. Unused bytes will be padded with 0x00.
        self.options = options # The options for the parameter.

class BoundSysexMessage:
    """
    Represents a sysex message message.
    """
    sysex_start = bytes([0xF0])
    sysex_end = bytes([0xF7])

    def __init__(self, device_id : bytes, message : bytes,message_parameters,data: bytes) -> None:
        self.device_id = device_id # The device id.
        self.sysex_message = message # The sysex message.
        # Dict of parameter names for the message and a list of options for each parameter.
        self.message_parameters : dict[str,SysexParameter] = message_parameters

        if not self.validate_parameters(data):
            raise ValueError(f"Sysex data {data} is not valid for message {message}.")
        self.data = data

    def validate_parameters(self, data : bytes):
        """ Validates the sysex data."""
        try:
            # Expected data length is equal to the combined length of size of all parameters.
            expected_data_length = 0
            for parameter in self.message_parameters.values():
                expected_data_length += parameter.size

            if len(data) != expected_data_length:
                raise ValueError(f"Expected sysex data length of \
                    {expected_data_length} but got {len(data)}.")

            # Check if the data is valid.
            # if the parameter option is empty, then any data of equal size is valid.
            # if the parameter option is not empty, then the data must be in the list of options.
            # if the parameter option is not empty and the data is not in the list of options,
                # then raise an error.
            data_index = 0
            for parameter_name, parameter in self.message_parameters.items():
                if len(parameter.options) > 0:
                    if data[data_index:data_index+parameter.size] not in parameter.options:
                        raise ValueError(
                            f"Sysex data {data[data_index:data_index+parameter.size]} \
                            is not a valid option for parameter {parameter_name}.")
                data_index += parameter.size

            return True
        except ValueError:
            return False

    def get(self):
        """
        Gets the sysex message.

        Returns:
            bytes: The sysex message.
        """

        return Sysexmessage.sysex_start \
                + self.device_id        \
                + self.sysex_message    \
                + self.data             \
                + Sysexmessage.sysex_end

    def matches(self, sysex_message : bytes, ignored_arg1,ignored_arg2):
        """
        Checks if the sysex message matches the sysex message.

        Args:
            sysex_message (bytes): The sysex message to check.

        Returns:
            bool: True if the sysex message matches the sysex message.
        """
        if sysex_message == self.sysex_message:
            return True
        else:
            return False

    def __str__(self) -> str:
        return f"Sysexmessage({self.device_id},{self.sysex_message},{self.message_parameters})"

class SysexMessage:
    """
    Represents a sysex message message.
    """
    sysex_start = bytes([0xF0])
    sysex_end = bytes([0xF7])

    def __init__(self, device_id : bytes, message : bytes,message_parameters) -> None:
        self.device_id = device_id # The device id.
        self.sysex_message = message # The sysex message.
        # Dict of parameter names for the message and a list of options for each parameter.
        self.message_parameters : dict[str,SysexParameter] = message_parameters

    def validate_parameters(self, data : bytes):
        """ Validates the sysex data."""
        try:
            # Expected data length is equal to the combined length of size of all parameters.
            expected_data_length = 0
            for parameter in self.message_parameters.values():
                expected_data_length += parameter.size

            if len(data) != expected_data_length:
                raise ValueError(f"Expected sysex data length of \
                    {expected_data_length} but got {len(data)}.")

            # Check if the data is valid.
            # if the parameter option is empty, then any data of equal size is valid.
            # if the parameter option is not empty, then the data must be in the list of options.
            # if the parameter option is not empty and the data is not in the list of options,
                # then raise an error.
            data_index = 0
            for parameter_name, parameter in self.message_parameters.items():
                if len(parameter.options) > 0:
                    if data[data_index:data_index+parameter.size] not in parameter.options:
                        raise ValueError(
                            f"Sysex data {data[data_index:data_index+parameter.size]} \
                            is not a valid option for parameter {parameter_name}.")
                data_index += parameter.size

            return True
        except ValueError:
            return False

    def get(self, data : bytes):
        """
        Gets the sysex message.

        Returns:
            bytes: The sysex message.
        """

        if not self.validate_parameters(data):
            raise ValueError(f"Sysex data {data} is not valid for message {self.sysex_message}.")

        return SysexMessage.sysex_start \
                + self.device_id        \
                + self.sysex_message    \
                + data                  \
                + SysexMessage.sysex_end

    def bind(self, data : bytes):
        """
        Binds the sysex message to a set of data. Returns a BoundSysexMessage object.

        Args:
            data (bytes): The data to bind to the sysex message.

        Returns:
            BoundSysexMessage: The bound sysex message.
        """
        if not self.validate_parameters(data):
            raise ValueError(f"Sysex data {data} is not valid for message {self.sysex_message}.")

        return BoundSysexMessage(self.device_id,self.sysex_message,self.message_parameters,data)

    def matches(self, sysex_message : bytes):
        """
        Checks if the sysex message matches the sysex message.

        Args:
            sysex_message (bytes): The sysex message to check.

        Returns:
            bool: True if the sysex message matches the sysex message.
        """
        if sysex_message == self.sysex_message:
            return True
        else:
            return False

    def __str__(self) -> str:
        return f"SysexMessage({self.device_id},{self.sysex_message},{self.message_parameters})"

class UserMidiCodes:
    """
        An instance class that stores user defined midi midi_messages.
    """
    INPUT = False
    OUTPUT = True

    def __init__(self) -> None:
        self.user_input_midi_messages : dict[str,MidiMessage] = {}
        self.user_input_midi_messages_inverse : dict[MidiMessage,str] = {}
        self.user_input_sysex_messages : dict[str,SysexMessage] = {}
        self.user_input_sysex_messages_inverse : dict[bytes,str] = {}

        self.user_output_midi_messages : dict[str,MidiMessage] = {}
        self.user_output_midi_messages_inverse : dict[MidiMessage,str] = {}
        self.user_output_sysex_messages : dict[str,SysexMessage] = {}
        self.user_output_sysex_messages_inverse : dict[bytes,str] = {}

    def emplace_sysex(self,input_output : bool ,message_name : str, sysex_message : SysexMessage):
        """
        Sets the sysex message for a user message. Emplaces message if it does not exist.

        Args:
            message_name (str): The name of the message.
            sysex_message (SysexMessage): The sysex message.
        """
        if input_output == UserMidiCodes.INPUT:
            if message_name in self.user_input_sysex_messages:
                raise ValueError(f"Message name '{message_name}' already exists.")
            if sysex_message.sysex_message in self.user_input_sysex_messages_inverse:
                raise ValueError(f"Sysex message '{sysex_message}' already exists.")

            self.user_input_sysex_messages[message_name] = sysex_message
            self.user_input_sysex_messages_inverse[sysex_message.sysex_message] = message_name
        elif input_output == UserMidiCodes.OUTPUT:
            if message_name in self.user_output_sysex_messages:
                raise ValueError(f"Message name '{message_name}' already exists.")
            if sysex_message.sysex_message in self.user_output_sysex_messages_inverse:
                raise ValueError(f"Sysex message '{sysex_message}' already exists.")

            self.user_output_sysex_messages[message_name] = sysex_message
            self.user_output_sysex_messages_inverse[sysex_message.sysex_message] = message_name
        else:
            raise ValueError(f"Invalid input_output value {input_output}.")

    def get_all_sysex_messages(self,input_output : bool):
        """
        Gets the user sysex messages. References the MidiCodes.user_input_sysex_messages dictionary.

        Returns:
            dict[str,SysexMessage]: The user sysex messages.
        """
        if input_output == UserMidiCodes.INPUT:
            return self.user_input_sysex_messages
        elif input_output == UserMidiCodes.OUTPUT:
            return self.user_output_sysex_messages
        else:
            raise ValueError(f"Invalid input_output value {input_output}.")

    def get_sysex_message(self,input_output : bool ,message_name : str):
        """
        Gets the sysex message for a user message.

        Args:
            message_name (str): The name of the message.

        Returns:
            SysexMessage(or None): The sysex message.
        """
        if input_output == UserMidiCodes.INPUT:
            if message_name in self.user_input_sysex_messages:
                return self.user_input_sysex_messages[message_name]
            return None
        elif input_output == UserMidiCodes.OUTPUT:
            if message_name in self.user_output_sysex_messages:
                return self.user_output_sysex_messages[message_name]
            return None
        else:
            raise ValueError(f"Invalid input_output value {input_output}.")

    def get_sysex_message_name(self,input_output : bool, sysex_message : bytes):
        """
        Gets the message for a user sysex message.

        Args:
            sysex_message (bytes): The sysex message.

        Returns:
            str(or None): The name of the message.
        """
        if input_output == UserMidiCodes.INPUT:
            if sysex_message in self.user_input_sysex_messages_inverse:
                return self.user_input_sysex_messages_inverse[sysex_message]
            return None
        elif input_output == UserMidiCodes.OUTPUT:
            if sysex_message in self.user_output_sysex_messages_inverse:
                return self.user_output_sysex_messages_inverse[sysex_message]
            return None
        else:
            raise ValueError(f"Invalid input_output value {input_output}.")

    def emplace_midi_message(self,input_output : bool,message_name : str, midi_message : MidiMessage):
        """
        Sets the midi_message for a user message. Emplaces message if it does not exist.

        Args:
            message_name (str): The name of the message.
            midi_message (MidiMessage): The midi_message for the message.
        """

        if input_output == UserMidiCodes.INPUT:
            if message_name in self.user_input_midi_messages:
                raise ValueError(f"Message name '{message_name}' already exists.")
            if midi_message in self.user_input_midi_messages_inverse:
                raise ValueError(f"Code '{midi_message}' already exists.")

            self.user_input_midi_messages[message_name] = midi_message
            self.user_input_midi_messages_inverse[midi_message] = message_name
        elif input_output == UserMidiCodes.OUTPUT:
            if message_name in self.user_output_midi_messages:
                raise ValueError(f"Message name '{message_name}' already exists.")
            if midi_message in self.user_output_midi_messages_inverse:
                raise ValueError(f"Code '{midi_message}' already exists.")

            self.user_output_midi_messages[message_name] = midi_message
            self.user_output_midi_messages_inverse[midi_message] = message_name
        else:
            raise ValueError(f"Invalid input_output value {input_output}.")

    def get_all_midi_messages(self,input_output : bool):
        """
        Gets the user midi_messages. References the MidiCodes.user_input_midi_messages dictionary.

        Returns:
            dict[str,bytes]: The user midi_messages.
        """
        if input_output == UserMidiCodes.INPUT:
            return self.user_input_midi_messages
        elif input_output == UserMidiCodes.OUTPUT:
            return self.user_output_midi_messages
        else:
            raise ValueError(f"Invalid input_output value {input_output}.")

    def get_midi_message(self,input_output : bool,midi_message_name : str):
        """
        Gets the midi_message for a user midi_message name

        Args:
            midi_message_name (str): The name of the message.

        Returns:
            bytes(or None): The midi_message for the message.
        """
        if input_output == UserMidiCodes.INPUT:
            if midi_message_name in self.user_input_midi_messages:
                return self.user_input_midi_messages[midi_message_name]
            return None
        elif input_output == UserMidiCodes.OUTPUT:
            if midi_message_name in self.user_output_midi_messages:
                return self.user_output_midi_messages[midi_message_name]
            return None
        else:
            raise ValueError(f"Invalid input_output value {input_output}.")

    def get_name(self,input_output : bool,midi_message : bytes):
        """
        Gets the message name for a user midi_message.

        Args:
            midi_message (bytes): The midi_message for the message.

        Returns:
            str(or None): The name of the message.
        """
        if input_output == UserMidiCodes.INPUT:
            if midi_message in self.user_input_midi_messages_inverse:
                return self.user_input_midi_messages_inverse[midi_message]
            return None
        elif input_output == UserMidiCodes.OUTPUT:
            if midi_message in self.user_output_midi_messages_inverse:
                return self.user_output_midi_messages_inverse[midi_message]
            return None
        else:
            raise ValueError(f"Invalid input_output value {input_output}.")

    def clear(self):
        """
        Clears all user midi_messages.
        """
        self.user_input_midi_messages.clear()
        self.user_input_midi_messages_inverse.clear()
        self.user_input_sysex_messages.clear()
        self.user_input_sysex_messages_inverse.clear()

        self.user_output_midi_messages.clear()
        self.user_output_midi_messages_inverse.clear()
        self.user_output_sysex_messages.clear()
        self.user_output_sysex_messages_inverse.clear()

    def matches(self,status : int,channel : int, note : int):
        """
        Returns true of midi_message entry in the input dictionary that matches with this command based on the behavior.
        Returns the matched command.
        """
        for midi_message in self.user_input_midi_messages.values():
            if midi_message.matches(status,channel,note):
                return self.user_input_midi_messages_inverse[midi_message],self.get_midi_message(UserMidiCodes.INPUT,self.user_input_midi_messages_inverse[midi_message])
        return None

# Set up default midi codes.
DEFAULT_MIDAS_CODES = UserMidiCodes()
DEFAULT_MIDAS_CODES.emplace_midi_message(UserMidiCodes.INPUT,"NOTE_ON",MidiMessage(144))
DEFAULT_MIDAS_CODES.emplace_midi_message(UserMidiCodes.INPUT,"NOTE_OFF",MidiMessage(128))
DEFAULT_MIDAS_CODES.emplace_midi_message(UserMidiCodes.INPUT,"CONTROL_CHANGE",MidiMessage(176))
DEFAULT_MIDAS_CODES.emplace_midi_message(UserMidiCodes.INPUT,"PROGRAM_CHANGE",MidiMessage(192))
DEFAULT_MIDAS_CODES.emplace_midi_message(UserMidiCodes.INPUT,"PITCH_BEND",MidiMessage(224))
DEFAULT_MIDAS_CODES.emplace_midi_message(UserMidiCodes.INPUT,"NOTE_PRESSURE",MidiMessage(160))
DEFAULT_MIDAS_CODES.emplace_midi_message(UserMidiCodes.INPUT,"CHANNEL_PRESSURE",MidiMessage(208))

'''
Example Setup for device minilab mk2
Minilab MkII
DeviceAdapter

Midi Controls are editable in the MIDI Control Center, an Arturia application.
The controls are stored in a file with the extension .mcc
NOTE:This adapter assume the user has set the controls using the included .mcc file.
The controls are mapped to the following functions:
    Knobs:
        CCKnobs 1-16: CC 0-15 (Controller) Absolute ( On keyboard channel)
        ShiftKnob1: CC 16 (Controller) Relative ( On keyboard channel)
        ShiftKnob9: CC 17 (Controller) Relative ( On keyboard channel)
    Faders:
        Modulator : CC 100 Absolute Fader ( On keyboard channel)
        SustainPedal: CC 101 Absolute Fader ( On keyboard channel)
    Buttons:
        Shift Button: Sysex Message (Toggle)
        Octave - Button: Sysex Message (Toggle)
        Octave + Button: Sysex Message (Toggle)
        Pad 1-8/9-16 Button: Sysex Message (Hold)
        PressKnob1: Press: Note 16 (Gate) ( On keyboard channel) (Hold)
        PressKnob9: Press: Note 17 (Gate) ( On keyboard channel) (Hold)
        Pads 1-16: MidiNote(with aftertouch) 0-15 Note (Toggle) ( On channel 16) note 0 to 16
    Pitch Bend:
        Pitch Bend : Standard Pitch Bend ( On keyboard channel)

Shift Button: Sysex Message (Toggle) |
    On Press: F0  00  20  6B  7F  42  02  00  00  2E  7F  F7
    On Release: F0  00  20  6B  7F  42  02  00  00  2E  00  F7
When Shift is pressed:
    1. You can press one of the 16 Keyboard MIDI CH keys to change the keyboard channel.
        The device will not send any Sysex to indicate a Keyboard Channel change.
        NOTE: Do not set the keyboard channel to 16,
                  the channel used for the pads in our .mcc preset.
              This is nescessary to allow the pads to send aftertouch.
              And be recognized as a pads by Midas.
    2. You can choose the source device memory using the 8 pads.
          First is default Analog Lab, then 6 user memories, then 8(Ableton Live Mode).
        NOTE: Adapter assumes user stored the included .mcc file in the first user memory(2).
        The device will send a memchange sysex message when a new memory is selected.
          Shift Button Press:  F0  00  20  6B  7F  42  02  00  00  2E  7F  F7  |  Sysex
          Mem Change 1-8:  F0  00  20  6B  7F  42  1B  [00-07(mem index #)]  F7  |  Sysex
          Shift Button Release:  F0  00  20  6B  7F  42  02  00  00  2E  00  F7  |  Sysex
    3. Knob 1 and Knob 9 control a diffrent CC number.
        CC 1 and CC 9 respectively. On shift press, the CC number is 17 and 18.

Octave - Buttons: Sysex Message (Toggle) |
     Pressed:  F0  00  20  6B  7F  42  02  00  00  10  7F  F7  |  Sysex
     Released:  F0  00  20  6B  7F  42  02  00  00  10  00  F7  |  Sysex

Octave + Button: Sysex Message (Toggle) |
     Pressed:  F0  00  20  6B  7F  42  02  00  00  11  7F  F7  |  Sysex
     Released:  F0  00  20  6B  7F  42  02  00  00  11  00  F7  |  Sysex

Octave + and - pressed at once reset the octave.
    F0  00  20  6B  7F  42  02  00  00  10  7F  F7
    F0  00  20  6B  7F  42  02  00  00  11  7F  F7
    F0  00  20  6B  7F  42  02  00  00  10  00  F7
    F0  00  20  6B  7F  42  02  00  00  11  00  F7

Pad 1-8/9-16 Button: Sysex Message (Toggle) | NOTE: Message wont report toggle state.
    Toggles between the 2 pages of pads in the 8 Pad buttons.
    State is toggled upon button press.
    Pressed:  F0  00  20  6B  7F  42  02  00  00  2F  7F  F7  |  Sysex
    Released:  F0  00  20  6B  7F  42  02  00  00  2F  00  F7  |  Sysex

Output Sysex Messages:

SetPadLights: Sysex Message (output) |
    Sets the color of the pads.
    F0  [00  20  6B  7F  42]  [02  00  10]  [(pad #)]  [(color)]  F7  |  Sysex

Color Bytes:
    NONE = 0
    RED = 1
    WHITE = 127
    GREEN = 4
    YELLOW = 5
    BLUE = 16
    CYAN = 20
    PURPLE = 17

Pad Bytes:
    1-8 = 70-77
    9-16 = 78-7F

Memory Index Bytes:
    1-8 = 00-07

ButtonState Bytes:
    PRESSED = 7F # integer 127
    RELEASED = 00 # released 0
'''

MiniLab2DeviceId = bytes([0x00, 0x20, 0x6B, 0x7F, 0x42])
MiniLab2SysexCommandParameterPressedReleased= {
    "PRESSED_RELEASED" : SysexParameter(1,[b'\x7F',b'\x00'])}
MiniLabSysexButtonPressedValue = bytes([0x7F])
MiniLabSysexButtonReleasedValue = bytes([0x00])
MiniLab2SysexCommandParameterMemChange= {
    "MEM_INDEX" : SysexParameter(1,
                    [b'\x00',b'\x01',b'\x02',b'\x03',b'\x04',b'\x05',b'\x06',b'\x07'])}
MiniLab2SysexCommandCodeShift = bytes([0x02, 0x00, 0x00, 0x2E])
MiniLab2SysexCommandCodeOctaveMinus = bytes([0x02, 0x00, 0x00, 0x10])
MiniLab2SysexCommandCodeOctavePlus = bytes([0x02, 0x00, 0x00, 0x11])
MiniLab2SysexCommandCodePadPage = bytes([0x02, 0x00, 0x00, 0x2F])
MiniLab2SysexCommandCodeMemChange = bytes([0x1B])

MiniLab2SysexCommandParameterLedId = {
    "LED_ID" :
        SysexParameter(1,[b'\x70',b'\x71',b'\x72',b'\x73',b'\x74',b'\x75',b'\x76',b'\x77',
                        b'\x78',b'\x79',b'\x7A',b'\x7B',b'\x7C',b'\x7D',b'\x7E',b'\x7F'])}
MiniLab2SysexCommandParameterLedColor = {
    'LED_COLOR' :
        SysexParameter(1,[b'\x00',b'\x01',b'\x7F',b'\x04',b'\x05',b'\x10',b'\x14',b'\x11'])}
MiniLab2SysexCommandCodeLed = bytes([0x02, 0x00, 0x10])


MiniLabMkIIInputCodes = UserMidiCodes()

MiniLabMkIIInputCodes.emplace_sysex(
    UserMidiCodes.OUTPUT,
    "LED",
    SysexMessage(
        MiniLab2DeviceId,
        MiniLab2SysexCommandCodeLed,
        {**MiniLab2SysexCommandParameterLedId,**MiniLab2SysexCommandParameterLedColor}
        )
    )


MiniLabMkIIInputCodes.emplace_sysex(UserMidiCodes.INPUT,"SHIFT",
    SysexMessage(MiniLab2DeviceId,
                 MiniLab2SysexCommandCodeShift,
                 {**MiniLab2SysexCommandParameterPressedReleased})
                            )
MiniLabMkIIInputCodes.emplace_sysex(UserMidiCodes.INPUT,"OCTAVE_MINUS",
    SysexMessage(MiniLab2DeviceId,MiniLab2SysexCommandCodeOctaveMinus,
                  {**MiniLab2SysexCommandParameterPressedReleased})
                            )
MiniLabMkIIInputCodes.emplace_sysex(UserMidiCodes.INPUT,"OCTAVE_PLUS",
    SysexMessage(MiniLab2DeviceId,MiniLab2SysexCommandCodeOctavePlus,
                 {**MiniLab2SysexCommandParameterPressedReleased})
                            )
MiniLabMkIIInputCodes.emplace_sysex(UserMidiCodes.INPUT,"PAD_PAGE",
    SysexMessage(MiniLab2DeviceId,MiniLab2SysexCommandCodePadPage,
                 {**MiniLab2SysexCommandParameterPressedReleased})
                            )
MiniLabMkIIInputCodes.emplace_sysex(UserMidiCodes.INPUT,"MEMCHANGE",
    SysexMessage(MiniLab2DeviceId,MiniLab2SysexCommandCodeMemChange,
                 {**MiniLab2SysexCommandParameterMemChange}))


class ControlModel:
    """
    Represents a physical control on the device.
    """
    def __init__(self) -> None:
        self.is_relative = False    # If the control is relative.
        self.is_led = False         # If the control has an led.

        self.midi_messages : list[TargetedMidiMessage]= None    # The input midi messages this control may send.
        self.led_message = None     # The output midi or sysex message to set the led color.
        self.led_states : 'dict[str,bytes]'= {'OFF' : int_to_byte(0) ,'ON' : int_to_byte(127)}   # The states available of the led as bytes. Default is OFF/ON 0,127 (Ignored if no led)

    def __str__(self) -> str:
        return f"ControlModel({self.is_relative},\n{self.is_led},\n{self.midi_message},\n{self.led_message},\n{self.led_states})"


class ButtonModel(ControlModel):
    """
    Represents a physical button on the device.
    """
    def __init__(self) -> None:
        super().__init__()
        self.is_toggle = True       # If the button is a toggle button, false if hold button.
        self.is_aftertouch = False  # If the button supports aftertouch.
        self.is_led = False         # If the button has an led.
        self.midi_messages = [None,None,None]    # The input midi messages this button may send.
        self.pressed_message = None    # The input midi or sysex message representing this button being pressed.
        self.released_message = None    # The input midi or sysex message representing this button being released.
        self.held_message = None        # The input midi or sysex message representing this button being held. (Aftertouch val or None if not aftertouch)

        self.led_message = None                     # The output midi or sysex message to set the led color.
        self.led_states : 'dict[str,bytes]'= {'OFF' : int_to_byte(0) ,'ON' : int_to_byte(127)}   # The states available of the led as bytes. Default is OFF/ON 0,127 (Ignored if no led)

    def __str__(self) -> str:
        return f"ButtonModel({self.is_toggle},\n{self.is_aftertouch},\n{self.is_led},\n{self.pressed_message},\
            \n{self.released_message},\n{self.held_message},\n{self.led_message},\n{self.led_states})"

    def set_pressed_message(self,message):
        """
        Sets the pressed message for the button.

        Args:
            message (TargetedMidiMessage): The midi or sysex message representing this button being pressed.
        """
        self.pressed_message = message
        self.midi_messages[0] = message

    def set_released_message(self,message ):
        """
        Sets the released message for the button.

        Args:
            message (TargetedMidiMessage): The midi or sysex message representing this button being released.
        """
        self.released_message = message
        self.midi_messages[1] = message

    def set_held_message(self,message):
        """
        Sets the held message for the button.

        Args:
            message (TargetedMidiMessage): The midi or sysex message representing this button being held.
        """
        self.held_message = message
        self.midi_messages[2] = message


# FIXME: add copy method to UserMidiCodes to be able to copy the default codes.(no acces to copy Python module)
MINILAB2_CODES = DEFAULT_MIDAS_CODES

MINILAB2_CODES.emplace_sysex(
    UserMidiCodes.OUTPUT,
    "LED",
    SysexMessage(
        MiniLab2DeviceId,
        MiniLab2SysexCommandCodeLed,
        {**MiniLab2SysexCommandParameterLedId,**MiniLab2SysexCommandParameterLedColor}
        )
    )


MINILAB2_CODES.emplace_sysex(UserMidiCodes.INPUT,"SHIFT",
    SysexMessage(MiniLab2DeviceId,
                 MiniLab2SysexCommandCodeShift,
                 {**MiniLab2SysexCommandParameterPressedReleased})
                            )
MINILAB2_CODES.emplace_sysex(UserMidiCodes.INPUT,"OCTAVE_MINUS",
    SysexMessage(MiniLab2DeviceId,MiniLab2SysexCommandCodeOctaveMinus,
                  {**MiniLab2SysexCommandParameterPressedReleased})
                            )
MINILAB2_CODES.emplace_sysex(UserMidiCodes.INPUT,"OCTAVE_PLUS",
    SysexMessage(MiniLab2DeviceId,MiniLab2SysexCommandCodeOctavePlus,
                 {**MiniLab2SysexCommandParameterPressedReleased})
                            )
MINILAB2_CODES.emplace_sysex(UserMidiCodes.INPUT,"PAD_PAGE",
    SysexMessage(MiniLab2DeviceId,MiniLab2SysexCommandCodePadPage,
                 {**MiniLab2SysexCommandParameterPressedReleased})
                            )
MINILAB2_CODES.emplace_sysex(UserMidiCodes.INPUT,"MEMCHANGE",
    SysexMessage(MiniLab2DeviceId,MiniLab2SysexCommandCodeMemChange,
                 {**MiniLab2SysexCommandParameterMemChange}))


MINILAB2_BUTTON_SHIFT = ButtonModel()
MINILAB2_BUTTON_SHIFT.is_led = False # FIXME: Led set command for shift button not known.
MINILAB2_BUTTON_SHIFT.set_pressed_message(MINILAB2_CODES.get_sysex_message(UserMidiCodes.INPUT,"SHIFT").bind(MiniLabSysexButtonPressedValue))
MINILAB2_BUTTON_SHIFT.set_pressed_message(MINILAB2_CODES.get_sysex_message(UserMidiCodes.INPUT,"SHIFT").bind(MiniLabSysexButtonReleasedValue))

MINILAB2_BUTTON_PAD1C1 = ButtonModel()
MINILAB2_BUTTON_PAD1C1.is_aftertouch = True
MINILAB2_BUTTON_PAD1C1.set_pressed_message(MINILAB2_CODES.get_midi_message(UserMidiCodes.INPUT,"NOTE_ON").target(0,0))
MINILAB2_BUTTON_PAD1C1.set_released_message(MINILAB2_CODES.get_midi_message(UserMidiCodes.INPUT,"NOTE_OFF").target(0,0))
MINILAB2_BUTTON_PAD1C1.set_held_message(MINILAB2_CODES.get_midi_message(UserMidiCodes.INPUT,"NOTE_PRESSURE").target(0,0))

MINILAB2_BUTTON_PAD1C1.is_led = True
MINILAB2_BUTTON_PAD1C1.led_message = MINILAB2_CODES.get_sysex_message(UserMidiCodes.OUTPUT,"LED") # TODO: Bind partial parameters to sysex message.

MINILAB2_BUTTON_PAD1C1.led_states = {'NONE' : int_to_byte(0) ,
                                     'RED' : int_to_byte(1),
                                     'WHITE' : int_to_byte(127),
                                     'GREEN' : int_to_byte(4),
                                     'YELLOW' : int_to_byte(5),
                                     'BLUE' : int_to_byte(16),
                                     'CYAN' : int_to_byte(20),
                                     'PURPLE' : int_to_byte(17)}

def GENERATE_CUBIC_DICTIONARY(x,y,z,default_value = None,value_method = None):
    '''
        The value method is a method that takes in the x,y,z and returns a value based on the x,y,z.
            ex. value_method(x,y,z): return x+y+z
            If the value method is not provided, or returns None, the default value is used.
        Given a x,y and z width height and depth, generates a dictionary of
        none values with the keys being the value of x,y,z as a string seperated by .
        Orderded by x,y,z.
        Like so: 'x.y.z' : value
        Example:
            GENERATE_CUBIC_DICTIONARY(2,2,2) ->
            {
                0: {0: {0: 0, 1: 1},
                    1: {0: 2, 1: 3}},
                1: {0: {0: 4, 1: 5},
                    1: {0: 6, 1: 7}}
            }
    '''
    dictionary = {}
    for x_index in range(x):
        dictionary[str(x_index)] = {}
        for y_index in range(y):
            dictionary[str(x_index)][str(y_index)] = {}
            for z_index in range(z):
                if value_method is not None:
                    value = value_method(x_index,y_index,z_index)
                    if value is not None:
                        dictionary[str(x_index)][str(y_index)][str(z_index)] = value
                    else:
                        dictionary[str(x_index)][str(y_index)][str(z_index)] = default_value
                else:
                    dictionary[str(x_index)][str(y_index)][str(z_index)] = default_value
    return dictionary


def make_minilab2_pad_button_model(x,y,z) -> ButtonModel:
    '''
        Generates a pad button model for the minilab2.
        x,y,z are the x,y,z coordinates of the pad.
        The pad button model
        Pads 1-16: MidiNote(with aftertouch) 0-15 Note (Gate) ( On channel 16)
    '''
    if x != 0:
        raise ValueError(f"Invalid x value {x}. Minilab2 Midas adapter only supports 1 channel(x-value) for the pad buttons. See spec/Arturia/MiniLabMk2 folder for details.")

    model = ButtonModel()
    model.is_aftertouch = True
    model.pressed_message = MINILAB2_CODES.get_midi_message(UserMidiCodes.INPUT,"NOTE_ON").target(15,y*8 + z) # 2 Rows of 8 pads.
    model.released_message = MINILAB2_CODES.get_midi_message(UserMidiCodes.INPUT,"NOTE_OFF").target(15,y*8 + z)
    model.held_message = MINILAB2_CODES.get_midi_message(UserMidiCodes.INPUT,"NOTE_PRESSURE").target(15,y*8 + z)

    model.is_led = True
    model.led_message = MINILAB2_CODES.get_sysex_message(UserMidiCodes.OUTPUT,"LED") # TODO: Bind partial parameters to sysex message.
    model.led_states = {'NONE' : int_to_byte(0) ,
                        'RED' : int_to_byte(1),
                        'WHITE' : int_to_byte(127),
                        'GREEN' : int_to_byte(4),
                        'YELLOW' : int_to_byte(5),
                        'BLUE' : int_to_byte(16),
                        'CYAN' : int_to_byte(20),
                        'PURPLE' : int_to_byte(17)}
    return model



# Example usage:
MINILAB2_CONTROLS = {
    'BUTTONS': {
        'SYSTEM': {
            'SHIFT': MINILAB2_BUTTON_SHIFT#,
            #'OCTAVE_MINUS': MINILAB_BUTTON_OCTAVE_MINUS,
            #'OCTAVE_PLUS': MINILAB_BUTTON_OCTAVE_PLUS,
            #'PAD_PAGE': MINILAB_BUTTON_PAD_PAGE
        },
        'PADS': GENERATE_CUBIC_DICTIONARY(1,2,8,None,make_minilab2_pad_button_model),
    }
}

def match_control(nested_dictionary , bound_midi_command : BoundMidiMessage = None):
    '''
        Matches a bound midi command to a control.
        Returns the control and the midi command.
        If no control is found, returns None,None.

        Structure of a control dictionary is a nested dictionary with the final value being the control.
    '''
    matching_controls = []
    # 1.Recusively iterate nested dictionary of controls.
    for key,value in nested_dictionary.items():
        # 2. Check if the bound_midi_command matches the a command in the list of midi_commands for each control.
        #       All values in the nested dictionary are subclasses of the ControlModel class. which has a midi_messages list.
        if isinstance(value,ControlModel):
            for midi_message in value.midi_messages:
                if midi_message is not None and bound_midi_command is not None:
                    if midi_message.matches(bound_midi_command.status,bound_midi_command.port,bound_midi_command.note):
                        matching_controls.append((key,value))

        # 3. If the value is a dictionary, recusively call this function.
        elif isinstance(value,dict):
            matching_controls.extend(match_control(value,bound_midi_command))
        else:
            raise ValueError(f"Invalid value type {type(value)} for key {key} in control dictionary.")

    # 4. Return the list of matching controls as a key , value tuple, and the bound midi command
    # 4. If there are no matching controls, return None,None.
    if not matching_controls:
        return None,None
    else:
        return matching_controls




a = MddsType.t1[MddsType.byte]

class MDDS:
    '''
        Midas Daw Device Signal
    '''
    def __init__(self,timestamp : bytes,signal_type : bytes,source : bytes,destination : bytes,command_id : bytes,payload_description : bytes) -> None:
        self.timestamp = timestamp
        self.signal_type = signal_type
        self.source = source
        self.destination = destination
        self.command_id = command_id
        self.payload_description = payload_description
        self.payload = None

        def bind_payload(self,payload : bytes):
            self.payload = payload
            return self

        def update_timestamp(time : float):
            digit , fraction = float_to_2int32(time.monotonic())
            self.timestamp = int32_to_bytes(digit).join(int32_to_bytes(fraction))
            return self

def float_to_2int32(f):
    integer_part = int(f)
    fractional_part = int((f - integer_part) * 10**9)  # Adjusted for 4-byte int precision
    return integer_part, fractional_part

def int32_to_bytes(i):
    return struct.pack('i', i)

# Returns a tuple of 2 32-bit integers as bytes representing the digit and fraction of the time in seconds.
def monotonic_bytes():
    digit , fraction= float_to_2int32(time.monotonic())
    return int32_to_bytes(digit),int32_to_bytes(fraction)

def get_script_device_id():
    return device.getDeviceID()

#iterate_nested_dict(MINILAB2_CONTROLS,'MINILAB2')
def process_MDDS(mdds : MDDS):
    print(MDDS)
    if(mdds.command_id == midasstd.eCommand.script_init.value.command_id):
        print("Script Init")
        if(mdds.payload == get_script_device_id()):
            print("Script Init for this device")
        else:
            print("Script Init for another device")
            print("Script Init for device id: ",mdds.payload)
    pass
# EXAMPLE
#MINILAB2_CONTROLS['BUTTONS']['SYSTEM']['SHIFT'].pressed_message = MINILAB2_CODES.get_sysex_message(UserMidiCodes.INPUT,"SHIFT").bind(MiniLabSysexButtonPressedValue)
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
    '''
        Called when the script has been started.

        Version : 1
    '''
    print("OnInit")
    print("Device Name: ",MiniLab2DeviceId)
    print("Device Name: ",device.getDeviceID())
    print("Device Name: ",device.dispatchReceiverCount())

    mdds_input = MDDS(timestamp= monotonic_bytes(),
                      signal_type= midasstd.eStatus.daw_to_device.value,
                      source=midasstd.eDaw.flstudio.value,
                      destination=midasstd.eDestination.all_.value,
                      command_id=midasstd.eCommand.script_init.value.command_id,
                      payload_description=midasstd.eCommand.script_init.value.payload_description)
    mdds_input.bind_payload(device.get_script_device_id())

    process_MDDS(mdds_input)

    DawEventBase.make_daw_event(DawEventScriptInit,time.monotonic())

def OnDeInit():
    '''
        Called when the script has been stopped.

        Version : 1
    '''
    print("OnDeInit")

    mdds_input = MDDS(timestamp= monotonic_bytes(),
                      signal_type= midasstd.status.daw_to_device.value,
                      source=midasstd.daw_id.flstudio.value,
                      destination=midasstd.eDestination.all_.value,
                      command_id=midasstd.command_id.script_exit.value.command_id,
                      payload_description=midasstd.command_id.script_init.value.payload_description)
    mdds_input.payload = device.get_script_device_id()


    DawEventBase.make_daw_event(DawEventScriptDeInit,time.monotonic())

def OnMidiMsg(eventData):
    '''
        Called first when a MIDI message is received.
        Set the event's handled property to True if you don't want further processing -
        (only raw data is included here: handled, timestamp, status, data1, data2, port, sysex, pmeflags)

        Subsequent events are called for specific MIDI messages (OnNoteOn, OnNoteOff, OnControlChange, OnProgramChange, OnPitchBend, OnKeyPressure, OnChannelPressure)
        NOTE: We will ignore the subsequent event callbacks for now.They are redundant with the OnMidiMsg callback.

        eventData parameter analysis:
        [INSIGNIFICANT]
            eventData.timestamp     : int   [INSIGNIFICANT] The timestamp of the event. Not reported by the DAW correctly.
                FIXME: Report this to the DAW devs.
            eventData.status        : int   [INSIGNIFICANT] The status of the event. Offset by the channel. Use eventData.midiId(status) to get the actual status.
            eventData.port          : int   [INSIGNIFICANT] The port of the event. Use eventData.midiChan(port) to get the actual port.
                FIXME: Not reported by the DAW correctly for all devices. Report this to the DAW devs.
            eventData.note          : int   [INSIGNIFICANT] The note of the event. Same as eventData.data1(note).
            eventData.velocity      : int   [INSIGNIFICANT] The velocity of the event. Same as eventData.data2(value/velocity/pressure).
            eventData.pressure      : int   [INSIGNIFICANT] The pressure of the event? Same as eventData.data1(note).
                FIXME: Makes no sense.
            eventData.progNum       : int   [INSIGNIFICANT] The program number of the event. Same as eventData.data1(note).
                FIXME: Makes no sense.
            eventData.controlNum    : int   [INSIGNIFICANT] The control number of the event. Same as eventData.data1(note).
                FIXME: Makes no sense.
            eventData.controlVal    : int   [INSIGNIFICANT] The control value of the event. Same as eventData.data2(value/velocity/pressure).
            eventData.pitchBend     : int   [INSIGNIFICANT] The pitch bend of the event. Reports 0 when pitch bend is at minimum value else report 1.
                FIXME: Makes no sense.
            eventData.sysex         : bytes [INSIGNIFICANT] The sysex data of the event. Does not display midi sysex for midi commands.
            eventData.isIncrement   : int   [INSIGNIFICANT] The increment of the event. No clue what this means. Always report 1.
            eventData.res           : float [INSIGNIFICANT] The resolution of the event. No clue what this means. Always reports 0.0078125.
            eventData.inEv          : int   [INSIGNIFICANT] The input event of the event. No clue what this means. Always reports 0.
            eventData.outEv         : int   [INSIGNIFICANT] The output event of the event. No clue what this means. Always reports 0.
            eventData.midiChanEx    : int   [INSIGNIFICANT] A unique identifier for the channel? Diffrent accross devices for the same commands.
                FIXME: Makes no sense.
        [SIGNIFICANT]
            eventData.handled : bool [SIGNIFICANT][REQUIRED] Tells the DAW if the event has been handled. If True, the DAW will not process the event further.
            eventData.data1 : int [SIGNIFICANT] The note of the event.
            eventData.data2 : int [SIGNIFICANT] The value/velocity/pressure of the event.
            eventData.midiId : int [SIGNIFICANT][REQUIRED] The actual status of the event. Use this to determine the midi command.
            eventData.midiChan : int [SIGNIFICANT][REQUIRED] The actual port of the event. Use this to determine the midi command.
            eventData.pmeFlags : int [SIGNIFICANT][REQUIRED] The PME flags of the event. Used to check if the event is coming from the device or the DAW.
                FIXME: Documentation says var name is pmeflags. Report this to the DAW devs.


        Therefore the significant values are:
        eventData.handled
        eventData.midiId ( Midi status)
        eventData.midiChan (Midi channel)
        eventData.data1 (Midi note)
        eventData.data2 (Midi value/velocity/pressure)

        Version : 1
    '''

    # If the sysex data is None, then we need to set it to an empty byte string for type-safety.
    # NOTE:(It seems to always be none for midi commands)
    # TODO: Generate sysex from midi data.
    if eventData.sysex is None:
        actual_sysex_data = b''
    else:
        actual_sysex_data = eventData.sysex

    DawEventBase.make_daw_event(DawEventDeviceMidiIn,time.monotonic(),[eventData.handled,
                                                                       time.monotonic(),
                                                                       eventData.midiId,
                                                                       eventData.midiChan,
                                                                       eventData.data1,
                                                                       eventData.data2,
                                                                       eventData.midiChanEx,
                                                                       actual_sysex_data])

    # Compare incoming status, port, and note agaisnt the current active adapter's command map and find a match.
    # Determine the command source type (Internal,Button, Knob(infinite abs controller), Fader(finite abs controller), Relative(infinite rel controller))

    name, command = MINILAB2_CODES.matches(eventData.midiId,eventData.midiChan,eventData.data1)
    # if there is a matcht then we bind the command to the event channel and note.
    if name is not None:
        bound_command = command.bind(eventData.midiChan,eventData.data1,eventData.data2)


    # Use the targeted midi message to determine the source control of the command based on the device adapter command dictionary.
    # The adapter dictionary is a names and a device object model which contains info about the possible midi messages these buttons can send.
    # We will return a list of all buttons that can send this midi message. It will be implied that they are the sender of the command.
    # If there is no match then we ignore the event.


    print("Matches:",name,command)
    # if this is a button command then initiate search for matching button in the active adapter's control dictionary.
    print(match_control(MINILAB2_CONTROLS,bound_command))


    #print("OnMidiMsg",eventData.status,eventData.port,eventData.note)
    #print("DEFAULT NOTE ON INTERP MATCHES:",DEFAULT_NOTE_ON.matches(eventData.status,eventData.port,eventData.note))
    #print("MINILAB NOTE OFF INTERP MATCHES:",DEFAULT_NOTE_OFF.matches(eventData.status,eventData.port,eventData.note))


def OnSysEx(eventData):
    '''
        Called for note sysex messages  recieved from the device.
        Version : 1
    '''
    print("OnSysEx")
    DawEventBase.make_daw_event(DawEventDeviceSysexIn,time.monotonic(),[eventData.sysex])

def OnMidiOutMsg(eventData):
    '''
        Called for short MIDI out messages sent from MIDI Out plugin - (event properties are limited to: handled, status, data1, data2, port, midiId, midiChan, midiChanEx)
    '''
    print("OnMidiOutMsg")
    DawEventBase.make_daw_event(DawEventDawMidiIn,time.monotonic(),[eventData.handled,eventData.status,eventData.data1,eventData.data2,eventData.port,eventData.midiId,eventData.midiChan,eventData.midiChanEx])

def OnIdle():
    '''
        Called from time to time. Can be used to do some small tasks, mostly UI related. For example: update activity meters.
    '''
    #print("OnIdle")
    DawEventBase.make_daw_event(DawEventIdle,time.monotonic())

def OnProjectLoad(status):
    '''
        Called when project is loaded.

        Version : 16
    '''
    print("OnProjectLoad")
    DawEventBase.make_daw_event(DawEventProjectLoaded,time.monotonic(),[status])

def OnRefresh(flags):
    '''
        Called when something changed that the script might want to respond to.
    '''
    print("OnRefresh")
    #DawEventBase.make_daw_event(DawEventRefresh,time.monotonic(),[flags])

def OnDoFullRefresh():
    '''
        Same as OnRefresh, but everything should be updated.

        Version : 1
    '''
    print("OnDoFullRefresh")
    DawEventBase.make_daw_event(DawEventFullRefresh,time.monotonic())

def OnUpdateBeatIndicator(value):
    '''
        Called when the beat indicator has changes - "value" can be off = 0, bar = 1 (on), beat = 2 (on)
    '''
    print("OnUpdateBeatIndicator")
    DawEventBase.make_daw_event(DawEventBeatIndicatorUpdate,time.monotonic(),[value])

def OnDisplayZone():
    '''
        Called when playlist zone changed

        Version : 1
    '''
    print("OnDisplayZone")
    DawEventBase.make_daw_event(DawEventDisplayZoneUpdate,time.monotonic())

def OnUpdateLiveMode(lastTrack):
    '''
        Called when something about performance mode has changed.

        Version : 1
    '''
    print("OnUpdateLiveMode")
    DawEventBase.make_daw_event(DawEventLiveModeUpdate,time.monotonic(),[lastTrack])

def OnDirtyMixerTrack(index):
    '''
    Called on mixer track(s) change, 'index' indicates track index of track that changed or -1 when all tracks changed
        collect info about 'dirty' tracks here but do not handle track(s) refresh, wait for OnRefresh event with HW_Dirty_Mixer_Controls flag

        Version : 1
    '''
    print("OnDirtyMixerTrack")
    DawEventBase.make_daw_event(DawEventMixerTrackChanged,time.monotonic(),[index])

def OnDirtyChannel(index,flag):
    '''
        Called on channel rack channel(s) change, 'index' indicates channel that changed or -1 when all channels changed
        collect info about 'dirty' channels here but do not handle channels(s) refresh, wait for OnRefresh event with HW_ChannelEvent flag

        OnDirtyChannel flags
        Parameter	Value	Documentation
        CE_New	0	new channel is added
        CE_Delete	1	channel deleted
        CE_Replace	2	channel replaced
        CE_Rename	3	channel renamed
        CE_Select	4	channel selection changed

        Version : 16
    '''
    print("OnDirtyChannel")
    DawEventBase.make_daw_event(DawEventChannelChanged,time.monotonic(),[index,flag])

def OnFirstConnect():
    '''
        Called when device is connected for the first time (ever)

        Version : 17
    '''
    print("OnFirstConnect")
    DawEventBase.make_daw_event(DawEventDeviceFirstConnect,time.monotonic())

def OnUpdateMeters():
    '''
        Called when peak meters needs to be updated
        call device.setHasMeters() in onInit to use this event!

        Version : 1
    '''
    #print("OnUpdateMeters")
    #DawEventBase.make_daw_event(DawEventRequestingUpdateMeters,time.monotonic())

def OnWaitingForInput():
    '''
        Called when FL Studio is set in waiting mode

        Version : 1
    '''
    print("OnWaitingForInput")
    DawEventBase.make_daw_event(DawEventRequestingInput,time.monotonic())

def OnSendTempMsg(message,duration):
    '''
        Called when hint message (to be displayed on controller display) is sent to the controller
        duration of message is in ms

        Version : 1
    '''
    print("OnSendTempMsg")
    DawEventBase.make_daw_event(DawEventSendingHintToDevice,time.monotonic(),[message,duration])



# map of the app controls associated with their device controls.
# eg. App.controls['DO_MAGICAL_STUFF_IN_THE_APP'] = DeviceAdapter.controls['BUTTONS']['SYSTEM']['SHIFT']
#

#

# class AppControl :
#     def __init__(self) -> None:
#         self.bound_device_control : 'DeviceControl' = None
#         self.last_reported_value = None

#     def onActive(self):
#         '''
#             Called when the bound device control is active.
#             When value is not changed but controller is active. This will still be called.
#         '''
#         pass

#     def onPress(self):
#         '''
#             Called when the bound device control is pressed.
#         '''
#         pass
#     def onRelease(self):
#         '''
#             Called when the bound device control is released.
#         '''
#         pass
#     def onHold(self):
#         '''
#             Called when the bound device control is held.
#         '''
#         pass

#     def onValueChange(self):
#         '''
#             Called when the bound device control value changes.
#             For buttons this will be the last reported onPress, onRelease, onHold value.
#             For knobs this will be the last reported value.
#         '''
#         pass

#     def isLed(self):
#         '''
#             Returns true if the bound device control has an led.
#         '''
#         pass
#     def getLedStates(self):
#         '''
#             Returns the available led states for the bound device control.
#         '''
#         pass
#     def setLed(self,led_color : str,led_value : int):
#         '''
#             Calls the appropriate led message for the bound device control.
#         '''
#         pass



# class DeviceAdapter:
#     """
#     The base class for a device adapter.
#     """
#     def __init__(self,device_name : str,device_id : bytes) -> None:
#         self.required_device_id = device_id
#         self.codes : UserMidiCodes() = DEFAULT_MIDAS_CODES
#         self.controls : dict[str,] = {}

class MddsMapEntry:
    def __init__(self) -> None:
        self.name = None
        self.signal_type = None
        self.source_mask = None
        self.destination_mask = None
        self.control = None # The control id.
        self.control_name = None # The control name.
        self.command = None # One of the predefined mdds commands.
        self.command_name = None
        self.message_name = None # The name of the underlying midi message.
        self.payload_mask = None # A mask for the payload.
        self.custom_command = None # Data for mdds command. Only used if mdds_command is None.

    def __str__(self) -> str:
        return "MddsMapEntry: " + str(self.__dict__)
    def __repr__(self) -> str:
        return self.__str__()

def generate_mdds_map(device_name,device_id,device_controls,device_controls_messages):
    ''' Generates a mdds map from the device id and controls messages '''
    mdds_map = {}
        # For each control in device controls.
        # Get the input and output messages for the control.
        # Add the control to the mdds map.
    for control_name,control_id in device_controls.items():
        control_input_messages = device_controls_messages[0][control_id]
        # for each input message in the control.
        # add the corresponding mdds message to the key of the device plus device control.
        for input_message_name,input_message in control_input_messages.items():
            midi_status = input_message[0]
            if midi_status == mdds.eDefaultMidiStatus.system_exclusive: #sysex message
                pass
            else: #midi message
                midi_port = input_message[1]
                midi_note = input_message[2]
                midi_value = input_message[3]

                mdds_entry = MddsMapEntry()
                mdds_entry.signal_type = mdds.eStatus.device_to_device.value # pylint: disable=no-member
                mdds_entry.source_mask = device_id

                mdds_entry.control = control_id
                mdds_entry.control_name = control_name

                mdds_entry.message_name = input_message_name
                mdds_entry.payload_mask = (midi_status,midi_port,midi_note,midi_value)

                # Check for control change messages.
                if midi_status == mdds.eDefaultMidiStatus.control_change or \
                    midi_status == mdds.eDefaultMidiStatus.aftertouch:
                    mdds_entry.command_name = mdds.eCommandName.moved_x + device_name + "_" + input_message_name
                    mdds_entry.command = mdds.eCommand.moved_x

                elif midi_status == mdds.eDefaultMidiStatus.note_on:
                    mdds_entry.command_name = mdds.eCommandName.pressed + device_name + "_" + input_message_name
                    mdds_entry.command = mdds.eCommand.pressed
                elif midi_status == mdds.eDefaultMidiStatus.note_off:
                    mdds_entry.command_name = mdds.eCommandName.released + device_name + "_" + input_message_name
                    mdds_entry.command = mdds.eCommand.released
                elif midi_status == mdds.eDefaultMidiStatus.pitch_bend:
                    mdds_entry.command_name = mdds.eCommandName.bent + device_name + "_" + input_message_name
                    mdds_entry.command = mdds.eCommand.bent
                elif midi_status == mdds.eDefaultMidiStatus.channel_aftertouch:
                    mdds_entry.command_name = mdds.eCommandName.held_x + device_name + "_" + input_message_name
                    mdds_entry.command = mdds.eCommand.held_x
                else: # its a user command for now raise an error.
                    raise ValueError("Unknown Midi Status")

                mdds_map[device_name + "_" + input_message_name] = mdds_entry

    return mdds_map

for mddsmsg in generate_mdds_map(NAME,ID,Controls,ControlsMessages).items():
    print(mddsmsg)

SampleDeviceMDDSMessageMap = generate_mdds_map(NAME,ID,Controls,ControlsMessages)
# Given a user defined "Event" name, return the corresponding mdds map entries.
# Given a mdds map entry, return the corresponding user defined "Event" name.
SampleApplicationControlMap = {

    # Example Knob mapping.
    "Knob1ValueChange" : ("Minilabmk2_Knob1_ControlChange", [None,1,None,None]), # Mask for the payload. Second byte is the port.

    # Example Sysex mapping.
    "ShiftButton" : ("Minilabmk2_ShiftButton_SysexNoteState", [None,None]) # Mask for the payload.

}


def get_mdds(status, port, note, val, sysex):
    """ Returns the mdds map entry name for the given midi message or sysex message. """
    for mdds_name, mdds_entry in SampleDeviceMDDSMessageMap.items():
        if mdds_entry == (status, port, note, val, sysex):
            return mdds_name
    return None




def get_mdds_from_name(name):
    """ Returns the mdds map entry for the given name. """
    return SampleDeviceMDDSMessageMap[name]

def get_mdds_from_name_with_mask(name,mask):
    # The mask is a list of values to match against the payload.
    # If the mask is None then the value is ignored.
    # The mask is in the order of the payload.
    mdds_entry = get_mdds_from_name(name)
    if mdds_entry is None:
        return None
    if mdds_entry.payload_mask is None:
        return mdds_entry
    if len(mdds_entry.payload_mask) != len(mask):
        return None
    for i in range(len(mask)):
        if mask[i] is not None and mask[i] != mdds_entry.payload_mask[i]:
            return None
    return mdds_entry


def get_app_event_from_mdds(mdds_name):
    """ Returns the application event name for the given mdds map entry. """
    return SampleApplicationControlMap[mdds_name][0]


def get_app_event_from_mdds_with_mask(mdds_name,mask):
    """ Returns the application event name for the given mdds map entry and a mask. """
    mdds_entry = get_mdds_from_name_with_mask(mdds_name,mask)
    if mdds_entry is None:
        return None
    return get_app_event_from_mdds(mdds_name)

def process_app_events(event : str, payload : list = None):
    """ Returns the mdds map entry name for the given midi message or sysex message. """
    if event is 'Knob1ValueChanged':
        # Extract payload data based on the corresponding mdds commman's payload description.
        # The payload is a list of values to match against the payload.
        # If the payload is None then the value is ignored.
        # The payload is in the order of the payload.
        # The payload is the second element of the SampleApplicationControlMap entry.
        # The first element is the corresponding mdds map entry name.
        # The third element is the mdds command name.
        # The fourth element is the mdds command.
        # The fifth element is the mdds message name.
        # The sixth element is the mask for the payload.
        app_map.get_payload_desc(event).extract_data(payload)['__value__']  = 127:

def process_app_events_internal(status, port, note, val, sysex):
    return process_app_events(get_app_event_from_mdds(get_mdds(status, port, note, val, sysex)))
