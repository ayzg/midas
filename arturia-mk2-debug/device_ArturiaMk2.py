# name=ArturiaMk2
import playlist
import channels
import mixer
import patterns
import arrangement
import ui
import transport
import device
import general
import launchMapPages

print('working')


import midi

class ZoomController:
    def __init__(self):
        self.grid_bit = 0
        self.zoom_levels = [1, 2, 4, 8]
        self.current_zoom = 0
        self.grid_offset = 0
        self.channels = list(range(1, 33))
        self.current_channel = 1

    def set_grid_bit(self):
        # Set grid bit based on current zoom level and offset
        grid_position = self.grid_bit + self.grid_offset
        print(f"Setting grid bit {grid_position} for zoom level {self.zoom_levels[self.current_zoom]} on channel {self.current_channel}")

    def zoom_in(self):
        # Zoom in and loop around if at the maximum zoom level
        self.current_zoom = (self.current_zoom + 1) % len(self.zoom_levels)
        print(f"Zooming in to level {self.zoom_levels[self.current_zoom]}")

    def zoom_out(self):
        # Zoom out and loop around if at the minimum zoom level
        self.current_zoom = (self.current_zoom - 1) % len(self.zoom_levels)
        print(f"Zooming out to level {self.zoom_levels[self.current_zoom]}")

    def offset_grid(self, direction):
        # Offset the grid bit by 16 in the specified direction
        if direction == 'forward':
            self.grid_offset += 16
            print(f"Offsetting grid forward to {self.grid_offset}")
        elif direction == 'backward':
            self.grid_offset -= 16
            print(f"Offsetting grid backward to {self.grid_offset}")

    def switch_channel(self, channel):
        # Switch the target channel
        if channel in self.channels:
            self.current_channel = channel
            print(f"Switched to channel {self.current_channel}")
        else:
            print("Invalid channel")

def printmsg(eventData):
   print("MIDI Message Event:")
   print("Handled:", eventData.handled, end='\t')
   print("Timestamp:", eventData.timestamp, end='\t')
   print("Status:", eventData.status, end='\t')
   print("Data1:", eventData.data1, end='\t')
    
    # Print 4 data points per line
   print()

   print("Data2:", eventData.data2, end='\t')
   print("Port:", eventData.port, end='\t')
   print("Note:", eventData.note, end='\t')
   print("Velocity:", eventData.velocity)

   print("Pressure:", eventData.pressure, end='\t')
   print("ProgNum:", eventData.progNum, end='\t')
   print("ControlNum:", eventData.controlNum, end='\t')
   print("ControlVal:", eventData.controlVal)

   print("PitchBend:", eventData.pitchBend, end='\t')
   print("SysEx:", eventData.sysex, end='\t')
   print("IsIncrement:", eventData.isIncrement, end='\t')
   print("Res:", eventData.res)

   print("InEv:", eventData.inEv, end='\t')
   print("OutEv:", eventData.outEv, end='\t')
   print("MidiId:", eventData.midiId, end='\t')
   print("MidiChan:", eventData.midiChan)

   print("MidiChanEx:", eventData.midiChanEx, end='\t')
   #print("Pmeflags:", eventData.pmeflags)

def OnInit():
    print("Initialization OK")

def OnDeInit():
	print("Deinitializing script")

#def OnMidiIn(eventData):
	#printmsg(eventData)

def OnMidiMsg(eventData):
	printmsg(eventData)


def OnSysEx(eventData): 
	printmsg(eventData)


#def OnNoteOn(eventData): 

#def OnNoteOff(eventData):