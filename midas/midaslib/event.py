from itertools import zip_longest as midaslib_event_zip_longest


class MidasControl:
    """
    Represents a control in the Midas system.

    Attributes:
        group (int): An integer representing the control group.
        index (int): An integer representing the control index.

    Methods:
        __init__(self, group: int = -1, index: int = -1): Initialize MidasControl with group and index.
        data1(self) -> int: Get the first data value.
        data2(self) -> int: Get the second data value.
        data(self) -> Tuple[int, int]: Get both data values.
        __hash__(self): Calculate hash value.
        __eq__(self, other): Check if two MidasControls are equal.
        __str__(self): Convert MidasControl to string.
        group(self) -> int: Get the control group.
        index(self) -> int: Get the control index.
    """

    def __init__(self, group: int = -1, index: int = -1):
        """
        Initialize MidasControl with group and index.

        Args:
            group (int): The control group.
            index (int): The control index.

        """
        self.__data = [group, index]

    def data1(self) -> int:
        """Get the first data value (MidasControl.group : int)."""
        return self.__data[0]

    def data2(self) -> int:
        """Get the first data value (MidasControl.index : int)."""
        return self.__data[1]

    def data(self):
        """Get both data values."""
        return self.__data

    def __hash__(self):
        """Calculate hash value."""
        return hash((self.__data[0], self.__data[1]))

    def __eq__(self, other):
        """Check if two MidasControls are equal."""
        return (
            (self.__data[0], self.__data[1])
            == (other.__data[0], other.__data[1])
        )

    def __str__(self):
        """Convert MidasControl to string."""
        return "MidasControl: group(data1): {0} index(data2): {1}  ".format(
            self.__data[0], self.__data[1]
        )

    def group(self) -> int:
        """Get the control group(data1)."""
        return self.__data[0]

    def index(self) -> int:
        """Get the control index(data2)."""
        return self.__data[1]


class MidiControl:
    """
    Represents a MIDI control.

    Attributes:
        port (int): An integer representing the MIDI port.
        note (int): An integer representing the MIDI note.

    Methods:
        __init__(self, port: int = -1, note: int = -1): Initialize MidiControl with port and note.
        data1(self) -> int: Get the first data value.
        data2(self) -> int: Get the second data value.
        data(self) -> Tuple[int, int]: Get both data values.
        __hash__(self): Calculate hash value.
        __eq__(self, other): Check if two MidiControls are equal.
        __str__(self): Convert MidiControl to string.
        port(self) -> int: Get the MIDI port.
        note(self) -> int: Get the MIDI note.
    """

    def __init__(self, port: int = -1, note: int = -1):
        """
        Initialize MidiControl with port and note.

        Args:
            port (int): The MIDI port.
            note (int): The MIDI note.

        """
        self.__data = [port, note]

    def data1(self) -> int:
        """Get the first data value(port)."""
        return self.__data[0]

    def data2(self) -> int:
        """Get the second data value(note)."""
        return self.__data[1]

    def data(self):
        """Get both data values(port,note)."""
        return self.__data

    def __hash__(self):
        """Calculate hash value."""
        return hash((self.__data[0], self.__data[1]))

    def __eq__(self, other):
        """Check if two MidiControls are equal."""
        return (
            (self.__data[0], self.__data[1])
            == (other.__data[0], other.__data[1])
        )

    def __str__(self):
        """Convert MidiControl to string."""
        return "param 1: {0} param 2: {1}  ".format(
            self.__data[0], self.__data[1]
        )

    def port(self) -> int:
        """Get the MIDI port.(data1)"""
        return self.__data[0]

    def note(self) -> int:
        """Get the MIDI note.(data2)"""
        return self.__data[1]


class MidasInputEvent:
    """
    Represents an input event in the Midas system.

    Attributes:
        EVENT_TYPE_NOTEON (int): Constant for the note-on event type.
        EVENT_TYPE_NOTEOFF (int): Constant for the note-off event type.
        EVENT_TYPE_CONTROLCHANGE (int): Constant for the control change event type.

    Members:
        type(int): The event type, determined by using a midas midi command map.
        event_value(int): The event value, passed to midas by FL Studio(Hardware Output/MidiOut Plugin) or the user(Simulated events)
        midas_constrol(MidasControl): The midas control (address) of this event, detemined using a midas midi control map.
    Methods:
        __init__(
            self, event_type: int, event_value: int, midas_control: 'MidasControl', midi_control: 'MidiControl'
        ): Initialize MidasEvent with event type, event value, MidasControl, and MidiControl.
        __str__(self): Convert MidasEvent to string.
    """

    EVENT_TYPE_NOTEON = 0
    EVENT_TYPE_NOTEOFF = 1
    EVENT_TYPE_CONTROLCHANGE = 2

    def __init__(
        self, event_type: int, event_value: int, midas_control: 'MidasControl'
    ):
        """
        Initialize MidasEvent with event type, event value, MidasControl, and MidiControl.

        Args:
            event_type (int): The event type.
            event_value (int): The event value.
            midas_control (MidasControl): The MidasControl associated with the event.
            midi_control (MidiControl): The MidiControl associated with the event.

        """
        self.type = event_type
        self.value = event_value
        self.control = midas_control

    def __hash__(self):
        """Calculate hash value."""
        return hash((self.type, self.value,self.control))

    def __eq__(self, other):
        """Check if two MidiControls are equal."""
        return (
            (self.type, self.value,self.control)
            == (self.type, self.value,self.control)
        )

    def __str__(self):
        """Convert MidasEvent to string."""
        return (
            f"Event(type={self.event_type}, value={self.event_value}, midas_control={self.midas_control}"
        )
    

class MidasOutputEvent:
    """
    Represents an input output in the Midas system.

    Attributes:
        EVENT_TYPE_NOTEON (int): Constant for the note-on event type.
        EVENT_TYPE_NOTEOFF (int): Constant for the note-off event type.
        EVENT_TYPE_CONTROLCHANGE (int): Constant for the control change event type.

    Members:
        type(int): The event type, determined by using a midas midi command map.
        event_value(int): The event value, passed to midas by FL Studio(Hardware Output/MidiOut Plugin) or the user(Simulated events)
        midas_constrol(MidasControl): The midas control (address) of this event, detemined using a midas midi control map.
    Methods:
        __init__(
            self, event_type: int, event_value: int, midas_control: 'MidasControl', midi_control: 'MidiControl'
        ): Initialize MidasEvent with event type, event value, MidasControl, and MidiControl.
        __str__(self): Convert MidasEvent to string.
    """

    EVENT_TYPE_NOTEON = 0
    EVENT_TYPE_NOTEOFF = 1
    EVENT_TYPE_CONTROLCHANGE = 2

    def __init__(
        self, event_type: int, event_value: int, midas_control: 'MidasControl'
    ):
        """
        Initialize MidasEvent with event type, event value, MidasControl, and MidiControl.

        Args:
            event_type (int): The event type.
            event_value (int): The event value.
            midas_control (MidasControl): The MidasControl associated with the event.
            midi_control (MidiControl): The MidiControl associated with the event.

        """
        self.type = event_type
        self.value = event_value
        self.control = midas_control

    def __hash__(self):
        """Calculate hash value."""
        return hash((self.type, self.value,self.control))

    def __eq__(self, other):
        """Check if two MidiControls are equal."""
        return (
            (self.type, self.value,self.control)
            == (self.type, self.value,self.control)
        )

    def __str__(self):
        """Convert MidasEvent to string."""
        return (
            f"Event(type={self.event_type}, value={self.event_value}, midas_control={self.midas_control}"
        )

class MidasMidiControlMap:
    """
    Represents a mapping between Midas controls and MIDI controls.

    Methods:
        __init__(self): Initialize MidasMidiControlMap with an empty dictionary.
        data(self) -> dict: Get the data dictionary.
        emplace(self, midas_control: MidasControl, midi_control: MidiControl): Add or update a mapping entry.
        get_midas(self, midi_control: MidiControl) -> list[MidasControl]: Get a list of Midas controls associated with the given MIDI control.
        get_first_midas(self, midi_control: MidiControl) -> MidasControl or None: Get the first Midas control associated with the given MIDI control.
        get_midi(self, midas_control: MidasControl) -> MidiControl: Get the MIDI control associated with the given Midas control.
        get_all(self) -> list[MidiControl]: Get a list of all MIDI controls in the mapping.
        contains_equal(self, midas_control: MidasControl, midi_control_d1: int, midi_control_d2: int) -> bool: Check if a mapping entry with the same values exists.
        generate(self, midas_control_list: list[MidasControl], midi_control_list: list[MidiControl]): Generate mapping entries from lists of Midas and MIDI controls.
        regenerate(self, midas_control_list: list[MidasControl], midi_control_list: list[MidiControl]): Regenerate the mapping from lists of Midas and MIDI controls.
        retarget(self, midi_control_list: list[MidiControl]): Retarget existing mapping entries using a new list of MIDI controls.

    """

    def __init__(self):
        """Initialize MidasMidiControlMap with an empty dictionary."""
        self.__data = {}

    def data(self) -> dict:
        """Get the data dictionary."""
        return self.__data

    def emplace(self, midas_control: MidasControl, midi_control: MidiControl):
        """
        Add or update a mapping entry.

        Args:
            midas_control: The MidasControl instance.
            midi_control: The MidiControl instance.

        """
        self.__data[midas_control] = midi_control

    def get_midas(self, midi_control: MidiControl) -> list[MidasControl]:
        """
        Get a list of Midas controls associated with the given MIDI control.

        Args:
            midi_control: The MidiControl instance.

        Returns:
            list[MidasControl]: A list of Midas controls.

        """
        return [a_midas_control for a_midas_control, a_midi_control in self.__data.items() if a_midi_control == midi_control]

    def get_first_midas(self, midi_control: MidiControl) -> MidasControl or None:
        """
        Get the first Midas control associated with the given MIDI control.

        Args:
            midi_control: The MidiControl instance.

        Returns:
            MidasControl or None: The first Midas control associated with the given MIDI control.

        """
        for a_midas_control, a_midi_control in self.__data.items():
            if a_midi_control == midi_control:
                return a_midas_control
        return None

    def get_midi(self, midas_control: MidasControl) -> MidiControl:
        """
        Get the MIDI control associated with the given Midas control.

        Args:
            midas_control: The MidasControl instance.

        Returns:
            MidiControl: The associated MidiControl instance.

        """
        return self.__data[midas_control]

    def get_all(self) -> list[MidiControl]:
        """Get a list of all MIDI controls in the mapping."""
        return list(self.__data.values())

    def contains_equal(self, midas_control: MidasControl, midi_control_d1: int, midi_control_d2: int) -> bool:
        """
        Check if a mapping entry with the same values exists.

        Args:
            midas_control: The MidasControl instance.
            midi_control_d1: The data1 value of the MidiControl instance.
            midi_control_d2: The data2 value of the MidiControl instance.

        Returns:
            bool: True if a matching entry exists, False otherwise.

        """
        if midas_control in self.__data:
            if (self.__data[midas_control]).data1() == midi_control_d1 and (self.__data[midas_control]).data2() == midi_control_d2:
                return True
        return False

    def generate(self, midas_control_list: list[MidasControl], midi_control_list: list[MidiControl]):
        """
        Generate mapping entries from lists of Midas and MIDI controls.

        Args:
            midas_control_list: List of MidasControl instances.
            midi_control_list: List of MidiControl instances.

        """
        for i in range(len(midas_control_list)):
            if i < len(midi_control_list):
                self.__data[midas_control_list[i]] = midi_control_list[i]
            else:
                self.__data[midas_control_list[i]] = MidiControl()

    def regenerate(self, midas_control_list: list[MidasControl], midi_control_list: list[MidiControl]):
        """
        Regenerate the mapping from lists of Midas and MIDI controls.

        Args:
            midas_control_list: List of MidasControl instances.
            midi_control_list: List of MidiControl instances.

        """
        self.__data.clear()
        for i in range(len(midas_control_list)):
            if i < len(midi_control_list):
                self.__data.update({midas_control_list[i]: midi_control_list[i]})
            else:
                self.__data[midas_control_list[i]] = MidiControl()

    def retarget(self, midi_control_list: list[MidiControl]):
        """
        Retarget existing mapping entries using a new list of MIDI controls.

        Args:
            midi_control_list: List of MidiControl instances.

        """
        data_keys_list = list(self.__data.keys())
        for i in range(len(data_keys_list)):
            if i < len(midi_control_list):
                self.__data[data_keys_list[i]] = midi_control_list[i]
            else:
                self.__data[data_keys_list[i]] = MidiControl()

class MidasMidiCommandMap:
    """
    Represents a mapping between Midas commands and MIDI commands.

    Methods:
        __init__(self): Initialize MidasMidiCommandMap with an empty dictionary.
        data(self): Get the data dictionary.
        emplace(self, midas_command: int, midi_command: int): Add or update a mapping entry.
        get_midas(self, midi_command: int): Get a list of Midas commands associated with the given MIDI command.
        get_first_midas(self, midi_command: int): Get the first Midas command associated with the given MIDI command.
        get_midi(self, midas_command: int): Get the MIDI command associated with the given Midas command.
        get_all(self): Get a list of all MIDI commands in the mapping.
        contains_equal(self, midas_command: int, midi_command_d1: int, midi_command_d2: int): Check if a mapping entry with the same values exists.
        generate(self, midas_command_list: list[int], midi_command_list: list[int]): Generate mapping entries from lists of Midas and MIDI commands.
        regenerate(self, midas_command_list: list[int], midi_command_list: list[int]): Regenerate the mapping from lists of Midas and MIDI commands.
        retarget(self, midi_command_list: list[int]): Retarget existing mapping entries using a new list of MIDI commands.

    """

    def __init__(self):
        """
        Initialize MidasMidiCommandMap with an empty dictionary.
        """
        self.__data = {}

    def data(self):
        """
        Get the data dictionary.
        """
        return self.__data

    def emplace(self, midas_command: int, midi_command: int):
        """
        Add or update a mapping entry.

        Args:
            midas_command: Midas command.
            midi_command: MIDI command.

        """
        self.__data[midas_command] = midi_command

    def get_midas(self, midi_command: int):
        """
        Get a list of Midas commands associated with the given MIDI command.

        Args:
            midi_command: MIDI command.

        Returns:
            List of Midas commands associated with the given MIDI command.

        """
        return [a_midas_command for a_midas_command, a_midi_command in self.__data.items() if a_midi_command == midi_command]

    def get_first_midas(self, midi_command: int):
        """
        Get the first Midas command associated with the given MIDI command.

        Args:
            midi_command: MIDI command.

        Returns:
            The first Midas command associated with the given MIDI command, or None if not found.

        """
        for a_midas_command, a_midi_command in self.__data.items():
            if a_midi_command == midi_command:
                return a_midas_command
        return None

    def get_midi(self, midas_command: int):
        """
        Get the MIDI command associated with the given Midas command.

        Args:
            midas_command: Midas command.

        Returns:
            MIDI command associated with the given Midas command.

        """
        return self.__data[midas_command]

    def get_all(self):
        """
        Get a list of all MIDI commands in the mapping.

        Returns:
            List of all MIDI commands in the mapping.

        """
        return list(self.__data.values())

    def contains_equal(self, midas_command: int, midi_command_d1: int, midi_command_d2: int):
        """
        Check if a mapping entry with the same values exists.

        Args:
            midas_command: Midas command.
            midi_command_d1: MIDI command data1.
            midi_command_d2: MIDI command data2.

        Returns:
            True if a mapping entry with the same values exists, False otherwise.

        """
        if midas_command in self.__data:
            if self.__data[midas_command] == midi_command_d1:
                return True
        return False

    def generate(self, midas_command_list: list[int], midi_command_list: list[int]):
        """
        Generate mapping entries from lists of Midas and MIDI commands.

        Args:
            midas_command_list: List of Midas commands.
            midi_command_list: List of MIDI commands.

        """
        for i in range(len(midas_command_list)):
            if i < len(midi_command_list):
                self.__data[midas_command_list[i]] = midi_command_list[i]
            else:
                self.__data[midas_command_list[i]] = int()

    def regenerate(self, midas_command_list: list[int], midi_command_list: list[int]):
        """
        Regenerate the mapping from lists of Midas and MIDI commands.

        Args:
            midas_command_list: List of Midas commands.
            midi_command_list: List of MIDI commands.

        """
        self.__data.clear()
        for i in range(len(midas_command_list)):
            if i < len(midi_command_list):
                self.__data.update({midas_command_list[i]: midi_command_list[i]})
            else:
                self.__data.update({midas_command_list[i]: int()})

    def retarget(self, midi_command_list: list[int]):
        """
        Retarget existing mapping entries using a new list of MIDI commands.

        Args:
            midi_command_list: New list of MIDI commands.

        """
        data_keys_list = list(self.__data.keys())
        for i in range(len(data_keys_list)):
            if i < len(midi_command_list):
                self.__data[data_keys_list[i]] = midi_command_list[i]
            else:
                self.__data[data_keys_list[i]] = int()

class MidasOS:
    """
    Represents the Midas operating system.

    Attributes:
        pages (dict): A dictionary to store pages where keys are page names and values are lists of applications.
        active_page (str): The currently active page.

    Methods:
        __init__(self): Initialize MidasOS with an empty dictionary for pages and a None active_page.
        add_page(self, page_name): Add a new page to MidasOS.
        add_application(self, page_name, application): Add an application to a specific page.
        switch_page(self, page_name): Switch to a different page.
        alt_tab(self, page_name, app_index): Simulate alt-tab functionality.
        close_page(self, page_name): Close a page and deactivate its applications.
        open_page(self, page_name): Open a closed page and activate its applications.
    """

    def __init__(self):
        """
        Initialize MidasOS with an empty dictionary for pages and a None active_page.
        """
        self.pages = {}
        self.active_page = None

    def add_page(self, page_name):
        """
        Add a new page to MidasOS.

        Args:
            page_name (str): The name of the new page.

        """
        if page_name not in self.pages:
            self.pages[page_name] = []

    def add_application(self, page_name, application):
        """
        Add an application to a specific page.

        Args:
            page_name (str): The name of the page.
            application: The application to add.

        """
        if page_name in self.pages:
            self.pages[page_name].append(application)
            application.set_midas_os(self, page_name)

    def switch_page(self, page_name):
        """
        Switch to a different page.

        Args:
            page_name (str): The name of the page to switch to.

        """
        if page_name in self.pages:
            self.active_page = page_name
            for app in self.pages[page_name]:
                app.on_page_activate()

    def alt_tab(self, page_name, app_index):
        """
        Simulate alt-tab functionality.

        Args:
            page_name (str): The name of the page.
            app_index (int): The index of the application to switch to.

        """
        if page_name in self.pages and 0 <= app_index < len(self.pages[page_name]):
            for app in self.pages[page_name]:
                app.on_deactivate()
            active_app = self.pages[page_name][app_index]
            active_app.on_activate()

    def close_page(self, page_name):
        """
        Close a page and deactivate its applications.

        Args:
            page_name (str): The name of the page to close.

        """
        if page_name in self.pages:
            for app in self.pages[page_name]:
                app.on_deactivate()
            del self.pages[page_name]

    def open_page(self, page_name):
        """
        Open a closed page and activate its applications.

        Args:
            page_name (str): The name of the page to open.

        """
        if page_name not in self.pages:
            self.pages[page_name] = []
            for app in self.pages[page_name]:
                app.on_activate()
    
    def delegate_midas_out(self, page_name, app_index, midas_output_event):
        """
        Delegate a MidasOutputEvent to the corresponding application.

        Args:
            page_name (str): The name of the page.
            app_index (int): The index of the application to delegate to.
            midas_output_event (MidasOutputEvent): The MidasOutputEvent to delegate.

        """
        if page_name in self.pages and 0 <= app_index < len(self.pages[page_name]):
            active_app = self.pages[page_name][app_index]
            midi_control = active_app._button_map.get_midi(midas_output_event.control)
            # FLSIDevice.midi_out( #FIXME: import flsi
            #     midas_output_event.type,
            #     midi_control.port(),
            #     midi_control.note(),
            #     midas_output_event.value,
            # )

class ApplicationBase:
    """
    Base class for applications in the Midas OS.

    Attributes:
        EVENT_TYPE_NOTEON (int): MIDI event type for note-on.
        EVENT_TYPE_NOTEOFF (int): MIDI event type for note-off.
        EVENT_TYPE_CONTROLCHANGE (int): MIDI event type for control change.

    Methods:
        __init__(self): Initialize the ApplicationBase instance.
        set_midas_os(self, midas_os, page_name): Set the MidasOS instance and page for the application.
        on_activate(self): Callback when the application is activated.
        on_deactivate(self): Callback when the application is deactivated.
        on_page_activate(self): Callback when the page containing the application is activated.
        onFruityLoopUpdate(self): Abstract callback for Fruity Loop update event.
        onFruityLoopProgramChange(self, flags): Abstract callback for Fruity Loop program change event.
        onFruityLoopScriptInit(self): Abstract callback for Fruity Loop script initialization event.
        onFruityLoopMidiInput(self, message): Abstract callback for Fruity Loop MIDI input event.
        onFruityLoopSysexInput(self, message): Abstract callback for Fruity Loop SysEx input event.
        onMidasUpdate(self): Callback for Midas update event.
        onMidasProcess(self, status, port, data1, data2, sysex=None): Callback for Midas process event.
        onMidasEvent(self, control, command): Callback for Midas control event.

    """

    EVENT_TYPE_NOTEON = 0
    EVENT_TYPE_NOTEOFF = 1
    EVENT_TYPE_CONTROLCHANGE = 2

    def __init__(self):
        """
        Initialize ApplicationBase with MidasMidiControlMap and MidasMidiCommandMap.
        """
        self._button_map = MidasMidiControlMap()
        self._controller_map = MidasMidiControlMap()
        self._command_map = MidasMidiCommandMap()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

    def __onFruityLoopUpdate(self):
        """Handle update event from Fruity Loops."""
        self.onMidasUpdate()
        self.onFruityLoopUpdate()
        pass

    def __onFruityLoopProgramChange(self, flags):
        """Handle program change event from Fruity Loops."""
        self.onMidasUpdate()
        self.onFruityLoopProgramChange(flags)
        pass

    def __onFruityLoopScriptInit(self):
        """Handle script init event from Fruity Loops."""
        self.onMidasUpdate()
        self.onFruityLoopScriptInit()
        pass

    def __onFruityLoopMidiInput(self, message):
        """
        Handle MIDI input event from Fruity Loops.

        Args:
            message: MIDI input message.

        """
        self.onMidasUpdate()
        self.onFruityLoopMidiInput(message)
        self._onMidasProcessInternal(message.status, message.port, message.data1, message.data2, message.sysex)
        pass

    def __onFruityLoopSysexInput(self, message):
        """
        Handle SysEx input event from Fruity Loops.

        Args:
            message: SysEx input message.

        """
        self.onMidasUpdate()
        self.onFruityLoopSysexInput(message)
        self._onMidasProcessInternal(message.status, message.port, message.data1, message.data2, message.sysex)
        pass

    def _onMidasProcessInternal(self, status, port, data1, data2, sysex=None):
        """
        Handle internal Midas process event.

        Args:
            status: MIDI status.
            port: MIDI port.
            data1: MIDI data1.
            data2: MIDI data2.
            sysex: Optional SysEx data.

        """
        self.onMidasProcess(status, port, data1, data2, sysex)
        print(status, port, data1, data2, sysex)

        self.__process_command_events(status, port, data1, data2)

    def __process_command_events(self, status, port, data1, data2):
        """
        Process Midas command events.

        Args:
            status: MIDI status.
            port: MIDI port.
            data1: MIDI data1.
            data2: MIDI data2.

        """
        for midas_command in self._command_map.get_midas(status):
            if midas_command == self.EVENT_TYPE_CONTROLCHANGE:
                self.__process_control_change_events(port, data1)
            elif midas_command in [self.EVENT_TYPE_NOTEON, self.EVENT_TYPE_NOTEOFF]:
                self.__process_button_events(port, data1)

    def __process_control_change_events(self, port, data1):
        """
        Process control change events.

        Args:
            port: MIDI port.
            data1: MIDI data1.

        """
        for midas_controller in self._controller_map.get_midas(MidiControl(port, data1)):
            self.onMidasEvent(midas_controller, self.EVENT_TYPE_CONTROLCHANGE)

    def __process_button_events(self, port, data1):
        """
        Process button events.

        Args:
            port: MIDI port.
            data1: MIDI data1.

        """
        for midas_button in self._button_map.get_midas(MidiControl(port, data1)):
            command = (
                self.EVENT_TYPE_NOTEON
                if midas_button == self.EVENT_TYPE_NOTEON
                else self.EVENT_TYPE_NOTEOFF
            )
            self.onMidasEvent(midas_button, command)

    def map_midi_control(self, midas_control, midi_control):
        """
        Dynamically map a Midas control to a MIDI control.

        Args:
            midas_control (MidasControl): The Midas control to map.
            midi_control (MidiControl): The MIDI control to map to.
        
        """
        self._button_map.emplace(midas_control, midi_control)

    def map_midi_command(self, midas_command, midi_command):
        """
        Dynamically map a Midas command to a MIDI command.

        Args:
            midas_command (int): The Midas command to map.
            midi_command (int): The MIDI command to map to.

        """
        self._command_map.emplace(midas_command, midi_command)

    def on_activate(self):
        """
        Callback when the application is activated.

        Override this method in subclasses to define activation behavior.

        """
        # Dynamically map controls during activation
        self.setup_dynamic_mappings()

    def setup_dynamic_mappings(self):
        """
        Set up dynamic MIDI mappings.

        Override this method in subclasses to define dynamic mapping behavior.

        Example:
            class CustomApplication(ApplicationBase):
                def setup_dynamic_mappings(self):
                # Dynamically map a specific Midas control to a MIDI control
                my_midas_control = MidasControl(group=1, index=1)
                my_midi_control = MidiControl(port=1, note=60)
                self.map_midi_control(my_midas_control, my_midi_control)

                # Dynamically map a custom Midas command to a MIDI command
                my_midas_command = 42
                my_midi_command = 127
                self.map_midi_command(my_midas_command, my_midi_command)
        """
        pass

    def set_midas_os(self, midas_os, page_name):
        """
        Set the owning MidasOS and page for the application.

        Args:
            midas_os (MidasOS): The MidasOS object.
            page_name (str): The name of the page.

        """
        self._midas_os = midas_os
        self._page_name = page_name

    def on_activate(self):
        """
        Callback when the application is activated.

        Override this method in subclasses to define activation behavior.

        """
        pass

    def on_deactivate(self):
        """
        Callback when the application is deactivated.

        Override this method in subclasses to define deactivation behavior.

        """
        pass

    def on_page_activate(self):
        """
        Callback when the page containing the application is activated.

        Override this method in subclasses to define page activation behavior.

        """
        pass

    def onFruityLoopUpdate(self):
        """
        Abstract callback for Fruity Loop update event.

        Override this method in subclasses to handle Fruity Loop update events.

        """
        pass

    def onFruityLoopProgramChange(self, flags):
        """
        Abstract callback for Fruity Loop program change event.

        Args:
            flags: Flags associated with the program change event.

        Override this method in subclasses to handle Fruity Loop program change events.

        """
        pass

    def onFruityLoopScriptInit(self):
        """
        Abstract callback for Fruity Loop script initialization event.

        Override this method in subclasses to handle Fruity Loop script initialization events.

        """
        pass

    def onFruityLoopMidiInput(self, message):
        """
        Abstract callback for Fruity Loop MIDI input event.

        Args:
            message: MIDI input message.

        Override this method in subclasses to handle Fruity Loop MIDI input events.

        """
        pass

    def onFruityLoopSysexInput(self, message):
        """
        Abstract callback for Fruity Loop SysEx input event.

        Args:
            message: SysEx input message.

        Override this method in subclasses to handle Fruity Loop SysEx input events.

        """
        pass

    def onMidasUpdate(self):
        """
        Callback for Midas update event.

        Override this method in subclasses to define Midas update behavior.

        """
        pass

    def onMidasProcess(self, status, port, data1, data2, sysex=None):
        """
        Callback for Midas process event.

        Args:
            status: MIDI status.
            port: MIDI port.
            data1: MIDI data1.
            data2: MIDI data2.
            sysex: Optional SysEx data.

        Override this method in subclasses to define Midas process behavior.

        """
        pass

    def onMidasEvent(self, control, command):
        """
        Callback for Midas control event.

        Args:
            control: MidasControl instance.
            command: MIDI command.

        Override this method in subclasses to define Midas control event behavior.

        """
        pass
"""
Other classes (MidasControl, MidiControl, MidasEvent, MidasMidiControlMap, MidasMidiCommandMap)...
"""