import playlist as flsiPlaylist
import channels as flsiChannels
import mixer as flsiMixer
import patterns as flsiPatterns
import arrangement as flsiArrangement
import ui as flsiUi
import transport as flsiTransport
import general as flsiGeneral
import launchMapPages as flsiLaunchMapPages
import device as flsiDevice
import plugins as flsiPlugins


# same as import midi
import flsiMidi as flsiMidi 
 # same as import utils
import flsiUtils as flsiUtils 


# Types
class EventDataType:
    """
    Type representing MIDI event data.

    Attributes:
    - handled (bool, read/write): Set to True to stop event propagation.
    - timestamp (time, read): Timestamp of the event.
    - status (int, read/write): MIDI status.
    - data1 (int, read/write): MIDI data1.
    - data2 (int, read/write): MIDI data2.
    - port (int, read): MIDI port.
    - note (int, read/write): MIDI note number.
    - velocity (int, read/write): MIDI velocity.
    - pressure (int, read/write): MIDI pressure.
    - progNum (int, read): MIDI program number.
    - controlNum (int, read): MIDI control number.
    - controlVal (int, read): MIDI control value.
    - pitchBend (int, read): MIDI pitch bend value.
    - sysex (bytes, read/write): MIDI sysex data.
    - isIncrement (bool, read/write): MIDI increment state.
    - res (float, read/write): MIDI resolution.
    - inEv (int, read/write): Original MIDI event value.
    - outEv (int, read/write): MIDI event output value.
    - midiId (int, read/write): MIDI ID.
    - midiChan (int, read/write): MIDI channel (0 based).
    - midiChanEx (int, read/write): Extended MIDI channel.
    - pmeflags (int, read): MIDI pmeflags.
    """
    def __init__(self):
        """
        Initialize eventData with default values set to None.
        """
        self.handled = None
        self.timestamp = None
        self.status = None
        self.data1 = None
        self.data2 = None
        self.port = None
        self.note = None
        self.velocity = None
        self.pressure = None
        self.progNum = None
        self.controlNum = None
        self.controlVal = None
        self.pitchBend = None
        self.sysex = None
        self.isIncrement = None
        self.res = None
        self.inEv = None
        self.outEv = None
        self.midiId = None
        self.midiChan = None
        self.midiChanEx = None
        self.pmeflags = None

# Script events - Callbacks called by FL Studio Python Bridge.
# These are reserved keywords in the global namespace.
# Override a callback to implement your custom script functionality.

# Event: OnInit
def on_init():
    """
    Called when the script has been started.
    """
    pass

# Event: OnDeInit
def on_de_init():
    """
    Called before the script will be stopped.
    """
    pass

# Event: OnMidiIn
def on_midi_in(event_data):
    """
    Called first when a MIDI message is received.
    Set the event's handled property to True if you don't want further processing -
    (only raw data is included here: handled, timestamp, status, data1, data2, port, sysex, pmeflags)
    Use this event for filtering, use OnMidiMsg event for actual processing.
    """
    pass

# Event: OnMidiMsg
def on_midi_msg(event_data):
    """
    Called for all MIDI messages that were not handled by OnMidiIn.
    """
    pass

# Event: OnSysEx
def on_sysex(event_data):
    """
    Called for note sysex messages that were not handled by OnMidiIn.
    """
    pass

# Event: OnNoteOn
def on_note_on(event_data):
    """
    Called for note on messages that were not handled by OnMidiMsg.
    """
    pass

# Event: OnNoteOff
def on_note_off(event_data):
    """
    Called for note off messages that were not handled by OnMidiMsg.
    """
    pass

# Event: OnControlChange
def on_control_change(event_data):
    """
    Called for CC messages that were not handled by OnMidiMsg.
    """
    pass

# Event: OnProgramChange
def on_program_change(event_data):
    """
    Called for program change messages that were not handled by OnMidiMsg.
    """
    pass

# Event: OnPitchBend
def on_pitch_bend(event_data):
    """
    Called for pitch bend change messages that were not handled by OnMidiMsg.
    """
    pass

# Event: OnKeyPressure
def on_key_pressure(event_data):
    """
    Called for key pressure messages that were not handled by OnMidiMsg.
    """
    pass

# Event: OnChannelPressure
def on_channel_pressure(event_data):
    """
    Called for channel pressure messages that were not handled by OnMidiMsg.
    """
    pass

# Event: OnMidiOutMsg
def on_midi_out_msg(event_data):
    """
    Called for short MIDI out messages sent from the MIDI Out plugin -
    (event properties are limited to: handled, status, data1, data2, port, midiId, midiChan, midiChanEx)
    """
    pass

# Event: OnIdle
def on_idle():
    """
    Called from time to time. Can be used to do some small tasks, mostly UI related.
    For example: update activity meters.
    """
    pass

# Event: OnProjectLoad
def on_project_load(status):
    """
    Called when the project is loaded.
    """
    pass

# Event: OnRefresh
def on_refresh(flags):
    """
    Called when something changed that the script might want to respond to.
    """
    pass

# Event: OnDoFullRefresh
def on_do_full_refresh():
    """
    Same as OnRefresh, but everything should be updated.
    """
    pass

# Event: OnUpdateBeatIndicator
def on_update_beat_indicator(value):
    """
    Called when the beat indicator has changed - "value" can be off = 0, bar = 1 (on), beat = 2 (on).
    """
    pass

# Event: OnDisplayZone
def on_display_zone():
    """
    Called when the playlist zone changed.
    """
    pass

# Event: OnUpdateLiveMode
def on_update_live_mode(last_track):
    """
    Called when something about performance mode has changed.
    """
    pass

# Event: OnDirtyMixerTrack
def on_dirty_mixer_track(index):
    """
    Called on mixer track(s) change, 'index' indicates track index of the track that changed
    or -1 when all tracks changed.
    Collect info about 'dirty' tracks here but do not handle track(s) refresh,
    wait for OnRefresh event with HW_Dirty_Mixer_Controls flag.
    """
    pass

# Event: OnDirtyChannel
def on_dirty_channel(index, flag):
    """
    Called on channel rack channel(s) change, 'index' indicates the channel that changed
    or -1 when all channels changed.
    Collect info about 'dirty' channels here but do not handle channels(s) refresh,
    wait for OnRefresh event with HW_ChannelEvent flag.
    """
    pass

# Event: OnFirstConnect
def on_first_connect():
    """
    Called when the device is connected for the first time (ever).
    """
    pass

# Event: OnUpdateMeters
def on_update_meters():
    """
    Called when peak meters need to be updated.
    Call device.setHasMeters() in OnInit to use this event!
    """
    pass

# Event: OnWaitingForInput
def on_waiting_for_input():
    """
    Called when FL Studio is set in waiting mode.
    """
    pass

# Event: OnSendTempMsg
def on_send_temp_msg(message, duration):
    """
    Called when the hint message (to be displayed on the controller display) is sent to the controller.
    Duration of the message is in ms.
    """
    pass


# FL Studio Python Bridge Callbacks

# FL Studio Python Bridge Overload OnInit()
def onInit():
    on_init()

# FL Studio Python Bridge Overload OnDeInit()
def onDeInit():
    on_de_init()

# FL Studio Python Bridge Overload OnMidiIn(eventData)
def onMidiIn(eventData):
    on_midi_in(eventData)

# FL Studio Python Bridge Overload OnMidiMsg(eventData)
def onMidiMsg(eventData):
    on_midi_msg(eventData)

# FL Studio Python Bridge Overload OnSysEx(eventData)
def onSysEx(eventData):
    on_sysex(eventData)

# FL Studio Python Bridge Overload OnNoteOn(eventData)
def onNoteOn(eventData):
    on_note_on(eventData)

# FL Studio Python Bridge Overload OnNoteOff(eventData)
def onNoteOff(eventData):
    on_note_off(eventData)

# FL Studio Python Bridge Overload OnControlChange(eventData)
def onControlChange(eventData):
    on_control_change(eventData)

# FL Studio Python Bridge Overload OnProgramChange(eventData)
def onProgramChange(eventData):
    on_program_change(eventData)

# FL Studio Python Bridge Overload OnPitchBend(eventData)
def onPitchBend(eventData):
    on_pitch_bend(eventData)

# FL Studio Python Bridge Overload OnKeyPressure(eventData)
def onKeyPressure(eventData):
    on_key_pressure(eventData)

# FL Studio Python Bridge Overload OnChannelPressure(eventData)
def onChannelPressure(eventData):
    on_channel_pressure(eventData)

# FL Studio Python Bridge Overload OnMidiOutMsg(eventData)
def onMidiOutMsg(eventData):
    on_midi_out_msg(eventData)

# FL Studio Python Bridge Overload OnIdle()
def onIdle():
    on_idle()

# FL Studio Python Bridge Overload OnProjectLoad(status)
def onProjectLoad(status):
    on_project_load(status)

# FL Studio Python Bridge Overload OnRefresh(flags)
def onRefresh(flags):
    on_refresh(flags)

# FL Studio Python Bridge Overload OnDoFullRefresh()
def onDoFullRefresh():
    on_do_full_refresh()

# FL Studio Python Bridge Overload OnUpdateBeatIndicator(value)
def onUpdateBeatIndicator(value):
    on_update_beat_indicator(value)

# FL Studio Python Bridge Overload OnDisplayZone()
def onDisplayZone():
    on_display_zone()

# FL Studio Python Bridge Overload OnUpdateLiveMode(lastTrack)
def onUpdateLiveMode(lastTrack):
    on_update_live_mode(lastTrack)

# FL Studio Python Bridge Overload OnDirtyMixerTrack(index)
def OnDirtyMixerTrack(index):
    on_dirty_mixer_track(index)

# FL Studio Python Bridge Overload OnDirtyChannel(index, flag)
def OnDirtyChannel(index, flag):
    on_dirty_channel(index, flag)

# FL Studio Python Bridge Overload OnFirstConnect()
def OnFirstConnect():
    on_first_connect()

# FL Studio Python Bridge Overload OnUpdateMeters()
def OnUpdateMeters():
    on_update_meters()

# FL Studio Python Bridge Overload OnWaitingForInput()
def OnWaitingForInput():
    on_waiting_for_input()

# FL Studio Python Bridge Overload OnSendTempMsg(message, duration)
def OnSendTempMsg(message, duration):
    on_send_temp_msg(message, duration)

# Device Module

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

# Channels Module

# Channels module allows you to control FL Studio Channels

# 'index' is respecting channel groups, 'indexGlobal' is global index
# Command Arguments Result Documentation Version
# Assume flsiChannels is the module providing the underlying functionality

def selected_channel(can_be_none=0, offset=0, index_global=0):
    """
    Returns 'index' (respecting groups) of the first selected channel.
    When there is no selection, function will return 0 (or -1 if can_be_none is 1).
    Use optional 'offset' parameter to find other selected channels.
    Set optional 'index_global' to 1 to return global channel index instead of index respecting groups.
    """
    return flsiChannels.selectedChannel(can_be_none, offset, index_global)

def channel_number(can_be_none=0, offset=0):
    """
    Returns 'index_global' of the first selected channel.
    When there is no selection, function will return -1 (or 0 if can_be_none is 1).
    Use optional 'offset' parameter to find other selected channels.
    """
    return flsiChannels.channelNumber(can_be_none, offset)

def channel_count(mode=0):
    """
    Returns the number of channels respecting groups - set optional mode parameter to 1 to get count of all channels.
    """
    return flsiChannels.channelCount(mode)

def get_channel_name(index):
    """
    Returns the name of the channel at "index".
    """
    return flsiChannels.getChannelName(index)

def set_channel_name(index, name):
    """
    Changes the name of the channel at "index" to "name".
    """
    flsiChannels.setChannelName(index, name)

def get_channel_color(index):
    """
    Returns the color of the channel at "index".
    """
    return flsiChannels.getChannelColor(index)

def set_channel_color(index, color):
    """
    Changes the color of the channel at "index" to the value of "color".
    """
    flsiChannels.setChannelColor(index, color)

def is_channel_muted(index):
    """
    Returns True if the channel at "index" is muted.
    """
    return flsiChannels.isChannelMuted(index)

def mute_channel(index, value=-1):
    """
    Toggles the muted state of the channel at "index" if value is default,
    otherwise mute channel if value is 1, or unmute if value is 0.
    """
    flsiChannels.muteChannel(index, value)

def is_channel_solo(index):
    """
    Returns True if the channel at "index" is soloed.
    """
    return flsiChannels.isChannelSolo(index)

def solo_channel(index, value=-1):
    """
    Toggles the state of the channel at "index" if value is default.
    Otherwise solo channel if value is 1 and unsolo if value is 0.
    """
    flsiChannels.soloChannel(index, value)

def get_channel_volume(index, mode=0):
    """
    Returns the normalized volume (between 0 and 1.0) of the channel at "index" -
    set optional mode to 1 to get volume in dB.
    """
    return flsiChannels.getChannelVolume(index, mode)

def set_channel_volume(index, volume, pickup_mode=None):
    """
    Changes the volume for the channel at "index" - volume is a value between 0 and 1.0.
    Use optional pickup_mode to override FL default pickup option.
    """
    flsiChannels.setChannelVolume(index, volume, pickup_mode)

def get_channel_pan(index):
    """
    Returns the pan value for the channel at "index", as a value between -1.0 and +1.0.
    """
    return flsiChannels.getChannelPan(index)

def set_channel_pan(index, pan, pickup_mode=None):
    """
    Change the pan value of the channel at "index" to the value of "pan" -
    The value should be between -1.0 and +1.0 -
    use optional pickup_mode to override FL default pickup option.
    """
    flsiChannels.setChannelPan(index, pan, pickup_mode)

def get_channel_pitch(index, mode=0):
    """
    Returns the pitch value for the channel at "index", as a value between -1.0 and +1.0 -
    use optional mode parameter to return pitch in semitones (mode = 1) or to return pitch range (mode = 2).
    """
    return flsiChannels.getChannelPitch(index, mode)

def set_channel_pitch(index, value, mode=0, pickup_mode=None):
    """
    Change the pitch value of the channel at "index" - The value should be between -1.0 and +1.0 -
    use optional mode parameter to send value in semitones (mode = 1) or to change pitch range (mode = 2)
    use optional pickup_mode to override FL default pickup option.
    """
    flsiChannels.setChannelPitch(index, value, mode, pickup_mode)

def get_channel_type(index):
    """
    Returns the type of channel, can be one of the following values.
    """
    return flsiChannels.getChannelType(index)

def is_channel_selected(index):
    """
    Returns True if the channel at "index" is selected.
    """
    return flsiChannels.isChannelSelected(index)

def select_one_channel(index):
    """
    Select channel at "index" exclusively.
    """
    flsiChannels.selectOneChannel(index)

def select_channel(index, value=-1):
    """
    Toggle the selection of the channel at "index" - to not toggle, set value to 1 (select) or 0 (deselect).
    """
    flsiChannels.selectChannel(index, value)

def select_all():
    """
    Select all channels in the current channel group.
    """
    flsiChannels.selectAll()

def deselect_all():
    """
    Deselect all channels in the current channel group.
    """
    flsiChannels.deselectAll()

def get_channel_midi_in_port(index):
    """
    Returns MIDI port for channel at "index" or one of the following:
    -3 receive notes from touch keyboard
    -2 this channel will only receive notes when it's the selected channel
    -1 receive notes from typing keyboard
    """
    return flsiChannels.getChannelMidiInPort(index)

def get_channel_index(index):
    """
    Returns 'indexGlobal' for channel at "index" (respecting the groups).
    """
    return flsiChannels.getChannelIndex(index)

def get_target_fx_track(index):
    """
    Returns target FX track for channel at "index".
    """
    return flsiChannels.getTargetFxTrack(index)

def set_target_fx_track(channel_index, mixer_index):
    """
    Routes the channel at "channelIndex" to the mixer track at "mixerIndex".
    """
    flsiChannels.setTargetFxTrack(channel_index, mixer_index)

def is_highlighted():
    """
    Returns True when the red highlight rectangle is active in the channel rack.
    """
    return flsiChannels.isHighLighted()

# Channel events
def get_rec_event_id(index):
    """
    Returns eventID for channel at "index".
    Use this eventID in process_REC_Event.
    Example (to get eventId for volume of the first channel):
    eventId = midi.REC_Chan_Vol + channels.getRecEventId(0)
    """
    return flsiChannels.getRecEventId(index)

def inc_event_value(event_id, step, resolution=1):
    """
    Get event value increased by step. Use (optional) resolution parameter to specify increment resolution.
    Use the result as a new value in process_REC_Event.
    Example (to increase the volume of the first channel):
    step = 1
    eventId = midi.REC_Chan_Vol + channels.getRecEventId(0)
    newValue = channels.incEventValue(eventId, step)
    general.process_REC_Event(eventId, newValue, midi.REC_UpdateValue | midi.REC_UpdateControl)
    """
    return flsiChannels.incEventValue(event_id, step, resolution)

def process_rec_event(event_id, value, flags):
    """
    This function is deprecated here and moved to the general module. More info here.
    """
    return flsiChannels.process_REC_Event(event_id, value, flags)

# Channel grid bits
def get_grid_bit(index, position):
    """
    Returns grid bit at "position" for channel at "index".
    """
    return flsiChannels.getGridBit(index, position)

def set_grid_bit(index, position, value):
    """
    Set grid bit value at "position" for channel at "index".
    """
    return flsiChannels.setGridBit(index, position, value)

def get_step_param(step, param, offset, start_pos, pads_stride=16):
    """
    Get step parameter for step at "step".
    """
    return flsiChannels.getStepParam(step, param, offset, start_pos, pads_stride)

def get_current_step_param(index, step, param):
    """
    Get current step parameter for channel at "index" and for step at "step".
    """
    return flsiChannels.getCurrentStepParam(index, step, param)

def set_step_parameter_by_index(index, pat_num, step, param, value, global_index=0):
    """
    Set current step parameter for channel at "index" and for step at "step".
    Set optional global_index to 1 to use global channel index.
    """
    return flsiChannels.setStepParameterByIndex(index, pat_num, step, param, value, global_index)

def get_grid_bit_with_loop(index, position):
    """
    Get grid bit with a loop for the channel at "index".
    """
    return flsiChannels.getGridBitWithLoop(index, position)

def show_graph_editor(temporary, param, step, index, global_index=1):
    """
    Show the graph editor for the channel at "index" and for step at "step".
    Set optional global_index to 0 to use the group channel index.
    Set temporary to False to keep the editor open.
    """
    return flsiChannels.showGraphEditor(temporary, param, step, index, global_index)

# Misc.
def is_graph_editor_visible():
    """
    Returns whether the graph editor is currently visible.
    """
    return flsiChannels.isGraphEditorVisible()

def show_editor(index, value=-1):
    """
    Show editor (plugin window) for the channel at "index" -
    set optional 'value' to 1 to show or to 0 to hide the editor.
    """
    return flsiChannels.showEditor(index, value)

def focus_editor(index):
    """
    Focus editor (plugin window) for the channel at "index".
    """
    return flsiChannels.focusEditor(index)

def show_cs_form(index, state=1):
    """
    Show channel settings (or plugin window for plugins) for the channel at "index" -
    use optional state to 0 (close), 1 (open), -1 (toggle) channel settings window.
    """
    return flsiChannels.showCSForm(index, state)

def midi_note_on(index_global, note, velocity, channel=-1):
    """
    Set MIDI note for channel at "index_global".
    """
    return flsiChannels.midiNoteOn(index_global, note, velocity, channel)

def get_activity_level(index):
    """
    Returns activity level for channel at "index".
    """
    return flsiChannels.getActivityLevel(index)

def quick_quantize(index, start_only=1):
    """
    Perform quick quantize for channel at "index".
    """
    return flsiChannels.quickQuantize(index, start_only)

# Playlist module
# Assume flsiPlaylist is the module providing the underlying functionality

def track_count() -> int:
    """
    Returns the current track count.
    """
    return flsiPlaylist.trackCount()

def get_track_name(index: int) -> str:
    """
    Returns the name of the track at "index".

    Parameters:
    - index (int): Index of the track.

    Returns:
    - name (str): Name of the track.
    """
    return flsiPlaylist.getTrackName(index)

def set_track_name(index: int, name: str):
    """
    Changes the name of the track at "index" to "name".

    Parameters:
    - index (int): Index of the track.
    - name (str): New name for the track.
    """
    flsiPlaylist.setTrackName(index, name)

def get_track_color(index: int) -> int:
    """
    Returns the color of the track at "index" as an RGBA value.

    Parameters:
    - index (int): Index of the track.

    Returns:
    - color (int): RGBA value representing the color of the track.
    """
    return flsiPlaylist.getTrackColor(index)

def set_track_color(index: int, color: int):
    """
    Changes the color of the track at "index" to the value of "color".

    Parameters:
    - index (int): Index of the track.
    - color (int): New color value for the track.
    """
    flsiPlaylist.setTrackColor(index, color)

def is_track_muted(index: int) -> bool:
    """
    Returns True if the track at "index" is muted.

    Parameters:
    - index (int): Index of the track.

    Returns:
    - is_muted (bool): True if the track is muted, False otherwise.
    """
    return flsiPlaylist.isTrackMuted(index)

def mute_track(index: int, value: int = -1):
    """
    Toggles the Mute status of the track at "index" if value is default.
    Otherwise mutes track if value is 1 and unmutes if value is 0.

    Parameters:
    - index (int): Index of the track.
    - value (int, optional): Mute status. Default is -1 (toggle).
    """
    flsiPlaylist.muteTrack(index, value)

def is_track_mute_lock(index: int) -> bool:
    """
    Returns True if the Mute for the track at "index" is locked.

    Parameters:
    - index (int): Index of the track.

    Returns:
    - is_locked (bool): True if the mute is locked, False otherwise.
    """
    return flsiPlaylist.isTrackMuteLock(index)

def mute_track_lock(index: int):
    """
    Toggles the Mute lock status of the track at "index".

    Parameters:
    - index (int): Index of the track.
    """
    flsiPlaylist.muteTrackLock(index)

def is_track_solo(index: int) -> bool:
    """
    Returns True if the track at "index" is currently solo'd.

    Parameters:
    - index (int): Index of the track.

    Returns:
    - is_solo (bool): True if the track is solo'd, False otherwise.
    """
    return flsiPlaylist.isTrackSolo(index)

def solo_track(index: int, value: int = -1, in_group: int = 0):
    """
    Toggle the solo state of the track at "index".
    Set optional 'value' to 1 to solo track or to 0 unsolo track.
    Set optional 'in_group' to 1 to solo track within track group.

    Parameters:
    - index (int): Index of the track.
    - value (int, optional): Solo status. Default is -1 (toggle).
    - in_group (int, optional): Solo within group status. Default is 0.
    """
    flsiPlaylist.soloTrack(index, value, in_group)

def is_track_selected(index: int) -> bool:
    """
    Returns True if the track at "index" is selected.

    Parameters:
    - index (int): Index of the track.

    Returns:
    - is_selected (bool): True if the track is selected, False otherwise.
    """
    return flsiPlaylist.isTrackSelected(index)

def select_track(index: int):
    """
    Toggle selection of the track at "index".

    Parameters:
    - index (int): Index of the track.
    """
    flsiPlaylist.selectTrack(index)

def select_all():
    """
    Select all playlist tracks.
    """
    flsiPlaylist.selectAll()

def deselect_all():
    """
    Deselect all playlist tracks.
    """
    flsiPlaylist.deselectAll()

def get_track_activity_level(index: int) -> float:
    """
    Returns the activity level of the track at "index" (zero if not active, > 0 if active).

    Parameters:
    - index (int): Index of the track.

    Returns:
    - activity_level (float): Activity level of the track.
    """
    return flsiPlaylist.getTrackActivityLevel(index)

def get_track_activity_level_vis(index: int) -> float:
    """
    Returns the visual activity level of the track at "index" as a normalized value.

    Parameters:
    - index (int): Index of the track.

    Returns:
    - activity_level_vis (float): Visual activity level of the track.
    """
    return flsiPlaylist.getTrackActivityLevelVis(index)

def get_display_zone() -> int:
    """
    Returns current display zone in the playlist or zero if none.
    """
    return flsiPlaylist.getDisplayZone()

def lock_display_zone(index: int, value: int):
    """
    Lock display zone at "index".

    Parameters:
    - index (int): Index of the display zone.
    - value (int): Lock status.
    """
    flsiPlaylist.lockDisplayZone(index, value)

def live_display_zone(left: int, top: int, right: int, bottom: int, duration: int = 0):
    """
    Set the display zone in the playlist to the specified co-ordinates.
    Use optional 'duration' parameter to make display zone temporary.

    Parameters:
    - left (int): Left coordinate of the display zone.
    - top (int): Top coordinate of the display zone.
    - right (int): Right coordinate of the display zone.
    - bottom (int): Bottom coordinate of the display zone.
    - duration (int, optional): Duration of the display zone. Default is 0.
    """
    flsiPlaylist.liveDisplayZone(left, top, right, bottom, duration)

def get_live_loop_mode(index: int) -> int:
    """
    Get live loop mode.

    Parameters:
    - index (int): Index of the track.

    Returns:
    - loop_mode (int): Live loop mode.
    """
    return flsiPlaylist.getLiveLoopMode(index)

def get_live_trigger_mode(index: int) -> int:
    """
    Get live trigger mode - Result is one of the constants.

    Parameters:
    - index (int): Index of the track.

    Returns:
    - trigger_mode (int): Live trigger mode.
    """
    return flsiPlaylist.getLiveTriggerMode(index)

def get_live_pos_snap(index: int) -> int:
    """
    Get live pos snap - Result is one of the constants.

    Parameters:
    - index (int): Index of the track.

    Returns:
    - pos_snap (int): Live pos snap mode.
    """
    return flsiPlaylist.getLivePosSnap(index)

def get_live_trig_snap(index: int) -> int:
    """
    Get live trig snap - Result is one of the constants.

    Parameters:
    - index (int): Index of the track.

    Returns:
    - trig_snap (int): Live trig snap mode.
    """
    return flsiPlaylist.getLiveTrigSnap(index)

def get_live_status(index: int, mode: int = flsiMidi.LB_Status_Default) -> int:
    """
    Get live status for track at "index" - Result depends on mode.

    Parameters:
    - index (int): Index of the track.
    - mode (int, optional): Live status mode. Default is LB_Status_Default.

    Returns:
    - status (int): Live status.
    """
    return flsiPlaylist.getLiveStatus(index, mode)

def get_live_block_status(index: int, block_num: int, mode: int = flsiMidi.LB_Status_Default) -> int:
    """
    Get live block status for track at "index" and for block "block_num".
    Result depends on mode.

    Parameters:
    - index (int): Index of the track.
    - block_num (int): Index of the block.
    - mode (int, optional): Live status mode. Default is LB_Status_Default.

    Returns:
    - block_status (int): Live block status.
    """
    return flsiPlaylist.getLiveBlockStatus(index, block_num, mode)

def get_live_block_color(index: int, block_num: int) -> int:
    """
    Get live block color for track at "index" and for block "block_num".

    Parameters:
    - index (int): Index of the track.
    - block_num (int): Index of the block.

    Returns:
    - block_color (int): Live block color.
    """
    return flsiPlaylist.getLiveBlockColor(index, block_num)

def trigger_live_clip(index: int, sub_num: int, flags: int, velocity: float = -1):
    """
    Trigger live clip for track at "index" and for block "block_num".
    Set sub_num to -1 and use the TLC_Fill flag to stop live clips on this track.

    Parameters:
    - index (int): Index of the track.
    - sub_num (int): Index of the subclip.
    - flags (int): Trigger flags.
    - velocity (float, optional): Velocity of the trigger. Default is -1.
    """
    flsiPlaylist.triggerLiveClip(index, sub_num, flags, velocity)

def refresh_live_clips(index: int, value: int):
    """
    Refresh live clips for track at "index".

    Parameters:
    - index (int): Index of the track.
    - value (int): Refresh value.
    """
    flsiPlaylist.refreshLiveClips(index, value)

def inc_live_pos_snap(index: int, value: int):
    """
    Increase live pos snap for track at "index".

    Parameters:
    - index (int): Index of the track.
    - value (int): Increment value.
    """
    flsiPlaylist.incLivePosSnap(index, value)

def inc_live_trig_snap(index: int, value: int):
    """
    Increase live trig snap for track at "index".

    Parameters:
    - index (int): Index of the track.
    - value (int): Increment value.
    """
    flsiPlaylist.incLiveTrigSnap(index, value)

def inc_live_loop_mode(index: int, value: int):
    """
    Increase live loop mode for track at "index".

    Parameters:
    - index (int): Index of the track.
    - value (int): Increment value.
    """
    flsiPlaylist.incLiveLoopMode(index, value)

def inc_live_trig_mode(index: int, value: int):
    """
    Increase live trig mode for track at "index".

    Parameters:
    - index (int): Index of the track.
    - value (int): Increment value.
    """
    flsiPlaylist.incLiveTrigMode(index, value)

def get_vis_time_bar() -> int:
    """
    Get time bar.
    """
    return flsiPlaylist.getVisTimeBar()

def get_vis_time_tick() -> int:
    """
    Get time tick.
    """
    return flsiPlaylist.getVisTimeTick()

def get_vis_time_step() -> int:
    """
    Get time step.
    """
    return flsiPlaylist.getVisTimeStep()

def get_performance_mode_state() -> int:
    """
    Returns 1 when the Playlist is in performance mode, 0 when it's not.
    """
    return flsiPlaylist.getPerformanceModeState()

# Patterns Module
# Assume flsiPatterns is the module providing the underlying functionality

def pattern_number() -> int:
    """
    Returns the current pattern number.
    """
    return flsiPatterns.patternNumber()

def pattern_count() -> int:
    """
    Returns the number of patterns.
    """
    return flsiPatterns.patternCount()

def pattern_max() -> int:
    """
    Returns the maximum pattern number.
    """
    return flsiPatterns.patternMax()

def get_pattern_name(index: int) -> str:
    """
    Returns the name of the pattern at "index".

    Parameters:
    - index (int): Index of the pattern.

    Returns:
    - name (str): Name of the pattern.
    """
    return flsiPatterns.getPatternName(index)

def set_pattern_name(index: int, name: str):
    """
    Changes the name of the pattern at "index" to "name".

    Parameters:
    - index (int): Index of the pattern.
    - name (str): New name for the pattern.
    """
    flsiPatterns.setPatternName(index, name)

def get_pattern_color(index: int) -> int:
    """
    Returns the color of the pattern at "index".

    Parameters:
    - index (int): Index of the pattern.

    Returns:
    - color (int): Color of the pattern.
    """
    return flsiPatterns.getPatternColor(index)

def set_pattern_color(index: int, color: int):
    """
    Changes the color of the pattern at "index" to "color".

    Parameters:
    - index (int): Index of the pattern.
    - color (int): New color for the pattern.
    """
    flsiPatterns.setPatternColor(index, color)

def get_pattern_length(index: int) -> int:
    """
    Returns the length of the pattern at "index", in beats.

    Parameters:
    - index (int): Index of the pattern.

    Returns:
    - length (int): Length of the pattern in beats.
    """
    return flsiPatterns.getPatternLength(index)

def get_block_set_status(left: int, top: int, right: int, bottom: int) -> int:
    """
    Returns the status of the live block.

    Parameters:
    - left (int): Left position of the block.
    - top (int): Top position of the block.
    - right (int): Right position of the block.
    - bottom (int): Bottom position of the block.

    Returns:
    - status (int): Status of the live block.
    """
    return flsiPatterns.getBlockSetStatus(left, top, right, bottom)

def ensure_valid_note_record(index: int, play_now: int = 0):
    """
    Ensure valid note of the pattern at "index".

    Parameters:
    - index (int): Index of the pattern.
    - play_now (int): Optional parameter (default is 0).
    """
    flsiPatterns.ensureValidNoteRecord(index, play_now)

def jump_to_pattern(index: int):
    """
    Jump to the pattern at "index".

    Parameters:
    - index (int): Index of the pattern.
    """
    flsiPatterns.jumpToPattern(index)

def find_first_next_empty_pat(flags: int, x: int = -1, y: int = -1):
    """
    Find the first empty pattern at position x, y.

    Parameters:
    - flags (int): Flags for finding the empty pattern.
    - x (int): Optional parameter for the x position (default is -1).
    - y (int): Optional parameter for the y position (default is -1).
    """
    flsiPatterns.findFirstNextEmptyPat(flags, x, y)

# Picker panel functions

def is_pattern_selected(index: int) -> bool:
    """
    Returns True if the pattern at "index" is selected in the Picker panel.

    Parameters:
    - index (int): Index of the pattern.

    Returns:
    - selected (bool): True if the pattern is selected.
    """
    return flsiPatterns.isPatternSelected(index)

def is_pattern_default(index: int) -> bool:
    """
    Returns True if the pattern at "index" is default (empty and unchanged by the user).

    Parameters:
    - index (int): Index of the pattern.

    Returns:
    - default_pattern (bool): True if the pattern is default.
    """
    return flsiPatterns.isPatternDefault(index)

def select_pattern(index: int, value: int = -1, preview: int = 0):
    """
    Select pattern at "index" in the Picker panel.

    Parameters:
    - index (int): Index of the pattern.
    - value (int): Optional parameter for selection (default is -1).
    - preview (int): Optional parameter for previewing (default is 0).
    """
    flsiPatterns.selectPattern(index, value, preview)

def clone_pattern(index: int = -1):
    """
    Clone selected pattern(s), or clone the panel specified by index (optional).

    Parameters:
    - index (int): Optional parameter for the index (default is -1).
    """
    flsiPatterns.clonePattern(index)

def select_all():
    """
    Select all patterns in the Picker panel.
    """
    flsiPatterns.selectAll()

def deselect_all():
    """
    Deselect all patterns in the Picker panel.
    """
    flsiPatterns.deselectAll()

def burn_loop(index: int, store_undo: int = 1, update_ui: int = 1):
    """
    Returns activity level for channel at "index".

    Parameters:
    - index (int): Index of the channel.
    - store_undo (int): Optional parameter to store undo step (default is 1).
    - update_ui (int): Optional parameter to update the UI (default is 1).

    Returns:
    - activity_level (int): Activity level for the channel.
    """
    return flsiPatterns.burnLoop(index, store_undo, update_ui)

# Pattern groups

def get_active_pattern_group() -> int:
    """
    Returns the index of the currently selected pattern group.
    The default "All patterns" grouping has index -1.
    User-defined pattern groups have indexes starting from 0.

    Returns:
    - active_group (int): Index of the active pattern group.
    """
    return flsiPatterns.getActivePatternGroup()

def get_pattern_group_count() -> int:
    """
    Returns the number of user-defined pattern groups.
    The default "All patterns" grouping is not included.

    Returns:
    - group_count (int): Number of user-defined pattern groups.
    """
    return flsiPatterns.getPatternGroupCount()

def get_pattern_group_name(index: int) -> str:
    """
    Returns the name of the pattern group at index.
    The default "All patterns" group's name cannot be accessed.

    Parameters:
    - index (int): Index of the pattern group.

    Returns:
    - group_name (str): Name of the pattern group.
    """
    return flsiPatterns.getPatternGroupName(index)

def get_patterns_in_group(index: int) -> tuple:
    """
    Returns a tuple containing all the patterns in the group at index.
    The default "All patterns" group returns a tuple containing all the patterns
    that haven't been added to any other groups.

    Parameters:
    - index (int): Index of the pattern group.

    Returns:
    - patterns (tuple): Tuple containing patterns in the group.
    """
    return flsiPatterns.getPatternsInGroup(index)


# Arrangement Module
# Assume flsiArrangement is the module providing the underlying functionality

def jump_to_marker(index, select):
    """
    Select a marker.

    Parameters:
    - index (int): Marker index. Set to -1 to select the previous marker or +1 to select the next marker.
    - select (bool): True to select the marker as well.
    """
    flsiArrangement.jumpToMarker(index, select)

def get_marker_name(index):
    """
    Returns the name of the requested marker.

    Parameters:
    - index (int): Marker index.

    Returns:
    - marker_name (str): Name of the requested marker. If the marker doesn't exist, an empty string is returned.
    """
    return flsiArrangement.getMarkerName(index)

def add_auto_time_marker(time, name):
    """
    Add an automatic time marker.

    Parameters:
    - time (int): Time at which the automatic marker should be added.
    - name (str): Name of the automatic marker.
    """
    flsiArrangement.addAutoTimeMarker(time, name)

def live_selection(time, stop):
    """
    Set a live selection point.

    Parameters:
    - time (int): Time at which the live selection point should be set.
    - stop (bool): True to use the end point of the selection instead of the start.
    """
    flsiArrangement.liveSelection(time, stop)

def live_selection_start():
    """
    Returns the start time of the current live selection.

    Returns:
    - start_time (int): Start time of the current live selection.
    """
    return flsiArrangement.liveSelectionStart()

def current_time(snap):
    """
    Returns the current time in the current arrangement.

    Parameters:
    - snap (bool): True to get the returned value snapped to the grid.

    Returns:
    - current_time (int): Current time in the current arrangement.
    """
    return flsiArrangement.currentTime(snap)

def current_time_hint(mode, time, set_rec_ppb=None, is_length=0):
    """
    Returns a hint string for the requested time in the current arrangement.

    Parameters:
    - mode (int): Mode is 0 for pattern mode and 1 for song mode.
    - time (int): Requested time in the current arrangement.
    - set_rec_ppb (int): Optional parameter to set the recording PPQ (Pulses Per Quarter note).
    - is_length (int): Indicates whether the time is a length.

    Returns:
    - hint (str): Hint string for the requested time.
    """
    return flsiArrangement.currentTimeHint(mode, time, set_rec_ppb, is_length)

def selection_start():
    """
    Returns the start time of the current selection in the current arrangement.

    Returns:
    - start_time (int): Start time of the current selection.
    """
    return flsiArrangement.selectionStart()

def selection_end():
    """
    Returns the end time of the current selection in the current arrangement.

    Returns:
    - end_time (int): End time of the current selection.
    """
    return flsiArrangement.selectionEnd()

# ui module
# Assume flsiUi is the module providing the underlying functionality

def jog(value):
    """
    Generic jog control. Can be used to select stuff.
    
    Parameters:
    - value (int): Increment value.

    Returns:
    - int: How the request was handled.
    """
    return flsiUi.jog(value)

def jog2(value):
    """
    Alternate jog control. Can be used to relocate stuff.
    
    Parameters:
    - value (int): Increment value.

    Returns:
    - int: How the request was handled.
    """
    return flsiUi.jog2(value)

def strip(value):
    """
    Touch-sensitive strip.
    
    Parameters:
    - value (int): -midi.FromMIDI_Max (left most) to midi.FromMIDI_Max (right most).

    Returns:
    - int: How the request was handled.
    """
    return flsiUi.strip(value)

def strip_jog(value):
    """
    Touch-sensitive strip in jog mode.
    
    Parameters:
    - value (int): Increment value.

    Returns:
    - int: How the request was handled.
    """
    return flsiUi.stripJog(value)

def strip_hold(value):
    """
    Touch-sensitive strip in hold mode.
    
    Parameters:
    - value (int): 0 for release, 1 and 2 for 1 or 2 fingers centered mode,
                 -1 and -2 for 1 or 2 fingers jog mode.

    Returns:
    - int: How the request was handled.
    """
    return flsiUi.stripHold(value)

def previous():
    """
    Generic previous control - in mixer: select previous mixer track
    in channel rack: select previous channel
    in browser: scroll to previous item
    in plugin: select previous preset
    
    Returns:
    - int: How the request was handled.
    """
    return flsiUi.previous()

def next():
    """
    Generic next control - in mixer: select next mixer track
    in channel rack: select next channel
    in browser: scroll to next item
    in plugin: select next preset
    
    Returns:
    - int: How the request was handled.
    """
    return flsiUi.next()

def move_jog(value):
    """
    Used to relocate items.
    
    Parameters:
    - value (int): Increment value.

    Returns:
    - int: How the request was handled.
    """
    return flsiUi.moveJog(value)

def up(value=1):
    """
    Generic way to move up.
    
    Parameters:
    - value (int): Increment value.

    Returns:
    - int: How the request was handled.
    """
    return flsiUi.up(value)

def down(value=1):
    """
    Generic way to move down.
    
    Parameters:
    - value (int): Increment value.

    Returns:
    - int: How the request was handled.
    """
    return flsiUi.down(value)

def left(value=1):
    """
    Generic way to move left.
    
    Parameters:
    - value (int): Increment value.

    Returns:
    - int: How the request was handled.
    """
    return flsiUi.left(value)

def right(value=1):
    """
    Generic way to move right.
    
    Parameters:
    - value (int): Increment value.

    Returns:
    - int: How the request was handled.
    """
    return flsiUi.right(value)

def hor_zoom(value):
    """
    Zoom horizontally by the increment value.
    
    Parameters:
    - value (int): Increment value.

    Returns:
    - int: How the request was handled.
    """
    return flsiUi.horZoom(value)

def ver_zoom(value):
    """
    Zoom vertically by the increment value.
    
    Parameters:
    - value (int): Increment value.

    Returns:
    - int: How the request was handled.
    """
    return flsiUi.verZoom(value)

def snap_on_off():
    """
    Toggle the snap value.
    
    Returns:
    - int: How the request was handled.
    """
    return flsiUi.snapOnOff()

def cut():
    """
    Cut what is selected, if possible.
    
    Returns:
    - int: How the request was handled.
    """
    return flsiUi.cut()

def copy():
    """
    Copy what is selected, if possible.
    
    Returns:
    - int: How the request was handled.
    """
    return flsiUi.copy()

def paste():
    """
    Paste previously copied data, if possible.
    
    Returns:
    - int: How the request was handled.
    """
    return flsiUi.paste()

def insert():
    """
    Press the insert key.
    
    Returns:
    - int: How the request was handled.
    """
    return flsiUi.insert()

def delete():
    """
    Press the delete key.
    
    Returns:
    - int: How the request was handled.
    """
    return flsiUi.delete()

def enter():
    """
    Press the enter key.
    
    Returns:
    - int: How the request was handled.
    """
    return flsiUi.enter()

def escape():
    """
    Press the escape key.
    
    Returns:
    - int: How the request was handled.
    """
    return flsiUi.escape()

def yes():
    """
    Press the 'Y' key.
    
    Returns:
    - int: How the request was handled.
    """
    return flsiUi.yes()

def not_():
    """
    Press the 'N' key.
    
    Returns:
    - int: How the request was handled.
    """
    return flsiUi.not_()

# FL Studio Hints
def get_hint_msg():
    """
    Returns program hint message.
    
    Returns:
    - str: Program hint message.
    """
    return flsiUi.getHintMsg()

def set_hint_msg(msg):
    """
    Set program hint message.
    
    Parameters:
    - msg (str): Program hint message.
    
    Returns:
    - int: How the request was handled.
    """
    return flsiUi.setHintMsg(msg)

def get_hint_value(value, max_value):
    """
    Returns hint for value.
    
    Parameters:
    - value (int): The value for which hint is requested.
    - max_value (int): Maximum value.
    
    Returns:
    - str: Hint for the given value.
    """
    return flsiUi.getHintValue(value, max_value)

def get_time_disp_min():
    """
    Returns True when time display is set to 'minutes'.
    
    Returns:
    - int: How the request was handled.
    """
    return flsiUi.getTimeDispMin()

def set_time_disp_min():
    """
    Set time display to minutes.
    
    Returns:
    - int: How the request was handled.
    """
    return flsiUi.setTimeDispMin()

# Window handling
def get_visible(index):
    """
    Returns visible state (0 or 1) of the window specified by index.
    
    Parameters:
    - index (int): Index of the window.

    Returns:
    - int: Visible state of the window.
    """
    return flsiUi.getVisible(index)

def show_window(index):
    """
    Show window specified by index.
    
    Parameters:
    - index (int): Index of the window.
    
    Returns:
    - int: How the request was handled.
    """
    return flsiUi.showWindow(index)

def hide_window(index):
    """
    Hide window specified by index.
    
    Parameters:
    - index (int): Index of the window.
    
    Returns:
    - int: How the request was handled.
    """
    return flsiUi.hideWindow(index)

def get_focused(index):
    """
    Returns focused state (0 or 1) of the window specified by index.
    
    Parameters:
    - index (int): Index of the window.
    
    Returns:
    - int: Focused state of the window.
    """
    return flsiUi.getFocused(index)

def set_focused(index):
    """
    Set focused state (0 or 1) of the window specified by index.
    
    Parameters:
    - index (int): Index of the window.
    
    Returns:
    - int: How the request was handled.
    """
    return flsiUi.setFocused(index)

def get_focused_form_caption():
    """
    Returns caption of the focused window.
    
    Returns:
    - str: Caption of the focused window.
    """
    return flsiUi.getFocusedFormCaption()

def get_focused_form_id():
    """
    Returns ID of the focused window.
    
    Returns:
    - int: ID of the focused window.
    """
    return flsiUi.getFocusedFormID()

def get_focused_plugin_name():
    """
    Returns Original Plugin Name of the focused window.
    
    Returns:
    - str: Original Plugin Name of the focused window.
    """
    return flsiUi.getFocusedPluginName()

def scroll_window(index, value, direction_flag=0):
    """
    Scroll window specified by index.

    Parameters:
    - index (int): Index of the window.
    - value (int): Track number (mixer), channel number (channel rack), playlist track (playlist)
                  or channel step (channel rack), playlist bar (playlist) when direction_flag is set to 1.
    - direction_flag (int): Direction flag.

    Returns:
    - int: How the request was handled.
    """
    return flsiUi.scrollWindow(index, value, direction_flag)

def next_window():
    """
    Focus the next window.
    
    Returns:
    - int: How the request was handled.
    """
    return flsiUi.nextWindow()

def select_window(shift):
    """
    Press the TAB key - set "shift" to True, to make it act as if Shift + TAB is pressed.
    
    Parameters:
    - shift (int): True to act as if Shift + TAB is pressed, False otherwise.

    Returns:
    - int: How the request was handled.
    """
    return flsiUi.selectWindow(shift)

def launch_audio_editor(reuse, filename, index, preset, preset_guid):
    """
    Launch audio editor for the track at "index" and return editor state.

    Parameters:
    - reuse (int): True to reuse opened audio editor (if any).
    - filename (str): Path to the audio file.
    - index (int): Index of the track.
    - preset (str): Preset information.
    - preset_guid (str): Preset GUID.

    Returns:
    - int: Editor state.
    """
    return flsiUi.launchAudioEditor(reuse, filename, index, preset, preset_guid)

def open_event_editor(event_id, mode, new_window=0):
    """
    Launch event editor for "event_id".

    Parameters:
    - event_id (int): Event ID.
    - mode (int): Mode information.
    - new_window (int): New window information.

    Returns:
    - int: How the request was handled.
    """
    return flsiUi.openEventEditor(event_id, mode, new_window)

# Menu handling
def is_in_popup_menu():
    """
    Returns True when the application popup menu is active.
    
    Returns:
    - int: How the request was handled.
    """
    return flsiUi.isInPopupMenu()

def close_active_popup_menu():
    """
    Close the active popup menu.
    
    Returns:
    - int: How the request was handled.
    """
    return flsiUi.closeActivePopupMenu()

# Assume flsiUi is the module providing the underlying functionality

def is_closing() -> int:
    """
    Returns True if the application is closing.
    """
    return flsiUi.isClosing()

def is_metronome_enabled() -> int:
    """
    Returns True when the metronome is enabled.
    """
    return flsiUi.isMetronomeEnabled()

def is_start_on_input_enabled() -> int:
    """
    Returns True when start on input is enabled.
    """
    return flsiUi.isStartOnInputEnabled()

def is_precount_enabled() -> int:
    """
    Returns True when precount is enabled.
    """
    return flsiUi.isPrecountEnabled()

def is_loop_rec_enabled() -> int:
    """
    Returns True when loop recording is enabled.
    """
    return flsiUi.isLoopRecEnabled()

def get_snap_mode() -> int:
    """
    Returns snap mode.
    """
    return flsiUi.getSnapMode()

def set_snap_mode(snap_mode: int) -> None:
    """
    Set snap mode.

    Parameters:
    - snap_mode: int
    """
    flsiUi.setSnapMode(snap_mode)

def select_another_snap_mode(value: int) -> None:
    """
    Select another snap mode.

    Parameters:
    - value: int
      Increment: -1 (previous), 1 (next) mode.
    """
    flsiUi.snapMode(value)

def get_step_edit_mode() -> bool:
    """
    Returns the state of the "step edit mode" control.
    """
    return flsiUi.getStepEditMode()

def set_step_edit_mode(new_value: bool) -> None:
    """
    Sets the state of the "step edit mode" control.

    Parameters:
    - new_value: bool
    """
    flsiUi.setStepEditMode(new_value)

def get_prog_title() -> str:
    """
    Returns the program title.
    """
    return flsiUi.getProgTitle()

def get_version(mode: int = 4) -> str:
    """
    Returns program version string (or number).

    Optional Parameters:
    - mode: int
      Can be one of the following values:
      VER_Major = 0; VER_Minor = 1; VER_Release = 2; VER_Build = 3;
      VER_VersionAndEdition = 4; VER_FullVersionAndEdition = 5;
      VER_ArchAndBuild = 6
    """
    return flsiUi.getVersion(mode)

def cr_display_rect(left: int, top: int, right: int, bottom: int, duration: int, flags: int = 0) -> None:
    """
    Display channel rack selection rectangle.

    Parameters:
    - left, top, right, bottom: int
      Rectangle coordinates.
    - duration: int
      Set 'duration' in ms, or use duration = midi.MaxInt to set rectangle 'on'
      and duration = 0 to set rectangle 'off'.
    - flags: int
      By default, the selection works on channel rack steps.
      See flags for additional options.
    """
    flsiUi.crDisplayRect(left, top, right, bottom, duration, flags)

def mi_display_rect(start: int, end: int, duration: int, flags: int = 0) -> None:
    """
    Display mixer selection rectangle.

    Parameters:
    - start, end: int
      Define "start" and "end" track number, use 0 for Master track, 126 for Current track.
    - duration: int
      Set 'duration' in ms, or use duration = midi.MaxInt to set rectangle 'on'
      and duration = 0 to set rectangle 'off'.
    - flags: int
      See flags for additional options.
    """
    flsiUi.miDisplayRect(start, end, duration, flags)

def mi_display_dock_rect(start: int, num_track: int, dock: int, duration: int) -> None:
    """
    Display selection rectangle in mixer dock.

    Parameters:
    - start, num_track: int
      Define "start" and "num_track" track number.
    - dock: int
      Set dock to 0 for left dock, or to 1 for right dock.
    - duration: int
      Set 'duration' in ms, or use duration = midi.MaxInt to set rectangle 'on'
      and duration = 0 to set rectangle 'off'.
    """
    flsiUi.miDisplayDockRect(start, num_track, dock, duration)

# Browser handling

def navigate_browser(direction: int, shift_held: int, string: str) -> str:
    """
    Navigate browser nodes or browser menu (right-click menu for the active node).

    Parameters:
    - direction: int
      Set direction to one of the FPT_Up, FPT_Down, FPT_Left, FPT_Right constants.
    - shift_held: int
      Set shift_held to 1 to expand/open the browser node.
    - string: str
      Function returns the caption of the active node.
    """
    return flsiUi.navigateBrowser(direction, shift_held, string)

def navigate_browser_tabs(direction: int) -> str:
    """
    Navigate browser tabs.

    Parameters:
    - direction: int
      Set direction to one of the FPT_Left, FPT_Right constants.
    """
    return flsiUi.navigateBrowserTabs(direction)

def select_browser_menu_item() -> None:
    """
    Select browser menu item (navigated by navigate_browser).
    """
    flsiUi.selectBrowserMenuItem()

def preview_browser_menu_item() -> None:
    """
    Start preview of the active browser node.
    """
    flsiUi.previewBrowserMenuItem()

def get_focused_node_file_type() -> int:
    """
    Return type for the active node or -1 when no node is active.
    """
    return flsiUi.getFocusedNodeFileType()

def get_focused_node_caption() -> str:
    """
    Return caption for the active node or an empty string when no node is active.
    """
    return flsiUi.getFocusedNodeCaption()

def is_browser_auto_hide() -> int:
    """
    Return 1 when the browser auto-hide option is enabled.
    """
    return flsiUi.isBrowserAutoHide()

def set_browser_auto_hide(auto_hide: int) -> None:
    """
    Set auto_hide to 1 to enable the browser auto-hide option.
    
    Parameters:
    - auto_hide: int
    """
    flsiUi.setBrowserAutoHide(auto_hide)

# Transport module
# Assume flsiTransport is the module providing the underlying functionality

def global_transport(command, value, pmeflags=flsiMidi.PME_System, flags=flsiMidi.GT_ALL):
    """
    Call the GlobalTransport function with the appropriate parameters.
    Use this function inside one of the eventData script events and pass eventData.pmeflags as "pmeflags" parameter.
    
    Parameters:
    - command (int): Transport command.
    - value (int): Transport value.
    - pmeflags (int): Flags for the GlobalTransport function.
    - flags (int): Transport flags.

    Returns:
    - result: Result of the GlobalTransport function.
    """
    return flsiTransport.globalTransport(command, value, pmeflags, flags)

def start():
    """
    Start playback.
    """
    flsiTransport.start()

def stop():
    """
    Stop playback.
    """
    flsiTransport.stop()

def record():
    """
    Toggle recording.
    """
    flsiTransport.record()

def is_recording():
    """
    Returns True when recording is active.
    """
    return flsiTransport.isRecording()

def get_loop_mode():
    """
    Returns the current looping mode (pattern = 0, song = 1).
    """
    return flsiTransport.getLoopMode()

def toggle_loop_mode():
    """
    Toggle loop mode.
    """
    flsiTransport.setLoopMode()

def get_song_pos(mode=-1):
    """
    Returns the song position as a normalized value (0..1) -
    or in specified format when mode is set.

    Parameters:
    - mode (int): Optional parameter to specify the format.

    Returns:
    - song_pos: Song position value.
    """
    return flsiTransport.getSongPos(mode)

def set_song_pos(position, mode=-1):
    """
    Set the song position - "position" is a normalized value (0..1) -
    or in specified format when mode is set.

    Parameters:
    - position (float): Song position value.
    - mode (int): Optional parameter to specify the format.
    """
    flsiTransport.setSongPos(position, mode)

def get_song_length(mode):
    """
    Get the song length.

    Parameters:
    - mode (int): Mode parameter for song length.

    Returns:
    - song_length: Song length value.
    """
    return flsiTransport.getSongLength(mode)

def get_song_pos_hint():
    """
    Returns a hint for the current song position.

    Returns:
    - hint (str): Hint for the current song position.
    """
    return flsiTransport.getSongPosHint()

def is_playing():
    """
    Returns True if the program is playing.
    """
    return flsiTransport.isPlaying()

def marker_jump_jog(value, flags=flsiMidi.GT_All):
    """
    Jump to a marker position - "value" is an increment.

    Parameters:
    - value (int): Increment value.
    - flags (int): Transport flags.
    """
    flsiTransport.markerJumpJog(value, flags)

def marker_sel_jog(value, flags=flsiMidi.GT_All):
    """
    Select a marker - "value" is an increment.

    Parameters:
    - value (int): Increment value.
    - flags (int): Transport flags.
    """
    flsiTransport.markerSelJog(value, flags)

def get_hw_beat_led_state():
    """
    Returns the state of the hardware LED beat indicator.

    Returns:
    - led_state: State of the hardware LED beat indicator.
    """
    return flsiTransport.getHWBeatLEDState()

# Playback speed control

def rewind(start_stop, flags=flsiMidi.GT_All):
    """
    Rewind the song position - Each call to this function with start_stop = SS_Start,
    must be stopped with start_stop = SS_Stop.

    Parameters:
    - start_stop (int): Start or stop indicator.
    - flags (int): Transport flags.
    """
    flsiTransport.rewind(start_stop, flags)

def fast_forward(start_stop, flags=flsiMidi.GT_All):
    """
    Forward the song position - Each call to this function with start_stop = SS_Start,
    must be stopped with start_stop = SS_Stop.

    Parameters:
    - start_stop (int): Start or stop indicator.
    - flags (int): Transport flags.
    """
    flsiTransport.fastForward(start_stop, flags)

def continuous_move(speed, start_stop):
    """
    Start Continuous move - This function does the same as rewind and fastforward but you can control speed.
    Set speed (> 0) to move forward and (< 0) to move backward (speed = (1) is normal speed forward).
    Each call to this function with start_stop = SS_Start, must be stopped with start_stop = SS_Stop.

    Parameters:
    - speed (int): Speed value.
    - start_stop (int): Start or stop indicator.
    """
    flsiTransport.continuousMove(speed, start_stop)

def continuous_move_pos(speed, start_stop):
    """
    Start Continuous move - Set speed (> 0) to move forward and (< 0) to move backward (speed = (1) is normal speed forward).
    Set start_stop to (2) to start and to (0) to stop.

    Parameters:
    - speed (int): Speed value.
    - start_stop (int): Start or stop indicator.
    """
    flsiTransport.continuousMovePos(speed, start_stop)

def set_playback_speed(speed_multiplier):
    """
    Set a playback speed multiplier - Set speedMultiplier = (1) is normal speed,
    set to value between (1/4 ... 1) for slower and between (1 ... 4) faster movement.

    Parameters:
    - speed_multiplier (float): Speed multiplier value.
    """
    flsiTransport.setPlaybackSpeed(speed_multiplier)

# Plugins Module
# Assume flsiPlugins is the module providing the underlying functionality

def is_valid(index, slot_index=-1, use_global_index=False):
    """
    Returns True if there is a valid plugin at the position of index/slot_index.

    Parameters:
    - index (int): Plugin position index.
    - slot_index (int, optional): Slot index for the plugin. Default is -1.
    - use_global_index (bool, optional): Use global channel index. Default is False.

    Returns:
    - is_valid (bool): True if the plugin is valid.
    """
    return flsiPlugins.isValid(index, slot_index, use_global_index)

def get_plugin_name(index, slot_index=-1, user_name=0, use_global_index=False):
    """
    Returns the plugin name for the plugin at the position of index/slot_index.

    Parameters:
    - index (int): Plugin position index.
    - slot_index (int, optional): Slot index for the plugin. Default is -1.
    - user_name (int, optional): Get user name for the plugin slot instead of the original plugin name.
                                Default is 0.
    - use_global_index (bool, optional): Use global channel index. Default is False.

    Returns:
    - plugin_name (str): Name of the plugin.
    """
    return flsiPlugins.getPluginName(index, slot_index, user_name, use_global_index)

def get_param_count(index, slot_index=-1, use_global_index=False):
    """
    Returns the plugin parameter count for the plugin at the position of index/slot_index.

    Parameters:
    - index (int): Plugin position index.
    - slot_index (int, optional): Slot index for the plugin. Default is -1.
    - use_global_index (bool, optional): Use global channel index. Default is False.

    Returns:
    - param_count (int): Number of parameters for the plugin.
    """
    return flsiPlugins.getParamCount(index, slot_index, use_global_index)

def get_param_name(param_index, index, slot_index=-1, use_global_index=False):
    """
    Returns the plugin parameter name for the specified parameter index.

    Parameters:
    - param_index (int): Index of the parameter.
    - index (int): Plugin position index.
    - slot_index (int, optional): Slot index for the plugin. Default is -1.
    - use_global_index (bool, optional): Use global channel index. Default is False.

    Returns:
    - param_name (str): Name of the parameter.
    """
    return flsiPlugins.getParamName(param_index, index, slot_index, use_global_index)

def get_param_value(param_index, index, slot_index=-1, use_global_index=False):
    """
    Returns the normalized value of the specified plugin parameter.

    Parameters:
    - param_index (int): Index of the parameter.
    - index (int): Plugin position index.
    - slot_index (int, optional): Slot index for the plugin. Default is -1.
    - use_global_index (bool, optional): Use global channel index. Default is False.

    Returns:
    - param_value (int): Normalized value of the parameter.
    """
    return flsiPlugins.getParamValue(param_index, index, slot_index, use_global_index)

def set_param_value(value, param_index, index, slot_index=-1, pickup_mode=flsiMidi.PIM_None, use_global_index=False):
    """
    Sets the normalized value for the specified plugin parameter.

    Parameters:
    - value (float): Normalized value to set.
    - param_index (int): Index of the parameter.
    - index (int): Plugin position index.
    - slot_index (int, optional): Slot index for the plugin. Default is -1.
    - pickup_mode (int, optional): Override FL default pickup option. Default is PIM_None.
    - use_global_index (bool, optional): Use global channel index. Default is False.

    Returns:
    - status (int): Status indicating the success of the operation.
    """
    return flsiPlugins.setParamValue(value, param_index, index, slot_index, pickup_mode, use_global_index)

def get_param_value_string(param_index, index, slot_index=-1, use_global_index=False):
    """
    Returns the plugin parameter value as a string.

    Parameters:
    - param_index (int): Index of the parameter.
    - index (int): Plugin position index.
    - slot_index (int, optional): Slot index for the plugin. Default is -1.
    - use_global_index (bool, optional): Use global channel index. Default is False.

    Returns:
    - param_value_string (str): String representation of the parameter value.
    """
    return flsiPlugins.getParamValueString(param_index, index, slot_index, use_global_index)

def get_color(index, slot_index=-1, flag=flsiMidi.GC_BackgroundColor, param_index=0, use_global_index=False):
    """
    Returns various plugin color parameter values for the plugin at the position of index/slot_index.

    Parameters:
    - index (int): Plugin position index.
    - slot_index (int, optional): Slot index for the plugin. Default is -1.
    - flag (int, optional): Color parameter flag. Default is GC_BackgroundColor.
    - param_index (int, optional): Parameter index. Default is 0.
    - use_global_index (bool, optional): Use global channel index. Default is False.

    Returns:
    - color_value (int): Value representing the color parameter.
    """
    return flsiPlugins.getColor(index, slot_index, flag, param_index, use_global_index)

def get_name(index, slot_index=-1, flag=flsiMidi.FPN_Param, param_index=0, use_global_index=False):
    """
    Returns various plugin name parameter values for the plugin at the position of index/slot_index.

    Parameters:
    - index (int): Plugin position index.
    - slot_index (int, optional): Slot index for the plugin. Default is -1.
    - flag (int, optional): Name parameter flag. Default is FPN_Param.
    - param_index (int, optional): Parameter index. Default is 0.
    - use_global_index (bool, optional): Use global channel index. Default is False.

    Returns:
    - name_value (str): Value representing the name parameter.
    """
    return flsiPlugins.getName(index, slot_index, flag, param_index, use_global_index)

def get_pad_info(chan_index, slot_index, param_option, param_index, use_global_index=False):
    """
    Returns pad parameters for the plugin at the specified position.

    Parameters:
    - chan_index (int): Channel index.
    - slot_index (int, optional): Slot index for the plugin.
    - param_option (int): Pad parameter option.
    - param_index (int): Parameter index.
    - use_global_index (bool, optional): Use global channel index. Default is False.

    Returns:
    - pad_info (str): Pad information for the specified parameters.
    """
    return flsiPlugins.getPadInfo(chan_index, slot_index, param_option, param_index, use_global_index)

def get_preset_count(index, slot_index=-1, use_global_index=False):
    """
    Returns the number of presets for the plugin at the position of index/slot_index.

    Parameters:
    - index (int): Plugin position index.
    - slot_index (int, optional): Slot index for the plugin. Default is -1.
    - use_global_index (bool, optional): Use global channel index. Default is False.

    Returns:
    - preset_count (int): Number of presets for the plugin.
    """
    return flsiPlugins.getPresetCount(index, slot_index, use_global_index)

def next_preset(index, slot_index=-1, use_global_index=False):
    """
    Navigate to the next preset in the plugin at the position of index/slot_index.

    Parameters:
    - index (int): Plugin position index.
    - slot_index (int, optional): Slot index for the plugin. Default is -1.
    - use_global_index (bool, optional): Use global channel index. Default is False.
    """
    return flsiPlugins.nextPreset(index, slot_index, use_global_index)

def prev_preset(index, slot_index=-1, use_global_index=False):
    """
    Navigate to the previous preset in the plugin at the position of index/slot_index.

    Parameters:
    - index (int): Plugin position index.
    - slot_index (int, optional): Slot index for the plugin. Default is -1.
    - use_global_index (bool, optional): Use global channel index. Default is False.
    """
    return flsiPlugins.prevPreset(index, slot_index, use_global_index)

# launchMapMapPages module
# Assume flsiLaunchMapPages is the module providing the underlying functionality

def init_launch_map_pages(device_name, width, height):
    """
    Initialize launchmap pages.

    Parameters:
    - device_name (str): Name of the device.
    - width (int): Width of the launchmap.
    - height (int): Height of the launchmap.
    """
    flsiLaunchMapPages.init(device_name, width, height)

def create_overlay_map(off_color, on_color, width, height):
    """
    Creates overlay map.

    Parameters:
    - off_color (int): Color when the item is off.
    - on_color (int): Color when the item is on.
    - width (int): Width of the overlay map.
    - height (int): Height of the overlay map.
    """
    flsiLaunchMapPages.createOverlayMap(off_color, on_color, width, height)

def get_launch_map_pages_length():
    """
    Returns launchmap pages length.

    Returns:
    - length (int): Length of the launchmap pages.
    """
    return flsiLaunchMapPages.length()

def update_launch_map_page(index):
    """
    Updates launchmap page at "index".

    Parameters:
    - index (int): Index of the launchmap page to update.
    """
    flsiLaunchMapPages.updateMap(index)

def get_map_item_color(index, item_index):
    """
    Returns color at "item_index" of page at "index".

    Parameters:
    - index (int): Index of the launchmap page.
    - item_index (int): Index of the item on the page.

    Returns:
    - color (int): Color of the specified item.
    """
    return flsiLaunchMapPages.getMapItemColor(index, item_index)

def get_map_count(index):
    """
    Returns length of items of page at "index".

    Parameters:
    - index (int): Index of the launchmap page.

    Returns:
    - count (int): Length of items on the specified page.
    """
    return flsiLaunchMapPages.getMapCount(index)

def get_map_item_channel(index, item_index):
    """
    Returns destination channel at "item_index" of page at "index".

    Parameters:
    - index (int): Index of the launchmap page.
    - item_index (int): Index of the item on the page.

    Returns:
    - channel (int): Destination channel of the specified item.
    """
    return flsiLaunchMapPages.getMapItemChannel(index, item_index)

def get_map_item_aftertouch(index, item_index):
    """
    Returns aftertouch for item at "item_index" of page at "index".

    Parameters:
    - index (int): Index of the launchmap page.
    - item_index (int): Index of the item on the page.

    Returns:
    - aftertouch (int): Aftertouch value for the specified item.
    """
    return flsiLaunchMapPages.getMapItemAftertouch(index, item_index)

def process_map_item(event_data, index, item_index, velocity):
    """
    Process map item at "item_index" of page at "index".

    Parameters:
    - event_data: Event data for the process.
    - index (int): Index of the launchmap page.
    - item_index (int): Index of the item on the page.
    - velocity (int): Velocity value for the item.
    """
    flsiLaunchMapPages.processMapItem(event_data, index, item_index, velocity)

def release_map_item(event_data, index):
    """
    Release map item at "item_index" of page at "index".

    Parameters:
    - event_data: Event data for the release.
    - index (int): Index of the launchmap page.
    """
    flsiLaunchMapPages.releaseMapItem(event_data, index)

def check_map_for_hidden_item():
    """
    Checks for launchpad hidden item.
    """
    flsiLaunchMapPages.checkMapForHiddenItem()

def set_map_item_target(index, item_index, target):
    """
    Set target for item at "item_index" of page at "index".

    Parameters:
    - index (int): Index of the launchmap page.
    - item_index (int): Index of the item on the page.
    - target (int): Target value for the item.
    """
    flsiLaunchMapPages.setMapItemTarget(index, item_index, target)

# MixerModule
# Assume flsiMixer is the module providing the underlying functionality

def track_number() -> int:
    """
    Returns the index of the currently selected mixer track.
    """
    return flsiMixer.trackNumber()

def get_track_info(mode: int) -> int:
    """
    Returns track info.

    Parameters:
    - mode (int): Mode parameter for track info.

    Returns:
    - int: Result of track info.
    """
    return flsiMixer.getTrackInfo(mode)

def set_track_number(track_number: int, flags: int = -1):
    """
    Sets the currently selected mixer track.

    Parameters:
    - track_number (int): Index of the mixer track to set.
    - flags (int): Optional flags parameter.
    """
    flsiMixer.setTrackNumber(track_number, flags)

def track_count() -> int:
    """
    Returns the number of tracks.
    """
    return flsiMixer.trackCount()

def get_track_name(index: int, max_len: int = -1) -> str:
    """
    Returns the name of the track at "index".

    Parameters:
    - index (int): Index of the track.
    - max_len (int): Optional maximum length parameter.

    Returns:
    - str: Name of the track.
    """
    return flsiMixer.getTrackName(index, max_len)

def set_track_name(index: int, name: str):
    """
    Changes the name of the track at "index" to "name".

    Parameters:
    - index (int): Index of the track.
    - name (str): New name for the track.
    """
    flsiMixer.setTrackName(index, name)

def get_track_color(index: int) -> int:
    """
    Returns the color of the track at "index".

    Parameters:
    - index (int): Index of the track.

    Returns:
    - int: Color of the track.
    """
    return flsiMixer.getTrackColor(index)

def set_track_color(index: int, color: int):
    """
    Changes the color of the track at "index" to "color".

    Parameters:
    - index (int): Index of the track.
    - color (int): New color for the track.
    """
    flsiMixer.setTrackColor(index, color)

def is_track_armed(index: int) -> bool:
    """
    Returns True if the track at "index" is armed.

    Parameters:
    - index (int): Index of the track.

    Returns:
    - bool: True if the track is armed, False otherwise.
    """
    return flsiMixer.isTrackArmed(index)

def arm_track(index: int):
    """
    Toggle the armed state of the track at "index".

    Parameters:
    - index (int): Index of the track.
    """
    flsiMixer.armTrack(index)

def is_track_solo(index: int) -> bool:
    """
    Returns True if the track at "index" is soloed.

    Parameters:
    - index (int): Index of the track.

    Returns:
    - bool: True if the track is soloed, False otherwise.
    """
    return flsiMixer.isTrackSolo(index)

def solo_track(index: int, value: int = -1, mode: int = -1):
    """
    Without value, this function will toggle the solo state of the track at "index".
    Set optional 'value' to 1 to solo track or to 0 to unsolo track.

    Parameters:
    - index (int): Index of the track.
    - value (int): Optional value parameter.
    - mode (int): Optional mode parameter.
    """
    flsiMixer.soloTrack(index, value, mode)

def is_track_enabled(index: int) -> bool:
    """
    Returns True if the track at "index" is enabled.

    Parameters:
    - index (int): Index of the track.

    Returns:
    - bool: True if the track is enabled, False otherwise.
    """
    return flsiMixer.isTrackEnabled(index)

def is_track_automation_enabled(index: int, plug_index: int) -> bool:
    """
    Returns True if the track at "index" has automation enabled.

    Parameters:
    - index (int): Index of the track.
    - plug_index (int): Plugin index.

    Returns:
    - bool: True if automation is enabled, False otherwise.
    """
    return flsiMixer.isTrackAutomationEnabled(index, plug_index)

def enable_track(index: int):
    """
    Toggle the enabled state of the track at "index".

    Parameters:
    - index (int): Index of the track.
    """
    flsiMixer.enableTrack(index)

def is_track_muted(index: int) -> bool:
    """
    Returns True if the track at "index" is muted.

    Parameters:
    - index (int): Index of the track.

    Returns:
    - bool: True if the track is muted, False otherwise.
    """
    return flsiMixer.isTrackMuted(index)

def mute_track(index: int, value: int = -1):
    """
    Toggles the Mute status of the track at "index" if value is default.
    Otherwise mutes track if value is 1 and unmutes if value is 0.

    Parameters:
    - index (int): Index of the track.
    - value (int): Optional value parameter.
    """
    flsiMixer.muteTrack(index, value)

def is_track_mute_lock(index: int) -> bool:
    """
    Returns True if the Mute for the track at "index" is locked.

    Parameters:
    - index (int): Index of the track.

    Returns:
    - bool: True if mute is locked, False otherwise.
    """
    return flsiMixer.isTrackMuteLock(index)

def get_track_plugin_id(index: int, plug_index: int) -> int:
    """
    Returns the plugin id of the plugin with plug_index on the track at "index".

    Parameters:
    - index (int): Index of the track.
    - plug_index (int): Plugin index.

    Returns:
    - int: Plugin id.
    """
    return flsiMixer.getTrackPluginId(index, plug_index)

def is_track_plugin_valid(index: int, plug_index: int) -> bool:
    """
    Returns True if the plugin with plug_index on the track at "index" is valid.

    Parameters:
    - index (int): Index of the track.
    - plug_index (int): Plugin index.

    Returns:
    - bool: True if the plugin is valid, False otherwise.
    """
    return flsiMixer.isTrackPluginValid(index, plug_index)

def get_track_volume(index: int, mode: int = 0) -> float:
    """
    Returns the normalized volume (between 0 and 1.0) of the track at "index".
    Set optional mode to 1 to get volume in dB.

    Parameters:
    - index (int): Index of the track.
    - mode (int): Optional mode parameter.

    Returns:
    - float: Normalized volume.
    """
    return flsiMixer.getTrackVolume(index, mode)

def set_track_volume(index: int, volume: float, pickup_mode: int = flsiMidi.PIM_None):
    """
    Changes the volume of the track at "index".
    Volume is a value between 0 and 1.0.
    Use optional pickup_mode to override FL default pickup option.

    Parameters:
    - index (int): Index of the track.
    - volume (float): New volume for the track.
    - pickup_mode (int): Optional pickup mode parameter.
    """
    flsiMixer.setTrackVolume(index, volume, pickup_mode)

def get_track_pan(index: int) -> float:
    """
    Returns the pan value (between -1.0 and 1.0) for the track at "index".

    Parameters:
    - index (int): Index of the track.

    Returns:
    - float: Pan value.
    """
    return flsiMixer.getTrackPan(index)

def set_track_pan(index: int, pan: float, pickup_mode: int = flsiMidi.PIM_None):
    """
    Changes the panning for the track at "index".
    "pan" pan value is between -1.0 and 1.0.
    Use optional pickup_mode to override FL default pickup option.

    Parameters:
    - index (int): Index of the track.
    - pan (float): New pan value for the track.
    - pickup_mode (int): Optional pickup mode parameter.
    """
    flsiMixer.setTrackPan(index, pan, pickup_mode)

def get_track_stereo_sep(index: int, pickup: int = 1) -> float:
    """
    Returns the stereo separation value (between -1.0 and 1.0) for the track at "index".
    Set optional 'pickup' to 1 to use pickup function, or to 2 to follow FL global pickup setting.

    Parameters:
    - index (int): Index of the track.
    - pickup (int): Optional pickup parameter.

    Returns:
    - float: Stereo separation value.
    """
    return flsiMixer.getTrackStereoSep(index, pickup)

def set_track_stereo_sep(index: int, sep: float, pickup: int = 0):
    """
    Changes the stereo separation for the track at "index".
    "sep" sep value is between -1.0 and 1.0.

    Parameters:
    - index (int): Index of the track.
    - sep (float): New stereo separation value for the track.
    - pickup (int): Optional pickup parameter.
    """
    flsiMixer.setTrackStereoSep(index, sep, pickup)

def is_track_selected(index: int) -> bool:
    """
    Returns True if the track at "index" is selected.

    Parameters:
    - index (int): Index of the track.

    Returns:
    - bool: True if the track is selected, False otherwise.
    """
    return flsiMixer.isTrackSelected(index)

def select_track(index: int):
    """
    Toggle selection of the track at "index".

    Parameters:
    - index (int): Index of the track.
    """
    flsiMixer.selectTrack(index)

def set_active_track(index: int):
    """
    Exclusively select the track at "index".

    Parameters:
    - index (int): Index of the track.
    """
    flsiMixer.setActiveTrack(index)

def select_all():
    """
    Select all mixer tracks.
    """
    flsiMixer.selectAll()

def deselect_all():
    """
    Deselect all mixer tracks.
    """
    flsiMixer.deselectAll()

def set_route_to(index: int, dest_index: int, value: int):
    """
    Set route for track at "index" to "dest_index".

    Parameters:
    - index (int): Index of the track.
    - dest_index (int): Destination index.
    - value (int): Value parameter.
    """
    flsiMixer.setRouteTo(index, dest_index, value)

def get_route_send_active(index: int, dest_index: int) -> bool:
    """
    Returns True if route sends from track at "index" to "dest_index" is active.

    Parameters:
    - index (int): Index of the track.
    - dest_index (int): Destination index.

    Returns:
    - bool: True if route sends are active, False otherwise.
    """
    return flsiMixer.getRouteSendActive(index, dest_index)

def after_routing_changed():
    """
    Notify FL about routing changes.
    """
    flsiMixer.afterRoutingChanged()

def get_event_value(index: int, value: int = flsiMidi.MaxInt, smooth_target: int = 1) -> int:
    """
    Returns event value from MIDI.

    Parameters:
    - index (int): Index of the track.
    - value (int): Optional value parameter.
    - smooth_target (int): Optional smooth target parameter.

    Returns:
    - int: Event value.
    """
    return flsiMixer.getEventValue(index, value, smooth_target)

def remote_find_event_value(index: int, flags: int = 0) -> float:
    """
    Returns event value.

    Parameters:
    - index (int): Index of the track.
    - flags (int): Optional flags parameter.

    Returns:
    - float: Event value.
    """
    return flsiMixer.remoteFindEventValue(index, flags)

def get_event_id_name(index: int, short_name: int = 0) -> str:
    """
    Returns event name.

    Parameters:
    - index (int): Index of the track.
    - short_name (int): Optional short name parameter.

    Returns:
    - str: Event name.
    """
    return flsiMixer.getEventIDName(index, short_name)

def get_event_id_value_string(index: int, value: int) -> str:
    """
    Returns event value as string.

    Parameters:
    - index (int): Index of the track.
    - value (int): Event value.

    Returns:
    - str: Event value as string.
    """
    return flsiMixer.getEventIDValueString(index, value)

def get_auto_smooth_event_value(index: int, locked: int = 1) -> int:
    """
    Returns auto smooth event value.

    Parameters:
    - index (int): Index of the track.
    - locked (int): Optional locked parameter.

    Returns:
    - int: Auto smooth event value.
    """
    return flsiMixer.getAutoSmoothEventValue(index, locked)

# Assume flsiMixer is the module providing the underlying functionality

def automate_event(index, value, flags, speed=0, is_increment=0, res=flsiMidi.EKRes):
    """
    Automate event.

    Parameters:
    - index (int): Index of the event.
    - value (int): Value of the event.
    - flags (int): Flags for the event.
    - speed (int): Speed of automation (optional, default is 0).
    - is_increment (int): Flag indicating if the value is an increment (optional, default is 0).
    - res (float): Resolution for the event (optional, default is EKRes).

    Returns:
    None
    """
    flsiMixer.automateEvent(index, value, flags, speed, is_increment, res)

def get_track_peaks(index, mode):
    """
    Returns peaks for track at "index".

    Parameters:
    - index (int): Index of the track.
    - mode (int): Mode for peak retrieval.

    Returns:
    - peaks (float): Peaks value between 0 (silence) and 1 (0db) or < 1 (clipping).
    """
    return flsiMixer.getTrackPeaks(index, mode)

def get_track_recording_file_name(index):
    """
    Returns recording file name for track at "index".

    Parameters:
    - index (int): Index of the track.

    Returns:
    - file_name (str): Recording file name.
    """
    return flsiMixer.getTrackRecordingFileName(index)

def link_track_to_channel(mode):
    """
    Link track to channel.

    Parameters:
    - mode (int): Mode for linking. ROUTE_ToThis = 0, ROUTE_StartingFromThis = 1.

    Returns:
    None
    """
    flsiMixer.linkTrackToChannel(mode)

def link_channel_to_track(channel, track, select=0):
    """
    Link channel to track.

    Parameters:
    - channel (int): Channel index respecting groups.
    - track (int): Track index.
    - select (int): Optional flag to make track selected (default is 0).

    Returns:
    None
    """
    flsiMixer.linkChannelToTrack(channel, track, select)

def get_song_step_pos():
    """
    Returns song step position.

    Returns:
    - step_pos (int): Song step position.
    """
    return flsiMixer.getSongStepPos()

def get_current_tempo(as_int=0):
    """
    Returns current tempo.

    Parameters:
    - as_int (int): Optional flag to get result as int (default is 0).

    Returns:
    - tempo (int/float): Current tempo.
    """
    return flsiMixer.getCurrentTempo(as_int)

def get_rec_pps():
    """
    Returns recording pps.

    Returns:
    - rec_pps (int): Recording pps.
    """
    return flsiMixer.getRecPPS()

def get_song_tick_pos(mode=flsiMidi.ST_Int):
    """
    Returns song ticks position.

    Parameters:
    - mode (int): Mode for tick position retrieval (default is ST_Int).

    Returns:
    - tick_pos (int/float): Song ticks position.
    """
    return flsiMixer.getSongTickPos(mode)

def get_last_peak_vol(section):
    """
    Returns last peak volume.

    Parameters:
    - section (int): Section for peak volume retrieval (0 for left, 1 for right).

    Returns:
    - peak_vol (float): Last peak volume.
    """
    return flsiMixer.getLastPeakVol(section)

def get_track_dock_side(index):
    """
    Returns dock side of the mixer track.

    Parameters:
    - index (int): Index of the mixer track.

    Returns:
    - dock_side (int): Dock side (0 = left, 1 = center, 2 = right).
    """
    return flsiMixer.getTrackDockSide(index)

def is_track_slots_enabled(index):
    """
    Returns state of mixer track 'Enable effect slots' option.

    Parameters:
    - index (int): Index of the mixer track.

    Returns:
    - enabled (int): State of the 'Enable effect slots' option.
    """
    return flsiMixer.isTrackSlotsEnabled(index)

def enable_track_slots(index, value=-1):
    """
    Toggle mixer track 'Enable effect slots' option.

    Parameters:
    - index (int): Index of the mixer track.
    - value (int): Toggle value (-1 = toggle, 0 = disable, 1 = enable, default is -1).

    Returns:
    None
    """
    flsiMixer.enableTrackSlots(index, value)

def is_track_rev_polarity(index):
    """
    Returns state of mixer track 'reverse polarity' option.

    Parameters:
    - index (int): Index of the mixer track.

    Returns:
    - rev_polarity (int): State of the 'reverse polarity' option.
    """
    return flsiMixer.isTrackRevPolarity(index)

def rev_track_polarity(index, value=-1):
    """
    Toggle mixer track 'reverse polarity' option.

    Parameters:
    - index (int): Index of the mixer track.
    - value (int): Toggle value (-1 = toggle, 0 = disable, 1 = enable, default is -1).

    Returns:
    None
    """
    flsiMixer.revTrackPolarity(index, value)

def is_track_swap_channels(index):
    """
    Returns state of mixer track 'swap l/r channels' option.

    Parameters:
    - index (int): Index of the mixer track.

    Returns:
    - swap_channels (int): State of the 'swap l/r channels' option.
    """
    return flsiMixer.isTrackSwapChannels(index)

def swap_track_channels(index, value=-1):
    """
    Toggle mixer track 'swap l/r channels' option.

    Parameters:
    - index (int): Index of the mixer track.
    - value (int): Toggle value (-1 = toggle, 0 = disable, 1 = enable, default is -1).

    Returns:
    None
    """
    flsiMixer.swapTrackChannels(index, value)

def focus_editor(index, plug_index):
    """
    Focus editor (plugin window) for plug_index on the track at "index".

    Parameters:
    - index (int): Index of the mixer track.
    - plug_index (int): Index of the plugin.

    Returns:
    None
    """
    flsiMixer.focusEditor(index, plug_index)

def get_active_effect_index():
    """
    Returns tracks index and plugIndex for focused effect editor or None if no effect editor is focused.

    Returns:
    - active_effect_index (tuple): Tracks index and plugIndex for focused effect editor.
    - None: If no effect editor is focused.
    """
    return flsiMixer.getActiveEffectIndex()


# Assume flsiGeneral is the module providing the underlying functionality

def save_undo(undo_name, flags, update_history=1):
    """
    Saves undo history point (level).
    Set optional update_history parameter to 0 to hide undo point in browser history.
    
    Parameters:
    - undo_name (str): Name of the undo.
    - flags (int): Flags for undo operation.
    - update_history (int, optional): Update history flag. Default is 1.

    Returns:
    - None
    """
    flsiGeneral.saveUndo(undo_name, flags, update_history)

def undo():
    """
    Undo last history level.
    This function mimics FL Studio CTRL+Z functionality: it steps forward through the history,
    unless you are at the latest step (in this case, undo works as the standard one step undo/redo shortcut).

    Returns:
    - int: Result of the undo operation.
    """
    return flsiGeneral.undo()

def undo_up():
    """
    Move up in undo history (up one level).

    Returns:
    - int: Result of the undo up operation.
    """
    return flsiGeneral.undoUp()

def undo_down():
    """
    Move down in undo history (down one level).

    Returns:
    - int: Result of the undo down operation.
    """
    return flsiGeneral.undoDown()

def undo_up_down(offset):
    """
    Move up or down in undo history by offset.

    Parameters:
    - offset (int): Offset value for the undo operation.

    Returns:
    - int: Result of the undo up/down operation.
    """
    return flsiGeneral.undoUpDown(offset)

def restore_undo_level(level):
    """
    Restore to a specific undo point (level).

    Parameters:
    - level (int): Undo level to restore.

    Returns:
    - None
    """
    flsiGeneral.restoreUndoLevel(level)

def get_undo_level_hint():
    """
    Returns undo level hint.

    Returns:
    - str: Undo level hint.
    """
    return flsiGeneral.getUndoLevelHint()

def get_undo_history_pos():
    """
    Returns undo history position.

    Returns:
    - int: Undo history position.
    """
    return flsiGeneral.getUndoHistoryPos()

def get_undo_history_count():
    """
    Returns undo history length.

    Returns:
    - int: Undo history count.
    """
    return flsiGeneral.getUndoHistoryCount()

def get_undo_history_last():
    """
    Returns last undo history position.

    Returns:
    - int: Last undo history position.
    """
    return flsiGeneral.getUndoHistoryLast()

def set_undo_history_pos(index):
    """
    Set undo history position.

    Parameters:
    - index (int): Undo history position.

    Returns:
    - None
    """
    flsiGeneral.setUndoHistoryPos(index)

def set_undo_history_count(value):
    """
    Set undo history count.

    Parameters:
    - value (int): Undo history count.

    Returns:
    - None
    """
    flsiGeneral.setUndoHistoryCount(value)

def set_undo_history_last(index):
    """
    Set undo history last position.

    Parameters:
    - index (int): Undo history last position.

    Returns:
    - None
    """
    flsiGeneral.setUndoHistoryLast(index)

def get_rec_ppb():
    """
    Returns the current time signature value. (Timebase * Numerator).

    Returns:
    - int: Current time signature value.
    """
    return flsiGeneral.getRecPPB()

def get_rec_ppq():
    """
    Returns the current timebase (PPQ).

    Returns:
    - int: Current timebase (PPQ).
    """
    return flsiGeneral.getRecPPQ()

def get_use_metronome():
    """
    Returns True when the metronome is used.

    Returns:
    - int: Metronome usage status.
    """
    return flsiGeneral.getUseMetronome()

def get_precount():
    """
    Returns precount value.

    Returns:
    - int: Precount value.
    """
    return flsiGeneral.getPrecount()

def get_changed_flag():
    """
    Get FL Studio project "changed" flag.
    Result is one of the: 0 = clean, 1 = dirty, 2 = dirty but clean for autosave.

    Returns:
    - int: Project changed flag.
    """
    return flsiGeneral.getChangedFlag()

def get_version():
    """
    Returns Midi scripting API version number.

    Returns:
    - int: MIDI scripting API version number.
    """
    return flsiGeneral.getVersion()

def restore_undo_deprecated():
    """
    Deprecated, use undo.

    Returns:
    - int: Result of the restore undo operation.
    """
    return flsiGeneral.restoreUndo()

def process_rec_event(event_id, value, flags):
    """
    Process recorded event for event with eventID.
    Use this function to do various operations (specified by flags) with FL Studio recorded events.
    You can, for example, set or get event values.
    Function will return event value or REC_InvalidID (for an invalid eventID).

    Parameters:
    - event_id (int): Event ID for the recorded event.
    - value (int): Value for the recorded event.
    - flags (int): Flags specifying the operation.

    Returns:
    - int: Result of the process REC event operation.
    """
    return flsiGeneral.processRECEvent(event_id, value, flags)

def dump_score_log(time, silent=0):
    """
    Dump score log, specify time to dump (time),
    use optional (silent) flag to suppress a message when the score is empty.

    Parameters:
    - time (int): Time to dump the score log.
    - silent (int, optional): Silent flag. Default is 0.

    Returns:
    - None
    """
    flsiGeneral.dumpScoreLog(time, silent)

def clear_log():
    """
    Clear log.

    Returns:
    - None
    """
    flsiGeneral.clearLog()

def safe_to_edit():
    """
    Returns 1 when safe to use setter functions.

    Returns:
    - int: Safe to edit flag.
    """
    return flsiGeneral.safeToEdit()
