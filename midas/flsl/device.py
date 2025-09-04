import playlist as flsiPlaylist
import channels as flsiChannels
import mixer as flsiMixer
import patterns as flsiPatterns
import arrangement as flsiArrangement
import ui as flsiUi
import transport as flsiTransport
import device as flsiDevice
import general as flsiGeneral
import launchMapPages as flsiLaunchMapPages
import midi	as flsiMidi # The script will use MIDI functions.  

# Device module
# The Device module handles MIDI devices connected to the FL Studio MIDI interface.
# You can send messages to the output interface, retrieve linked control values, etc.
# MIDI scripts assigned to an input interface can be mapped (linked) to an Output interface via the Port Number.
# With mapped (linked) output interfaces, scripts can send MIDI messages to output interfaces using midiOut*** messages.
def is_assigned() -> int:
    """
    Returns True if (linked) output interface is assigned.

    Returns:
    - int: Result of the assignment check.
    """
    return flsiDevice.isAssigned()

def get_port_number() -> int:
    """
    Returns the interface port number or -1 when the port number is not assigned.
    This is the same number as the interface port number set in FL Studio MIDI settings.

    Returns:
    - int: Interface port number.
    """
    return flsiDevice.getPortNumber()

def get_name() -> int:
    """
    Returns the device name.

    Returns:
    - int: Device name.
    """
    return flsiDevice.getName()

def midi_out_msg(message: int) -> None:
    """
    Send a MIDI message to the (linked) output interface.
    The 'message' parameter holds the value to be sent, with the channel and command in the lower byte
    and the first and second data values in the next two bytes.

    Parameters:
    - message (int): MIDI message to be sent.

    Returns:
    - None
    """
    return flsiDevice.midiOutMsg(message)

def midi_out_msg_params(midi_id: int, channel: int, data1: int, data2: int) -> None:
    """
    Send a MIDI message to the (linked) output interface (alternative version with separate parameters).

    Parameters:
    - midi_id (int): MIDI identifier.
    - channel (int): MIDI channel.
    - data1 (int): First data value.
    - data2 (int): Second data value.

    Returns:
    - None
    """
    return flsiDevice.midiOutMsg(midi_id, channel, data1, data2)

def midi_out_new_msg(slot_index: int, message: int) -> None:
    """
    Send a MIDI message to the (linked) output interface, but only if the value has changed.
    The 'slot_index' is a value chosen by the caller, it should be the same as it was for the previous message
    that should be compared with. The 'message' holds the value to be sent.

    Parameters:
    - slot_index (int): Index value for comparison.
    - message (int): MIDI message to be sent.

    Returns:
    - None
    """
    return flsiDevice.midiOutNewMsg(slot_index, message)

def midi_out_sysex(message: str) -> None:
    """
    Send a SYSEX message to the (linked) output interface.

    Parameters:
    - message (str): SYSEX message to be sent.

    Returns:
    - None
    """
    return flsiDevice.midiOutSysex(message)

def send_msg_generic(id: int, message: str, last_msg: str, offset: int = 0) -> str:
    """
    Send a text string as a SYSEX message to the (linked) output interface.
    'id' holds the first 6 bytes of the message (starting with 0xF0). The end value 0xF7 is added automatically.
    'message' is the text to send, 'last_msg' is the string returned by the previous call to this function.
    The function returns the updated 'last_msg'.

    Parameters:
    - id (int): First 6 bytes of the message.
    - message (str): Text to send.
    - last_msg (str): String returned by the previous call.
    - offset (int): Offset value. Default is 0.

    Returns:
    - str: Updated 'last_msg'.
    """
    return flsiDevice.sendMsgGeneric(id, message, last_msg, offset)

# Control events

def find_event_id(control_id: int, flags: int = []) -> int:
    """
    Returns eventID for controlId or REC_InvalidID when nothing is linked to this control.
    'flags' can be one of the: FEID_Flags_Skip_Unsafe = 1 (skip unsafe (using formula) links).

    Parameters:
    - control_id (int): Control ID.
    - flags (int): Flags value. Default is an empty list.

    Returns:
    - int: Resulting eventID.
    """
    return flsiDevice.findEventID(control_id, flags)

def get_linked_value(event_id: int) -> float:
    """
    Returns the normalized value of the linked control via eventID.
    To get control eventId, use the findEventID function. Result is -1 if there is no linked control.

    Parameters:
    - event_id (int): Event ID.

    Returns:
    - float: Normalized value.
    """
    return flsiDevice.getLinkedValue(event_id)

def get_linked_value_string(event_id: int) -> str:
    """
    Returns the text value of linked control via eventID.
    To get control eventId, use the findEventID function. Result is ERR_PLUGINNOTVALID if there is no linked control.

    Parameters:
    - event_id (int): Event ID.

    Returns:
    - str: Text value.
    """
    return flsiDevice.getLinkedValueString(event_id)

def get_linked_channel(event_id: int) -> int:
    """
    Returns the MIDI channel number for linked control via eventID.
    To get control eventId, use the findEventID function. Result is -1 if there is no linked control.

    Parameters:
    - event_id (int): Event ID.

    Returns:
    - int: MIDI channel number.
    """
    return flsiDevice.getLinkedChannel(event_id)

def get_linked_param_name(event_id: int) -> str:
    """
    Returns the parameter name of the control linked via eventID.
    To get control eventId, use the findEventID function. Result is ERR_PLUGINNOTVALID if there is no linked control.

    Parameters:
    - event_id (int): Event ID.

    Returns:
    - str: Parameter name.
    """
    return flsiDevice.getLinkedParamName(event_id)

def get_linked_info(event_id: int) -> int:
    """
    Returns information about the linked control via eventID.
    To get control eventId, use the findEventID function. Result is -1 if there is no linked control,
    otherwise, the result is one or more of the constants.

    Parameters:
    - event_id (int): Event ID.

    Returns:
    - int: Information about the linked control.
    """
    return flsiDevice.getLinkedInfo(event_id)

def link_to_last_tweaked(control_index: int, channel: int, global_: int, event_id: int) -> int:
    """
    This function will create a regular (or global) controller link for the last tweaked parameter.
    Set optional eventID to assign link to a specific control instead of the last tweaked control.
    The function returns (0) on success, (1) when nothing was tweaked,

 or (2) when the control is in use.

    Parameters:
    - control_index (int): Control index.
    - channel (int): Channel value.
    - global_ (int): Global value.
    - event_id (int): Event ID.

    Returns:
    - int: Result of the linking process.
    """
    return flsiDevice.linkToLastTweaked(control_index, channel, global_, event_id)

def get_device_id() -> bytes:
    """
    Returns the ID of the device, which is the identifying component of its response to a universal device enquiry Sysex message.
    Note that this does not include the Sysex header (0xF0, 0x7E, 0x01, 0x06, 0x02), or the ending byte (0xF7).
    Also note that for many devices, it will also contain the firmware version, meaning that you should may wish to ignore
    the final 4 bytes of the response.

    Returns:
    - bytes: Device ID.
    """
    return flsiDevice.getDeviceID()

# Refresh thread

def create_refresh_thread() -> None:
    """
    Start a threaded refresh of the entire MIDI flsiDevice.

    Returns:
    - None
    """
    return flsiDevice.createRefreshThread()

def destroy_refresh_thread() -> None:
    """
    Stop a previously started threaded refresh.

    Returns:
    - None
    """
    return flsiDevice.destroyRefreshThread()

def full_refresh() -> None:
    """
    Trigger a previously started threaded refresh - If there is none, the refresh is triggered immediately.

    Returns:
    - None
    """
    return flsiDevice.fullRefresh()

# Helpers

def is_double_click(index: int) -> int:
    """
    Returns True if the function was called with the same index shortly before, indicating a double click.

    Parameters:
    - index (int): Index value.

    Returns:
    - int: Result of the double click check.
    """
    return flsiDevice.isDoubleClick(index)

def set_has_meters() -> None:
    """
    Use this in OnInit event to tell FL Studio device use peak meters.

    Returns:
    - None
    """
    return flsiDevice.setHasMeters()

def base_track_select(index: int, step: int) -> None:
    """
    Base track selection (for control surfaces). Set step to MaxInt for reset.

    Parameters:
    - index (int): Index value.
    - step (int): Step value.

    Returns:
    - None
    """
    return flsiDevice.baseTrackSelect(index, step)

def hardware_refresh_mixer_track(index: int) -> None:
    """
    Let FL Studio dispatch OnDirtyMixerTrack event to all MIDI devices. Use index = -1 for all tracks.

    Parameters:
    - index (int): Index value.

    Returns:
    - None
    """
    return flsiDevice.hardwareRefreshMixerTrack(index)

# Dispatching between devices

def dispatch(ctrl_index: int, message: int, sysex: bytes) -> None:
    """
    Dispatch midi message (or sysex) to the controller specified by ctrlIndex.
    Receiver (script) must define sender(s) inside script: # receiveFrom="Sender name".

    Parameters:
    - ctrl_index (int): Control index.
    - message (int): MIDI message.
    - sysex (bytes): SYSEX message.

    Returns:
    - None
    """
    return flsiDevice.dispatch(ctrl_index, message, sysex)

def dispatch_receiver_count() -> int:
    """
    Returns the number of available receivers.

    Returns:
    - int: Number of receivers.
    """
    return flsiDevice.dispatchReceiverCount()

def dispatch_get_receiver_port_number(ctrl_index: int) -> int:
    """
    Returns the port number of the receiver specified by ctrlIndex.

    Parameters:
    - ctrl_index (int): Control index.

    Returns:
    - int: Port number of the receiver.
    """
    return flsiDevice.dispatchGetReceiverPortNumber(ctrl_index)

def set_master_sync(value: int) -> None:
    """
    Toggle (value = 1 to enable, 0 to disable) send master synch for the current flsiDevice.

    Parameters:
    - value (int): Value to toggle.

    Returns:
    - None
    """
    return flsiDevice.setMasterSync(value)

def get_master_sync() -> int:
    """
    Returns 'send master synch' state for the current device (1 = enabled).

    Returns:
    - int: State of master synch.
    """
    return flsiDevice.getMasterSync()