# name = MIDAS Device Module
# midos Device module
# The Device module handles MIDI devices connected to the FL Studio MIDI interface.
# You can send messages to the output interface, retrieve linked control values, etc.
# MIDI scripts assigned to an input interface can be mapped (linked) to an Output interface via the Port Number.
# With mapped (linked) output interfaces, scripts can send MIDI messages to output interfaces using midiOut*** messages.
import flsl.device as flslDevice
from midas.system import debug_print

class Button:
	index = 0 # global index of the button in the list of all buttons
	midi_id  = 0  # the midi id (note), associated with the data1 value of a midi message
	midi_chan  = 0 
	on_status  = 0 # the status byte for the noteOn command
	off_status = 0 # the status byte for the noteOff command
	led_status = 0 # the status byte to set the LED command

class Control:
	index = 0 # global index of button in the list of all buttons
	midi_id = 0 
	midi_chan = 0
	on_status = 0 # the status byte for the cc command

class Device :
    name : str("Unknown")
    port = 0
    id = 0
    is_dispatch = False
    buttons = [] # an array of buttons
    controls = [] # an array of controls


def init(device):
	"""
    Initialize the currently linked device.

    Parameters:
    - device (Device): The device to connect to the currently assigned Fl Studio Script.
	"""	
	if flslDevice.is_assigned() :
		debug_print("[FATAL ERROR] Device not linked. In Fl Studio MIDI Setting, set the input and output target channels of the device to the same channel.")
		return False # Stop initializing device module
	else: # Begin initialization
		debug_print("[Initializing Device: ", flslDevice.get_name()," on Port: ",flslDevice.get_port_number(), " with DeviceID:", flslDevice.get_device_id,". ]")
		debug_print("[ Checking all device buttons by flashing them on. ]")
		for button in device.buttons:
			flslDevice.midi_out_msg_params(button.led_status,button.midi_channel,button.midi_id,127)
	# Initialize dispatch devices if any exist
		debug_print("[Initializing Devices, # of devices detected: ",flslDevice.dispatch_receiver_count,". ]")
		if flslDevice.dispatch_receiver_count < 1 :
			debug_print("[WARNING] No Dispatch Devices found. Receiver (script) must define sender(s) inside script: # receiveFrom=\"Sender name\".")
		else: # Scan devices
			for device in range(flslDevice.dispatch_receiver_count):
				debug_print("[Initializing Reciever Device with index: ", device," on Port: ",flslDevice.dispatch_get_receiver_port_number, ". ]")