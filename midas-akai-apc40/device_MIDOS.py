name=MIDOS

import flsl.device

### import midas scripts as needed
import midas.hardware.apc40.app
import midas.system
import midas.device

### Import fl studio scripts as needed
import device as flslDevice
# import playlist as flslPlaylist
import channels as flslChannels
# import mixer as flslMixer
# import patterns as flslPatterns
# import arrangement as flslArrangement
# import ui as flslUi
import transport as flslTransport
# import device as flslDevice
# import general as flslGeneral
# import launchMapPages as flslLaunchMapPages 
# import midi	as flslMidi # The script will use MIDI functions.  

# Globals
ZoomLevel = 1
global DrumPadTargetChannel
global DrumPadTargetChannelOffset
global DrumPadFuncCCVPPControl_State
DrumPadFuncCCVPPControl_State = 0 # Current Channel Volume Pan Pitch Control 0=Volume 1=Pan 2=Pitch
DrumPadTargetChannel = 0
DrumPadTargetChannelOffset = 0

def ClearAkaiAPC40DrumPadLEDs(value):
	for row in range(4):  # Iterate over each row
		for col in range(8):  # Iterate over each column in the row
			# Access the LED in the current row and column
			flslDevice.midiOutMsg(144,0+col,53+row,value)

def UpdateAkaiAPC40DrumPadLEDs(channel,zoom,offset):
	print("Updating AKAI APC 40 Drumpad LEDs to Channel : ",DrumPadTargetChannel, "Zoom :", ZoomLevel , "Index 0")
	for row in range(4):  # Iterate over each row
		for col in range(8):  # Iterate over each column in the row
			# Access the LED in the current row and column
			if(flslChannels.getGridBit(channel,((((col)*zoom)) + ((row)*8)*zoom) + ((offset * 32)*zoom)) > 0) : # Check if the grid bit is on.
				flslDevice.midiOutMsg(144,0+col,53+row,3)	# Turn the LED on		
			else : # the bit is off
				flslDevice.midiOutMsg(144,0+col,53+row,0)	#update the led	

def updateZoomLevel():
	global ZoomLevel
	print("Updating Zoom Level of Channel Drum Pads...",ZoomLevel)
	if ZoomLevel == 1:
		ZoomLevel = 2
		UpdateAkaiAPC40DrumPadLEDs(DrumPadTargetChannel,ZoomLevel,DrumPadTargetChannelOffset)
		return ZoomLevel
	if ZoomLevel == 2:
		ZoomLevel = 4
		UpdateAkaiAPC40DrumPadLEDs(DrumPadTargetChannel,ZoomLevel,DrumPadTargetChannelOffset)
		return ZoomLevel
	if ZoomLevel == 4:
		ZoomLevel = 8
		UpdateAkaiAPC40DrumPadLEDs(DrumPadTargetChannel,ZoomLevel,DrumPadTargetChannelOffset)
		return ZoomLevel
	if ZoomLevel == 8:
		ZoomLevel = 1
		UpdateAkaiAPC40DrumPadLEDs(DrumPadTargetChannel,ZoomLevel,DrumPadTargetChannelOffset)
		return ZoomLevel

def UpdateAkaiAPC40DrumPadFunctionLEDs():
	print("Updating AKAI APC 40 Drumpad Function LEDs")
	flslDevice.midiOutMsg(144,0,57,5) # Zoom Level
	flslDevice.midiOutMsg(144,1,57,5) # Prev Channel
	flslDevice.midiOutMsg(144,2,57,5) # Next Channel
	flslDevice.midiOutMsg(144,3,57,5) # Prev Index
	flslDevice.midiOutMsg(144,4,57,5) # Next Index

def SetAkaiAPC40DrumPadFunctionLED_Zoom(val):
	flslDevice.midiOutMsg(144,0,57,val) # Prev Channel

def SetAkaiAPC40DrumPadFunctionLED_PrevChannel(val):
	flslDevice.midiOutMsg(144,1,57,val) # Prev Channel

def SetAkaiAPC40DrumPadFunctionLED_NextChannel(val):
	flslDevice.midiOutMsg(144,2,57,val) # Next Channel

def SetAkaiAPC40DrumPadFunctionLED_PrevIndex(val):
	flslDevice.midiOutMsg(144,3,57,val) # Next Channel

def SetAkaiAPC40DrumPadFunctionLED_NextIndex(val):
	flslDevice.midiOutMsg(144,4,57,val) # Next Channel

def OnInit():
    print(flslDevice)
    print(midas.device)
    print("Initialization OK")
	#mydevice = BTOSDevice.Device
	#BTOSDevice.init(mydevice)
    print("Clearing AKAI APC 40 Drumpad LEDs...")
    ClearAkaiAPC40DrumPadLEDs(0)
    print("Updating AKAI APC 40 Drumpad LEDs to Channel 0, Zoom 1 , Index 0")
    UpdateAkaiAPC40DrumPadLEDs(0,1,0)
    UpdateAkaiAPC40DrumPadFunctionLEDs()
    # CR_HighlightChannels = 1
    #flslUi.crDisplayRect(32,0,64,1, flslMidi.MaxInt)
    #flslUi.cut()
    print("Initialization OK")
	
def OnDeInit():
	print("Deinitializing script")

def OnRefresh(flags):
	if ((flags & 1024) == 1024): # HW_Dirty_Patterns	1024	pattern changes
		UpdateAkaiAPC40DrumPadLEDs(DrumPadTargetChannel,ZoomLevel,DrumPadTargetChannelOffset)


#def OnIdle():
	#print(mixer.getSongStepPos())

def OnMidiMsg(event): 
	global DrumPadTargetChannel
	global DrumPadTargetChannelOffset
	global DrumPadFuncCCVPPControl_State
	event.handled = True					# If the script does not recognize the event, do nothing. It's then passed onto FL Studio to use. 
	print("*********EVENT OCCURED:", "id:",event.midiId,"channel:",event.midiChan,"data1:" ,event.data1,"status:",event.status)		# Prints the data recieved to the 'Script output' window				
	if event.data2 > 0:														# If there is data in the second byte 		
		# Handle MIDI CC Events
		if event.data1 == 48 and event.midiChan == 0: # Channel Volume CC Control
			if DrumPadFuncCCVPPControl_State == 0: # Targeting Volume Knob
				flslChannels.setChannelVolume(flslChannels.getChannelIndex(DrumPadTargetChannel),event.data2/127.0) # set the volume in fl studio
				flslDevice.midiOutMsg(176,0,48,event.data2) 				# Update the value of the Track Control 1 Knob Target to the Volume of selected channel

			elif DrumPadFuncCCVPPControl_State == 1: # Targeting Pan Knob
				flslChannels.setChannelPan(flslChannels.getChannelIndex(DrumPadTargetChannel),((event.data2/127.0)*2)-1)
				flslDevice.midiOutMsg(176,0,48,event.data2)

			elif DrumPadFuncCCVPPControl_State == 2: # Targeting Pitch Knob
				flslChannels.setChannelPitch(flslChannels.getChannelIndex(DrumPadTargetChannel),((event.data2/127.0)*2)-1)
				flslDevice.midiOutMsg(176,0,48,event.data2)

		# Handle MIDI Note Events
		if event.midiId == 128:
			if event.data1 > 52 and event.data1 < 57:	#if its a released event of the pad buttons
																				# flslChannels.getGridBit(channel,(((col)*zoom)) + ((row)*8)*zoom) > 0
				currGridBit = (((event.midiChan)*ZoomLevel)) + (((event.data1 - 53)*8)*ZoomLevel) + ((DrumPadTargetChannelOffset * 32)*ZoomLevel)		# Check if the current pad is on, using flslChannels.getGridBit() int index, int position, get grid bit value at "position" for channel at "index".
				if(flslChannels.getGridBit(DrumPadTargetChannel,currGridBit) > 0) :					# if bit is above 0 then its on
					flslChannels.setGridBit(DrumPadTargetChannel,currGridBit,0)						# Turn the bit off	
					flslDevice.midiOutMsg(144,event.midiChan,event.data1,0)			#update the led			
				else :															# the bit is off
					flslChannels.setGridBit(DrumPadTargetChannel,currGridBit,1)						# set the bit on using flslChannels.setGridBit	int index, int position, int value Set grid bit value at "position" for channel at "index".
					flslDevice.midiOutMsg(144,event.midiChan,event.data1,3)			#update the led				
				event.handled = True											# Flag the event was handled so it does not go to FL Studio and get used twice.
			
			if event.data1 == 57 and event.midiChan == 0: # Zoom Level Button
				updateZoomLevel()
				UpdateAkaiAPC40DrumPadLEDs(DrumPadTargetChannel,ZoomLevel,DrumPadTargetChannelOffset)
				UpdateAkaiAPC40DrumPadFunctionLEDs()
				if ZoomLevel == 1: # Set the LED to green when we are at zoom level 1
					SetAkaiAPC40DrumPadFunctionLED_Zoom(1)

			if event.data1 == 57 and event.midiChan == 1: # Previous Channel Button
				if(DrumPadTargetChannel > 0):
					DrumPadTargetChannel = DrumPadTargetChannel - 1
					# Set the selected channel to the selected channel in FL Studio
					# selectOneChannel	int index	-	Select channel at "index" exclusively.
					# getChannelIndex	int index	int	Returns 'indexGlobal' for channel at "index" (respecting the groups).
					print("Selecting AKAIAPC40 DrumPads Target Channel in Fl Studio: Target Channel:", DrumPadTargetChannel," Global Channel Index: ", flslChannels.getChannelIndex(DrumPadTargetChannel))
					flslChannels.selectOneChannel(flslChannels.getChannelIndex(DrumPadTargetChannel))

					# Update the LEDs
					UpdateAkaiAPC40DrumPadLEDs(DrumPadTargetChannel,ZoomLevel,DrumPadTargetChannelOffset)
					UpdateAkaiAPC40DrumPadFunctionLEDs()
					if DrumPadTargetChannel == 0: # Set the next button led to green when we are on the first channel
						SetAkaiAPC40DrumPadFunctionLED_PrevChannel(1) 
					# set the next button led to green when we are on the last channel
					if DrumPadTargetChannel == (flslChannels.channelCount()-1):
						SetAkaiAPC40DrumPadFunctionLED_NextChannel(1) 

					print("Current Drum Pad Channel:",DrumPadTargetChannel)
				else: # The channel is 0 or less, warp back to the last channel in the current group
					DrumPadTargetChannel = flslChannels.channelCount() - 1
					# Set the selected channel to the selected channel in FL Studio
					# selectOneChannel	int index	-	Select channel at "index" exclusively.
					# getChannelIndex	int index	int	Returns 'indexGlobal' for channel at "index" (respecting the groups).
					print("Selecting AKAIAPC40 DrumPads Target Channel in Fl Studio: Target Channel:", DrumPadTargetChannel," Global Channel Index: ", flslChannels.getChannelIndex(DrumPadTargetChannel))
					flslChannels.selectOneChannel(flslChannels.getChannelIndex(DrumPadTargetChannel))
					UpdateAkaiAPC40DrumPadLEDs(DrumPadTargetChannel,ZoomLevel,DrumPadTargetChannelOffset)
					UpdateAkaiAPC40DrumPadFunctionLEDs()
					if DrumPadTargetChannel == (flslChannels.channelCount()-1): # set the next button led to green when we are on the last channel
						SetAkaiAPC40DrumPadFunctionLED_NextChannel(1)

					print("Current Drum Pad Channel:",DrumPadTargetChannel)
				
				# Update the CCVPPControl
				if DrumPadFuncCCVPPControl_State == 0: # Targeting volume knob
					# Update the value of the Track Control 1 Knob Target to the Volume of selected channel
					flslDevice.midiOutMsg(176,0,48,int(flslChannels.getChannelVolume(flslChannels.getChannelIndex(DrumPadTargetChannel))*127.0))
					# Update the type  Track Control 1 Knob Type 0=off, 1=Single, 2=Volume Style, 3=Pan Style, 4-127=Single
					flslDevice.midiOutMsg(176,0,0x38,2)
				elif DrumPadFuncCCVPPControl_State == 1: # Targeting Pan knob
					# Update the value of the Track Control 1 Knob Target to the Volume of selected channel
					flslDevice.midiOutMsg(176,0,48,int(flslChannels.getChannelPan(flslChannels.getChannelIndex(DrumPadTargetChannel))*127.0))
					# Update the type  Track Control 1 Knob Type 0=off, 1=Single, 2=Volume Style, 3=Pan Style, 4-127=Single
					flslDevice.midiOutMsg(176,0,0x38,3)
				elif DrumPadFuncCCVPPControl_State == 2: # Targeting Pitch knob
					# Update the value of the Track Control 1 Knob Target to the Volume of selected channel
					flslDevice.midiOutMsg(176,0,48,int(flslChannels.getChannelPitch(flslChannels.getChannelIndex(DrumPadTargetChannel))*127.0))
					# Update the type  Track Control 1 Knob Type 0=off, 1=Single, 2=Volume Style, 3=Pan Style, 4-127=Single
					flslDevice.midiOutMsg(176,0,0x38,3)

			if event.data1 == 57 and event.midiChan == 2: # Next Channel Button
				if DrumPadTargetChannel < (flslChannels.channelCount()-1):
					DrumPadTargetChannel = DrumPadTargetChannel + 1

					# Set the selected channel to the selected channel in FL Studio
					# selectOneChannel	int index	-	Select channel at "index" exclusively.
					# getChannelIndex	int index	int	Returns 'indexGlobal' for channel at "index" (respecting the groups).
					print("Selecting AKAIAPC40 DrumPads Target Channel in Fl Studio: Target Channel:", DrumPadTargetChannel," Global Channel Index: ", flslChannels.getChannelIndex(DrumPadTargetChannel))
					flslChannels.selectOneChannel(flslChannels.getChannelIndex(DrumPadTargetChannel))

					# Update the LEDs
					UpdateAkaiAPC40DrumPadLEDs(DrumPadTargetChannel,ZoomLevel,DrumPadTargetChannelOffset)
					UpdateAkaiAPC40DrumPadFunctionLEDs()

					# set the next button led to green when we are on the last channel
					if DrumPadTargetChannel == (flslChannels.channelCount()-1):
						SetAkaiAPC40DrumPadFunctionLED_NextChannel(1) 

					print("Current Drum Pad Channel:",DrumPadTargetChannel)

				else: # The channel is the last channel in the group, warp back to the fisrtchannel in the current group
					DrumPadTargetChannel = 0
					# Set the selected channel to the selected channel in FL Studio
					# selectOneChannel	int index	-	Select channel at "index" exclusively.
					# getChannelIndex	int index	int	Returns 'indexGlobal' for channel at "index" (respecting the groups).
					print("Selecting AKAIAPC40 DrumPads Target Channel in Fl Studio: Target Channel:", DrumPadTargetChannel," Global Channel Index: ", flslChannels.getChannelIndex(DrumPadTargetChannel))
					flslChannels.selectOneChannel(flslChannels.getChannelIndex(DrumPadTargetChannel))
					UpdateAkaiAPC40DrumPadLEDs(DrumPadTargetChannel,ZoomLevel,DrumPadTargetChannelOffset)
					UpdateAkaiAPC40DrumPadFunctionLEDs()
					if DrumPadTargetChannel == 0: # Set the next button led to green when we are on the first channel
						SetAkaiAPC40DrumPadFunctionLED_PrevChannel(1) 
					print("Current Drum Pad Channel:",DrumPadTargetChannel)

			if event.data1 == 57 and event.midiChan == 3: # Previous Channel Offset Button
				if(DrumPadTargetChannelOffset > 0):
					DrumPadTargetChannelOffset = DrumPadTargetChannelOffset - 1
					UpdateAkaiAPC40DrumPadLEDs(DrumPadTargetChannel,ZoomLevel,DrumPadTargetChannelOffset)
					UpdateAkaiAPC40DrumPadFunctionLEDs()
					print("Current Drum Pad Channel Offset:",DrumPadTargetChannelOffset)
				if DrumPadTargetChannelOffset == 0: # Set the LED to green when we are at index 0
					SetAkaiAPC40DrumPadFunctionLED_PrevIndex(1)

			if event.data1 == 57 and event.midiChan == 4: # Next Channel Offset Button
				DrumPadTargetChannelOffset = DrumPadTargetChannelOffset + 1
				UpdateAkaiAPC40DrumPadLEDs(DrumPadTargetChannel,ZoomLevel,DrumPadTargetChannelOffset)
				UpdateAkaiAPC40DrumPadFunctionLEDs()
				print("Current Drum Pad Channel Offset:",DrumPadTargetChannelOffset)
			if event.data1 == 57 and event.midiChan == 5: # Fill 16 Pattern Button
				for bit_idx in range(0 + (DrumPadTargetChannelOffset*32),(32+(DrumPadTargetChannelOffset*32)) * ZoomLevel):
					flslChannels.setGridBit(DrumPadTargetChannel,bit_idx,0)
				for bit_idx in range(0 + (DrumPadTargetChannelOffset*32),(32+(DrumPadTargetChannelOffset*32)) * ZoomLevel,2):
					flslChannels.setGridBit(DrumPadTargetChannel,bit_idx,1)
				UpdateAkaiAPC40DrumPadLEDs(DrumPadTargetChannel,ZoomLevel,DrumPadTargetChannelOffset)
				UpdateAkaiAPC40DrumPadFunctionLEDs()
				print("Pattern filled at zoom level:",ZoomLevel)
			if event.data1 == 57 and event.midiChan == 6: # Fill 8 Pattern Button
				for bit_idx in range(0 + (DrumPadTargetChannelOffset*32),(32+(DrumPadTargetChannelOffset*32)) * ZoomLevel):
					flslChannels.setGridBit(DrumPadTargetChannel,bit_idx,0)
				for bit_idx in range(0 + (DrumPadTargetChannelOffset*32),(32+(DrumPadTargetChannelOffset*32)) * ZoomLevel,4):
					flslChannels.setGridBit(DrumPadTargetChannel,bit_idx,1)
				UpdateAkaiAPC40DrumPadLEDs(DrumPadTargetChannel,ZoomLevel,DrumPadTargetChannelOffset)
				UpdateAkaiAPC40DrumPadFunctionLEDs()
				print("Pattern filled at zoom level:",ZoomLevel)
			if event.data1 == 57 and event.midiChan == 7: # Fill 4 Pattern Button
				for bit_idx in range(0 + (DrumPadTargetChannelOffset*32),(32+(DrumPadTargetChannelOffset*32)) * ZoomLevel):
					flslChannels.setGridBit(DrumPadTargetChannel,bit_idx,0)
				for bit_idx in range(0 + (DrumPadTargetChannelOffset*32),(32+(DrumPadTargetChannelOffset*32)) * ZoomLevel,8):
					flslChannels.setGridBit(DrumPadTargetChannel,bit_idx,1)
				UpdateAkaiAPC40DrumPadLEDs(DrumPadTargetChannel,ZoomLevel,DrumPadTargetChannelOffset)
				UpdateAkaiAPC40DrumPadFunctionLEDs()
				print("Pattern filled at zoom level:",ZoomLevel)

			if event.data1 == 91 and event.midiChan == 0: # Play Button
				#FPT_Play	10	(button) play/pause
				flslTransport.start()
				UpdateAkaiAPC40DrumPadLEDs(DrumPadTargetChannel,ZoomLevel,DrumPadTargetChannelOffset)
				UpdateAkaiAPC40DrumPadFunctionLEDs()
			if event.data1 == 92 and event.midiChan == 0: # Stop Button
				#FPT_Play	10	(button) play/pause
				flslTransport.stop()
				UpdateAkaiAPC40DrumPadLEDs(DrumPadTargetChannel,ZoomLevel,DrumPadTargetChannelOffset)
				UpdateAkaiAPC40DrumPadFunctionLEDs()
			if event.data1 == 93 and event.midiChan == 0: # Rec Button
				#FPT_Play	10	(button) play/pause
				flslTransport.record()
				UpdateAkaiAPC40DrumPadLEDs(DrumPadTargetChannel,ZoomLevel,DrumPadTargetChannelOffset)
				UpdateAkaiAPC40DrumPadFunctionLEDs()
			if event.data1 == 99 and event.midiChan == 0: # Tap Tempo Button
				#globalTransport	int command, int value, (int pmeflags = PME_System), (int flags = GT_ALL)
				#FPT_TapTempo	106	(button) tempo tapping , 
				flslTransport.globalTransport(106,1)
				UpdateAkaiAPC40DrumPadLEDs(DrumPadTargetChannel,ZoomLevel,DrumPadTargetChannelOffset)
				UpdateAkaiAPC40DrumPadFunctionLEDs()
				#UpdateAkaiAPC40DrumPadLEDs(DrumPadTargetChannel,ZoomLevel,DrumPadTargetChannelOffset)
				#UpdateAkaiAPC40DrumPadFunctionLEDs()
			if event.data1 == 52 and event.midiChan == 0: # DrumPadFuncCCVPPControl Button 
				# CCVPPControl State
				if DrumPadFuncCCVPPControl_State == 2:
					DrumPadFuncCCVPPControl_State = 0
				else:
					DrumPadFuncCCVPPControl_State = DrumPadFuncCCVPPControl_State + 1
				print("Updating Target Channel Knob, Target:",DrumPadFuncCCVPPControl_State)

				# Update the CCVPPControl
				if DrumPadFuncCCVPPControl_State == 0: # Targeting volume knob
					# Update the value of the Track Control 1 Knob Target to the Volume of selected channel
					flslDevice.midiOutMsg(176,0,48,int(flslChannels.getChannelVolume(flslChannels.getChannelIndex(DrumPadTargetChannel))*127.0))
					# Update the type  Track Control 1 Knob Type 0=off, 1=Single, 2=Volume Style, 3=Pan Style, 4-127=Single
					flslDevice.midiOutMsg(176,0,0x38,2)
				elif DrumPadFuncCCVPPControl_State == 1: # Targeting Pan knob
					# Update the value of the Track Control 1 Knob Target to the Volume of selected channel
					flslDevice.midiOutMsg(176,0,48,int(flslChannels.getChannelPan(flslChannels.getChannelIndex(DrumPadTargetChannel))*127.0))
					# Update the type  Track Control 1 Knob Type 0=off, 1=Single, 2=Volume Style, 3=Pan Style, 4-127=Single
					flslDevice.midiOutMsg(176,0,0x38,3)
				elif DrumPadFuncCCVPPControl_State == 2: # Targeting Pitch knob
					# Update the value of the Track Control 1 Knob Target to the Volume of selected channel
					flslDevice.midiOutMsg(176,0,48,int(flslChannels.getChannelPitch(flslChannels.getChannelIndex(DrumPadTargetChannel))*127.0))
					# Update the type  Track Control 1 Knob Type 0=off, 1=Single, 2=Volume Style, 3=Pan Style, 4-127=Single
					flslDevice.midiOutMsg(176,0,0x38,3)

				UpdateAkaiAPC40DrumPadLEDs(DrumPadTargetChannel,ZoomLevel,DrumPadTargetChannelOffset)
				UpdateAkaiAPC40DrumPadFunctionLEDs()
				#UpdateAkaiAPC40DrumPadLEDs(DrumPadTargetChannel,ZoomLevel,DrumPadTargetChannelOffset)
				#UpdateAkaiAPC40DrumPadFunctionLEDs()

