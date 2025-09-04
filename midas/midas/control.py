#import flsi as FLSI

class MidasControl :
    __data = [int(-1),int(-1)]
    def __init__(self,group:int = -1,index:int = -1):
        self.__data[0] = group
        self.__data[1] = index    
    def data1(self)->int:
        return self.__data[0]
    def data2(self)->int:
        return self.__data[1]
    def data(self)-> [int,int]:
        return self.__data
    def __hash__(self):
        return hash((self.__data[0],
                self.__data[1]))
    def __eq__(self, other):
        return ( ( self.__data[0],
                self.__data[1] ) == ( other.__data[0],other.__data[1]) )
    def __str__(self):
        return "param 1: {0} param 2: {1}  ".format(self.__data[0], self.__data[1])
    
    def group(self)->int:
        return self.__data[0]
    def index(self)->int:
        return self.__data[1]
    
class MidiControl :
    __data = [int(-1),int(-1)]
    
    def __init__(self,d1:int = -1,d2:int = -1):
        self.__data = [d1,d2]
    def data1(self)->int:
        return self.__data[0]
    def data2(self)->int:
        return self.__data[1]
    def data(self)-> [int,int]:
        return self.__data
    def __hash__(self):
        return hash((self.__data[0],
                self.__data[1]))
    def __eq__(self, other):
        return ( ( self.__data[0],
                self.__data[1] ) == ( other.__data[0],other.__data[1]) )
    def __str__(self):
        return "param 1: {0} param 2: {1}  ".format(self.__data[0], self.__data[1])
    
    def channel(self)->int:
        return self.__data[0]
    def id(self)->int:
        return self.__data[1]

class MidasMidiControlMap:

    def __init__(self):
        self.__data = {}
        pass   
    def data(self):
        return self.__data      
    def emplace(self,midas_control : MidasControl,midi_control : MidiControl):
        self.__data[midas_control] = midi_control
    def get_midas(self,midi_control : MidiControl): # returns a list of all midas controls associated with this midi input
        return [a_midas_control for a_midas_control,a_midi_control in self.__data.items() if a_midi_control == midi_control]
    def get_first_midas(self,midi_control : MidiControl): # returns the first midas control associated with this input
        for a_midas_control, a_midi_control in self.__data.items():
            if a_midi_control == midi_control:
                return a_midas_control
        return None
    def get_midi(self,midas_control : MidasControl):
        return self.__data[midas_control]
        
    def get_all(self):
        return self.__data.values()
    
    def contains_equal(self,midas_control : MidasControl,midi_control_d1 : int,midi_control_d2 : int):
        if midas_control in self.__data:
            if (self.__data[midas_control]).data1() == midi_control_d1 and (self.__data[midas_control]).data2() == midi_control_d2 :
                return True
        return False
        
    def generate(self,midas_control_list:list[MidasControl],midi_control_list:list[MidiControl]):
        for i in range(len(midas_control_list)) :
            if i < len(midi_control_list):
                self.__data[midas_control_list[i]] = midi_control_list[i]
            else:
                self.__data[midas_control_list[i]] = MidiControl()
        pass
    
    def regenerate(self,midas_control_list:list[MidasControl],midi_control_list:list[MidiControl]):
        self.__data.clear()
        for i in range(len(midas_control_list)) :
            if i < len(midi_control_list):
                self.__data[midas_control_list[i]] = midi_control_list[i]
            else:
                self.__data[midas_control_list[i]] = MidiControl()
        pass
    
    def retarget(self,midi_control_list:list[MidiControl]):
        data_keys_list = list(self.__data.keys())
        for i in range(len(data_keys_list)) :
            if i < len(midi_control_list):
                self.__data[data_keys_list[i]] = midi_control_list[i]
            else:
                self.__data[data_keys_list[i]] = MidiControl()
        pass    

class MidasMidiCommandMap:

    def __init__(self):
        self.__data = {}
        pass   
    def data(self):
        return self.__data      
    def emplace(self,midas_command : int,midi_command : int):
        self.__data[midas_command] = midi_command
    def get_midas(self,midi_command : int): # returns a list of all midas commands associated with this midi input
        return [a_midas_command for a_midas_command,a_midi_command in self.__data.items() if a_midi_command == midi_command]
    def get_first_midas(self,midi_command : int): # returns the first midas command associated with this input
        for a_midas_command, a_midi_command in self.__data.items():
            if a_midi_command == midi_command:
                return a_midas_command
        return None
    def get_midi(self,midas_command : int):
        return self.__data[midas_command]
        
    def get_all(self):
        return self.__data.values()
    
    def contains_equal(self,midas_command : int,midi_command_d1 : int,midi_command_d2 : int):
        if midas_command in self.__data:
            if self.__data[midas_command] == midi_command_d1 :
                return True
        return False
        
    def generate(self,midas_command_list:list[int],midi_command_list:list[int]):
        for i in range(len(midas_command_list)) :
            if i < len(midi_command_list):
                self.__data[midas_command_list[i]] = midi_command_list[i]
            else:
                self.__data[midas_command_list[i]] = int()
        pass
    
    def regenerate(self,midas_command_list:list[int],midi_command_list:list[int]):
        self.__data.clear()
        for i in range(len(midas_command_list)) :
            if i < len(midi_command_list):
                print(i)
                self.__data[midas_command_list[i]] = midi_command_list[i]
            else:
                self.__data[midas_command_list[i]] = int()
        pass
    
    def retarget(self,midi_command_list:list[int]):
        data_keys_list = list(self.__data.keys())
        for i in range(len(data_keys_list)) :
            if i < len(midi_command_list):
                self.__data[data_keys_list[i]] = midi_command_list[i]
            else:
                self.__data[data_keys_list[i]] = int()
        pass    
    


class ApplicationBase:
    _button_map : MidasMidiControlMap
    _controller_map : MidasMidiControlMap
    _command_map : MidasMidiCommandMap  

    def __init_subclass__(cls,**kwargs): 
        cls._button_map = MidasMidiControlMap()   
        cls._controller_map = MidasMidiControlMap()
        cls._command_map = MidasMidiCommandMap()

    # Called by midas OS
    # Events recieved from Fruity Loops
    def __onFruityLoopUpdate(self):
        self.onMidasUpdate()
        self.onFruityLoopUpdate()
        pass
    def __onFruityLoopProgramChange(self,flags):
        self.onMidasUpdate()
        self.onFruityLoopProgramChange(flags)
        pass
    def __onFruityLoopScriptInit(self):    
        self.onMidasUpdate()
        self.onFruityLoopScriptInit()
        pass
    # Events Recieved from device
    def __onFruityLoopMidiInput(self,message):
        self.onMidasUpdate()
        self.onFruityLoopMidiInput(message)
        self._onMidasProcessInternal(message.status,message.port,message.data1,message.data2,message.sysex)
        pass
    def __onFruityLoopSysexInput(self,message):
        self.onMidasUpdate()
        self.onFruityLoopSysexInput(message)
        self._onMidasProcessInternal(message.status,message.port,message.data1,message.data2,message.sysex)
        pass  

    def _onMidasProcessInternal(self,status,port,data1,data2,sysex = None): # Converts midi signal to midas event based on current map
        self.onMidasProcess(status,port,data1,data2,sysex)
        for midas_command in self._command_map.get_midas(status-port):
            for midas_control in self._button_map.get_midas(MidiControl(port,data1)):
                self.onMidasEvent(midas_control,midas_command)
        pass        
    # abstract callbacks to be written for each application
    def onFruityLoopUpdate(self):
        pass
    def onFruityLoopProgramChange(self,flags):
        pass
    def onFruityLoopScriptInit(self):    
        pass
    # Events Recieved from device
    def onFruityLoopMidiInput(self,message):
        pass
    def onFruityLoopSysexInput(self,message):
        pass  
    # Called on all callbacks from FLSTUDIO 
    def onMidasUpdate(self):
        pass

    def onMidasProcess(self,status,port,data1,data2,sysex = None):
        pass
    def onMidasEvent(self,control : MidasControl, command : int):
        pass
        

class TestApp(ApplicationBase):
    def onMidasProcess(self,status,port,data1,data2,sysex = None):
        if self._button_map.contains_equal(MidasControl(0,0),1,7):
            print(self._button_map.data())
        pass
    def onMidasEvent(self,control : MidasControl, command : int):
        if command ==  BEATMAKER_COMMAND_IN_NOTEON:
            pass
        elif  command ==  BEATMAKER_COMMAND_IN_NOTEOFF:
            print("Note On Detected")
            if control == BEATMAKER_BUTTON_PAD_FUNC_CHANNEL_UP: 
                print("Func Channel + Detected.")
                if self.target_channel > 0:
                    self.target_channel -= 1
                #flslChannels.select_single_channel(flslChannels.get_channel_index(self.target_channel)) # Set the selected channel to the current_channel in FL Studio
            elif control == BEATMAKER_BUTTON_PAD_FUNC_CHANNEL_DOWN: 
                if self.target_channel < self.channel_count - 1:
                    self.target_channel += 1
                #flslChannels.select_single_channel(flslChannels.get_channel_index(self.target_channel)) # Set the selected channel to the current_channel in FL Studio              
            elif control == BEATMAKER_BUTTON_PAD_FUNC_ZOOM_IN:
                self.zoom_in()        
            elif control == BEATMAKER_BUTTON_PAD_FUNC_ZOOM_OUT: 
                self.zoom_out() 
            elif control == BEATMAKER_BUTTON_PAD_FUNC_MOVE_LEFT: 
                if self.channel_offset > 0:
                    self.channel_offset -= 1
            elif control == BEATMAKER_BUTTON_PAD_FUNC_MOVE_RIGHT: 
                if self.channel_offset < 4:
                    self.channel_offset += self.channel_offset
            elif control == BEATMAKER_BUTTON_PAD_FUNC_FILL: 
                if self.is_filling == False:
                    self.is_filling = True
                else:
                    self.is_filling = False
                    # Apply fill based on self.fill_type
                    if BEATMAKER_FILL_TYPE_16 == self.fill_type:
                        pass
                    elif BEATMAKER_FILL_TYPE_8 == self.fill_type:
                        pass
                    elif BEATMAKER_FILL_TYPE_4 == self.fill_type:
                        pass
                    elif BEATMAKER_FILL_TYPE_16_DOTTED == self.fill_type:
                        pass
                    elif BEATMAKER_FILL_TYPE_8_DOTTED == self.fill_type:
                        pass
                    elif BEATMAKER_FILL_TYPE_4_DOTTED == self.fill_type:
                        pass
                    elif BEATMAKER_FILL_TYPE_16_TRIPLET == self.fill_type:
                        pass
                    elif BEATMAKER_FILL_TYPE_8_TRIPLET == self.fill_type:
                        pass
                    elif BEATMAKER_FILL_TYPE_4_TRIPLET == self.fill_type:
                        pass
            elif control == BEATMAKER_BUTTON_PAD_FUNC_FILL_TYPE: 
                if self.is_filling :
                    if self.fill_type <= 9: # we have 9 fill types
                        self.fill_type += 1
                    else: # warp back to first fill type
                        self.fill_type = BEATMAKER_FILL_TYPE_16
            elif control == BEATMAKER_BUTTON_PAD_FUNC_CLEAR: 
                print("Channel+ button detected.") # handle button presses
            elif control == BEATMAKER_BUTTON_PAD_FUNC_SOLO: 
                print("Channel+ button detected.") # handle button presses
            elif control == BEATMAKER_BUTTON_PAD_FUNC_MUTE: 
                print("Channel+ button detected.") # handle button presses
            elif control == BEATMAKER_BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_COMP_GATE_DIST: 
                print("Channel+ button detected.") # handle button presses
            elif control == BEATMAKER_BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_VOLUME_PAN_PITCH: 
                print("Channel+ button detected.") # handle button presses
            elif control == BEATMAKER_BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_TARGET_BAND: 
                print("Channel+ button detected.") # handle button presses
            elif control == BEATMAKER_BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_COMP_GATE_DIST: 
                print("Channel+ button detected.") # handle button presses                
            elif control in BEATMAKER_BUTTONS_PAD: # handle drum pads
                print("One of the pad buttons detected.") 
        elif  command ==  BEATMAKER_COMMAND_IN_CONTROLCHANGE: # Handle Control Change Commands
                if control == BEATMAKER_CONTROLLER_CHANNEL_CONTROL_VOLUME_PAN_PITCH: 
                    if self.ccvpp_control_state == BEATMAKER_PCVPP_CONTROL_STATE_VOLUME: # Targeting Volume Knob
                        #flslChannels.setChannelVolume(flslChannels.getChannelIndex(DrumPadTargetChannel),event.data2/127.0) # set the volume in fl studio
                        #flsl.device.midi_out_msg_params(176,0,48,event.data2) 				# Update the value of the Track Control 1 Knob Target to the Volume of selected channel
                        pass
                    elif self.ccvpp_control_state == BEATMAKER_PCVPP_CONTROL_STATE_PAN: # Targeting Pan Knob
                        #flslChannels.setChannelPan(flslChannels.getChannelIndex(DrumPadTargetChannel),((event.data2/127.0)*2)-1)
                        #flsl.device.midi_out_msg_params(176,0,48,event.data2)
                        pass
                    elif self.ccvpp_control_state == BEATMAKER_PCVPP_CONTROL_STATE_PITCH: # Targeting Pitch Knob
                        # flslChannels.setChannelPitch(flslChannels.getChannelIndex(DrumPadTargetChannel),((event.data2/127.0)*2)-1)
                        # flsl.device.midi_out_msg_params(176,0,48,event.data2)
                        pass
                elif control == BEATMAKER_CONTROLLER_CHANNEL_CONTROL_COMP_GATE_DIST: 
                        pass  

        print("Midas command recieved:", command)
        if command == 0:
            print("Command 0 detected.")
            if control == MidasControl(0,0):
                print("Midas Control 0 Detected")  
  


class TestApp2(ApplicationBase):
    def onMidasProcess(self,status,port,data1,data2,sysex = None):
        #self.my_int = status
        if self._button_map.contains_equal(MidasControl(0,0),1,8):
            print(self._button_map.data())
        pass
    def onMidasEvent(self,control : MidasControl, command : int):
        print("Midas command recieved:", command)
        if command == 0:
            print("Command 0 detected.")      


# MyTestApp = TestApp()
# MyTestApp._command_map.regenerate([0],[-1])
# MyTestApp._button_map.regenerate([MidasControl(0,0),MidasControl(0,1)],[MidiControl(1,7),MidiControl(5,22)])

# MyTestAppA = TestApp2()
# MyTestAppA._command_map.regenerate([0],[0])
# MyTestAppA._button_map.regenerate([MidasControl(0,0),MidasControl(0,1)],[MidiControl(1,8),MidiControl(5,22)])

# MyTestApp._onMidasProcessInternal(0,1,7,0)
# MyTestAppA._onMidasProcessInternal(0,1,8,0)


BEATMAKER_COMMAND_IN_NOTEON = 0
BEATMAKER_COMMAND_IN_NOTEOFF = 1
BEATMAKER_COMMAND_IN_CONTROLCHANGE = 2

BEATMAKER_COMMAND_OUT_LEDON = 3
BEATMAKER_COMMAND_OUT_LEDOFF = 4
BEATMAKER_COMMAND_OUT_CONTROLSET = 5

BEATMAKER_COMMANDS_IN = [BEATMAKER_COMMAND_IN_NOTEON,BEATMAKER_COMMAND_IN_NOTEOFF,BEATMAKER_COMMAND_IN_CONTROLCHANGE]
BEATMAKER_COMMANDS_OUT = [BEATMAKER_COMMAND_OUT_LEDON,BEATMAKER_COMMAND_OUT_LEDOFF,BEATMAKER_COMMAND_OUT_CONTROLSET]
BEATMAKER_COMMANDS = BEATMAKER_COMMANDS_IN + BEATMAKER_COMMANDS_OUT

BEATMAKER_BUTTONS_GROUP_PAD = 0
BEATMAKER_BUTTONS_GROUP_PAD_FUNC = 1
BEATMAKER_BUTTONS_GROUP_LED_FUNC = 2
BEATMAKER_CONTROLLERS_GROUP_CHANNEL_CONTROL = 0

BEATMAKER_BUTTONS_PAD = [(None, None)] * 32
for i in range(len(BEATMAKER_BUTTONS_PAD)):
    BEATMAKER_BUTTONS_PAD[i] = i, BEATMAKER_BUTTONS_GROUP_PAD

BEATMAKER_BUTTON_PAD_FUNC_CHANNEL_UP = MidasControl(BEATMAKER_BUTTONS_GROUP_PAD_FUNC,0)
BEATMAKER_BUTTON_PAD_FUNC_CHANNEL_DOWN = 1, BEATMAKER_BUTTONS_GROUP_PAD_FUNC
BEATMAKER_BUTTON_PAD_FUNC_ZOOM_IN = 2, BEATMAKER_BUTTONS_GROUP_PAD_FUNC
BEATMAKER_BUTTON_PAD_FUNC_ZOOM_OUT = 3, BEATMAKER_BUTTONS_GROUP_PAD_FUNC
BEATMAKER_BUTTON_PAD_FUNC_MOVE_RIGHT = 4, BEATMAKER_BUTTONS_GROUP_PAD_FUNC
BEATMAKER_BUTTON_PAD_FUNC_MOVE_LEFT = 5, BEATMAKER_BUTTONS_GROUP_PAD_FUNC
BEATMAKER_BUTTON_PAD_FUNC_SOLO = 6, BEATMAKER_BUTTONS_GROUP_PAD_FUNC
BEATMAKER_BUTTON_PAD_FUNC_MUTE = 7, BEATMAKER_BUTTONS_GROUP_PAD_FUNC
BEATMAKER_BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_VOLUME_PAN_PITCH = 8, BEATMAKER_BUTTONS_GROUP_PAD_FUNC
BEATMAKER_BUTTON_PAD_FUNC_FILL = 9, BEATMAKER_BUTTONS_GROUP_PAD_FUNC
BEATMAKER_BUTTON_PAD_FUNC_FILL_TYPE = 10, BEATMAKER_BUTTONS_GROUP_PAD_FUNC
BEATMAKER_BUTTON_PAD_FUNC_CLEAR = 11, BEATMAKER_BUTTONS_GROUP_PAD_FUNC
BEATMAKER_BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_TARGET_BAND = 12, BEATMAKER_BUTTONS_GROUP_PAD_FUNC
BEATMAKER_BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_COMP_GATE_DIST = 13, BEATMAKER_BUTTONS_GROUP_PAD_FUNC

BEATMAKER_BUTTON_LED_FUNC_PROGRAM_CHANGE_CHANNEL_CONTROLS_PAGE = 14, BEATMAKER_BUTTONS_GROUP_LED_FUNC
BEATMAKER_BUTTON_LED_FUNC_MUTE_CGD = 15, BEATMAKER_BUTTONS_GROUP_LED_FUNC  # mute/unmute the compressor gate or distortion/limiter
BEATMAKER_BUTTON_LED_FUNC_MUTE_BAND = 16, BEATMAKER_BUTTONS_GROUP_LED_FUNC
BEATMAKER_BUTTON_LED_FUNC_BAND_TYPE = 17, BEATMAKER_BUTTONS_GROUP_LED_FUNC

BEATMAKER_BUTTONS_PAD_FUNC = [
    BEATMAKER_BUTTON_PAD_FUNC_CHANNEL_UP,
    BEATMAKER_BUTTON_PAD_FUNC_CHANNEL_DOWN,
    BEATMAKER_BUTTON_PAD_FUNC_ZOOM_IN,
    BEATMAKER_BUTTON_PAD_FUNC_ZOOM_OUT,
    BEATMAKER_BUTTON_PAD_FUNC_MOVE_RIGHT,
    BEATMAKER_BUTTON_PAD_FUNC_MOVE_LEFT,
    BEATMAKER_BUTTON_PAD_FUNC_SOLO,
    BEATMAKER_BUTTON_PAD_FUNC_MUTE,
    BEATMAKER_BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_VOLUME_PAN_PITCH,
    BEATMAKER_BUTTON_PAD_FUNC_FILL,
    BEATMAKER_BUTTON_PAD_FUNC_CLEAR,
    BEATMAKER_BUTTON_PAD_FUNC_FILL_TYPE,
    BEATMAKER_BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_TARGET_BAND,
    BEATMAKER_BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_COMP_GATE_DIST,
]

BEATMAKER_BUTTONS_LED_FUNC = [
    BEATMAKER_BUTTON_LED_FUNC_PROGRAM_CHANGE_CHANNEL_CONTROLS_PAGE,
    BEATMAKER_BUTTON_LED_FUNC_MUTE_CGD,
    BEATMAKER_BUTTON_LED_FUNC_MUTE_BAND,
    BEATMAKER_BUTTON_LED_FUNC_BAND_TYPE
]

BEATMAKER_BUTTONS = BEATMAKER_BUTTONS_PAD + BEATMAKER_BUTTONS_PAD_FUNC + BEATMAKER_BUTTONS_LED_FUNC

BEATMAKER_CONTROLLERS_CHANNEL_CONTROL = [(0, 0)] * 8
BEATMAKER_CONTROLLER_CHANNEL_CONTROL_VOLUME_PAN_PITCH = 0 , BEATMAKER_CONTROLLERS_GROUP_CHANNEL_CONTROL
BEATMAKER_CONTROLLER_CHANNEL_CONTROL_COMP_GATE_DIST = 1 , BEATMAKER_CONTROLLERS_GROUP_CHANNEL_CONTROL

for i in range(len(BEATMAKER_CONTROLLERS_CHANNEL_CONTROL)):
    BEATMAKER_CONTROLLERS_CHANNEL_CONTROL[i] = i, BEATMAKER_CONTROLLERS_GROUP_CHANNEL_CONTROL

BEATMAKER_CONTROLLERS = BEATMAKER_CONTROLLERS_CHANNEL_CONTROL

BEATMAKER_PCVPP_CONTROL_STATE_VOLUME = 0
BEATMAKER_PCVPP_CONTROL_STATE_PAN = 1
BEATMAKER_PCVPP_CONTROL_STATE_PITCH = 2
BEATMAKER_PCVPP_CONTROL_STATES = [BEATMAKER_PCVPP_CONTROL_STATE_VOLUME, BEATMAKER_PCVPP_CONTROL_STATE_PAN, BEATMAKER_PCVPP_CONTROL_STATE_PITCH]

BEATMAKER_PCCGD_CONTROL_STATE_COMP = 0
BEATMAKER_PCCGD_CONTROL_STATE_GATE = 1
BEATMAKER_PCCGD_CONTROL_STATE_DIST = 2
BEATMAKER_PCCGD_CONTROL_STATES = [BEATMAKER_PCCGD_CONTROL_STATE_COMP, BEATMAKER_PCCGD_CONTROL_STATE_GATE, BEATMAKER_PCCGD_CONTROL_STATE_DIST]

BEATMAKER_FILL_TYPE_16 = 0
BEATMAKER_FILL_TYPE_8 = 1
BEATMAKER_FILL_TYPE_4 = 2
BEATMAKER_FILL_TYPE_16_DOTTED = 3
BEATMAKER_FILL_TYPE_8_DOTTED = 4
BEATMAKER_FILL_TYPE_4_DOTTED = 5
BEATMAKER_FILL_TYPE_16_TRIPLET = 6
BEATMAKER_FILL_TYPE_8_TRIPLET = 7
BEATMAKER_FILL_TYPE_4_TRIPLET = 8

class App_Beatmaker(ApplicationBase):
    ccvpp_control_state = BEATMAKER_PCVPP_CONTROL_STATE_VOLUME
    zoom_level = 1
    target_channel = 0
    channel_offset = 0
    channel_count = 0 # retrieve value from flsl.channels.channel_count()
    is_filling = False
    fill_type = BEATMAKER_FILL_TYPE_16

    def onMidasEvent(self,control : MidasControl, command : int):
        if command ==  BEATMAKER_COMMAND_IN_NOTEON:
            print("Note On Detected")
            pass
        elif  command ==  BEATMAKER_COMMAND_IN_NOTEOFF:
            print("Note Off Detected")
            if control == BEATMAKER_BUTTON_PAD_FUNC_CHANNEL_UP: 
                print("Func Channel + Detected.")
                if self.target_channel > 0:
                    self.target_channel -= 1
                #FLSI.select_one_channel(FLSI.get_channel_index(self.target_channel)) # Set the selected channel to the current_channel in FL Studio
            elif control == BEATMAKER_BUTTON_PAD_FUNC_CHANNEL_DOWN: 
                if self.target_channel < self.channel_count - 1:
                    self.target_channel += 1
                #FLSI.select_one_channel(FLSI.get_channel_index(self.target_channel)) # Set the selected channel to the current_channel in FL Studio              
            elif control == BEATMAKER_BUTTON_PAD_FUNC_ZOOM_IN:
                self.zoom_in()        
            elif control == BEATMAKER_BUTTON_PAD_FUNC_ZOOM_OUT: 
                self.zoom_out() 
            elif control == BEATMAKER_BUTTON_PAD_FUNC_MOVE_LEFT: 
                if self.channel_offset > 0:
                    self.channel_offset -= 1
            elif control == BEATMAKER_BUTTON_PAD_FUNC_MOVE_RIGHT: 
                if self.channel_offset < 4:
                    self.channel_offset += self.channel_offset
            elif control == BEATMAKER_BUTTON_PAD_FUNC_FILL: 
                if self.is_filling == False:
                    self.is_filling = True
                else:
                    self.is_filling = False
                    # Apply fill based on self.fill_type
                    if BEATMAKER_FILL_TYPE_16 == self.fill_type:
                        pass
                    elif BEATMAKER_FILL_TYPE_8 == self.fill_type:
                        pass
                    elif BEATMAKER_FILL_TYPE_4 == self.fill_type:
                        pass
                    elif BEATMAKER_FILL_TYPE_16_DOTTED == self.fill_type:
                        pass
                    elif BEATMAKER_FILL_TYPE_8_DOTTED == self.fill_type:
                        pass
                    elif BEATMAKER_FILL_TYPE_4_DOTTED == self.fill_type:
                        pass
                    elif BEATMAKER_FILL_TYPE_16_TRIPLET == self.fill_type:
                        pass
                    elif BEATMAKER_FILL_TYPE_8_TRIPLET == self.fill_type:
                        pass
                    elif BEATMAKER_FILL_TYPE_4_TRIPLET == self.fill_type:
                        pass
            elif control == BEATMAKER_BUTTON_PAD_FUNC_FILL_TYPE: 
                if self.is_filling :
                    if self.fill_type <= 9: # we have 9 fill types
                        self.fill_type += 1
                    else: # warp back to first fill type
                        self.fill_type = BEATMAKER_FILL_TYPE_16
            elif control == BEATMAKER_BUTTON_PAD_FUNC_CLEAR: 
                print("Channel+ button detected.") # handle button presses
            elif control == BEATMAKER_BUTTON_PAD_FUNC_SOLO: 
                print("Channel+ button detected.") # handle button presses
            elif control == BEATMAKER_BUTTON_PAD_FUNC_MUTE: 
                print("Channel+ button detected.") # handle button presses
            elif control == BEATMAKER_BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_COMP_GATE_DIST: 
                print("Channel+ button detected.") # handle button presses
            elif control == BEATMAKER_BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_VOLUME_PAN_PITCH: 
                print("Channel+ button detected.") # handle button presses
            elif control == BEATMAKER_BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_TARGET_BAND: 
                print("Channel+ button detected.") # handle button presses
            elif control == BEATMAKER_BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_COMP_GATE_DIST: 
                print("Channel+ button detected.") # handle button presses                
            elif control in BEATMAKER_BUTTONS_PAD: # handle drum pads
                print("One of the pad buttons detected.") 
        elif  command ==  BEATMAKER_COMMAND_IN_CONTROLCHANGE: # Handle Control Change Commands
                if control == BEATMAKER_CONTROLLER_CHANNEL_CONTROL_VOLUME_PAN_PITCH: 
                    if self.ccvpp_control_state == BEATMAKER_PCVPP_CONTROL_STATE_VOLUME: # Targeting Volume Knob
                        #flslChannels.setChannelVolume(flslChannels.getChannelIndex(DrumPadTargetChannel),event.data2/127.0) # set the volume in fl studio
                        #flsl.device.midi_out_msg_params(176,0,48,event.data2) 				# Update the value of the Track Control 1 Knob Target to the Volume of selected channel
                        pass
                    elif self.ccvpp_control_state == BEATMAKER_PCVPP_CONTROL_STATE_PAN: # Targeting Pan Knob
                        #flslChannels.setChannelPan(flslChannels.getChannelIndex(DrumPadTargetChannel),((event.data2/127.0)*2)-1)
                        #flsl.device.midi_out_msg_params(176,0,48,event.data2)
                        pass
                    elif self.ccvpp_control_state == BEATMAKER_PCVPP_CONTROL_STATE_PITCH: # Targeting Pitch Knob
                        # flslChannels.setChannelPitch(flslChannels.getChannelIndex(DrumPadTargetChannel),((event.data2/127.0)*2)-1)
                        # flsl.device.midi_out_msg_params(176,0,48,event.data2)
                        pass
                elif control == BEATMAKER_CONTROLLER_CHANNEL_CONTROL_COMP_GATE_DIST: 
                        pass  

        # print("Midas command recieved:", command)
        # if command == BEATMAKER_COMMAND_IN_NOTEON:
        #     print("Command 0 detected.")
        #     #print(MidasControl(*BEATMAKER_BUTTON_PAD_FUNC_CHANNEL_UP))
        #     print(control)
        #     if control == BEATMAKER_BUTTON_PAD_FUNC_CHANNEL_UP:
        #         print("Midas Control 0 Detected")     


MyTestAppC = App_Beatmaker()
MyTestAppC._command_map.regenerate([0,1],[144,128])
MyTestAppC._button_map.regenerate([BEATMAKER_BUTTON_PAD_FUNC_CHANNEL_UP],[MidiControl(0,53)])

MyTestAppC._onMidasProcessInternal(3,1,0,88)

def OnInit():
	print("Initialization OK")

def OnMidiMsg(event): 
	print(event.midiId,event.midiChan,event.data1)
	MyTestAppC._onMidasProcessInternal(event.midiId,event.midiChan,event.data1,event.data2)	



class TestApp(ApplicationBase):
    def onMidasProcess(self,status,port,data1,data2,sysex = None):
        if self._button_map.contains_equal(MidasControl(0,0),1,7):
            print(self._button_map.data())
        pass
    def onMidasEvent(self,control : MidasControl, command : int):
        if command ==  BM_COMMAND_IN_NOTEON:
            pass
        elif  command ==  BM_COMMAND_IN_NOTEOFF:
            print("Note On Detected")
            if control == BM_BUTTON_PAD_FUNC_CHANNEL_UP: 
                print("Func Channel + Detected.")
                if self.target_channel > 0:
                    self.target_channel -= 1
                #flslChannels.select_single_channel(flslChannels.get_channel_index(self.target_channel)) # Set the selected channel to the current_channel in FL Studio
            elif control == BM_BUTTON_PAD_FUNC_CHANNEL_DOWN: 
                if self.target_channel < self.channel_count - 1:
                    self.target_channel += 1
                #flslChannels.select_single_channel(flslChannels.get_channel_index(self.target_channel)) # Set the selected channel to the current_channel in FL Studio              
            elif control == BM_BUTTON_PAD_FUNC_ZOOM_IN:
                self.zoom_in()        
            elif control == BM_BUTTON_PAD_FUNC_ZOOM_OUT: 
                self.zoom_out() 
            elif control == BM_BUTTON_PAD_FUNC_MOVE_LEFT: 
                if self.channel_offset > 0:
                    self.channel_offset -= 1
            elif control == BM_BUTTON_PAD_FUNC_MOVE_RIGHT: 
                if self.channel_offset < 4:
                    self.channel_offset += self.channel_offset
            elif control == BM_BUTTON_PAD_FUNC_FILL: 
                if self.is_filling == False:
                    self.is_filling = True
                else:
                    self.is_filling = False
                    # Apply fill based on self.fill_type
                    if BM_FILL_TYPE_16 == self.fill_type:
                        pass
                    elif BM_FILL_TYPE_8 == self.fill_type:
                        pass
                    elif BM_FILL_TYPE_4 == self.fill_type:
                        pass
                    elif BM_FILL_TYPE_16_DOTTED == self.fill_type:
                        pass
                    elif BM_FILL_TYPE_8_DOTTED == self.fill_type:
                        pass
                    elif BM_FILL_TYPE_4_DOTTED == self.fill_type:
                        pass
                    elif BM_FILL_TYPE_16_TRIPLET == self.fill_type:
                        pass
                    elif BM_FILL_TYPE_8_TRIPLET == self.fill_type:
                        pass
                    elif BM_FILL_TYPE_4_TRIPLET == self.fill_type:
                        pass
            elif control == BM_BUTTON_PAD_FUNC_TOOL: 
                if self.is_filling :
                    if self.fill_type <= 9: # we have 9 fill types
                        self.fill_type += 1
                    else: # warp back to first fill type
                        self.fill_type = BM_FILL_TYPE_16
            elif control == BM_BUTTON_PAD_FUNC_CLEAR: 
                print("Channel+ button detected.") # handle button presses
            elif control == BM_BUTTON_PAD_FUNC_SOLO: 
                print("Channel+ button detected.") # handle button presses
            elif control == BM_BUTTON_PAD_FUNC_MUTE: 
                print("Channel+ button detected.") # handle button presses
            elif control == BM_BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_COMP_GATE_DIST: 
                print("Channel+ button detected.") # handle button presses
            elif control == BM_BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_VOLUME_PAN_PITCH: 
                print("Channel+ button detected.") # handle button presses
            elif control == BM_BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_TARGET_BAND: 
                print("Channel+ button detected.") # handle button presses
            elif control == BM_BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_COMP_GATE_DIST: 
                print("Channel+ button detected.") # handle button presses                
            elif control in BM_BUTTONS_PAD: # handle drum pads
                print("One of the pad buttons detected.") 
        elif  command ==  BM_COMMAND_IN_CONTROLCHANGE: # Handle Control Change Commands
                if control == BM_CONTROLLER_CHANNEL_CONTROL_VOLUME_PAN_PITCH: 
                    if self.ccvpp_control_state == BM_PCVPP_CONTROL_STATE_VOLUME: # Targeting Volume Knob
                        #flslChannels.setChannelVolume(flslChannels.getChannelIndex(DrumPadTargetChannel),event.data2/127.0) # set the volume in fl studio
                        #flsl.device.midi_out_msg_params(176,0,48,event.data2) 				# Update the value of the Track Control 1 Knob Target to the Volume of selected channel
                        pass
                    elif self.ccvpp_control_state == BM_PCVPP_CONTROL_STATE_PAN: # Targeting Pan Knob
                        #flslChannels.setChannelPan(flslChannels.getChannelIndex(DrumPadTargetChannel),((event.data2/127.0)*2)-1)
                        #flsl.device.midi_out_msg_params(176,0,48,event.data2)
                        pass
                    elif self.ccvpp_control_state == BM_PCVPP_CONTROL_STATE_PITCH: # Targeting Pitch Knob
                        # flslChannels.setChannelPitch(flslChannels.getChannelIndex(DrumPadTargetChannel),((event.data2/127.0)*2)-1)
                        # flsl.device.midi_out_msg_params(176,0,48,event.data2)
                        pass
                elif control == BM_CONTROLLER_CHANNEL_CONTROL_COMP_GATE_DIST: 
                        pass  

        print("Midas command recieved:", command)
        if command == 0:
            print("Command 0 detected.")
            if control == MidasControl(0,0):
                print("Midas Control 0 Detected")  

class TestApp2(ApplicationBase):
    # MyTestApp = TestApp()
    # MyTestApp._command_map.regenerate([0],[-1])
    # MyTestApp._button_map.regenerate([MidasControl(0,0),MidasControl(0,1)],[MidiControl(1,7),MidiControl(5,22)])

    # MyTestAppA = TestApp2()
    # MyTestAppA._command_map.regenerate([0],[0])
    # MyTestAppA._button_map.regenerate([MidasControl(0,0),MidasControl(0,1)],[MidiControl(1,8),MidiControl(5,22)])

    # MyTestApp._onMidasProcessInternal(0,1,7,0)
    # MyTestAppA._onMidasProcessInternal(0,1,8,0)

    def onMidasProcess(self,status,port,data1,data2,sysex = None):
        #self.my_int = status
        if self._button_map.contains_equal(MidasControl(0,0),1,8):
            print(self._button_map.data())
        pass
    def onMidasEvent(self,control : MidasControl, command : int):
        print("Midas command recieved:", command)
        if command == 0:
            print("Command 0 detected.")      

# ####################################################################################################################
# ####################################################################################################################
# # Fruity Loop Scripting Module Interface
# ####################################################################################################################
# ####################################################################################################################
# class flslTransport:
#     @staticmethod
#     def start():
#         pass
#     @staticmethod
#     def stop():
#         pass
#     @staticmethod
#     def record():
#         pass
#     @staticmethod
#     def global_transport(p1:int,p2:int):
#         pass

# class flslDevice:
#     @staticmethod
#     def midi_out_msg_params(midi_id: int, channel: int, data1: int, data2: int) -> None:
#         """
#         Send a MIDI message to the (linked) output interface (alternative version with separate parameters).

#         Parameters:
#         - midi_id (int): MIDI identifier.
#         - channel (int): MIDI channel.
#         - data1 (int): First data value.
#         - data2 (int): Second data value.

#         Returns:
#         - None
#         """
#         pass

# class flslChannels:
#     @staticmethod
#     def set_channel_volume(channel:int,vol:float):
#         pass
#     @staticmethod
#     def set_channel_pan(channel:int,vol:float):
#         pass
#     @staticmethod
#     def set_channel_pitch(channel:int,vol:float):
#         pass

#     @staticmethod
#     def channel_count():
#         pass

#     @staticmethod
#     def get_channel_index(global_index):
#         pass

#     @staticmethod
#     def select_single_channel(channel_index):
#         pass

#     @staticmethod
#     def set_grid_bit(channel,bit,value):
#         pass

#     @staticmethod
#     def get_grid_bit(channel,bit):
#         pass

# ####################################################################################################################
# ####################################################################################################################
# ####################################################################################################################
# ####################################################################################################################

# # Random stuff
# BUTTON_INDEX = 0
# BUTTON_GROUP = 1
# BUTTON_MIDI_CHANNEL = 2
# BUTTON_MIDI_ID = 3


# def is_command(command_statuses,command,midi_channel,midi_status):
#     event_status = midi_status - midi_channel
#     for cmd in command_statuses:
#         if cmd[0] == command:
#             if cmd[1] == event_status:
#                 return True
#     return False


# def generate_button_controls(buttons,midi_buttons) :
#     """
#         Generates a list of controls from a list of buttons and a list of midi buttons
#     Params:
#         param1[buttons]: List of pair of ints [[index,group]]
#         param2[midi_buttons]: List of pair of ints [[midi_channel,midi_id]]
#     Outputs:
#         output1: List of tuple of 4 ints [[index,group,midi_channel,midi_id]]
#     """    
#     controls = []
#     for i in range(len(buttons)) :
#         if i < len(midi_buttons):
#             controls += [(buttons[i][0],buttons[i][1],midi_buttons[i][0],midi_buttons[i][1])]
#         else:
#             # if there is not enough midi buttons for each control, the control is set to None, None
#             controls += [(buttons[i][0],buttons[i][1],None,None)]
#     return controls


# def is_control(controls,button,midi_channel,midi_id):
#     """
#         Checks if button is in controls, then returns True if the port and data1 match the midi channel and midi id of the button.
#     Params:
#         param1[controls]: List of buttons
#         param2[button]: List of 2 ints [index,group]
#         param3[midi_channel]: int
#         param4[midi_id]: int 
#     Outputs:
#         output1: bool
#     """
#     for control in controls:
#         if (control[BUTTON_INDEX],control[BUTTON_GROUP]) == button :
#             if (control[BUTTON_MIDI_CHANNEL],control[BUTTON_MIDI_ID]) == (midi_channel,midi_id) :
#                 return True
#     return False
    
# def is_control_from_list(controls,buttons,midi_channel,midi_id):
#     """
#         Checks if the buttons is in controls, then returns True if the port and data1 match the midi channel and midi id of the any of the buttons.
#     Params:
#         param1[controls]: List of Controls
#         param2[buttons]: List of buttons
#         param3[midi_channel]: int
#         param4[midi_id]: int 
#     Outputs:
#         output1: bool
#     """
#     for button in buttons:
#         for control in controls:
#             if (control[BUTTON_INDEX],control[BUTTON_GROUP]) == button :
#                 if (control[BUTTON_MIDI_CHANNEL],control[BUTTON_MIDI_ID]) == (midi_channel,midi_id) :
#                     return True
#     return False

# def get_control_data_param(controls,buttonid,buttongroup):
#     """
#         Checks if button is in controls, then returns the midi channel and midi id of the button.
#     Params:
#         param1[controls]: List of controls
#         param2[buttonid]: int
#         param3[buttongroup]: int
        
#     Outputs:
#         output1[midi_channel]: int
#         output2[midi_id]: int 
#     """
#     for control in controls:
#         if (control[0],control[1]) == (buttonid,buttongroup) :
#             return (control[BUTTON_MIDI_CHANNEL],control[BUTTON_MIDI_ID])
#     return None
    
    
# def get_control_data(controls,button):
#     """
#         Checks if button is in controls, then returns the midi channel and midi id of the button.
#     Params:
#         param1[controls]: List of buttons
#         param2[button]: List of 2 ints [index,group]
#     Outputs:
#         output1[midi_channel]: int
#         output2[midi_id]: int 
#     """
#     for control in controls:
#         if (control[0],control[1]) == (button[BUTTON_INDEX],button[BUTTON_GROUP]) :
#             return (control[BUTTON_MIDI_CHANNEL],control[BUTTON_MIDI_ID])
#     return None

# def get_fl_gridbit_value(channel,zoom,offset):
#     pass

# def send_midi_out(status,value,midi_address):
#     #flsl.device.midi_out_msg_params(status,midi_address[BUTTON_MIDI_CHANNEL],midi_address[BUTTON_MIDI_ID],value)	# Turn the LED on	
#     pass
# def send_midi_out_control(midi_control_map,status,value,app_control):
#     #send_midi_out(status,value,get_control_data(midi_control_map,app_control))  # 3 is APC device specific value for Red LED 
#     pass    

# def send_midi_out_param(midi_id,midi_channel,status,value):
#     flsl.device.midi_out_msg_params(status,midi_id,midi_channel,value)	# Turn the LED on	

# def generate_command_map(midos_commands,device_commands):
#     command_map = []
#     for i in range(len(midos_commands)) :
#         if i < len(device_commands):
#             command_map += [(midos_commands[i],device_commands[i])]
#         else:
#             # if there is not enough midi commands for each midas command, the control is set to midas_command, None
#             command_map += [(midos_commands[i], None)]
#     return command_map


# ####################################################################################################################
# ####################################################################################################################
# # module: Midas
# ####################################################################################################################
# ####################################################################################################################
# MIDAS_CONTROL_GROUP = 0
# MIDAS_CONTROL_GROUP_INDEX = 1
# class MidasControl:
#     __data = [int(-1),int(-1)]
    
#     def __init__(self,d1:int = -1,d2:int = -1):
#         self.__data = [d1,d2]
#     def __hash__(self):
#         return hash((self.__data[0],
#                 self.__data[1]))
#     def __eq__(self, other):
#         return ( ( self.__data[0],
#                 self.__data[1] ) == ( other.__data[0],other.__data[1]) )
#     def __str__(self):
#         return "param 1: {0} param 2: {1}  ".format(self.__data[0], self.__data[1])
    
#     def data(self)-> [int,int]:
#         return self.__data
#     def index(self)-> int:
#         return self.__data[1]
#     def group(self)-> int:
#         return self.__data[0]
#     def valid(self):
#         if self.__data[0]<0 or self.__data[1]<0:
#             return False
#         return True
    
#     @classmethod
#     def from_tuple(cls,tuple_):
#         return cls(tuple_[0],tuple_[1])


# MIDAS_MIDICONTROL_CHANNEL = 0
# MIDAS_MIDISCONTROL_ID = 1
# class MidasMidiControl:
#     __data = [int(-1),int(-1)]
    
#     def __init__(self,d1:int = -1,d2:int = -1):
#         self.__data = [d1,d2]
#     def __hash__(self):
#         return hash((self.__data[0],
#                 self.__data[1]))
#     def __eq__(self, other):
#         return ( ( self.__data[0],
#                 self.__data[1] ) == ( other.__data[0],other.__data[1]) )
#     def __str__(self):
#         return "param 1: {0} param 2: {1}  ".format(self.__data[0], self.__data[1])
    
#     def data(self)-> [int,int]:
#         return self.__data
#     def id(self)-> int:
#         return self.__data[1]
#     def channel(self)-> int:
#         return self.__data[0]
#     def valid(self):
#         if self.__data[0]<0 or self.__data[1]<0:
#             return False
#         return True
    
#     @classmethod
#     def from_tuple(cls,tuple_):
#         return cls(tuple_[0],tuple_[1])
   
# class MidasAppControlMap:
#     data = {}

#     def is_control(self,midas_control,midi_channel,midi_id):
#         """
#             Checks if button is in the control map, then returns True if match the midi channel and midi id of the associated midi control.
#         Params:
#             param2[button]: MidasControl
#             param3[midi_channel]: int
#             param4[midi_id]: int 
#         Outputs:
#             output1: bool
#         """
#         if midas_control in self.data:
#             if self.data[midas_control].channel() == midi_channel and self.data[midas_control].id() == midi_id :
#                 return True
#         return False    
    
#     def is_control_from_list(self,midas_control_list,midi_channel,midi_id)-> bool: # FIXME: import typing , midas_control_list : List[MidasControl]
#         for control in midas_control_list:
#             return self.is_control(control,midi_channel,midi_id)
    
#     def get_control_data(self,midas_control : MidasControl)-> (int,int):
#         """
#             Checks if button is in controls, then returns the midi channel and midi id of the button.
#         Params:
#             param1[controls]: List of buttons
#             param2[button]: List of 2 ints [index,group]
#         Outputs:
#             output1[midi_channel]: int
#             output2[midi_id]: int 
#         """
#         if midas_control in self.data:
#             return self.data[midas_control].channel(),self.data[midas_control].id()
#         return None    
    
#     def generate(self,midas_control_list,midi_control_list) :
#         """
#             Generates a control map from a list of midas controls and a list of midi controls.
#         Params:
#             param1[midas_control_list]: List of MidasControl
#             param2[midi_control_list]: List of MidasMidiControl
#         """    
#         for i in range(len(midas_control_list)) :
#             if i < len(midi_control_list):
#                 self.data[midas_control_list[i]] = MidasMidiControl(midi_control_list[i][MIDAS_MIDICONTROL_CHANNEL],midi_control_list[i][MIDAS_MIDISCONTROL_ID])
#             else:
#                 # if there is not enough midi buttons for each control, the control is set to None, None
#                 self.data[midas_control_list[i]:MidasMidiControl(None,None)] 

#     def retarget(self,midi_control_list) :
#         """
#             Retargets current control map of midas controls with a new list of midi controls.
#         Params:
#             param1[midi_control_list]: List of MidasMidiControl
#         """   
#         midas_control_list = self.data.keys() 
#         for i in range(len(midas_control_list)) :
#             if i < len(midi_control_list):
#                 self.data[midas_control_list[i]:midi_control_list[i]]
#             else:
#                 # if there is not enough midi buttons for each control, the control is set to None, None
#                 self.data[midas_control_list[i]:MidasMidiControl(None,None)]    
    
# class MidasAppCommandMap:
#     data = {int:int}
#     def is_command(self,midas_command,midi_command):
#         """
#             Checks if button is in the control map, then returns True if match the midi channel and midi id of the associated midi control.
#         Params:
#             param2[button]: MidasControl
#             param3[midi_channel]: int
#             param4[midi_id]: int 
#         Outputs:
#             output1: bool
#         """
#         if midas_command in self.data:
#             if self.data[midas_command] == midi_command :
#                 return True
#         return False  
    
#     def is_command_offset_by_channel(self,midas_command,midi_command,midi_channel,offset_flag : bool = False):
#         """
#             Checks if button is in the control map, then returns True if match the midi channel and midi id of the associated midi control.
#         Params:
#             param2[button]: MidasControl
#             param3[midi_channel]: int
#             param4[midi_id]: int 
#         Outputs:
#             output1: bool
#         """
#         if offset_flag == False:
#             if midas_command in self.data:
#                 if self.data[midas_command] == midi_command - midi_channel:
#                     return True
#         else:
#             if midas_command in self.data:
#                 if self.data[midas_command] == midi_command + midi_channel:
#                     return True            
#         return False     
         
    
#     def is_command_from_list(self,midas_control_list)-> bool: # FIXME: import typing , midas_control_list : List[MidasControl]
#         for command in midas_control_list:
#             return self.is_command(command)
    
#     def get_command_data(self,midas_command : int)-> int:
#         """
#             Checks if button is in controls, then returns the midi channel and midi id of the button.
#         Params:
#             param1[controls]: List of buttons
#             param2[button]: List of 2 ints [index,group]
#         Outputs:
#             output1[midi_channel]: int
#             output2[midi_id]: int 
#         """
#         if midas_command in self.data:
#             return self.data[midas_command]
#         return None    
    
#     def get_command(self,midi_status):
#         if midi_status in self.data.values():
#             return self.data.keys()[self.data.values().index(midi_status)]
#         else:
#             return None

#     def generate(self,midas_command_list,midi_command_list) :
#         """
#             Generates a command map from a list of midas commands and a list of midi commands.
#         Params:
#             param1[midas_command_list]: list of midas commands [int]
#             param2[midi_command_list]: list of midi commands [int]
#         """    
#         for i in range(len(midas_command_list)) :
#             if i < len(midi_command_list):
#                 self.data[midas_command_list[i]] = midi_command_list[i]
#             else:
#                 # if there is not enough midi buttons for each command, the command is set to None
#                 self.data[midas_command_list[i]:None] 

#     def retarget(self,midi_command_list) :
#         """
#             Retargets current command map of midas commands with a new list of midi commands.
#         Params:
#             param1[midi_command_list]: List of MidasMidicommand
#         """   
#         midas_command_list = self.data.keys() 
#         for i in range(len(midas_command_list)) :
#             if i < len(midi_command_list):
#                 self.data[midas_command_list[i]:midi_command_list[i]]
#             else:
#                 # if there is not enough midi buttons for each command, the command is set to None, None
#                 self.data[midas_command_list[i]:None]        

# class MidasApplication:
#     """
#     # Models the communication protocol between a device's midi controls and midasControls of a midasApplication.
#     # A MidasApp will be able to accept 3 types of commands:
#     # RecieveDirect : string message for raw processing
#     # RecievePressed : midi NoteOn
#     # RecieveReleased : midi NoteOff
#     # RecieveControlChange : midi CC
#     # SendProgramChange : midi PC 
#     # A midas app will be able to output these types of commands:
#     # SendDirect : send a string (sysex, or custom midi commands)
#     # SendPressed : midi NoteOn out
#     # SendReleased : midi NoteOff out
#     # SendControlChange : midi CC out
#     # SendProgramChange : midi PC out
#     # Contains a map of app commands and their associated midi command status on the device 
#     # Contains a map of app buttons and their associated midi channel and midi id on the device
#     # Contains a map of app absolute controls(range from 0 to 1(float)) associated midi channel and midi id on the device
#     # Contains a map of app relative controls(range -1 to 1 (float)) associated midi channel and midi id on the device
#     """
#     button_map : MidasAppControlMap
#     controller_map : MidasAppControlMap
#     command_map : MidasAppCommandMap
#     is_running : bool

#     def __init_subclass__(cls, **kwargs): 
#         cls.button_map : MidasAppControlMap = MidasAppControlMap()
#         cls.controller_map : MidasAppControlMap = MidasAppControlMap()
#         cls.command_map : MidasAppCommandMap = MidasAppCommandMap()
#         cls.is_running : bool = False
#     # Called by midas OS
#     # Events recieved from Fruity Loops
#     def __onFruityLoopUpdate(self):
#         self.onMidasUpdate()
#         self.onFruityLoopUpdate()
#         pass
#     def __onFruityLoopProgramChange(self,flags):
#         self.onMidasUpdate()
#         self.onFruityLoopProgramChange(flags)
#         pass
#     def __onFruityLoopScriptInit(self):    
#         self.onMidasUpdate()
#         self.onFruityLoopScriptInit()
#         pass
#     # Events Recieved from device
#     def __onFruityLoopMidiInput(self,message):
#         self.onMidasUpdate()
#         self.onFruityLoopMidiInput(message)
#         self.onMidasProcess(message.status,message.port,message.data1,message.data2,message.sysex)
#         pass
#     def __onFruityLoopSysexInput(self,message):
#         self.onMidasUpdate()
#         self.onFruityLoopSysexInput(message)
#         self.onMidasProcess(message.status,message.port,message.data1,message.data2,message.sysex)
#         pass  

#     # abstract callbacks to be written for each application
#     def onFruityLoopUpdate(self):
#         pass
#     def onFruityLoopProgramChange(self,flags):
#         pass
#     def onFruityLoopScriptInit(self):    
#         pass
#     # Events Recieved from device
#     def onFruityLoopMidiInput(self,message):
#         pass
#     def onFruityLoopSysexInput(self,message):
#         pass  
#     # Called on all callbacks from FLSTUDIO 
#     def onMidasUpdate(self):
#         pass
#     def onMidasProcess(self,status,port,data1,data2,sysex = None):
#         pass
# ####################################################################################################################
# ####################################################################################################################
# ####################################################################################################################
# ####################################################################################################################


# ####################################################################################################################
# ####################################################################################################################
# # module: APC40 MIDI DATA
# ####################################################################################################################
# ####################################################################################################################
# # Outbound APC40 Sysex Message Types
# # There will be four types of messages from the PC host to the device.
# # Outbound Message Type 0: Introduction
# # This message is sent before any other device-specific message (i.e. other than Device Enquiry).
# # It instructs the APC40 to perform the necessary initialization and informs the firmware of the version number of the
# # application to cater for changes in the application in the APC40 firmware.
# # There are three modes that are accepted. The unit defaults to Mode 0 on startup.

# # Mode Identifier Name
# # 0   0x40   Generic Mode
# # 1   0x41   Ableton Live Mode
# # 2   0x42   Alternate Ableton Live Mode

# # Notes Regarding Generic Mode (Mode 0):
# # -[CLIP LAUNCH] buttons are momentary and should light the green LED when ON
# # -[CLIP STOP] buttons are momentary and should light its LED when ON
# # -[ACTIVATOR], [SOLO], [RECORD ARM] are toggle buttons and should light its LED when ON
# # -[TRACK SELECTION] buttons (1-8 + MASTER) are radio style and only one of the 9 buttons are ON at a time.
# #  When ON its LED should light. These buttons will NOT send out MIDI in generic mode for its state.
# #  These buttons dictate which one of nine banks the DEVICE CONTROL knobs and DEVICE
# #  CONTROL switches belong to. These knobs and switches will output on a different MIDI channel
# #  based on the current Track Selection (track 1 = MIDI channel 0, track 8 = MIDI channel 7, MASTER = MIDI channel 8).
# #  Upon pressing one of the Track Selection buttons, the current position of the 8
# #  Device Control knobs will be sent.
# # -[CLIP/TRACK (1)], [DEVICE ON/OFF (2)], [Å (3)], [Æ (4)] will be toggle style and will light its LED when
# #  ON
# # -[DETAIL VIEW (5)], [REC QUANTIZATION (6)], [MIDI OVERDUB (7)], [METRONOME (8)] will be
# #  momentary style and will light its LED when ON
# # -[SCENE LAUNCH] and [STOP ALL CLIPS] buttons are momentary buttons and will light its LED when
# #  ON
# # -TRACK CONTROL buttons are toggle buttons and will light its LED when ON
# # -TRACK CONTROL KNOBS and buttons are NOT banked in any way
# # -[PLAY], [STOP], [RECORD], [UP], [DOWN], [LEFT], [RIGHT], [SHIFT], [NUDGE+], [NUDGE-], [TAP TEMPO] are momentary buttons
# # -LED rings are all set to SINGLE style

# # Notes Regarding Ableton Live Mode (Mode 1):
# # - All buttons are momentary buttons
# # - Device control knobs and buttons are not banked within the APC40
# # - LED Rings around the knobs are controlled by the APC40 but can be updated by the Host
# # - All other LEDs are controlled by the Host

# # Notes Regarding Alternate Ableton Live Mode (Mode 2):
# # - All buttons are momentary buttons
# # - Device control knobs and buttons are not banked within the APC40
# # - All LEDs are controlled by the Host

# # Format of Type 0 outbound message
# # byte number  value description
# # 1            0xF0   MIDI System exclusive message start
# # 2            0x47   Manufacturers ID Byte
# # 3            <DeviceID> System Exclusive Device ID
# # 4            0x73   Product model ID
# # 5            0x60   Message type identifier
# # 6            0x0   Number of data bytes to follow (most significant)
# # 7            0x04   Number of data bytes to follow (least significant)
# # 8            0x40 or 0x41 or 0x42   Application/Configuration identifier
# # 9            <Version High> PC application Software version major
# # 10           <Version Low> PC application Software version minor
# # 11           <Bugfix Level> PC Application Software bug-fix level
# # 12           0xF7   MIDI System exclusive message terminator



# APC40_N_CHANNELS = 9
# APC40_N_CHANNELS_NO_MASTER = APC40_N_CHANNELS - 1
# APC40_N_CLIP_LAUNCH_ROWS = 5
# APC40_N_DEVICE_CONTROL_BUTTONS = 8
# APC40_N_DEVICE_CONTROL_CONTROLLER_ABSOLUTE = 8

# APC40_OUT_MIDI_COMMAND_SYSTEM = 0xF0
# APC40_OUT_MIDI_COMMAND_LED_ON = 0x90
# APC40_OUT_MIDI_COMMAND_LED_OFF = 0x80
# APC40_OUT_MIDI_COMMAND_CONTROL_SET = 0xB0

# APC40_IN_MIDI_COMMAND_BUTTON_PRESS = 0x90
# APC40_IN_MIDI_COMMAND_BUTTON_RELEASE = 0x80
# APC40_IN_MIDI_COMMAND_CONTROL_CHANGE = 0xB0
# APC40_IN_MIDI_COMMAND_CONTROL_RELATIVE_CHANGE = 0xB0

# APC40_OUT_MIDI_CHANNEL_MASTER = 0x0


# # Outbound Message Type 1: LEDs.
# # This message is used to control the states of the LEDs. A note-on message will cause the specified LED to
# # switch on. A note-off message will cause the specified LED to switch off. The field normally associated with
# # note number will be used to specify the LED. The field normally associated with velocity will indicate the
# # LED display type. The field normally associated with MIDI Channel will indicate the Track for certain LEDs.
# # A Note On message with a velocity of zero is equivalent to a Note Off message, however it is preferred that
# # an actual Note Off message is used.

# # Format of Type 1 outbound Midi note-on messages
# # byte number value description
# # 1    0x9<chan> (0x90) [144+<chan>]  MIDI Note-on. The 4-bit <chan> value will be used for the track strips
# # 2    <ControlID> [ControlID] identifier for LED object (“note number”)
# # 3    state control value (This value will describe the state or color of the LED: OFF/ON/blinking, etc)

# # Format of Type 1 outbound Midi note-off messages
# # byte number value description
# # 1    0x8<chan> (0x80) [128+<chan>]  MIDI Note-off. The 4-bit <chan> value will be used for the track strips
# # 2    <ControlID> [ControlID] identifier for LED object (“note number”)
# # 3    (unused) control value (ignored)

# APC40_BUTTONS_CLIP_LAUNCH = [(None,None)] * ((APC40_N_CLIP_LAUNCH_ROWS*APC40_N_CHANNELS_NO_MASTER))

# for id in range(APC40_N_CLIP_LAUNCH_ROWS) : 
#     for channel in range(APC40_N_CHANNELS_NO_MASTER) :
#         APC40_BUTTONS_CLIP_LAUNCH[(id*APC40_N_CHANNELS_NO_MASTER) + channel] = channel , 0x35 + id

# APC40_BUTTONS_RECARM = [(None,None)] * (APC40_N_CHANNELS_NO_MASTER)
# APC40_BUTTONS_SOLOCUE = [(None,None)] * (APC40_N_CHANNELS_NO_MASTER)
# APC40_BUTTONS_ACTIVATOR = [(None,None)] * (APC40_N_CHANNELS_NO_MASTER)
# APC40_BUTTONS_CLIP_STOP = [(None,None)] * (APC40_N_CHANNELS_NO_MASTER)
# APC40_BUTTONS_TRACK_SELECT = [(None,None)] * (APC40_N_CHANNELS_NO_MASTER)
# for channel in range(APC40_N_CHANNELS_NO_MASTER) :
#     APC40_BUTTONS_RECARM[channel] = channel,0x30
#     APC40_BUTTONS_SOLOCUE[channel] = channel,0x31
#     APC40_BUTTONS_ACTIVATOR[channel] = channel,0x32
#     APC40_BUTTONS_CLIP_STOP[channel] = channel,0x34
#     APC40_BUTTONS_TRACK_SELECT[channel] = channel ,0x33
    
# APC40_BUTTONS_SCENE_LAUNCH = [(None,None)] * (5)
# for i in range(5):
#     APC40_BUTTONS_SCENE_LAUNCH[i] = APC40_OUT_MIDI_CHANNEL_MASTER, 0x52 + i

# APC40_BUTTON_MASTER = APC40_OUT_MIDI_CHANNEL_MASTER, 0x50
# APC40_BUTTON_STOP_ALL_CLIPS = APC40_OUT_MIDI_CHANNEL_MASTER, 0x51

# APC40_BUTTON_PAN = APC40_OUT_MIDI_CHANNEL_MASTER , 0x57
# APC40_BUTTON_SEND_A = APC40_OUT_MIDI_CHANNEL_MASTER, 0x58
# APC40_BUTTON_SEND_B = APC40_OUT_MIDI_CHANNEL_MASTER, 0x59
# APC40_BUTTON_SEND_C = APC40_OUT_MIDI_CHANNEL_MASTER, 0x5A

# APC40_BUTTON_PLAY = APC40_OUT_MIDI_CHANNEL_MASTER ,0x5B #(G_6) Momentary 
# APC40_BUTTON_STOP = APC40_OUT_MIDI_CHANNEL_MASTER, 0x5C #(G#6) Momentary 
# APC40_BUTTON_RECORD= APC40_OUT_MIDI_CHANNEL_MASTER ,0x5D #(A_6) Momentary 
# APC40_BUTTON_UP = APC40_OUT_MIDI_CHANNEL_MASTER, 0x5E #(A#6) Momentary 
# APC40_BUTTON_DOWN= APC40_OUT_MIDI_CHANNEL_MASTER, 0x5F# (B_6) Momentary 
# APC40_BUTTON_RIGHT= APC40_OUT_MIDI_CHANNEL_MASTER, 0x60# (C_7) Momentary 
# APC40_BUTTON_LEFT = APC40_OUT_MIDI_CHANNEL_MASTER, 0x61 #(C#7) Momentary 
# APC40_BUTTON_SHIFT = APC40_OUT_MIDI_CHANNEL_MASTER, 0x62 #(D_7) Momentary 
# APC40_BUTTON_TAP_TEMPO= APC40_OUT_MIDI_CHANNEL_MASTER,0x63# (D#7) Momentary 
# APC40_BUTTON_NUDGE_PLUS = APC40_OUT_MIDI_CHANNEL_MASTER,0x64 #(E_7) Momentary 
# APC40_BUTTON_NUDGE_MINUS = APC40_OUT_MIDI_CHANNEL_MASTER,0x65 #(F_7) Momentary

# APC40_BUTTONS_CLIPTRACK = [(None, 0x3A)] * APC40_N_CHANNELS # Toggle
# APC40_BUTTONS_DEVICEONOFF = [(None, 0x3B)] * APC40_N_CHANNELS # Toggle
# APC40_BUTTONS_DEVICELEFT = [(None, 0x3C)] * APC40_N_CHANNELS # Toggle
# APC40_BUTTONS_DEVICERIGHT = [(None, 0x3D)] * APC40_N_CHANNELS # Toggle
# APC40_BUTTONS_DETAILVIEW = [(None, 0x3E)] * APC40_N_CHANNELS # Toggle
# APC40_BUTTONS_RECQUANTIZATION = [(None, 0x3F)] * APC40_N_CHANNELS # Toggle
# APC40_BUTTONS_MIDIOVERDUB = [(None, 0x40)] * APC40_N_CHANNELS # Toggle 
# APC40_BUTTONS_METRONOME = [(None, 0x41)] * APC40_N_CHANNELS # Toggle

# for channel in range(APC40_N_CHANNELS) :
#     APC40_BUTTONS_CLIPTRACK[channel] = channel,0x3A
#     APC40_BUTTONS_DEVICEONOFF[channel] = channel,0x3B
#     APC40_BUTTONS_DEVICELEFT[channel] = channel,0x3C
#     APC40_BUTTONS_DEVICERIGHT[channel] = channel,0x3D
#     APC40_BUTTONS_DETAILVIEW[channel] = channel, 0x3E
#     APC40_BUTTONS_RECQUANTIZATION[channel] = channel, 0x3F
#     APC40_BUTTONS_MIDIOVERDUB[channel] = channel,0x40
#     APC40_BUTTONS_METRONOME[channel] = channel,0x41
    
# APC40_BUTTONS_DEVICE_CONTROL = [
#     APC40_BUTTONS_CLIPTRACK ,
#     APC40_BUTTONS_DEVICEONOFF ,
#     APC40_BUTTONS_DEVICELEFT ,
#     APC40_BUTTONS_DEVICERIGHT ,
#     APC40_BUTTONS_DETAILVIEW ,
#     APC40_BUTTONS_RECQUANTIZATION ,
#     APC40_BUTTONS_MIDIOVERDUB ,
#     APC40_BUTTONS_METRONOME
#     ]    


# # Outbound Message Type 2: Controller Value Update messages
# # Controls that report an absolute value for their position for inbound messages
# # can have their controller value updated via a Controller Value Update message.
# # This will be done using a MIDI controller message. The field normally associated
# # with the controller number will be used to specify the Control ID.
# # The field normally associated with the controller value will be used to update
# # the value of a controller on the APC40.
# # MIDI Controller message byte number value description
# # 1                0xB<chan>              # MIDI Controller. The 4-bit <chan> value will be used for the track strips
# # 2                <ControlID>            # Identifier for control surface object
# # 3                data                   # Control value

# APC40_CONTROLLER_FADER = APC40_OUT_MIDI_CHANNEL_MASTER ,0x0F
# APC40_CONTROLLER_MASTER_LEVEL = APC40_OUT_MIDI_CHANNEL_MASTER , 0x0E
# APC40_CONTROLLER_FOOTSWITCH_1 = APC40_OUT_MIDI_CHANNEL_MASTER , 0x40
# APC40_CONTROLLER_FOOTSWITCH_2 = APC40_OUT_MIDI_CHANNEL_MASTER , 0x43


# APC40_CONTROLLERS_TRACK_LEVEL = [(None,None)] * APC40_N_CHANNELS_NO_MASTER
# for channel in range(APC40_N_CHANNELS_NO_MASTER):
#     APC40_CONTROLLERS_TRACK_LEVEL[channel] = channel, 0x07   

# APC40_CONTROLLERS_TRACK_CONTROL_ABSOLUTE = [(None,None)] * 8
# for i in range(APC40_N_DEVICE_CONTROL_CONTROLLER_ABSOLUTE) :
#     APC40_CONTROLLERS_TRACK_CONTROL_ABSOLUTE[i] = APC40_OUT_MIDI_CHANNEL_MASTER, 0x30 + i

# APC40_CONTROLLERS_TRACK_CONTROL_LEDRINGTYPE = [(None,None)] * 8
# for i in range(APC40_N_DEVICE_CONTROL_CONTROLLER_ABSOLUTE) :
#     APC40_CONTROLLERS_TRACK_CONTROL_ABSOLUTE[i] = APC40_OUT_MIDI_CHANNEL_MASTER, 0x38 + i

# APC40_CONTROLLERS_DEVICE_CONTROL_ABSOLUTE = [(None,None)] * (APC40_N_DEVICE_CONTROL_CONTROLLER_ABSOLUTE * APC40_N_CHANNELS)
# for id in range(APC40_N_DEVICE_CONTROL_CONTROLLER_ABSOLUTE) :
#     for channel in range(APC40_N_CHANNELS) :
#         APC40_CONTROLLERS_DEVICE_CONTROL_ABSOLUTE[channel+(id*APC40_N_CHANNELS)] = channel , 0x10 + id

# APC40_CONTROLLERS_DEVICE_CONTROL_LEDRINGTYPE = [(None,None)] * (APC40_N_DEVICE_CONTROL_CONTROLLER_ABSOLUTE * APC40_N_CHANNELS)
# for id in range(APC40_N_DEVICE_CONTROL_CONTROLLER_ABSOLUTE) :
#     for channel in range(APC40_N_CHANNELS) :
#         APC40_CONTROLLERS_DEVICE_CONTROL_LEDRINGTYPE[channel+(id*APC40_N_CHANNELS)] = channel , 0x18 + id

# APC40_CONTROLLER_CUE_LEVEL_RELATIVE = APC40_OUT_MIDI_CHANNEL_MASTER ,0x2F

# # Absolute controller LED state types
# APC40_LED_ABSOLUTE_CONTROLLER_STATE_OFF = 0
# APC40_LED_ABSOLUTE_CONTROLLER_STATE_SINGLE = 1
# APC40_LED_ABSOLUTE_CONTROLLER_STATE_VOLUMESTYLE = 2
# APC40_LED_ABSOLUTE_CONTROLLER_STATE_PANSTYLE = 3

# APC40_LED_ABSOLUTE_CONTROLLER_STATES= [
#     APC40_LED_ABSOLUTE_CONTROLLER_STATE_OFF,
#     APC40_LED_ABSOLUTE_CONTROLLER_STATE_SINGLE,
#     APC40_LED_ABSOLUTE_CONTROLLER_STATE_VOLUMESTYLE,
#     APC40_LED_ABSOLUTE_CONTROLLER_STATE_PANSTYLE
#     ]

# # Interpretation of LED Ring Types 
# # The LED rings will display its controller value with the LEDs based on the LED Ring Types. This LED Ring 
# # Type can be set by the Host by sending an appropriate controller value message. The “Min” and “Max” 
# # columns below will state the range of the controller value that will match the LED states as shown in the 
# # “Display” column. The “LED STATES” column below will show the state of each of the 15 LEDs going from 
# # left to right. A “0” indicates that the LED within the LED ring is OFF. A “1” indicates that the LED within the 
# # LED ring in ON. 
# APC40_LED_STATES_CONTROLLER_SINGLE = [
# (0,3,0b100000000000000)
# ,(4,8,0b110000000000000)
# ,(9,12,0b010000000000000)
# ,(13,17,0b011000000000000)
# ,(18,21,0b001000000000000)
# ,(22,25,0b001100000000000)
# ,(26,30,0b000100000000000)
# ,(31,34,0b000110000000000)
# ,(35,38,0b000010000000000)
# ,(39,43,0b000011000000000)
# ,(44,47,0b000001000000000)
# ,(48,52,0b000001100000000)
# ,(53,56,0b000000100000000)
# ,(57,60,0b000000110000000)
# ,(61,65,0b000000010000000)
# ,(66,69,0b000000011000000)
# ,(70,73,0b000000001000000)
# ,(74,78,0b000000001100000)
# ,(79,82,0b000000000100000)
# ,(83,87,0b000000000110000)
# ,(88,91,0b000000000010000)
# ,(92,95,0b000000000011000)
# ,(96,100,0b000000000001000)
# ,(101,104,0b000000000001100)
# ,(105,108,0b000000000000100)
# ,(109,113,0b000000000000110)
# ,(114,117,0b000000000000010)
# ,(118,122,0b000000000000011)
# ,(123,127,0b000000000000001)
# ]

# # B. VOLUME STYLE
# APC40_LED_STATES_CONTROLLER_VOLUME = [
#     (0, 0, 0b000000000000000),
#     (1, 9, 0b100000000000000),
#     (10, 18, 0b110000000000000),
#     (19, 27, 0b111000000000000),
#     (28, 36, 0b111100000000000),
#     (37, 45, 0b111110000000000),
#     (46, 54, 0b111111000000000),
#     (55, 63, 0b111111100000000),
#     (64, 71, 0b111111110000000),
#     (72, 80, 0b111111111000000),
#     (81, 89, 0b111111111100000),
#     (90, 98, 0b111111111110000),
#     (99, 107, 0b111111111111000),
#     (108, 116, 0b111111111111100),
#     (117, 126, 0b111111111111110),
#     (127, 127, 0b111111111111111)
# ]

# # C. PAN STYLE
# APC40_LED_STATES_CONTROLLER_PAN = [
#     (0, 8, 0b111111110000000),
#     (9, 17, 0b011111110000000),
#     (18, 26, 0b001111110000000),
#     (27, 35, 0b000111110000000),
#     (36, 44, 0b000011110000000),
#     (45, 53, 0b000001110000000),
#     (54, 62, 0b000000110000000),
#     (63, 64, 0b000000010000000),
#     (65, 73, 0b000000011000000),
#     (74, 82, 0b000000011100000),
#     (83, 91, 0b000000011110000),
#     (92, 100, 0b000000011111000),
#     (101, 109, 0b000000011111100),
#     (110, 118, 0b000000011111110),
#     (119, 127, 0b000000011111111)
# ]

# # Interpretation of MIDI Controller values for Relative Controllers 
# # The value in the data field will indicate a relative change; values 01 to 63 describe a positive change and 
# # values 127 down to 64 describe a negative change. 
# # data value sent interpretation 
# # 0x00 No change occured. Control is stationary. 
# # 0x01 The controller incremented its value by 1 since the last report 
# # 0x02 The controller incremented its value by 2 since the last report 
# # ... ... 
# # 0x3f The controller incremented its value by 63 since the last report 
# # 0x40 The controller decremented its value by 64 since the last report 
# # 0x41 The controller decremented its value by 63 since the last report 
# # ... ... 
# # 0x7e The controller decremented its value by 2 since the last report 
# # 0x7f The controller decremented its value by 1 since the last report 
# APC40_RELATIVE_CONTROLLER_VALUES = [
#     (0x00, 0),
#     (0x01, 1),
#     (0x02, 2),
#     (0x03, 3),
#     (0x04, 4),
#     (0x05, 5),
#     (0x06, 6),
#     (0x07, 7),
#     (0x08, 8),
#     (0x09, 9),
#     (0x0A, 10),
#     (0x0B, 11),
#     (0x0C, 12),
#     (0x0D, 13),
#     (0x0E, 14),
#     (0x0F, 15),
#     (0x10, 16),
#     (0x11, 17),
#     (0x12, 18),
#     (0x13, 19),
#     (0x14, 20),
#     (0x15, 21),
#     (0x16, 22),
#     (0x17, 23),
#     (0x18, 24),
#     (0x19, 25),
#     (0x1A, 26),
#     (0x1B, 27),
#     (0x1C, 28),
#     (0x1D, 29),
#     (0x1E, 30),
#     (0x1F, 31),
#     (0x20, 32),
#     (0x21, 33),
#     (0x22, 34),
#     (0x23, 35),
#     (0x24, 36),
#     (0x25, 37),
#     (0x26, 38),
#     (0x27, 39),
#     (0x28, 40),
#     (0x29, 41),
#     (0x2A, 42),
#     (0x2B, 43),
#     (0x2C, 44),
#     (0x2D, 45),
#     (0x2E, 46),
#     (0x2F, 47),
#     (0x30, 48),
#     (0x31, 49),
#     (0x32, 50),
#     (0x33, 51),
#     (0x34, 52),
#     (0x35, 53),
#     (0x36, 54),
#     (0x37, 55),
#     (0x38, 56),
#     (0x39, 57),
#     (0x3A, 58),
#     (0x3B, 59),
#     (0x3C, 60),
#     (0x3D, 61),
#     (0x3E, 62),
#     (0x3F, 63),
#     (0x40, -64),
#     (0x41, -63),
#     (0x42, -62),
#     (0x43, -61),
#     (0x44, -60),
#     (0x45, -59),
#     (0x46, -58),
#     (0x47, -57),
#     (0x48, -56),
#     (0x49, -55),
#     (0x4A, -54),
#     (0x4B, -53),
#     (0x4C, -52),
#     (0x4D, -51),
#     (0x4E, -50),
#     (0x4F, -49),
#     (0x50, -48),
#     (0x51, -47),
#     (0x52, -46),
#     (0x53, -45),
#     (0x54, -44),
#     (0x55, -43),
#     (0x56, -42),
#     (0x57, -41),
#     (0x58, -40),
#     (0x59, -39),
#     (0x5A, -38),
#     (0x5B, -37),
#     (0x5C, -36),
#     (0x5D, -35),
#     (0x5E, -34),
#     (0x5F, -33),
#     (0x60, -32),
#     (0x61, -31),
#     (0x62, -30),
#     (0x63, -29),
#     (0x64, -28),
#     (0x65, -27),
#     (0x66, -26),
#     (0x67, -25),
#     (0x68, -24),
#     (0x69, -23),
#     (0x6A, -22),
#     (0x6B, -21),
#     (0x6C, -20),
#     (0x6D, -19),
#     (0x6E, -18),
#     (0x6F, -17),
#     (0x70, -16),
#     (0x71, -15),
#     (0x72, -14),
#     (0x73, -13),
#     (0x74, -12),
#     (0x75, -11),
#     (0x76, -10),
#     (0x77, -9),
#     (0x78, -8),
#     (0x79, -7),
#     (0x7A, -6),
#     (0x7B, -5),
#     (0x7C, -4),
#     (0x7D, -3),
#     (0x7E, -2),
#     (0x7F, -1)
# ]

# ####################################################################################################################
# ####################################################################################################################
# ####################################################################################################################
# ####################################################################################################################


# ####################################################################################################################
# ####################################################################################################################
# # module: app_beatmaker
# ####################################################################################################################
# ####################################################################################################################
# COMMAND_IN_NOTEON = 0
# COMMAND_IN_NOTEOFF = 1
# COMMAND_IN_CONTROLCHANGE = 2

# COMMAND_OUT_LEDON = 3
# COMMAND_OUT_LEDOFF = 4
# COMMAND_OUT_CONTROLSET = 5

# COMMANDS_IN = [COMMAND_IN_NOTEON,COMMAND_IN_NOTEOFF,COMMAND_IN_CONTROLCHANGE]
# COMMANDS_OUT = [COMMAND_OUT_LEDON,COMMAND_OUT_LEDOFF,COMMAND_OUT_CONTROLSET]
# COMMANDS = COMMANDS_IN + COMMANDS_OUT

# BUTTONS_GROUP_PAD = 0
# BUTTONS_GROUP_PAD_FUNC = 1
# BUTTONS_GROUP_LED_FUNC = 2
# CONTROLLERS_GROUP_CHANNEL_CONTROL = 0

# BUTTONS_PAD = [(None, None)] * 32
# for i in range(len(BUTTONS_PAD)):
#     BUTTONS_PAD[i] = i, BUTTONS_GROUP_PAD

# BUTTON_PAD_FUNC_CHANNEL_UP = 0, BUTTONS_GROUP_PAD_FUNC
# BUTTON_PAD_FUNC_CHANNEL_DOWN = 1, BUTTONS_GROUP_PAD_FUNC
# BUTTON_PAD_FUNC_ZOOM_IN = 2, BUTTONS_GROUP_PAD_FUNC
# BUTTON_PAD_FUNC_ZOOM_OUT = 3, BUTTONS_GROUP_PAD_FUNC
# BUTTON_PAD_FUNC_MOVE_RIGHT = 4, BUTTONS_GROUP_PAD_FUNC
# BUTTON_PAD_FUNC_MOVE_LEFT = 5, BUTTONS_GROUP_PAD_FUNC
# BUTTON_PAD_FUNC_SOLO = 6, BUTTONS_GROUP_PAD_FUNC
# BUTTON_PAD_FUNC_MUTE = 7, BUTTONS_GROUP_PAD_FUNC
# BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_VOLUME_PAN_PITCH = 8, BUTTONS_GROUP_PAD_FUNC
# BUTTON_PAD_FUNC_FILL = 9, BUTTONS_GROUP_PAD_FUNC
# BUTTON_PAD_FUNC_FILL_TYPE = 10, BUTTONS_GROUP_PAD_FUNC
# BUTTON_PAD_FUNC_CLEAR = 11, BUTTONS_GROUP_PAD_FUNC
# BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_TARGET_BAND = 12, BUTTONS_GROUP_PAD_FUNC
# BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_COMP_GATE_DIST = 13, BUTTONS_GROUP_PAD_FUNC

# BUTTON_LED_FUNC_PROGRAM_CHANGE_CHANNEL_CONTROLS_PAGE = 14, BUTTONS_GROUP_LED_FUNC
# BUTTON_LED_FUNC_MUTE_CGD = 15, BUTTONS_GROUP_LED_FUNC  # mute/unmute the compressor gate or distortion/limiter
# BUTTON_LED_FUNC_MUTE_BAND = 16, BUTTONS_GROUP_LED_FUNC
# BUTTON_LED_FUNC_BAND_TYPE = 17, BUTTONS_GROUP_LED_FUNC

# BUTTONS_PAD_FUNC = [
#     BUTTON_PAD_FUNC_CHANNEL_UP,
#     BUTTON_PAD_FUNC_CHANNEL_DOWN,
#     BUTTON_PAD_FUNC_ZOOM_IN,
#     BUTTON_PAD_FUNC_ZOOM_OUT,
#     BUTTON_PAD_FUNC_MOVE_RIGHT,
#     BUTTON_PAD_FUNC_MOVE_LEFT,
#     BUTTON_PAD_FUNC_SOLO,
#     BUTTON_PAD_FUNC_MUTE,
#     BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_VOLUME_PAN_PITCH,
#     BUTTON_PAD_FUNC_FILL,
#     BUTTON_PAD_FUNC_CLEAR,
#     BUTTON_PAD_FUNC_FILL_TYPE,
#     BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_TARGET_BAND,
#     BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_COMP_GATE_DIST,
# ]

# BUTTONS_LED_FUNC = [
#     BUTTON_LED_FUNC_PROGRAM_CHANGE_CHANNEL_CONTROLS_PAGE,
#     BUTTON_LED_FUNC_MUTE_CGD,
#     BUTTON_LED_FUNC_MUTE_BAND,
#     BUTTON_LED_FUNC_BAND_TYPE
# ]

# BUTTONS = BUTTONS_PAD + BUTTONS_PAD_FUNC + BUTTONS_LED_FUNC

# CONTROLLERS_CHANNEL_CONTROL = [(0, 0)] * 8
# CONTROLLER_CHANNEL_CONTROL_VOLUME_PAN_PITCH = 0 , CONTROLLERS_GROUP_CHANNEL_CONTROL
# CONTROLLER_CHANNEL_CONTROL_COMP_GATE_DIST = 1 , CONTROLLERS_GROUP_CHANNEL_CONTROL

# for i in range(len(CONTROLLERS_CHANNEL_CONTROL)):
#     CONTROLLERS_CHANNEL_CONTROL[i] = i, CONTROLLERS_GROUP_CHANNEL_CONTROL

# CONTROLLERS = CONTROLLERS_CHANNEL_CONTROL

# PCVPP_CONTROL_STATE_VOLUME = 0
# PCVPP_CONTROL_STATE_PAN = 1
# PCVPP_CONTROL_STATE_PITCH = 2
# PCVPP_CONTROL_STATES = [PCVPP_CONTROL_STATE_VOLUME, PCVPP_CONTROL_STATE_PAN, PCVPP_CONTROL_STATE_PITCH]

# PCCGD_CONTROL_STATE_COMP = 0
# PCCGD_CONTROL_STATE_GATE = 1
# PCCGD_CONTROL_STATE_DIST = 2
# PCCGD_CONTROL_STATES = [PCCGD_CONTROL_STATE_COMP, PCCGD_CONTROL_STATE_GATE, PCCGD_CONTROL_STATE_DIST]

# APP_BEATMAKER_FILL_TYPE_16 = 0
# APP_BEATMAKER_FILL_TYPE_8 = 1
# APP_BEATMAKER_FILL_TYPE_4 = 2
# APP_BEATMAKER_FILL_TYPE_16_DOTTED = 3
# APP_BEATMAKER_FILL_TYPE_8_DOTTED = 4
# APP_BEATMAKER_FILL_TYPE_4_DOTTED = 5
# APP_BEATMAKER_FILL_TYPE_16_TRIPLET = 6
# APP_BEATMAKER_FILL_TYPE_8_TRIPLET = 7
# APP_BEATMAKER_FILL_TYPE_4_TRIPLET = 8


# class MidasAppBeatmaker(MidasApplication):
#     ccvpp_control_state = PCVPP_CONTROL_STATE_VOLUME
#     zoom_level = 1
#     target_channel = 0
#     channel_offset = 0
#     channel_count = 0 # retrieve value from flsl.channels.channel_count()
#     is_filling = False
#     fill_type = APP_BEATMAKER_FILL_TYPE_16
    
#     def clear_drum_pad_leds(self,value):
#         for button in range(BUTTONS_PAD):
#             flslDevice.midi_out_msg_params(COMMAND_IN_NOTEOFF,*self.get_button_data(button),value)

#     def clear_drum_pad_bits(self,value):
#         for button in range(BUTTONS_PAD):
#             flslDevice.midi_out_msg_params(COMMAND_IN_NOTEOFF,*self.get_button_data(button),value)

#     def update_drum_pad_leds(self):
#         for i in range(BUTTONS_PAD):
#             if(flslChannels.get_grid_bit(self.target_channel,(i+self.channel_offset)*self.zoom_level)) > 0:
#                 flslDevice.midi_out_msg_params(COMMAND_IN_NOTEOFF,*self.get_button_data(BUTTONS_PAD[i]),3)  # TODO:3 should be replaced with an mapped led type, for now we pass 3 (red on apc40)      
#             else: # the bit is off
#                 flslDevice.midi_out_msg_params(COMMAND_IN_NOTEOFF,*self.get_button_data(BUTTONS_PAD[i]),0)  # TODO:3 should be replaced with an mapped led type, for now we pass 3 (red on apc40)      
                
#     def zoom_in(self):
#         if self.zoom_level == 1:
#             self.zoom_level = 2
#         elif self.zoom_level == 2:
#             self.zoom_level = 4
#         elif self.zoom_level == 4:
#             self.zoom_level = 8
#         elif self.zoom_level == 8:
#             pass # last zoom level
#         else :
#             print("[LOGICAL ERROR] appBeatmaker.zoom_in() , self.zoom_level set to invalid value. Expected 1, 4 or 8.")
    
#     def zoom_out(self):
#         if self.zoom_level == 1:
#             pass # first zoom level
#         elif self.zoom_level == 2:
#             self.zoom_level = 1
#         elif self.zoom_level == 4:
#             self.zoom_level = 2
#         elif self.zoom_level == 8:
#             self.zoom_level = 4
#         else :
#             print("[LOGICAL ERROR] appBeatmaker.zoom_out() , self.zoom_level set to invalid value. Expected 1, 4 or 8.")  

#     def onMidasProcess(self,status,port,data1,data2,sysex = None):
#             if self.command_map.is_command_offset_by_channel(COMMAND_IN_NOTEON,status,port):
#                 pass
#             elif self.command_map.is_command_offset_by_channel(COMMAND_IN_NOTEOFF,status,port):
#                 print("Note On Detected")
#                 if self.button_map.is_control(BUTTON_PAD_FUNC_CHANNEL_UP,port,data1): 
#                     print("Func Channel + Detected.")
#                     if self.target_channel > 0:
#                         self.target_channel -= 1
#                     flslChannels.select_single_channel(flslChannels.get_channel_index(self.target_channel)) # Set the selected channel to the current_channel in FL Studio
#                 elif self.button_map.is_control(BUTTON_PAD_FUNC_CHANNEL_DOWN,port,data1): 
#                     if self.target_channel < self.channel_count - 1:
#                         self.target_channel += 1
#                     flslChannels.select_single_channel(flslChannels.get_channel_index(self.target_channel)) # Set the selected channel to the current_channel in FL Studio              
#                 elif self.button_map.is_control(BUTTON_PAD_FUNC_ZOOM_IN,port,data1):
#                     self.zoom_in()        
#                 elif self.button_map.is_control(BUTTON_PAD_FUNC_ZOOM_OUT,port,data1): 
#                     self.zoom_out() 
#                 elif self.button_map.is_control(BUTTON_PAD_FUNC_MOVE_LEFT,port,data1): 
#                     if self.channel_offset > 0:
#                         self.channel_offset -= 1
#                 elif self.button_map.is_control(BUTTON_PAD_FUNC_MOVE_RIGHT,port,data1): 
#                     if self.channel_offset < 4:
#                         self.channel_offset += self.channel_offset
#                 elif self.button_map.is_control(BUTTON_PAD_FUNC_FILL,port,data1): 
#                     if self.is_filling == False:
#                         self.is_filling = True
#                     else:
#                         self.is_filling = False
#                         # Apply fill based on self.fill_type
#                         if APP_BEATMAKER_FILL_TYPE_16 == self.fill_type:
#                             pass
#                         elif APP_BEATMAKER_FILL_TYPE_8 == self.fill_type:
#                             pass
#                         elif APP_BEATMAKER_FILL_TYPE_4 == self.fill_type:
#                             pass
#                         elif APP_BEATMAKER_FILL_TYPE_16_DOTTED == self.fill_type:
#                             pass
#                         elif APP_BEATMAKER_FILL_TYPE_8_DOTTED == self.fill_type:
#                             pass
#                         elif APP_BEATMAKER_FILL_TYPE_4_DOTTED == self.fill_type:
#                             pass
#                         elif APP_BEATMAKER_FILL_TYPE_16_TRIPLET == self.fill_type:
#                             pass
#                         elif APP_BEATMAKER_FILL_TYPE_8_TRIPLET == self.fill_type:
#                             pass
#                         elif APP_BEATMAKER_FILL_TYPE_4_TRIPLET == self.fill_type:
#                             pass
#                 elif self.button_map.is_control(BUTTON_PAD_FUNC_FILL_TYPE,port,data1): 
#                     if self.is_filling :
#                         if self.fill_type <= 9: # we have 9 fill types
#                             self.fill_type += 1
#                         else: # warp back to first fill type
#                             self.fill_type = APP_BEATMAKER_FILL_TYPE_16
#                 elif self.button_map.is_control(BUTTON_PAD_FUNC_CLEAR,port,data1): 
#                     print("Channel+ button detected.") # handle button presses
#                 elif self.button_map.is_control(BUTTON_PAD_FUNC_SOLO,port,data1): 
#                     print("Channel+ button detected.") # handle button presses
#                 elif self.button_map.is_control(BUTTON_PAD_FUNC_MUTE,port,data1): 
#                     print("Channel+ button detected.") # handle button presses
#                 elif self.button_map.is_control(BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_COMP_GATE_DIST,port,data1): 
#                     print("Channel+ button detected.") # handle button presses
#                 elif self.button_map.is_control(BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_VOLUME_PAN_PITCH,port,data1): 
#                     print("Channel+ button detected.") # handle button presses
#                 elif self.button_map.is_control(BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_TARGET_BAND,port,data1): 
#                     print("Channel+ button detected.") # handle button presses
#                 elif self.button_map.is_control(BUTTON_PAD_FUNC_PROGRAM_CHANGE_CHANNEL_COMP_GATE_DIST,port,data1): 
#                     print("Channel+ button detected.") # handle button presses                
#                 elif self.button_map.is_control_from_list(BUTTONS_PAD,port,data1): # handle drum pads
#                     print("One of the pad buttons detected.") 
#             elif self.command_map.is_command_offset_by_channel(COMMAND_IN_CONTROLCHANGE,port,status): # Handle Control Change Commands
#                     if self.button_map.is_control(CONTROLLER_CHANNEL_CONTROL_VOLUME_PAN_PITCH,port,data1): 
#                         if self.ccvpp_control_state == PCVPP_CONTROL_STATE_VOLUME: # Targeting Volume Knob
#                             #flslChannels.setChannelVolume(flslChannels.getChannelIndex(DrumPadTargetChannel),event.data2/127.0) # set the volume in fl studio
#                             #flsl.device.midi_out_msg_params(176,0,48,event.data2) 				# Update the value of the Track Control 1 Knob Target to the Volume of selected channel
#                             pass
#                         elif self.ccvpp_control_state == PCVPP_CONTROL_STATE_PAN: # Targeting Pan Knob
#                             #flslChannels.setChannelPan(flslChannels.getChannelIndex(DrumPadTargetChannel),((event.data2/127.0)*2)-1)
#                             #flsl.device.midi_out_msg_params(176,0,48,event.data2)
#                             pass
#                         elif self.ccvpp_control_state == PCVPP_CONTROL_STATE_PITCH: # Targeting Pitch Knob
#                             # flslChannels.setChannelPitch(flslChannels.getChannelIndex(DrumPadTargetChannel),((event.data2/127.0)*2)-1)
#                             # flsl.device.midi_out_msg_params(176,0,48,event.data2)
#                             pass
#                     elif self.button_map.is_control(CONTROLLER_CHANNEL_CONTROL_COMP_GATE_DIST,port,data1): 
#                             pass          
# # midi input simulation    
# #proccess_event_raw(APP_DRUMPAD_DEVICE_APC40_BUTTON_MAP,APP_DRUMPAD_DEVICE_APC40_COMMAND_MAP,APC40_IN_MIDI_COMMAND_BUTTON_RELEASE,0,APC40_BUTTONS_CLIP_LAUNCH[1][1],127)


# ####################################################################################################################
# ####################################################################################################################
# ####################################################################################################################
# ####################################################################################################################

# ####################################################################################################################
# ####################################################################################################################
# # Utility Functions
# ####################################################################################################################
# ####################################################################################################################

# def merge_list_alternating(list1, list2):
#     return [item for pair in zip(list1, list2) for item in pair]

# ####################################################################################################################
# ####################################################################################################################
# ####################################################################################################################
# ####################################################################################################################

# Test = MidasAppBeatmaker()
# # Generate button map
# Test.button_map.generate(BUTTONS,    
#     # First 4 rows of the Clip Launch section: 32 buttons
#     APC40_BUTTONS_CLIP_LAUNCH[:(APC40_N_CLIP_LAUNCH_ROWS - 1) * (APC40_N_CHANNELS_NO_MASTER)] +
#     # Last row of clip launch and clip stop [first 7 buttons, alternating]: 14 buttons
#     merge_list_alternating(
#         APC40_BUTTONS_CLIP_LAUNCH[(APC40_N_CLIP_LAUNCH_ROWS - 1) * (APC40_N_CHANNELS_NO_MASTER):-1],
#         APC40_BUTTONS_CLIP_STOP[:-1]
#     ) +
#     # Channel Control Buttons = Track Control buttons | 4 buttons
#     [APC40_BUTTON_PAN, APC40_BUTTON_SEND_A, APC40_BUTTON_SEND_B, APC40_BUTTON_SEND_C]
# )
# #print('My button list:', *Test.button_map.data.keys(), sep='\n- ')
# #print('My button list:', *Test.button_map.data.values(), sep='\n- ')
# # for i in range(len(list(Test.button_map.data.values()))):
# #     print("chan:",list(Test.button_map.data.values())[i].channel(int(list(Test.button_map.data.values())[i])))
#     # print("id",list(Test.button_map.data.values())[i].id(list(Test.button_map.data.values())[i]))



# for k, v in Test.button_map.data.items():
#     print(v.channel())
#     print(k, v)


# # Generate command map
# Test.command_map.generate(COMMANDS,[
#     APC40_IN_MIDI_COMMAND_BUTTON_PRESS,
#     APC40_IN_MIDI_COMMAND_BUTTON_RELEASE,
#     APC40_IN_MIDI_COMMAND_CONTROL_CHANGE,
#     APC40_OUT_MIDI_COMMAND_LED_ON,
#     APC40_OUT_MIDI_COMMAND_LED_OFF,
#     APC40_OUT_MIDI_COMMAND_CONTROL_SET
#     ])


# #for k, v in Test.command_map.data.items():
# #    print(k, v)


# #print(APC40_BUTTONS_CLIP_LAUNCH[4*8][1])
# #print(APC40_BUTTONS_CLIP_LAUNCH[4*8][0])
# Test.onMidasProcess(APC40_IN_MIDI_COMMAND_BUTTON_RELEASE,APC40_BUTTONS_CLIP_LAUNCH[4*8][0],APC40_BUTTONS_CLIP_LAUNCH[4*8][1],127)






