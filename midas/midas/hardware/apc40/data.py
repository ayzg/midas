# Models the Drum Pattern Application for the APC40 device
#import midas.hardware.apc40.data as ApcData
#import channels as flslChannels
#import flsl.device
# Outbound APC40 Sysex Message Types
# There will be four types of messages from the PC host to the device.
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
# 6            0x0   Number of data bytes to follow (most significant)
# 7            0x04   Number of data bytes to follow (least significant)
# 8            0x40 or 0x41 or 0x42   Application/Configuration identifier
# 9            <Version High> PC application Software version major
# 10           <Version Low> PC application Software version minor
# 11           <Bugfix Level> PC Application Software bug-fix level
# 12           0xF7   MIDI System exclusive message terminator



APC40_N_CHANNELS = 9
APC40_N_CHANNELS_NO_MASTER = APC40_N_CHANNELS - 1
APC40_N_CLIP_LAUNCH_ROWS = 5
APC40_N_DEVICE_CONTROL_BUTTONS = 8
APC40_N_DEVICE_CONTROL_CONTROLLER_ABSOLUTE = 8

APC40_OUT_MIDI_COMMAND_SYSTEM = 0xF0
APC40_OUT_MIDI_COMMAND_LED_ON = 0x90
APC40_OUT_MIDI_COMMAND_LED_OFF = 0x80
APC40_OUT_MIDI_COMMAND_CONTROL_SET = 0xB0

APC40_IN_MIDI_COMMAND_BUTTON_PRESS = 0x90
APC40_IN_MIDI_COMMAND_BUTTON_RELEASE = 0x80
APC40_IN_MIDI_COMMAND_CONTROL_CHANGE = 0xB0
APC40_IN_MIDI_COMMAND_CONTROL_RELATIVE_CHANGE = 0xB0

APC40_OUT_MIDI_CHANNEL_MASTER = 0x0


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

APC40_BUTTONS_CLIP_LAUNCH = [(None,None)] * ((APC40_N_CLIP_LAUNCH_ROWS*APC40_N_CHANNELS_NO_MASTER))

for id in range(APC40_N_CLIP_LAUNCH_ROWS) : 
    for channel in range(APC40_N_CHANNELS_NO_MASTER) :
        APC40_BUTTONS_CLIP_LAUNCH[(id*APC40_N_CHANNELS_NO_MASTER) + channel] = channel , 0x35 + id

APC40_BUTTONS_RECARM = [(None,None)] * (APC40_N_CHANNELS_NO_MASTER)
APC40_BUTTONS_SOLOCUE = [(None,None)] * (APC40_N_CHANNELS_NO_MASTER)
APC40_BUTTONS_ACTIVATOR = [(None,None)] * (APC40_N_CHANNELS_NO_MASTER)
APC40_BUTTONS_CLIP_STOP = [(None,None)] * (APC40_N_CHANNELS_NO_MASTER)
APC40_BUTTONS_TRACK_SELECT = [(None,None)] * (APC40_N_CHANNELS_NO_MASTER)
for channel in range(APC40_N_CHANNELS_NO_MASTER) :
    APC40_BUTTONS_RECARM[channel] = channel,0x30
    APC40_BUTTONS_SOLOCUE[channel] = channel,0x31
    APC40_BUTTONS_ACTIVATOR[channel] = channel,0x32
    APC40_BUTTONS_CLIP_STOP[channel] = channel,0x34
    APC40_BUTTONS_TRACK_SELECT[channel] = channel ,0x33
    
APC40_BUTTONS_SCENE_LAUNCH = [(None,None)] * (5)
for i in range(5):
    APC40_BUTTONS_SCENE_LAUNCH[i] = APC40_OUT_MIDI_CHANNEL_MASTER, 0x52 + i

APC40_BUTTON_MASTER = APC40_OUT_MIDI_CHANNEL_MASTER, 0x50
APC40_BUTTON_STOP_ALL_CLIPS = APC40_OUT_MIDI_CHANNEL_MASTER, 0x51

APC40_BUTTON_PAN = APC40_OUT_MIDI_CHANNEL_MASTER , 0x57
APC40_BUTTON_SEND_A = APC40_OUT_MIDI_CHANNEL_MASTER, 0x58
APC40_BUTTON_SEND_B = APC40_OUT_MIDI_CHANNEL_MASTER, 0x59
APC40_BUTTON_SEND_C = APC40_OUT_MIDI_CHANNEL_MASTER, 0x5A

APC40_BUTTON_PLAY = APC40_OUT_MIDI_CHANNEL_MASTER ,0x5B #(G_6) Momentary 
APC40_BUTTON_STOP = APC40_OUT_MIDI_CHANNEL_MASTER, 0x5C #(G#6) Momentary 
APC40_BUTTON_RECORD= APC40_OUT_MIDI_CHANNEL_MASTER ,0x5D #(A_6) Momentary 
APC40_BUTTON_UP = APC40_OUT_MIDI_CHANNEL_MASTER, 0x5E #(A#6) Momentary 
APC40_BUTTON_DOWN= APC40_OUT_MIDI_CHANNEL_MASTER, 0x5F# (B_6) Momentary 
APC40_BUTTON_RIGHT= APC40_OUT_MIDI_CHANNEL_MASTER, 0x60# (C_7) Momentary 
APC40_BUTTON_LEFT = APC40_OUT_MIDI_CHANNEL_MASTER, 0x61 #(C#7) Momentary 
APC40_BUTTON_SHIFT = APC40_OUT_MIDI_CHANNEL_MASTER, 0x62 #(D_7) Momentary 
APC40_BUTTON_TAP_TEMPO= APC40_OUT_MIDI_CHANNEL_MASTER,0x63# (D#7) Momentary 
APC40_BUTTON_NUDGE_PLUS = APC40_OUT_MIDI_CHANNEL_MASTER,0x64 #(E_7) Momentary 
APC40_BUTTON_NUDGE_MINUS = APC40_OUT_MIDI_CHANNEL_MASTER,0x65 #(F_7) Momentary

APC40_BUTTONS_CLIPTRACK = [(None, 0x3A)] * APC40_N_CHANNELS # Toggle
APC40_BUTTONS_DEVICEONOFF = [(None, 0x3B)] * APC40_N_CHANNELS # Toggle
APC40_BUTTONS_DEVICELEFT = [(None, 0x3C)] * APC40_N_CHANNELS # Toggle
APC40_BUTTONS_DEVICERIGHT = [(None, 0x3D)] * APC40_N_CHANNELS # Toggle
APC40_BUTTONS_DETAILVIEW = [(None, 0x3E)] * APC40_N_CHANNELS # Toggle
APC40_BUTTONS_RECQUANTIZATION = [(None, 0x3F)] * APC40_N_CHANNELS # Toggle
APC40_BUTTONS_MIDIOVERDUB = [(None, 0x40)] * APC40_N_CHANNELS # Toggle 
APC40_BUTTONS_METRONOME = [(None, 0x41)] * APC40_N_CHANNELS # Toggle

for channel in range(APC40_N_CHANNELS) :
    APC40_BUTTONS_CLIPTRACK[channel] = channel,0x3A
    APC40_BUTTONS_DEVICEONOFF[channel] = channel,0x3B
    APC40_BUTTONS_DEVICELEFT[channel] = channel,0x3C
    APC40_BUTTONS_DEVICERIGHT[channel] = channel,0x3D
    APC40_BUTTONS_DETAILVIEW[channel] = channel, 0x3E
    APC40_BUTTONS_RECQUANTIZATION[channel] = channel, 0x3F
    APC40_BUTTONS_MIDIOVERDUB[channel] = channel,0x40
    APC40_BUTTONS_METRONOME[channel] = channel,0x41
    
APC40_BUTTONS_DEVICE_CONTROL = [
    APC40_BUTTONS_CLIPTRACK +
    APC40_BUTTONS_DEVICEONOFF +
    APC40_BUTTONS_DEVICELEFT +
    APC40_BUTTONS_DEVICERIGHT +
    APC40_BUTTONS_DETAILVIEW +
    APC40_BUTTONS_RECQUANTIZATION +
    APC40_BUTTONS_MIDIOVERDUB +
    APC40_BUTTONS_METRONOME
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

APC40_CONTROLLER_FADER = APC40_OUT_MIDI_CHANNEL_MASTER ,0x0F
APC40_CONTROLLER_MASTER_LEVEL = APC40_OUT_MIDI_CHANNEL_MASTER , 0x0E
APC40_CONTROLLER_FOOTSWITCH_1 = APC40_OUT_MIDI_CHANNEL_MASTER , 0x40
APC40_CONTROLLER_FOOTSWITCH_2 = APC40_OUT_MIDI_CHANNEL_MASTER , 0x43


APC40_CONTROLLERS_TRACK_LEVEL = [(None,None)] * APC40_N_CHANNELS_NO_MASTER
for channel in range(APC40_N_CHANNELS_NO_MASTER):
    APC40_CONTROLLERS_TRACK_LEVEL[channel] = channel, 0x07   

APC40_CONTROLLERS_TRACK_CONTROL_ABSOLUTE = [(None,None)] * 8
for i in range(APC40_N_DEVICE_CONTROL_CONTROLLER_ABSOLUTE) :
    APC40_CONTROLLERS_TRACK_CONTROL_ABSOLUTE[i] = APC40_OUT_MIDI_CHANNEL_MASTER, 0x30 + i

APC40_CONTROLLERS_TRACK_CONTROL_LEDRINGTYPE = [(None,None)] * 8
for i in range(APC40_N_DEVICE_CONTROL_CONTROLLER_ABSOLUTE) :
    APC40_CONTROLLERS_TRACK_CONTROL_ABSOLUTE[i] = APC40_OUT_MIDI_CHANNEL_MASTER, 0x38 + i

APC40_CONTROLLERS_DEVICE_CONTROL_ABSOLUTE = [(None,None)] * (APC40_N_DEVICE_CONTROL_CONTROLLER_ABSOLUTE * APC40_N_CHANNELS)
for id in range(APC40_N_DEVICE_CONTROL_CONTROLLER_ABSOLUTE) :
    for channel in range(APC40_N_CHANNELS) :
        APC40_CONTROLLERS_DEVICE_CONTROL_ABSOLUTE[channel+(id*APC40_N_CHANNELS)] = channel , 0x10 + id

APC40_CONTROLLERS_DEVICE_CONTROL_LEDRINGTYPE = [(None,None)] * (APC40_N_DEVICE_CONTROL_CONTROLLER_ABSOLUTE * APC40_N_CHANNELS)
for id in range(APC40_N_DEVICE_CONTROL_CONTROLLER_ABSOLUTE) :
    for channel in range(APC40_N_CHANNELS) :
        APC40_CONTROLLERS_DEVICE_CONTROL_LEDRINGTYPE[channel+(id*APC40_N_CHANNELS)] = channel , 0x18 + id

APC40_CONTROLLER_CUE_LEVEL_RELATIVE = APC40_OUT_MIDI_CHANNEL_MASTER ,0x2F

# Absolute controller LED state types
APC40_LED_ABSOLUTE_CONTROLLER_STATE_OFF = 0
APC40_LED_ABSOLUTE_CONTROLLER_STATE_SINGLE = 1
APC40_LED_ABSOLUTE_CONTROLLER_STATE_VOLUMESTYLE = 2
APC40_LED_ABSOLUTE_CONTROLLER_STATE_PANSTYLE = 3

APC40_LED_ABSOLUTE_CONTROLLER_STATES= [
    APC40_LED_ABSOLUTE_CONTROLLER_STATE_OFF,
    APC40_LED_ABSOLUTE_CONTROLLER_STATE_SINGLE,
    APC40_LED_ABSOLUTE_CONTROLLER_STATE_VOLUMESTYLE,
    APC40_LED_ABSOLUTE_CONTROLLER_STATE_PANSTYLE
    ]

# Interpretation of LED Ring Types 
# The LED rings will display its controller value with the LEDs based on the LED Ring Types. This LED Ring 
# Type can be set by the Host by sending an appropriate controller value message. The “Min” and “Max” 
# columns below will state the range of the controller value that will match the LED states as shown in the 
# “Display” column. The “LED STATES” column below will show the state of each of the 15 LEDs going from 
# left to right. A “0” indicates that the LED within the LED ring is OFF. A “1” indicates that the LED within the 
# LED ring in ON. 
APC40_LED_STATES_CONTROLLER_SINGLE = [
(0,3,0b100000000000000)
,(4,8,0b110000000000000)
,(9,12,0b010000000000000)
,(13,17,0b011000000000000)
,(18,21,0b001000000000000)
,(22,25,0b001100000000000)
,(26,30,0b000100000000000)
,(31,34,0b000110000000000)
,(35,38,0b000010000000000)
,(39,43,0b000011000000000)
,(44,47,0b000001000000000)
,(48,52,0b000001100000000)
,(53,56,0b000000100000000)
,(57,60,0b000000110000000)
,(61,65,0b000000010000000)
,(66,69,0b000000011000000)
,(70,73,0b000000001000000)
,(74,78,0b000000001100000)
,(79,82,0b000000000100000)
,(83,87,0b000000000110000)
,(88,91,0b000000000010000)
,(92,95,0b000000000011000)
,(96,100,0b000000000001000)
,(101,104,0b000000000001100)
,(105,108,0b000000000000100)
,(109,113,0b000000000000110)
,(114,117,0b000000000000010)
,(118,122,0b000000000000011)
,(123,127,0b000000000000001)
]

# B. VOLUME STYLE
APC40_LED_STATES_CONTROLLER_VOLUME = [
    (0, 0, 0b000000000000000),
    (1, 9, 0b100000000000000),
    (10, 18, 0b110000000000000),
    (19, 27, 0b111000000000000),
    (28, 36, 0b111100000000000),
    (37, 45, 0b111110000000000),
    (46, 54, 0b111111000000000),
    (55, 63, 0b111111100000000),
    (64, 71, 0b111111110000000),
    (72, 80, 0b111111111000000),
    (81, 89, 0b111111111100000),
    (90, 98, 0b111111111110000),
    (99, 107, 0b111111111111000),
    (108, 116, 0b111111111111100),
    (117, 126, 0b111111111111110),
    (127, 127, 0b111111111111111)
]

# C. PAN STYLE
APC40_LED_STATES_CONTROLLER_PAN = [
    (0, 8, 0b111111110000000),
    (9, 17, 0b011111110000000),
    (18, 26, 0b001111110000000),
    (27, 35, 0b000111110000000),
    (36, 44, 0b000011110000000),
    (45, 53, 0b000001110000000),
    (54, 62, 0b000000110000000),
    (63, 64, 0b000000010000000),
    (65, 73, 0b000000011000000),
    (74, 82, 0b000000011100000),
    (83, 91, 0b000000011110000),
    (92, 100, 0b000000011111000),
    (101, 109, 0b000000011111100),
    (110, 118, 0b000000011111110),
    (119, 127, 0b000000011111111)
]

# Interpretation of MIDI Controller values for Relative Controllers 
# The value in the data field will indicate a relative change; values 01 to 63 describe a positive change and 
# values 127 down to 64 describe a negative change. 
# data value sent interpretation 
# 0x00 No change occured. Control is stationary. 
# 0x01 The controller incremented its value by 1 since the last report 
# 0x02 The controller incremented its value by 2 since the last report 
# ... ... 
# 0x3f The controller incremented its value by 63 since the last report 
# 0x40 The controller decremented its value by 64 since the last report 
# 0x41 The controller decremented its value by 63 since the last report 
# ... ... 
# 0x7e The controller decremented its value by 2 since the last report 
# 0x7f The controller decremented its value by 1 since the last report 
APC40_RELATIVE_CONTROLLER_VALUES = [
    (0x00, 0),
    (0x01, 1),
    (0x02, 2),
    (0x03, 3),
    (0x04, 4),
    (0x05, 5),
    (0x06, 6),
    (0x07, 7),
    (0x08, 8),
    (0x09, 9),
    (0x0A, 10),
    (0x0B, 11),
    (0x0C, 12),
    (0x0D, 13),
    (0x0E, 14),
    (0x0F, 15),
    (0x10, 16),
    (0x11, 17),
    (0x12, 18),
    (0x13, 19),
    (0x14, 20),
    (0x15, 21),
    (0x16, 22),
    (0x17, 23),
    (0x18, 24),
    (0x19, 25),
    (0x1A, 26),
    (0x1B, 27),
    (0x1C, 28),
    (0x1D, 29),
    (0x1E, 30),
    (0x1F, 31),
    (0x20, 32),
    (0x21, 33),
    (0x22, 34),
    (0x23, 35),
    (0x24, 36),
    (0x25, 37),
    (0x26, 38),
    (0x27, 39),
    (0x28, 40),
    (0x29, 41),
    (0x2A, 42),
    (0x2B, 43),
    (0x2C, 44),
    (0x2D, 45),
    (0x2E, 46),
    (0x2F, 47),
    (0x30, 48),
    (0x31, 49),
    (0x32, 50),
    (0x33, 51),
    (0x34, 52),
    (0x35, 53),
    (0x36, 54),
    (0x37, 55),
    (0x38, 56),
    (0x39, 57),
    (0x3A, 58),
    (0x3B, 59),
    (0x3C, 60),
    (0x3D, 61),
    (0x3E, 62),
    (0x3F, 63),
    (0x40, -64),
    (0x41, -63),
    (0x42, -62),
    (0x43, -61),
    (0x44, -60),
    (0x45, -59),
    (0x46, -58),
    (0x47, -57),
    (0x48, -56),
    (0x49, -55),
    (0x4A, -54),
    (0x4B, -53),
    (0x4C, -52),
    (0x4D, -51),
    (0x4E, -50),
    (0x4F, -49),
    (0x50, -48),
    (0x51, -47),
    (0x52, -46),
    (0x53, -45),
    (0x54, -44),
    (0x55, -43),
    (0x56, -42),
    (0x57, -41),
    (0x58, -40),
    (0x59, -39),
    (0x5A, -38),
    (0x5B, -37),
    (0x5C, -36),
    (0x5D, -35),
    (0x5E, -34),
    (0x5F, -33),
    (0x60, -32),
    (0x61, -31),
    (0x62, -30),
    (0x63, -29),
    (0x64, -28),
    (0x65, -27),
    (0x66, -26),
    (0x67, -25),
    (0x68, -24),
    (0x69, -23),
    (0x6A, -22),
    (0x6B, -21),
    (0x6C, -20),
    (0x6D, -19),
    (0x6E, -18),
    (0x6F, -17),
    (0x70, -16),
    (0x71, -15),
    (0x72, -14),
    (0x73, -13),
    (0x74, -12),
    (0x75, -11),
    (0x76, -10),
    (0x77, -9),
    (0x78, -8),
    (0x79, -7),
    (0x7A, -6),
    (0x7B, -5),
    (0x7C, -4),
    (0x7D, -3),
    (0x7E, -2),
    (0x7F, -1)
]



