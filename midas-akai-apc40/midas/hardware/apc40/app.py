# Import examples:
#import flsl.device as device
#import midas.deviceFl2 as dev2
#print(dev2)
import midas.hardware.apc40.data as Apc40Data

#print("Printing from midas/hardware/apc/app.py")

def get_button_led_out_data(led_name):
    """
    Get LED out data by name.

    Parameters:
    - led_name (str): Name of the LED.

    Returns:
    - status (int): Status byte for Note-on Output Signal.
    - channel (int): MIDI channel for the LED.
    - note (int): Note value for the LED.
    """
    # Iterate through LED_DATA to find the LED with the specified name
    for led_data in Apc40Data.BUTTON_LED_OUT_DATA:
        if led_data["name"] == led_name:
            # Retrieve MIDI channel and note from LED_DATA
            channel = led_data["midi_channel"]
            note = led_data["note"]

            # Note-on Output Signal Status 0x9<idx> used to turn a LED on or off. 
            # Assume all idx is 0 for now. The 4-bit <chan> value will be used for the track strips. 
            # Calculate the status byte for Note-on Output Signal
            status = 0x90 | 0x00

            # Return the extracted data
            return status, channel, note

    # If LED with the specified name is not found, return None
    return None
