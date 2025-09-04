# pylint: disable=line-too-long
'''
Midas Control Data
    - Manufacturer: Arturia
    - Device Name: MINILAB MKII
    - Device ID: 0x20 0x6B 0x7F 0x42

Adater Setup Notes:
    - Midi Controls are editable in the MIDI Control Center, an Arturia application.
    - The controls are stored in a file with the extension .mcc
    - This adapter assume the user has set the controls using the included .mcc file.
    - The minilab mk2 has 8 memory slots for storing .mcc file settings.
    - The first memory slot is reserved for the default Analog Lab settings.(index 0)
    - The last memory slot is reserved for Ableton Live Mode.(index 7)
    - The adapter will assume the user has stored the .mcc file in the 6th user memory 7(index 6).
    - All knobs except the 2 shift knobs are set to absolute mode.
    - The shift knobs are set to relative mode type 1.
    - **DO NOT** set the keyboard midi channel to 16, used for the pads in our .mcc preset.
Adapter Setup instructions:
    1. Download the .mcc file from the github repo.
    2. Open the MIDI Control Center application.
    3. Click the "Import" button and select the .mcc file.
    4. Choose the 7th memory slot.
    5. Click the "Write" button to write the settings to the device.

Controller Mapping Notes:
    - This device uses standard midi messages for its controls.
    - The device uses sysex messages for the Shift, Octave, and Pad buttons.
    - Keyboard MIDI Channel can be set by holding shift and clicking a corresponding channel key.
    - The device will not report a change in Keyboard Midi Channel.
    - Device memory can be changed by holding shift and clicking a corresponding pad.
    - The device will send a sysex message to report a change in device memory.
    - The knob 1 and 9 CC switch will be considered a button control.
    - There are device commands for setting the type of signal sent from a controller
        but the information is not available.
    - Sysex message for setting pad color and value has been extracted from
        the Official Fl Studio Minilab Mk2 python script.

Controller Mappings:
| Input | Signals sent from the device.
    | Control Type | MIDI
    Knob:   | Name              | Midi Status       | Midi Channel(port)        | Midi Data1(note)  | Midi Data2(value) | Control Type      | Control Modes     | Led Colors        | Led Modes     |
            | Knob 1-16:        | Control Change    | 0-14(Keyboard Channel)    | 0-15              | Any               | Knob              | Absolute          | None              | None          |
            | ShiftKnob1:       | Control Change    | 0-14(Keyboard Channel)    | 16                | Any               | Knob              | Relative          | None              | None          |
            | ShiftKnob9:       | Control Change    | 0-14(Keyboard Channel)    | 17                | Any               | Knob              | Relative          | None              | None          |
    Faders:
            | Modulator 1-16:    | Control Change    | 0-14(Keyboard Channel)    | 100               | Any               | Fader             | Absolute          | None              | None          |
            | SustainPedal:      | Control Change    | 0-14(Keyboard Channel)    | 101               | Any               | Fader             | Absolute          | None              | None          |
    Buttons:
            | Pad 1-8/9-16:      | Note On           | 15(Pad Channel)           | 0-15              | Any               | Button            | Gate            | None              | None          |
            | Pad 1-8/9-16:      | Note Off          | 15(Pad Channel)           | 0-15              | Any               | Button            | Gate            | None              | None          |
            | Pad 1-8/9-16:      | Key Aftertouch    | 15(Pad Channel)           | 0-15              | Any               | Button            | Gate            | None              | None          |

            | Keyboard 0-127:    | Note On           | 0-14(Keyboard Channel)    | 0-127             | Any               | Button            | Gate              | None              | None          |

            | PressKnob1:        | Control Change    | 0-14(Keyboard Channel)    | 16                | 127 or 0              | Button            | Gate              | None              | None          |
            | PressKnob9:        | Control Change    | 0-14(Keyboard Channel)    | 17                | 127 or 0              | Button            | Gate              | None              | None          |
    Pitch Bend:
            | Pitch Bend:        | Pitch Bend        | 0-14(Keyboard Channel)    | Any               | Any               | Pitch Bend        | Absolute          | None              | None          |

    | Control Type | Sysex
    Buttons:
            | Shift Button: | Start Sysex | Device ID | Sysex Command | Target | Value | End Sysex |
                | Pressed:  F0  (00  20  6B  7F  42)  (02  00  00)  2E  7F  F7  |  Sysex
                | Released: F0  (00  20  6B  7F  42)  (02  00  00)  2E  00  F7  |  Sysex
            | Octave - Button:  |
                | Pressed:  F0  (00  20  6B  7F  42)  (02  00  00)  10  7F  F7  |  Sysex
                | Released: F0  (00  20  6B  7F  42)  (02  00  00)  10  00  F7  |  Sysex
            | Octave + Button:  |
                | Pressed:  F0  (00  20  6B  7F  42)  (02  00  00)  11  7F  F7  |  Sysex
                | Released: F0  (00  20  6B  7F  42)  (02  00  00)  11  00  F7  |  Sysex
            | Pad 1-8/9-16 Button:  |
                | Pressed:  F0  (00  20  6B  7F  42)  (02  00  00)  2F  7F  F7  |  Sysex
                | Released: F0  (00  20  6B  7F  42)  (02  00  00)  2F  00  F7  |  Sysex

            | Memchange 1-8:  |
                | F0  (00  20  6B  7F  42)  (1B)  [00-07(mem index #)]  F7  |  Sysex

| Output | Signals sent to the device.
    | Control Type | Sysex
    Buttons:
            | SetPadLights: | Start Sysex | Device ID | Sysex Command | Target | Pad # | Color | End Sysex |
                | F0  (00  20  6B  7F  42)  (02  00  10)  (pad #)  (color)  F7  |  Sysex
                     Arg1 Options: 70-77(1-8)  78-7F(9-16)
                     Arg2 Options: 0(None)  1(Red)  4(Green)  5(Yellow)  16(Blue)  17(Purple)  20(Cyan)  127(White)


Additional Notes:
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

    SetPadLights: Sysex Message (output) |
        Sets the color of the pads.
        F0  [00  20  6B  7F  42]  [02  00  10]  [(pad #)]  [(color)]  F7  |  Sysex

    Color Bytes:
        NONE = 0 # 0x00
        RED = 1 # 0x01
        WHITE = 127 # 0x7F
        GREEN = 4 # 0x04
        YELLOW = 5 # 0x05
        BLUE = 16 # 0x10
        CYAN = 20 # 0x14
        PURPLE = 17 # 0x11

    Pad Bytes:
        1-8 = 70-77
        9-16 = 78-7F

    Memory Index Bytes:
        1-8 = 00-07

    ButtonState Bytes:
        PRESSED = 7F # 127
        RELEASED = 00 # 0
'''
# pylint: enable=line-too-long
import mdds_standard as mdds

__CONTROL_IDGEN = mdds.UIIDGenerator()
''' For generating unique ids for controls '''

def make_control_name(name : str, number : str = None):
    ''' Accessibility method to generate an dictionary entry for a control,
        Appends an underscore followed by the number to the name.
        Automatically generates a unique id for the control.
        Refers to the global instance of UIIDGenerator named minilabmk2_data.__CONTROL_IDGEN.
    '''
    if number is not None:
        name += "_" + number
    return name


# Midas Control Data
MANUFACTURER = "Arturia"
NAME = "Minilabmk2"
ID = bytes([0x00, 0x20, 0x6B, 0x7F, 0x42])

KnobControls = {make_control_name("Knob", str(i+1)) : __CONTROL_IDGEN() for i in range(16)}
PadControls = {make_control_name("Pad", str(i+1)) : __CONTROL_IDGEN() for i in range(16)}
KeyboardButtonControls = {make_control_name(
    "KeyboardButton_" + chr(65 + i % 7) + str((i // 7) + 4))  : __CONTROL_IDGEN()
    for i in range(25)
 } # 25 Keys, Middle C is the 6th key when Octave is 0.

ModulatorControl = {make_control_name("Modulator")  : __CONTROL_IDGEN()}
PitchBendControl = {make_control_name("PitchBend") : __CONTROL_IDGEN()}
SustainPedalControl = {make_control_name("SustainPedal") : __CONTROL_IDGEN()}
ShiftButtonControl = {make_control_name("ShiftButton") : __CONTROL_IDGEN()}
OctaveUpButtonControl = {make_control_name("OctaveUpButton") : __CONTROL_IDGEN()}
OctaveDownButtonControl = {make_control_name("OctaveDownButton") : __CONTROL_IDGEN()}
Pad18916ButtonControl = {make_control_name("Pad18916Button") : __CONTROL_IDGEN()}

Controls = {**KnobControls ,**PadControls, **KeyboardButtonControls,
            **ModulatorControl, **PitchBendControl, **SustainPedalControl,
            **ShiftButtonControl, **OctaveUpButtonControl, **OctaveDownButtonControl,
            **Pad18916ButtonControl}

KnobControlsOutputMessages = { knob_id :
    {knob_name + "_ControlChange" : (mdds.eDefaultMidiStatus.control_change,(0,15),(0,15),None)}
    for knob_name,knob_id in KnobControls.items()
}

PadControlsOutputMessages = { pad_id :
    {pad_name + "_NoteOn" : (mdds.eDefaultMidiStatus.note_on,(15,15),(0,15),None),
     pad_name + "_NoteOff" : (mdds.eDefaultMidiStatus.note_off,(15,15),(0,15),None),
     pad_name + "_KeyAftertouch" : (mdds.eDefaultMidiStatus.aftertouch,(15,15),(0,15),None)}
    for pad_name,pad_id in PadControls.items()
}

KeyboardButtonControlsOutputMessages = { keyboard_button_id :
    {keyboard_button_name + "_NoteOn" : (mdds.eDefaultMidiStatus.note_on,(0,14),(0,127),None),
     keyboard_button_name + "_NoteOff" : (mdds.eDefaultMidiStatus.note_off,(0,14),(0,127),None)}
    for keyboard_button_name,keyboard_button_id in KeyboardButtonControls.items()
}

ModulatorControlOutputMessages = { modulator_control_id :
    {modulator_control_name + "_ControlChange" : (mdds.eDefaultMidiStatus.control_change,(0,15),100,None)}
    for modulator_control_name,modulator_control_id in ModulatorControl.items()
}

SustainPedalControlOutputMessages = { sustain_pedal_control_id :
    {sustain_pedal_control_name + "_ControlChange" : (mdds.eDefaultMidiStatus.control_change,(0,15),101,None)}
    for sustain_pedal_control_name,sustain_pedal_control_id in SustainPedalControl.items()
}

PitchBendControlOutputMessages = { pitch_bend_control_id :
    {pitch_bend_control_name + "_PitchBend" : (mdds.eDefaultMidiStatus.pitch_bend,(0,15),None,None)}
    for pitch_bend_control_name,pitch_bend_control_id in PitchBendControl.items()
}

ShiftButtonControlOutputMessages = { list(ShiftButtonControl.values())[0] :
    { list(ShiftButtonControl.keys())[0] + "_SysexNoteState" : (mdds.eDefaultMidiStatus.system_exclusive,
                                                          mdds.nbyte(0x02,0x00,0x00),   # Command Id
                                                          mdds.byte(0x2E),              # Target Id
                                                          [mdds.byte(0x7F),             # Value On: 127, Off: 0
                                                            mdds.byte(0x00)])
    }
}

OctaveDownButtonControlOutputMessages = { list(OctaveDownButtonControl.values())[0] :
    { list(OctaveDownButtonControl.keys())[0] + "_SysexNoteState" : (mdds.eDefaultMidiStatus.system_exclusive,
                                                               mdds.nbyte(0x02,0x00,0x00),   # Command Id
                                                               mdds.byte(0x10),              # Target Id
                                                               [mdds.byte(0x7F),             # Value On: 127, Off: 0
                                                                mdds.byte(0x00)])
    }
}

OctaveUpButtonControlOutputMessages = { list(OctaveUpButtonControl.values())[0] :
    { list(OctaveUpButtonControl.keys())[0] + "_SysexNoteState" : (mdds.eDefaultMidiStatus.system_exclusive,
                                                             mdds.nbyte(0x02,0x00,0x00),   # Command Id
                                                             mdds.byte(0x11),              # Target Id
                                                             [mdds.byte(0x7F),             # Value On: 127, Off: 0
                                                              mdds.byte(0x00)])
    }
}

Pad18916ButtonControlOutputMessages = { list(Pad18916ButtonControl.values())[0] :
    { list(Pad18916ButtonControl.keys())[0] + "_SysexNoteState" : (mdds.eDefaultMidiStatus.system_exclusive,
                                                             mdds.nbyte(0x02,0x00,0x00),   # Command Id
                                                             mdds.byte(0x2F),              # Target Id
                                                             [mdds.byte(0x7F),             # Value On: 127, Off: 0
                                                              mdds.byte(0x00)])
    }
}

AnonymousOutputMessages = { None : { "_SysexSetMemory" : (mdds.eDefaultMidiStatus.system_exclusive,
                                                    mdds.nbyte(0x1B),   # Command Id
                                                    mdds.byte(0x00),    # Target Id
                                                    (mdds.byte(0x00),mdds.byte(0x7)))} # Value
    }

ControlsOutputMessages = {**KnobControlsOutputMessages, **PadControlsOutputMessages, \
                            **KeyboardButtonControlsOutputMessages, **ModulatorControlOutputMessages, \
                            **PitchBendControlOutputMessages, **SustainPedalControlOutputMessages, \
                            **ShiftButtonControlOutputMessages, **OctaveUpButtonControlOutputMessages, \
                            **OctaveDownButtonControlOutputMessages, **Pad18916ButtonControlOutputMessages, \
                            **AnonymousOutputMessages}


PadControlsInputMessages = { pad_id :
    { pad_name + "_SysexSetLed" : (mdds.eDefaultMidiStatus.system_exclusive,
                              mdds.nbyte(0x02,0x00,0x10),   # Command Id
                              mdds.byte(0x00),              # Target Id
                              [(mdds.byte(0x00),mdds.byte(0x7F)),             # Pad # 1-8: 70-77, 9-16: 78-7F
                               [mdds.byte(0x00),mdds.byte(0x01),mdds.byte(0x04),mdds.byte(0x05), # Color 0(None)  1(Red)  4(Green)  5(Yellow)
                                mdds.byte(0x10),mdds.byte(0x11),mdds.byte(0x14),mdds.byte(0x7F)]])} # 16(Blue)  17(Purple)  20(Cyan)  127(White)
    for pad_name,pad_id in PadControls.items()
}

ControlsInputMessages = PadControlsInputMessages

ControlsMessages = (ControlsOutputMessages,ControlsInputMessages)
