# MIDAS - FL Studio MIDI Operating System
FL Studio device python scripts emulating an operating system for MIDI controllers.

## Brief
FL Studio device python script which makes an Akai APC 40 and Arturia MkII act os-like.
These are the devices I own and could test. You may repurpose this codebade for any device.

If you are making a custom python script for your device, extract and reference anything you
need from this codebase. It is a goldmine of info for this very specific python version
used only in FL Studio(see post mortem for detail).


Allows opening different functionalities through a main "window" like a desktop on a computer.
The display is mapped to the grid pads of a midi device. The resolution can be adjusted to fit
any device- unfortunatley devices dont conform to any standard and enumerating them all is
not an option(see post mortem for details). 
Each device midi signal can be mapped to an intermediate layer which then maps to the actual functionality.

This IN THEORY would allow someone to write a script for their device, map it to the intermediate layer
and share it with other people - who would only have to do minimal mapping back to their controller.
Like creating an app for an operating system.

This project also includes an interface to the fl studio python library which corrects some of its errors.
And provides more detailed docs.

## Purpose
I wanted to use my Arturia MkII like the Akai Fire(FLStudio Official controller), which is able to make drum 
patterns in the FL Studio step sequencer. Appently this info is not so easy to attain.

Only potantial example I found was a youtuber his midi controller script for an Arturia MKII but then
at the end he forwards you to a website that charges $20 for the script. Also, it didint have
step sequencer functionality I wanted anyways.

So I decided to make my own. 

I also made a script for my ancient Akai APC 40 enroute.

Lastly, I went too far and tried make it modular and 'easy' to repurpose for other devices.

## Post-Mortem 

The project is abandoned because:
- Allowing multiple devices to share script apps through an operating system is an impossible endeavour.
  
  The MIDI protocol is a protocol not a standard. Every device manufacturer has their own set of midi signals
  and they dont care to make them similar to other devices(in fact it would be detrimental to them).
  So this idea will have to remain a fantasy unless: all future devices accept a standard set of signals
  for a standard set of musical controls. OR, all software uses a new device communication protocol which
  is backwards compatible with midi but has a new ruleset for standard controls, and new devices are then
  implicitly forced to accept it.
- **??Conspiracy??** FL Studio python scripting is intentionally difficult to force people to buy their 
  official controllers.

  The python version is embedded and stripped from most modern python patterns, its python from the ice age.
  Library provided by Image Line has undocumented bugs. The official documentation is also incomplete 
  and sometimes wrong. For example(event to this day, initially written in 2023): `pmeflags` variable of
  `eventData` is not a variable. Its actually called `pmeFlags`. Thats negligence to not fix it for 5 years.
  I almost smashed a wall over pmeflags. I will never forget pme**F**lags for the rest of my life.
[You shouldof known to check the url for the actual variable name! :grinning:](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm#pmeFlags)



