# name = MIDAS System Utilities

global MIDAS_G_DEBUG_PRINT
MIDAS_G_DEBUG_PRINT = True
def debug_print(val):
    if(MIDAS_G_DEBUG_PRINT):
        print(val)
    else:
        pass