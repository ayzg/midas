# Import examples:
import flsl.device as device
import midas as dev2
#print("Printing from midas/hardware/apc40/data/py")

# Outbound APC40 Sysex Message Types
# There will be three types of messages from the PC host to the device.

# Outbound Message Type 0: Introduction
# This message is sent before any other device-specific message (i.e. other than Device Enquiry).
# It instructs the APC40 to perform the necessary initialization and informs the firmware of the version number of the
# application to cater for changes in the application in the APC40 firmware.
# There are three modes that are accepted. The unit defaults to Mode 0 on startup.

# Mode Identifier Name
# 0   0x40   Generic Mode
# 1   0x41   Ableton Live Mode
# 2   0x42   Alternate Ableton Live Mode

# Notes Regarding Generic Mode (Mode 0):
# -[CLIP LAUNCH] buttons are momentary and should light the green LED when ON
# -[CLIP STOP] buttons are momentary and should light its LED when ON
# -[ACTIVATOR], [SOLO], [RECORD ARM] are toggle buttons and should light its LED when ON
# -[TRACK SELECTION] buttons (1-8 + MASTER) are radio style and only one of the 9 buttons are ON at a time.
#  When ON its LED should light. These buttons will NOT send out MIDI in generic mode for its state.
#  These buttons dictate which one of nine banks the DEVICE CONTROL knobs and DEVICE
#  CONTROL switches belong to. These knobs and switches will output on a different MIDI channel
#  based on the current Track Selection (track 1 = MIDI channel 0, track 8 = MIDI channel 7, MASTER = MIDI channel 8).
#  Upon pressing one of the Track Selection buttons, the current position of the 8
#  Device Control knobs will be sent.
# -[CLIP/TRACK (1)], [DEVICE ON/OFF (2)], [Å (3)], [Æ (4)] will be toggle style and will light its LED when
#  ON
# -[DETAIL VIEW (5)], [REC QUANTIZATION (6)], [MIDI OVERDUB (7)], [METRONOME (8)] will be
#  momentary style and will light its LED when ON
# -[SCENE LAUNCH] and [STOP ALL CLIPS] buttons are momentary buttons and will light its LED when
#  ON
# -TRACK CONTROL buttons are toggle buttons and will light its LED when ON
# -TRACK CONTROL KNOBS and buttons are NOT banked in any way
# -[PLAY], [STOP], [RECORD], [UP], [DOWN], [LEFT], [RIGHT], [SHIFT], [NUDGE+], [NUDGE-], [TAP TEMPO] are momentary buttons
# -LED rings are all set to SINGLE style

# Notes Regarding Ableton Live Mode (Mode 1):
# - All buttons are momentary buttons
# - Device control knobs and buttons are not banked within the APC40
# - LED Rings around the knobs are controlled by the APC40 but can be updated by the Host
# - All other LEDs are controlled by the Host

# Notes Regarding Alternate Ableton Live Mode (Mode 2):
# - All buttons are momentary buttons
# - Device control knobs and buttons are not banked within the APC40
# - All LEDs are controlled by the Host

# Format of Type 0 outbound message
# byte number  value description
# 1            0xF0   MIDI System exclusive message start
# 2            0x47   Manufacturers ID Byte
# 3            <DeviceID> System Exclusive Device ID
# 4            0x73   Product model ID
# 5            0x60   Message type identifier
# 6            0x00   Number of data bytes to follow (most significant)
# 7            0x04   Number of data bytes to follow (least significant)
# 8            0x40 or 0x41 or 0x42   Application/Configuration identifier
# 9            <Version High> PC application Software version major
# 10           <Version Low> PC application Software version minor
# 11           <Bugfix Level> PC Application Software bug-fix level
# 12           0xF7   MIDI System exclusive message terminator


# Outbound Message Type 1: LEDs.
# This message is used to control the states of the LEDs. A note-on message will cause the specified LED to
# switch on. A note-off message will cause the specified LED to switch off. The field normally associated with
# note number will be used to specify the LED. The field normally associated with velocity will indicate the
# LED display type. The field normally associated with MIDI Channel will indicate the Track for certain LEDs.
# A Note On message with a velocity of zero is equivalent to a Note Off message, however it is preferred that
# an actual Note Off message is used.

# Format of Type 1 outbound Midi note-on messages
# byte number value description
# 1    0x9<chan> (0x90) [144+<chan>]  MIDI Note-on. The 4-bit <chan> value will be used for the track strips
# 2    <ControlID> [ControlID] identifier for LED object (“note number”)
# 3    state control value (This value will describe the state or color of the LED: OFF/ON/blinking, etc)

# Format of Type 1 outbound Midi note-off messages
# byte number value description
# 1    0x8<chan> (0x80) [128+<chan>]  MIDI Note-off. The 4-bit <chan> value will be used for the track strips
# 2    <ControlID> [ControlID] identifier for LED object (“note number”)
# 3    (unused) control value (ignored)

# Assignment of Note number messages to LEDs. Note 0x30 to 0x39 use MIDI Channel 0 to 7 to indicate Tracks 1-8.
# All other note values ignore the MIDI Channel.

# Note(ControlId)  | MIDI Channel     | Name                          | Corresponding LED Velocity
# 0x30 [48] (C_3)    0-7 = Track 1-8    RECORD ARM                      0=off, 1-127=on
# 0x31 [49] (C#3)    0-7 = Track 1-8    SOLO                            0=off, 1-127=on
# 0x32 [50] (D_3)    0-7 = Track 1-8    ACTIVATOR                       0=off, 1-127=on
# 0x33 [51] (D#3)    0-7 = Track 1-8    TRACK SELECTION                 0=off, 1-127=on
# 0x34 [52] (E_3)    0-7 = Track 1-8    CLIP STOP                       0=off, 1=on, 2=blink, 3-127=on
# 0x35 [53] (F_3)    0-7 = Track 1-8    CLIP LAUNCH 1                   0=off, 1=green, 2=green blink, 3=red, 4=red blink, 5=yellow, 6=yellow blink, 7-127=green
# 0x36 [54] (F#3)    0-7 = Track 1-8    CLIP LAUNCH 2                   0=off, 1=green, 2=green blink, 3=red, 4=red blink, 5=yellow, 6=yellow blink, 7-127=green
# 0x37 [55] (G_3)    0-7 = Track 1-8    CLIP LAUNCH 3                   0=off, 1=green, 2=green blink, 3=red, 4=red blink, 5=yellow, 6=yellow blink, 7-127=green
# 0x38 [56] (G#3)    0-7 = Track 1-8    CLIP LAUNCH 4                   0=off, 1=green, 2=green blink, 3=red, 4=red blink, 5=yellow, 6=yellow blink, 7-127=green
# 0x39 [57] (A_3)    0-7 = Track 1-8    CLIP LAUNCH 5                   0=off, 1=green, 2=green blink, 3=red, 4=red blink, 5=yellow, 6=yellow blink, 7-127=green
# 0x3A [58] (A#3)    0-8 = Track 1-8    MASTER (0) CLIP/TRACK (1)       0=off, 1-127=on
# 0x3B [59] (B_3)    0-8 = Track 1-8    MASTER (0) DEVICE ON/OFF (2)    0=off, 1-127=on
# 0x3C [60] (C_4)    0-8 = Track 1-8    MASTER (0) Å (3)                0=off, 1-127=on
# 0x3D [61] (C#4)    0-8 = Track 1-8    MASTER (0) Î (4)                0=off, 1-127=on
# 0x3E [62] (D_4)    0-8 = Track 1-8    MASTER (0) DETAIL VIEW (5)      0=off, 1-127=on
# 0x3F [63] (D#4)    0-8 = Track 1-8    MASTER (0) REC QUANT (6)        0=off, 1-127=on
# 0x40 [64] (E_4)    0-8 = Track 1-8    MASTER (0) MIDI OVERDUB (7)     0=off, 1-127=on
# 0x41 [65] (F_4)    0-8 = Track 1-8    MASTER (0) METRONOME (8)        0=off, 1-127=on
# 0x50 [80] (G#5)                       MASTER                          0=off, 1-127=on
# 0x52 [82] (A#5)                       SCENE LAUNCH 1                  0=off, 1=on, 2=blink, 3-127=on
# 0x53 [83] (B_5)                       SCENE LAUNCH 2                  0=off, 1=on, 2=blink, 3-127=on
# 0x54 [84] (C_6)                       SCENE LAUNCH 3                  0=off, 1=on, 2=blink, 3-127=on
# 0x55 [85] (C#7)                       SCENE LAUNCH 4                  0=off, 1=on, 2=blink, 3-127=on
# 0x56 [86] (D_7)                       SCENE LAUNCH 5                  0=off, 1=on, 2=blink, 3-127=on
# 0x57 [87] (D#7)                       PAN                             0=off, 1-127=on
# 0x58 [88] (E_7)                       SEND A                          0=off, 1-127=on
# 0x59 [89] (F_7)                       SEND B                          0=off, 1-127=on
# 0x5A [90] (F#_7)                      SEND C                          0=off, 1-127=on


BUTTON_LED_OUT_DATA = [
    # Record Arm Row Tracks 0 to 7
    {"id": 0x30, "channel": 0x00, "name": "rec_arm_0", "desc": "Track 0 RECORD ARM"},
    {"id": 0x30, "channel": 0x01, "name": "rec_arm_1", "desc": "Track 1 RECORD ARM"},
    {"id": 0x30, "channel": 0x02, "name": "rec_arm_2", "desc": "Track 2 RECORD ARM"},
    {"id": 0x30, "channel": 0x03, "name": "rec_arm_3", "desc": "Track 3 RECORD ARM"},
    {"id": 0x30, "channel": 0x04, "name": "rec_arm_4", "desc": "Track 4 RECORD ARM"},
    {"id": 0x30, "channel": 0x05, "name": "rec_arm_5", "desc": "Track 5 RECORD ARM"},
    {"id": 0x30, "channel": 0x06, "name": "rec_arm_6", "desc": "Track 6 RECORD ARM"},
    {"id": 0x30, "channel": 0x07, "name": "rec_arm_7", "desc": "Track 7 RECORD ARM"},

    # Solo Row Tracks 0 to 7
    {"id": 0x31, "channel": 0x0, "name": "solo_0", "desc": "Track 0 SOLO"},
    {"id": 0x31, "channel": 0x1, "name": "solo_1", "desc": "Track 1 SOLO"},
    {"id": 0x31, "channel": 0x2, "name": "solo_2", "desc": "Track 2 SOLO"},
    {"id": 0x31, "channel": 0x3, "name": "solo_3", "desc": "Track 3 SOLO"},
    {"id": 0x31, "channel": 0x4, "name": "solo_4", "desc": "Track 4 SOLO"},
    {"id": 0x31, "channel": 0x5, "name": "solo_5", "desc": "Track 5 SOLO"},
    {"id": 0x31, "channel": 0x6, "name": "solo_6", "desc": "Track 6 SOLO"},
    {"id": 0x31, "channel": 0x7, "name": "solo_7", "desc": "Track 7 SOLO"},

    # Activator Row Tracks 0 to 7
    {"id": 0x32, "channel": 0x0, "name": "activator_0", "desc": "Track 0 ACTIVATOR"},
    {"id": 0x32, "channel": 0x1, "name": "activator_1", "desc": "Track 1 ACTIVATOR"},
    {"id": 0x32, "channel": 0x2, "name": "activator_2", "desc": "Track 2 ACTIVATOR"},
    {"id": 0x32, "channel": 0x3, "name": "activator_3", "desc": "Track 3 ACTIVATOR"},
    {"id": 0x32, "channel": 0x4, "name": "activator_4", "desc": "Track 4 ACTIVATOR"},
    {"id": 0x32, "channel": 0x5, "name": "activator_5", "desc": "Track 5 ACTIVATOR"},
    {"id": 0x32, "channel": 0x6, "name": "activator_6", "desc": "Track 6 ACTIVATOR"},
    {"id": 0x32, "channel": 0x7, "name": "activator_7", "desc": "Track 7 ACTIVATOR"},

    # Track Select Row Tracks 0 to 7
    {"id": 0x33, "channel": 0x0, "name": "track_select_0", "desc": "Track 0 TRACK SELECTION"},
    {"id": 0x33, "channel": 0x1, "name": "track_select_1", "desc": "Track 1 TRACK SELECTION"},
    {"id": 0x33, "channel": 0x2, "name": "track_select_2", "desc": "Track 2 TRACK SELECTION"},
    {"id": 0x33, "channel": 0x3, "name": "track_select_3", "desc": "Track 3 TRACK SELECTION"},
    {"id": 0x33, "channel": 0x4, "name": "track_select_4", "desc": "Track 4 TRACK SELECTION"},
    {"id": 0x33, "channel": 0x5, "name": "track_select_5", "desc": "Track 5 TRACK SELECTION"},
    {"id": 0x33, "channel": 0x6, "name": "track_select_6", "desc": "Track 6 TRACK SELECTION"},
    {"id": 0x33, "channel": 0x7, "name": "track_select_7", "desc": "Track 7 TRACK SELECTION"},
    {"id": 0x50, "channel": 0x0, "name": "track_select_master", "desc": "Track Master TRACK SELECTION"},

    # Clip Stop
    {"id": 0x34, "channel": 0x00, "name": "clip_stop_0", "desc": "Track 0 CLIP STOP"},
    {"id": 0x34, "channel": 0x01, "name": "clip_stop_1", "desc": "Track 1 CLIP STOP"},
    {"id": 0x34, "channel": 0x02, "name": "clip_stop_2", "desc": "Track 2 CLIP STOP"},
    {"id": 0x34, "channel": 0x03, "name": "clip_stop_3", "desc": "Track 3 CLIP STOP"},
    {"id": 0x34, "channel": 0x04, "name": "clip_stop_4", "desc": "Track 4 CLIP STOP"},
    {"id": 0x34, "channel": 0x05, "name": "clip_stop_5", "desc": "Track 5 CLIP STOP"},
    {"id": 0x34, "channel": 0x06, "name": "clip_stop_6", "desc": "Track 6 CLIP STOP"},
    {"id": 0x34, "channel": 0x07, "name": "clip_stop_7", "desc": "Track 7 CLIP STOP"},

    # Clip 1 to Clip 5# Clip 1 to Clip 5
    {"id": 0x35, "channel": 0x00, "name": "clip_0_0", "desc": "Track 0 CLIP LAUNCH 1"},
    {"id": 0x35, "channel": 0x01, "name": "clip_0_1", "desc": "Track 1 CLIP LAUNCH 1"},
    {"id": 0x35, "channel": 0x02, "name": "clip_0_2", "desc": "Track 2 CLIP LAUNCH 1"},
    {"id": 0x35, "channel": 0x03, "name": "clip_0_3", "desc": "Track 3 CLIP LAUNCH 1"},
    {"id": 0x35, "channel": 0x04, "name": "clip_0_4", "desc": "Track 4 CLIP LAUNCH 1"},
    {"id": 0x35, "channel": 0x05, "name": "clip_0_5", "desc": "Track 5 CLIP LAUNCH 1"},
    {"id": 0x35, "channel": 0x06, "name": "clip_0_6", "desc": "Track 6 CLIP LAUNCH 1"},
    {"id": 0x35, "channel": 0x07, "name": "clip_0_7", "desc": "Track 7 CLIP LAUNCH 1"},

    {"id": 0x36, "channel": 0x00, "name": "clip_1_0", "desc": "Track 0 CLIP LAUNCH 2"},
    {"id": 0x36, "channel": 0x01, "name": "clip_1_1", "desc": "Track 1 CLIP LAUNCH 2"},
    {"id": 0x36, "channel": 0x02, "name": "clip_1_2", "desc": "Track 2 CLIP LAUNCH 2"},
    {"id": 0x36, "channel": 0x03, "name": "clip_1_3", "desc": "Track 3 CLIP LAUNCH 2"},
    {"id": 0x36, "channel": 0x04, "name": "clip_1_4", "desc": "Track 4 CLIP LAUNCH 2"},
    {"id": 0x36, "channel": 0x05, "name": "clip_1_5", "desc": "Track 5 CLIP LAUNCH 2"},
    {"id": 0x36, "channel": 0x06, "name": "clip_1_6", "desc": "Track 6 CLIP LAUNCH 2"},
    {"id": 0x36, "channel": 0x07, "name": "clip_1_7", "desc": "Track 7 CLIP LAUNCH 2"},

    {"id": 0x37, "channel": 0x00, "name": "clip_2_0", "desc": "Track 0 CLIP LAUNCH 3"},
    {"id": 0x37, "channel": 0x01, "name": "clip_2_1", "desc": "Track 1 CLIP LAUNCH 3"},
    {"id": 0x37, "channel": 0x02, "name": "clip_2_2", "desc": "Track 2 CLIP LAUNCH 3"},
    {"id": 0x37, "channel": 0x03, "name": "clip_2_3", "desc": "Track 3 CLIP LAUNCH 3"},
    {"id": 0x37, "channel": 0x04, "name": "clip_2_4", "desc": "Track 4 CLIP LAUNCH 3"},
    {"id": 0x37, "channel": 0x05, "name": "clip_2_5", "desc": "Track 5 CLIP LAUNCH 3"},
    {"id": 0x37, "channel": 0x06, "name": "clip_2_6", "desc": "Track 6 CLIP LAUNCH 3"},
    {"id": 0x37, "channel": 0x07, "name": "clip_2_7", "desc": "Track 7 CLIP LAUNCH 3"},

    {"id": 0x38, "channel": 0x00, "name": "clip_3_0", "desc": "Track 0 CLIP LAUNCH 4"},
    {"id": 0x38, "channel": 0x01, "name": "clip_3_1", "desc": "Track 1 CLIP LAUNCH 4"},
    {"id": 0x38, "channel": 0x02, "name": "clip_3_2", "desc": "Track 2 CLIP LAUNCH 4"},
    {"id": 0x38, "channel": 0x03, "name": "clip_3_3", "desc": "Track 3 CLIP LAUNCH 4"},
    {"id": 0x38, "channel": 0x04, "name": "clip_3_4", "desc": "Track 4 CLIP LAUNCH 4"},
    {"id": 0x38, "channel": 0x05, "name": "clip_3_5", "desc": "Track 5 CLIP LAUNCH 4"},
    {"id": 0x38, "channel": 0x06, "name": "clip_3_6", "desc": "Track 6 CLIP LAUNCH 4"},
    {"id": 0x38, "channel": 0x07, "name": "clip_3_7", "desc": "Track 7 CLIP LAUNCH 4"},

    {"id": 0x39, "channel": 0x00, "name": "clip_4_0", "desc": "Track 0 CLIP LAUNCH 5"},
    {"id": 0x39, "channel": 0x01, "name": "clip_4_1", "desc": "Track 1 CLIP LAUNCH 5"},
    {"id": 0x39, "channel": 0x02, "name": "clip_4_2", "desc": "Track 2 CLIP LAUNCH 5"},
    {"id": 0x39, "channel": 0x03, "name": "clip_4_3", "desc": "Track 3 CLIP LAUNCH 5"},
    {"id": 0x39, "channel": 0x04, "name": "clip_4_4", "desc": "Track 4 CLIP LAUNCH 5"},
    {"id": 0x39, "channel": 0x05, "name": "clip_4_5", "desc": "Track 5 CLIP LAUNCH 5"},
    {"id": 0x39, "channel": 0x06, "name": "clip_4_6", "desc": "Track 6 CLIP LAUNCH 5"},
    {"id": 0x39, "channel": 0x07, "name": "clip_4_7", "desc": "Track 7 CLIP LAUNCH 5"},

    {"id": 0x3A, "channel": 0x00, "name": "dcontrol_1_clip_track_master", "desc": "MASTER CLIP/TRACK"},
    {"id": 0x3A, "channel": 0x01, "name": "dcontrol_1_clip_track_0", "desc": "CLIP/TRACK 0"},
    {"id": 0x3A, "channel": 0x02, "name": "dcontrol_1_clip_track_1", "desc": "CLIP/TRACK 1"},
    {"id": 0x3A, "channel": 0x03, "name": "dcontrol_1_clip_track_2", "desc": "CLIP/TRACK 2"},
    {"id": 0x3A, "channel": 0x04, "name": "dcontrol_1_clip_track_3", "desc": "CLIP/TRACK 3"},
    {"id": 0x3A, "channel": 0x05, "name": "dcontrol_1_clip_track_4", "desc": "CLIP/TRACK 4"},
    {"id": 0x3A, "channel": 0x06, "name": "dcontrol_1_clip_track_5", "desc": "CLIP/TRACK 5"},
    {"id": 0x3A, "channel": 0x07, "name": "dcontrol_1_clip_track_6", "desc": "CLIP/TRACK 6"},
    {"id": 0x3A, "channel": 0x08, "name": "dcontrol_1_clip_track_7", "desc": "CLIP/TRACK 7"},

    {"id": 0x3B, "channel": 0x00, "name": "dcontrol_2_device_on_off_master", "desc": "MASTER DEVICE ON/OFF"},
    {"id": 0x3B, "channel": 0x01, "name": "dcontrol_2_device_on_off_0", "desc": "DEVICE ON/OFF 0"},
    {"id": 0x3B, "channel": 0x02, "name": "dcontrol_2_device_on_off_1", "desc": "DEVICE ON/OFF 1"},
    {"id": 0x3B, "channel": 0x03, "name": "dcontrol_2_device_on_off_2", "desc": "DEVICE ON/OFF 2"},
    {"id": 0x3B, "channel": 0x04, "name": "dcontrol_2_device_on_off_3", "desc": "DEVICE ON/OFF 3"},
    {"id": 0x3B, "channel": 0x05, "name": "dcontrol_2_device_on_off_4", "desc": "DEVICE ON/OFF 4"},
    {"id": 0x3B, "channel": 0x06, "name": "dcontrol_2_device_on_off_5", "desc": "DEVICE ON/OFF 5"},
    {"id": 0x3B, "channel": 0x07, "name": "dcontrol_2_device_on_off_6", "desc": "DEVICE ON/OFF 6"},
    {"id": 0x3B, "channel": 0x08, "name": "dcontrol_2_device_on_off_7", "desc": "DEVICE ON/OFF 7"},

    {"id": 0x3C, "channel": 0x00, "name": "dcontrol_3_left_master", "desc": "MASTER LEFT"},
    {"id": 0x3C, "channel": 0x01, "name": "dcontrol_3_left_0", "desc": "LEFT 0"},
    {"id": 0x3C, "channel": 0x02, "name": "dcontrol_3_left_1", "desc": "LEFT 1"},
    {"id": 0x3C, "channel": 0x03, "name": "dcontrol_3_left_2", "desc": "LEFT 2"},
    {"id": 0x3C, "channel": 0x04, "name": "dcontrol_3_left_3", "desc": "LEFT 3"},
    {"id": 0x3C, "channel": 0x05, "name": "dcontrol_3_left_4", "desc": "LEFT 4"},
    {"id": 0x3C, "channel": 0x06, "name": "dcontrol_3_left_5", "desc": "LEFT 5"},
    {"id": 0x3C, "channel": 0x07, "name": "dcontrol_3_left_6", "desc": "LEFT 6"},
    {"id": 0x3C, "channel": 0x08, "name": "dcontrol_3_left_7", "desc": "LEFT 7"},

    {"id": 0x3D, "channel": 0x00, "name": "dcontrol_4_right_master", "desc": "DEVICE CONTROL 4 RIGHT MASTER"},
    {"id": 0x3D, "channel": 0x01, "name": "dcontrol_4_right_0", "desc": "DEVICE CONTROL 4 RIGHT 0"},
    {"id": 0x3D, "channel": 0x02, "name": "dcontrol_4_right_1", "desc": "DEVICE CONTROL 4 RIGHT 1"},
    {"id": 0x3D, "channel": 0x03, "name": "dcontrol_4_right_2", "desc": "DEVICE CONTROL 4 RIGHT 2"},
    {"id": 0x3D, "channel": 0x04, "name": "dcontrol_4_right_3", "desc": "DEVICE CONTROL 4 RIGHT 3"},
    {"id": 0x3D, "channel": 0x05, "name": "dcontrol_4_right_4", "desc": "DEVICE CONTROL 4 RIGHT 4"},
    {"id": 0x3D, "channel": 0x06, "name": "dcontrol_4_right_5", "desc": "DEVICE CONTROL 4 RIGHT 5"},
    {"id": 0x3D, "channel": 0x07, "name": "dcontrol_4_right_6", "desc": "DEVICE CONTROL 4 RIGHT 6"},
    {"id": 0x3D, "channel": 0x08, "name": "dcontrol_4_right_7", "desc": "DEVICE CONTROL 4 RIGHT 7"},

    {"id": 0x3E, "channel": 0x00, "name": "dcontrol_5_detail_view_master", "desc": "DEVICE CONTROL 5 DETAIL VIEW MASTER"},
    {"id": 0x3E, "channel": 0x01, "name": "dcontrol_5_detail_view_0", "desc": "DEVICE CONTROL 5 DETAIL VIEW 0"},
    {"id": 0x3E, "channel": 0x02, "name": "dcontrol_5_detail_view_1", "desc": "DEVICE CONTROL 5 DETAIL VIEW 1"},
    {"id": 0x3E, "channel": 0x03, "name": "dcontrol_5_detail_view_2", "desc": "DEVICE CONTROL 5 DETAIL VIEW 2"},
    {"id": 0x3E, "channel": 0x04, "name": "dcontrol_5_detail_view_3", "desc": "DEVICE CONTROL 5 DETAIL VIEW 3"},
    {"id": 0x3E, "channel": 0x05, "name": "dcontrol_5_detail_view_4", "desc": "DEVICE CONTROL 5 DETAIL VIEW 4"},
    {"id": 0x3E, "channel": 0x06, "name": "dcontrol_5_detail_view_5", "desc": "DEVICE CONTROL 5 DETAIL VIEW 5"},
    {"id": 0x3E, "channel": 0x07, "name": "dcontrol_5_detail_view_6", "desc": "DEVICE CONTROL 5 DETAIL VIEW 6"},
    {"id": 0x3E, "channel": 0x08, "name": "dcontrol_5_detail_view_7", "desc": "DEVICE CONTROL 5 DETAIL VIEW 7"},

    {"id": 0x3F, "channel": 0x00, "name": "dcontrol_6_rec_quant_master", "desc": "DEVICE CONTROL 6 REC QUANT MASTER"},
    {"id": 0x3F, "channel": 0x01, "name": "dcontrol_6_rec_quant_0", "desc": "DEVICE CONTROL 6 REC QUANT 0"},
    {"id": 0x3F, "channel": 0x02, "name": "dcontrol_6_rec_quant_1", "desc": "DEVICE CONTROL 6 REC QUANT 1"},
    {"id": 0x3F, "channel": 0x03, "name": "dcontrol_6_rec_quant_2", "desc": "DEVICE CONTROL 6 REC QUANT 2"},
    {"id": 0x3F, "channel": 0x04, "name": "dcontrol_6_rec_quant_3", "desc": "DEVICE CONTROL 6 REC QUANT 3"},
    {"id": 0x3F, "channel": 0x05, "name": "dcontrol_6_rec_quant_4", "desc": "DEVICE CONTROL 6 REC QUANT 4"},
    {"id": 0x3F, "channel": 0x06, "name": "dcontrol_6_rec_quant_5", "desc": "DEVICE CONTROL 6 REC QUANT 5"},
    {"id": 0x3F, "channel": 0x07, "name": "dcontrol_6_rec_quant_6", "desc": "DEVICE CONTROL 6 REC QUANT 6"},
    {"id": 0x3F, "channel": 0x08, "name": "dcontrol_6_rec_quant_7", "desc": "DEVICE CONTROL 6 REC QUANT 7"},
    {"id": 0x40, "channel": 0x0, "name": "dcontrol_7_midi_overdub", "desc": "Track 1-8 MASTER (0) MIDI OVERDUB (7)"},

    {"id": 0x41, "channel": 0x00, "name": "dcontrol_8_metronome_master", "desc": "DEVICE CONTROL 8 METRONOME MASTER"},
    {"id": 0x41, "channel": 0x01, "name": "dcontrol_8_metronome_0", "desc": "DEVICE CONTROL 8 METRONOME 0"},
    {"id": 0x41, "channel": 0x02, "name": "dcontrol_8_metronome_1", "desc": "DEVICE CONTROL 8 METRONOME 1"},
    {"id": 0x41, "channel": 0x03, "name": "dcontrol_8_metronome_2", "desc": "DEVICE CONTROL 8 METRONOME 2"},
    {"id": 0x41, "channel": 0x04, "name": "dcontrol_8_metronome_3", "desc": "DEVICE CONTROL 8 METRONOME 3"},
    {"id": 0x41, "channel": 0x05, "name": "dcontrol_8_metronome_4", "desc": "DEVICE CONTROL 8 METRONOME 4"},
    {"id": 0x41, "channel": 0x06, "name": "dcontrol_8_metronome_5", "desc": "DEVICE CONTROL 8 METRONOME 5"},
    {"id": 0x41, "channel": 0x07, "name": "dcontrol_8_metronome_6", "desc": "DEVICE CONTROL 8 METRONOME 6"},
    {"id": 0x41, "channel": 0x08, "name": "dcontrol_8_metronome_7", "desc": "DEVICE CONTROL 8 METRONOME 7"},

    {"id": 0x52, "channel": 0x0, "name": "scene_0", "desc": "SCENE LAUNCH 0"},
    {"id": 0x53, "channel": 0x0, "name": "scene_1", "desc": "SCENE LAUNCH 1"},
    {"id": 0x54, "channel": 0x0, "name": "scene_2", "desc": "SCENE LAUNCH 2"},
    {"id": 0x55, "channel": 0x0, "name": "scene_3", "desc": "SCENE LAUNCH 3"},
    {"id": 0x56, "channel": 0x0, "name": "scene_4", "desc": "SCENE LAUNCH 4"},

    {"id": 0x57, "channel": 0x0, "name": "pan", "desc": "PAN"},
    {"id": 0x58, "channel": 0x0, "name": "send_a", "desc": "SEND A"},
    {"id": 0x59, "channel": 0x0, "name": "send_b", "desc": "SEND B"},
    {"id": 0x5A, "channel": 0x0, "name": "send_c", "desc": "SEND C"}
]

# Outbound Message Type 2: Controller Value Update messages
# Controls that report an absolute value for their position for inbound messages
# can have their controller value updated via a Controller Value Update message.
# This will be done using a MIDI controller message. The field normally associated
# with the controller number will be used to specify the Control ID.
# The field normally associated with the controller value will be used to update
# the value of a controller on the APC40.
# MIDI Controller message byte number value description
# 1                0xB<chan>              # MIDI Controller. The 4-bit <chan> value will be used for the track strips
# 2                <ControlID>            # Identifier for control surface object
# 3                data                   # Control value

# Assignment of controller numbers to absolute controllers
# Control          MIDI Channel           Control ID        Notes
# Track Level       0-7 = Tracks 1-8       0x07
# Master Level                              0x0E
# Crossfader                                0x0F
# DEVICE Knob 1     0-8 = Tracks 1-8, Master (for mode 0 only)    0x10
# DEVICE Knob 2     0-8 = Tracks 1-8, Master (for mode 0 only)    0x11
# DEVICE Knob 3     0-8 = Tracks 1-8, Master (for mode 0 only)    0x12
# DEVICE Knob 4     0-8 = Tracks 1-8, Master (for mode 0 only)    0x13
# DEVICE Knob 5     0-8 = Tracks 1-8, Master (for mode 0 only)    0x14
# DEVICE Knob 6     0-8 = Tracks 1-8, Master (for mode 0 only)    0x15
# DEVICE Knob 7     0-8 = Tracks 1-8, Master (for mode 0 only)    0x16
# DEVICE Knob 8     0-8 = Tracks 1-8, Master (for mode 0 only)    0x17
# DEVICE Knob 1 LED Ring Type    0-8 = Tracks 1-8, Master (for mode 0 only)    0x18    [24]=off, [1]=Single, [2]=Volume Style, [3]=Pan Style, [4-127]=Single
# DEVICE Knob 2 LED Ring Type    0-8 = Tracks 1-8, Master (for mode 0 only)    0x19    [25]=off, [1]=Single, [2]=Volume Style, [3]=Pan Style, [4-127]=Single
# DEVICE Knob 3 LED Ring Type    0-8 = Tracks 1-8, Master (for mode 0 only)    0x1A    [26]=off, [1]=Single, [2]=Volume Style, [3]=Pan Style, [4-127]=Single
# DEVICE Knob 4 LED Ring Type    0-8 = Tracks 1-8, Master (for mode 0 only)    0x1B    [27]=off, [1]=Single, [2]=Volume Style, [3]=Pan Style, [4-127]=Single
# DEVICE Knob 5 LED Ring Type    0-8 = Tracks 1-8, Master (for mode 0 only)    0x1C    [28]=off, [1]=Single, [2]=Volume Style, [3]=Pan Style, [4-127]=Single
# DEVICE Knob 6 LED Ring Type    0-8 = Tracks 1-8, Master (for mode 0 only)    0x1D    [29]=off, [1]=Single, [2]=Volume Style, [3]=Pan Style, [4-127]=Single
# DEVICE Knob 7 LED Ring Type    0-8 = Tracks 1-8, Master (for mode 0 only)    0x1E    [30]=off, [1]=Single, [2]=Volume Style, [3]=Pan Style, [4-127]=Single
# DEVICE Knob 8 LED Ring Type    0-8 = Tracks 1-8, Master (for mode 0 only)    0x1F    [31]=off, [1]=Single, [2]=Volume Style, [3]=Pan Style, [4-127]=Single
# TRACK Knob 1      0x30
# TRACK Knob 2      0x31
# TRACK Knob 3      0x32
# TRACK Knob 4      0x33
# TRACK Knob 5      0x34
# TRACK Knob 6      0x35
# TRACK Knob 7      0x36
# TRACK Knob 8      0x37
# TRACK Knob 1 LED Ring Type    0x38    [48]=off, [1]=Single, [2]=Volume Style, [3]=Pan Style, [4-127]=Single
# TRACK Knob 2 LED Ring Type    0x39    [49]=off, [1]=Single, [2]=Volume Style, [3]=Pan Style, [4-127]=Single
# TRACK Knob 3 LED Ring Type    0x3A    [50]=off, [1]=Single, [2]=Volume Style, [3]=Pan Style, [4-127]=Single
# TRACK Knob 4 LED Ring Type    0x3B    [51]=off, [1]=Single, [2]=Volume Style, [3]=Pan Style, [4-127]=Single
# TRACK Knob 5 LED Ring Type    0x3C    [52]=off, [1]=Single, [2]=Volume Style, [3]=Pan Style, [4-127]=Single
# TRACK Knob 6 LED Ring Type    0x3D    [53]=off, [1]=Single, [2]=Volume Style, [3]=Pan Style, [4-127]=Single
# TRACK Knob 7 LED Ring Type    0x3E    [54]=off, [1]=Single, [2]=Volume Style, [3]=Pan Style, [4-127]=Single
# TRACK Knob 8 LED Ring Type    0x3F    [55]=off, [1]=Single, [2]=Volume Style, [3]=Pan Style, [4-127]=Single
# MASTER KNOB ?? CUE LEVEL
CONTROL_LED_OUT_DATA = [ 
    # Track Level Tracks 0 to 7
    {"id": 0x07, "channel": 0x00, "name": "track_level_level_0", "desc": "Track Level 0 "},
    {"id": 0x07, "channel": 0x01, "name": "track_level_level_1", "desc": "Track Level 1 "},
    {"id": 0x07, "channel": 0x02, "name": "track_level_level_2", "desc": "Track Level 2 "},
    {"id": 0x07, "channel": 0x03, "name": "track_level_level_3", "desc": "Track Level 3 "},
    {"id": 0x07, "channel": 0x04, "name": "track_level_level_4", "desc": "Track Level 4 "},
    {"id": 0x07, "channel": 0x05, "name": "track_level_level_5", "desc": "Track Level 5 "},
    {"id": 0x07, "channel": 0x06, "name": "track_level_level_6", "desc": "Track Level 6 "},
    {"id": 0x07, "channel": 0x07, "name": "track_level_level_7", "desc": "Track Level 7 "},

    {"id": 0x0E, "channel": 0x00, "name": "track_level_level_master", "desc": "Track Level Master "},
    
    # Crossfader
    {"id": 0x0F, "channel": 0x00, "name": "crossfader", "desc": "Crossfader "},
    
    # DEVICE Knob 1 to DEVICE Knob 8
    {"id": 0x10, "channel": 0x01, "name": "device_knob_1_track_0", "desc": "DEVICE Knob 1 Track 0"},
    {"id": 0x10, "channel": 0x02, "name": "device_knob_1_track_1", "desc": "DEVICE Knob 1 Track 1"},
    {"id": 0x10, "channel": 0x03, "name": "device_knob_1_track_2", "desc": "DEVICE Knob 1 Track 2"},
    {"id": 0x10, "channel": 0x04, "name": "device_knob_1_track_3", "desc": "DEVICE Knob 1 Track 3"},
    {"id": 0x10, "channel": 0x05, "name": "device_knob_1_track_4", "desc": "DEVICE Knob 1 Track 4"},
    {"id": 0x10, "channel": 0x06, "name": "device_knob_1_track_5", "desc": "DEVICE Knob 1 Track 5"},
    {"id": 0x10, "channel": 0x07, "name": "device_knob_1_track_6", "desc": "DEVICE Knob 1 Track 6"},
    {"id": 0x10, "channel": 0x08, "name": "device_knob_1_track_7", "desc": "DEVICE Knob 1 Track 7"},
    {"id": 0x10, "channel": 0x00, "name": "device_knob_1_track_master", "desc": "DEVICE Knob 1 Track Master"},


    # DEVICE Knob 2 to DEVICE Knob 8
    {"id": 0x11, "channel": 0x01, "name": "device_knob_2_track_0", "desc": "DEVICE Knob 2 Track 0"},
    {"id": 0x11, "channel": 0x02, "name": "device_knob_2_track_1", "desc": "DEVICE Knob 2 Track 1"},
    {"id": 0x11, "channel": 0x03, "name": "device_knob_2_track_2", "desc": "DEVICE Knob 2 Track 2"},
    {"id": 0x11, "channel": 0x04, "name": "device_knob_2_track_3", "desc": "DEVICE Knob 2 Track 3"},
    {"id": 0x11, "channel": 0x05, "name": "device_knob_2_track_4", "desc": "DEVICE Knob 2 Track 4"},
    {"id": 0x11, "channel": 0x06, "name": "device_knob_2_track_5", "desc": "DEVICE Knob 2 Track 5"},
    {"id": 0x11, "channel": 0x07, "name": "device_knob_2_track_6", "desc": "DEVICE Knob 2 Track 6"},
    {"id": 0x11, "channel": 0x08, "name": "device_knob_2_track_7", "desc": "DEVICE Knob 2 Track 7"},
    {"id": 0x11, "channel": 0x00, "name": "device_knob_2_track_master", "desc": "DEVICE Knob 2 Track Master"},

    # DEVICE Knob 3 to DEVICE Knob 8
    {"id": 0x12, "channel": 0x01, "name": "device_knob_3_track_0", "desc": "DEVICE Knob 3 Track 0"},
    {"id": 0x12, "channel": 0x02, "name": "device_knob_3_track_1", "desc": "DEVICE Knob 3 Track 1"},
    {"id": 0x12, "channel": 0x03, "name": "device_knob_3_track_2", "desc": "DEVICE Knob 3 Track 2"},
    {"id": 0x12, "channel": 0x04, "name": "device_knob_3_track_3", "desc": "DEVICE Knob 3 Track 3"},
    {"id": 0x12, "channel": 0x05, "name": "device_knob_3_track_4", "desc": "DEVICE Knob 3 Track 4"},
    {"id": 0x12, "channel": 0x06, "name": "device_knob_3_track_5", "desc": "DEVICE Knob 3 Track 5"},
    {"id": 0x12, "channel": 0x07, "name": "device_knob_3_track_6", "desc": "DEVICE Knob 3 Track 6"},
    {"id": 0x12, "channel": 0x08, "name": "device_knob_3_track_7", "desc": "DEVICE Knob 3 Track 7"},
    {"id": 0x12, "channel": 0x00, "name": "device_knob_3_track_master", "desc": "DEVICE Knob 3 Track Master"},

    # DEVICE Knob 4 to DEVICE Knob 8
    {"id": 0x13, "channel": 0x01, "name": "device_knob_4_track_0", "desc": "DEVICE Knob 4 Track 0"},
    {"id": 0x13, "channel": 0x02, "name": "device_knob_4_track_1", "desc": "DEVICE Knob 4 Track 1"},
    {"id": 0x13, "channel": 0x03, "name": "device_knob_4_track_2", "desc": "DEVICE Knob 4 Track 2"},
    {"id": 0x13, "channel": 0x04, "name": "device_knob_4_track_3", "desc": "DEVICE Knob 4 Track 3"},
    {"id": 0x13, "channel": 0x05, "name": "device_knob_4_track_4", "desc": "DEVICE Knob 4 Track 4"},
    {"id": 0x13, "channel": 0x06, "name": "device_knob_4_track_5", "desc": "DEVICE Knob 4 Track 5"},
    {"id": 0x13, "channel": 0x07, "name": "device_knob_4_track_6", "desc": "DEVICE Knob 4 Track 6"},
    {"id": 0x13, "channel": 0x08, "name": "device_knob_4_track_7", "desc": "DEVICE Knob 4 Track 7"},
    {"id": 0x13, "channel": 0x00, "name": "device_knob_4_track_master", "desc": "DEVICE Knob 4 Track Master"},

    # DEVICE Knob 5 to DEVICE Knob 8
    {"id": 0x14, "channel": 0x01, "name": "device_knob_5_track_0", "desc": "DEVICE Knob 5 Track 0"},
    {"id": 0x14, "channel": 0x02, "name": "device_knob_5_track_1", "desc": "DEVICE Knob 5 Track 1"},
    {"id": 0x14, "channel": 0x03, "name": "device_knob_5_track_2", "desc": "DEVICE Knob 5 Track 2"},
    {"id": 0x14, "channel": 0x04, "name": "device_knob_5_track_3", "desc": "DEVICE Knob 5 Track 3"},
    {"id": 0x14, "channel": 0x05, "name": "device_knob_5_track_4", "desc": "DEVICE Knob 5 Track 4"},
    {"id": 0x14, "channel": 0x06, "name": "device_knob_5_track_5", "desc": "DEVICE Knob 5 Track 5"},
    {"id": 0x14, "channel": 0x07, "name": "device_knob_5_track_6", "desc": "DEVICE Knob 5 Track 6"},
    {"id": 0x14, "channel": 0x08, "name": "device_knob_5_track_7", "desc": "DEVICE Knob 5 Track 7"},
    {"id": 0x14, "channel": 0x00, "name": "device_knob_5_track_master", "desc": "DEVICE Knob 5 Track Master"},

    # DEVICE Knob 6 to DEVICE Knob 8
    {"id": 0x15, "channel": 0x01, "name": "device_knob_6_track_0", "desc": "DEVICE Knob 6 Track 0"},
    {"id": 0x15, "channel": 0x02, "name": "device_knob_6_track_1", "desc": "DEVICE Knob 6 Track 1"},
    {"id": 0x15, "channel": 0x03, "name": "device_knob_6_track_2", "desc": "DEVICE Knob 6 Track 2"},
    {"id": 0x15, "channel": 0x04, "name": "device_knob_6_track_3", "desc": "DEVICE Knob 6 Track 3"},
    {"id": 0x15, "channel": 0x05, "name": "device_knob_6_track_4", "desc": "DEVICE Knob 6 Track 4"},
    {"id": 0x15, "channel": 0x06, "name": "device_knob_6_track_5", "desc": "DEVICE Knob 6 Track 5"},
    {"id": 0x15, "channel": 0x07, "name": "device_knob_6_track_6", "desc": "DEVICE Knob 6 Track 6"},
    {"id": 0x15, "channel": 0x08, "name": "device_knob_6_track_7", "desc": "DEVICE Knob 6 Track 7"},
    {"id": 0x15, "channel": 0x09, "name": "device_knob_6_track_master", "desc": "DEVICE Knob 6 Track Master"},

    # DEVICE Knob 7 to DEVICE Knob 8
    {"id": 0x16, "channel": 0x01, "name": "device_knob_7_track_0", "desc": "DEVICE Knob 7 Track 0"},
    {"id": 0x16, "channel": 0x02, "name": "device_knob_7_track_1", "desc": "DEVICE Knob 7 Track 1"},
    {"id": 0x16, "channel": 0x03, "name": "device_knob_7_track_2", "desc": "DEVICE Knob 7 Track 2"},
    {"id": 0x16, "channel": 0x04, "name": "device_knob_7_track_3", "desc": "DEVICE Knob 7 Track 3"},
    {"id": 0x16, "channel": 0x05, "name": "device_knob_7_track_4", "desc": "DEVICE Knob 7 Track 4"},
    {"id": 0x16, "channel": 0x06, "name": "device_knob_7_track_5", "desc": "DEVICE Knob 7 Track 5"},
    {"id": 0x16, "channel": 0x07, "name": "device_knob_7_track_6", "desc": "DEVICE Knob 7 Track 6"},
    {"id": 0x16, "channel": 0x08, "name": "device_knob_7_track_7", "desc": "DEVICE Knob 7 Track 7"},
    {"id": 0x16, "channel": 0x00, "name": "device_knob_7_track_master", "desc": "DEVICE Knob 7 Track Master"},

    # DEVICE Knob 8
    {"id": 0x17, "channel": 0x01, "name": "device_knob_8_track_0", "desc": "DEVICE Knob 8 Track 0"},
    {"id": 0x17, "channel": 0x02, "name": "device_knob_8_track_1", "desc": "DEVICE Knob 8 Track 1"},
    {"id": 0x17, "channel": 0x03, "name": "device_knob_8_track_2", "desc": "DEVICE Knob 8 Track 2"},
    {"id": 0x17, "channel": 0x04, "name": "device_knob_8_track_3", "desc": "DEVICE Knob 8 Track 3"},
    {"id": 0x17, "channel": 0x05, "name": "device_knob_8_track_4", "desc": "DEVICE Knob 8 Track 4"},
    {"id": 0x17, "channel": 0x06, "name": "device_knob_8_track_5", "desc": "DEVICE Knob 8 Track 5"},
    {"id": 0x17, "channel": 0x07, "name": "device_knob_8_track_6", "desc": "DEVICE Knob 8 Track 6"},
    {"id": 0x17, "channel": 0x08, "name": "device_knob_8_track_7", "desc": "DEVICE Knob 7 Track 7"},
    {"id": 0x16, "channel": 0x00, "name": "device_knob_7_track_master", "desc": "DEVICE Knob 7 Track Master"},

    # Led state
    # DEVICE Knob Type 1 to DEVICE Knob Type 8
    {"id": 0x10, "channel": 0x01, "name": "device_knob_type_1_track_0", "desc": "DEVICE Knob Type 1 Track 0"},
    {"id": 0x10, "channel": 0x02, "name": "device_knob_type_1_track_1", "desc": "DEVICE Knob Type 1 Track 1"},
    {"id": 0x10, "channel": 0x03, "name": "device_knob_type_1_track_2", "desc": "DEVICE Knob Type 1 Track 2"},
    {"id": 0x10, "channel": 0x04, "name": "device_knob_type_1_track_3", "desc": "DEVICE Knob Type 1 Track 3"},
    {"id": 0x10, "channel": 0x05, "name": "device_knob_type_1_track_4", "desc": "DEVICE Knob Type 1 Track 4"},
    {"id": 0x10, "channel": 0x06, "name": "device_knob_type_1_track_5", "desc": "DEVICE Knob Type 1 Track 5"},
    {"id": 0x10, "channel": 0x07, "name": "device_knob_type_1_track_6", "desc": "DEVICE Knob Type 1 Track 6"},
    {"id": 0x10, "channel": 0x08, "name": "device_knob_type_1_track_7", "desc": "DEVICE Knob Type 1 Track 7"},
    {"id": 0x10, "channel": 0x00, "name": "device_knob_type_1_track_master", "desc": "DEVICE Knob Type 1 Track Master"},


    # DEVICE Knob Type 2 to DEVICE Knob Type 8
    {"id": 0x11, "channel": 0x01, "name": "device_knob_type_2_track_0", "desc": "DEVICE Knob Type 2 Track 0"},
    {"id": 0x11, "channel": 0x02, "name": "device_knob_type_2_track_1", "desc": "DEVICE Knob Type 2 Track 1"},
    {"id": 0x11, "channel": 0x03, "name": "device_knob_type_2_track_2", "desc": "DEVICE Knob Type 2 Track 2"},
    {"id": 0x11, "channel": 0x04, "name": "device_knob_type_2_track_3", "desc": "DEVICE Knob Type 2 Track 3"},
    {"id": 0x11, "channel": 0x05, "name": "device_knob_type_2_track_4", "desc": "DEVICE Knob Type 2 Track 4"},
    {"id": 0x11, "channel": 0x06, "name": "device_knob_type_2_track_5", "desc": "DEVICE Knob Type 2 Track 5"},
    {"id": 0x11, "channel": 0x07, "name": "device_knob_type_2_track_6", "desc": "DEVICE Knob Type 2 Track 6"},
    {"id": 0x11, "channel": 0x08, "name": "device_knob_type_2_track_7", "desc": "DEVICE Knob Type 2 Track 7"},
    {"id": 0x11, "channel": 0x00, "name": "device_knob_type_2_track_master", "desc": "DEVICE Knob Type 2 Track Master"},

    # DEVICE Knob Type 3 to DEVICE Knob Type 8
    {"id": 0x12, "channel": 0x01, "name": "device_knob_type_3_track_0", "desc": "DEVICE Knob Type 3 Track 0"},
    {"id": 0x12, "channel": 0x02, "name": "device_knob_type_3_track_1", "desc": "DEVICE Knob Type 3 Track 1"},
    {"id": 0x12, "channel": 0x03, "name": "device_knob_type_3_track_2", "desc": "DEVICE Knob Type 3 Track 2"},
    {"id": 0x12, "channel": 0x04, "name": "device_knob_type_3_track_3", "desc": "DEVICE Knob Type 3 Track 3"},
    {"id": 0x12, "channel": 0x05, "name": "device_knob_type_3_track_4", "desc": "DEVICE Knob Type 3 Track 4"},
    {"id": 0x12, "channel": 0x06, "name": "device_knob_type_3_track_5", "desc": "DEVICE Knob Type 3 Track 5"},
    {"id": 0x12, "channel": 0x07, "name": "device_knob_type_3_track_6", "desc": "DEVICE Knob Type 3 Track 6"},
    {"id": 0x12, "channel": 0x08, "name": "device_knob_type_3_track_7", "desc": "DEVICE Knob Type 3 Track 7"},
    {"id": 0x12, "channel": 0x00, "name": "device_knob_type_3_track_master", "desc": "DEVICE Knob Type 3 Track Master"},

    # DEVICE Knob Type 4 to DEVICE Knob Type 8
    {"id": 0x13, "channel": 0x01, "name": "device_knob_type_4_track_0", "desc": "DEVICE Knob Type 4 Track 0"},
    {"id": 0x13, "channel": 0x02, "name": "device_knob_type_4_track_1", "desc": "DEVICE Knob Type 4 Track 1"},
    {"id": 0x13, "channel": 0x03, "name": "device_knob_type_4_track_2", "desc": "DEVICE Knob Type 4 Track 2"},
    {"id": 0x13, "channel": 0x04, "name": "device_knob_type_4_track_3", "desc": "DEVICE Knob Type 4 Track 3"},
    {"id": 0x13, "channel": 0x05, "name": "device_knob_type_4_track_4", "desc": "DEVICE Knob Type 4 Track 4"},
    {"id": 0x13, "channel": 0x06, "name": "device_knob_type_4_track_5", "desc": "DEVICE Knob Type 4 Track 5"},
    {"id": 0x13, "channel": 0x07, "name": "device_knob_type_4_track_6", "desc": "DEVICE Knob Type 4 Track 6"},
    {"id": 0x13, "channel": 0x08, "name": "device_knob_type_4_track_7", "desc": "DEVICE Knob Type 4 Track 7"},
    {"id": 0x13, "channel": 0x00, "name": "device_knob_type_4_track_master", "desc": "DEVICE Knob Type 4 Track Master"},

    # DEVICE Knob Type 5 to DEVICE Knob Type 8
    {"id": 0x14, "channel": 0x01, "name": "device_knob_type_5_track_0", "desc": "DEVICE Knob Type 5 Track 0"},
    {"id": 0x14, "channel": 0x02, "name": "device_knob_type_5_track_1", "desc": "DEVICE Knob Type 5 Track 1"},
    {"id": 0x14, "channel": 0x03, "name": "device_knob_type_5_track_2", "desc": "DEVICE Knob Type 5 Track 2"},
    {"id": 0x14, "channel": 0x04, "name": "device_knob_type_5_track_3", "desc": "DEVICE Knob Type 5 Track 3"},
    {"id": 0x14, "channel": 0x05, "name": "device_knob_type_5_track_4", "desc": "DEVICE Knob Type 5 Track 4"},
    {"id": 0x14, "channel": 0x06, "name": "device_knob_type_5_track_5", "desc": "DEVICE Knob Type 5 Track 5"},
    {"id": 0x14, "channel": 0x07, "name": "device_knob_type_5_track_6", "desc": "DEVICE Knob Type 5 Track 6"},
    {"id": 0x14, "channel": 0x08, "name": "device_knob_type_5_track_7", "desc": "DEVICE Knob Type 5 Track 7"},
    {"id": 0x14, "channel": 0x00, "name": "device_knob_type_5_track_master", "desc": "DEVICE Knob Type 5 Track Master"},

    # DEVICE Knob Type 6 to DEVICE Knob Type 8
    {"id": 0x15, "channel": 0x01, "name": "device_knob_type_6_track_0", "desc": "DEVICE Knob Type 6 Track 0"},
    {"id": 0x15, "channel": 0x02, "name": "device_knob_type_6_track_1", "desc": "DEVICE Knob Type 6 Track 1"},
    {"id": 0x15, "channel": 0x03, "name": "device_knob_type_6_track_2", "desc": "DEVICE Knob Type 6 Track 2"},
    {"id": 0x15, "channel": 0x04, "name": "device_knob_type_6_track_3", "desc": "DEVICE Knob Type 6 Track 3"},
    {"id": 0x15, "channel": 0x05, "name": "device_knob_type_6_track_4", "desc": "DEVICE Knob Type 6 Track 4"},
    {"id": 0x15, "channel": 0x06, "name": "device_knob_type_6_track_5", "desc": "DEVICE Knob Type 6 Track 5"},
    {"id": 0x15, "channel": 0x07, "name": "device_knob_type_6_track_6", "desc": "DEVICE Knob Type 6 Track 6"},
    {"id": 0x15, "channel": 0x08, "name": "device_knob_type_6_track_7", "desc": "DEVICE Knob Type 6 Track 7"},
    {"id": 0x15, "channel": 0x09, "name": "device_knob_type_6_track_master", "desc": "DEVICE Knob Type 6 Track Master"},

    # DEVICE Knob Type 7 to DEVICE Knob Type 8
    {"id": 0x16, "channel": 0x01, "name": "device_knob_type_7_track_0", "desc": "DEVICE Knob Type 7 Track 0"},
    {"id": 0x16, "channel": 0x02, "name": "device_knob_type_7_track_1", "desc": "DEVICE Knob Type 7 Track 1"},
    {"id": 0x16, "channel": 0x03, "name": "device_knob_type_7_track_2", "desc": "DEVICE Knob Type 7 Track 2"},
    {"id": 0x16, "channel": 0x04, "name": "device_knob_type_7_track_3", "desc": "DEVICE Knob Type 7 Track 3"},
    {"id": 0x16, "channel": 0x05, "name": "device_knob_type_7_track_4", "desc": "DEVICE Knob Type 7 Track 4"},
    {"id": 0x16, "channel": 0x06, "name": "device_knob_type_7_track_5", "desc": "DEVICE Knob Type 7 Track 5"},
    {"id": 0x16, "channel": 0x07, "name": "device_knob_type_7_track_6", "desc": "DEVICE Knob Type 7 Track 6"},
    {"id": 0x16, "channel": 0x08, "name": "device_knob_type_7_track_7", "desc": "DEVICE Knob Type 7 Track 7"},
    {"id": 0x16, "channel": 0x00, "name": "device_knob_type_7_track_master", "desc": "DEVICE Knob Type 7 Track Master"},

    # DEVICE Knob Type 8
    {"id": 0x17, "channel": 0x01, "name": "device_knob_type_8_track_0", "desc": "DEVICE Knob Type 8 Track 0"},
    {"id": 0x17, "channel": 0x02, "name": "device_knob_type_8_track_1", "desc": "DEVICE Knob Type 8 Track 1"},
    {"id": 0x17, "channel": 0x03, "name": "device_knob_type_8_track_2", "desc": "DEVICE Knob Type 8 Track 2"},
    {"id": 0x17, "channel": 0x04, "name": "device_knob_type_8_track_3", "desc": "DEVICE Knob Type 8 Track 3"},
    {"id": 0x17, "channel": 0x05, "name": "device_knob_type_8_track_4", "desc": "DEVICE Knob Type 8 Track 4"},
    {"id": 0x17, "channel": 0x06, "name": "device_knob_type_8_track_5", "desc": "DEVICE Knob Type 8 Track 5"},
    {"id": 0x17, "channel": 0x07, "name": "device_knob_type_8_track_6", "desc": "DEVICE Knob Type 8 Track 6"},
    {"id": 0x17, "channel": 0x08, "name": "device_knob_type_8_track_7", "desc": "DEVICE Knob Type 7 Track 7"},
    {"id": 0x16, "channel": 0x00, "name": "device_knob_type_7_track_master", "desc": "DEVICE Knob Type 7 Track Master"}
    
]