# pyaehw4a1
Python module and client for Hisense AEH-W4A1 wifi module 


## Usage
### Read status
    python -m pyaehw4a1 --host IP_ADDRESS

### Send update command
    python -m pyaehw4a1 --host IP_ADDRESS --command COMMAND

## Supported commands
- on
- off
- mode_(cool, heat, fan, dry)
- speed_(mute, low, med, max, auto)
- temp_$1_C ($1 from 16 to 32)
- temp_$1_F ($1 from 61 to 90)
- turbo_on
- turbo_off
- energysave_on
- energysave_off
- display_on
- display_off
- sleep_(1, 2, 3, 4, off)
- vert_dir
- vert_swing
- hor_dir
- hor_swing
- temp_to_F
- temp_to_C


## Note
    I am NOT a programmer and this is my first attempt to write in Python!
    So, it comes with ABSOLUTELY NO WARRANTY!!!
    
    I started this work to implement support to my Hisense multi splip AC
    in Home Assistant... This is the first part.
    
    The module Hisense AEH-W4A1 uses a serial protocol called XM, sending
    AT+XMV command my AC reports v4.4.6;
    on https://github.com/htqwe22/device I found some specifications on
    v3.2.6 and on https://github.com/cgdgithub/ControlJavaEdition I found
    the official protocol implementation but sadly without protocol
    specifications.
    
    If you have updated information, please send it to me!

    My template is https://github.com/JonasPed/pydanfoss-air code.
    Many thanks to the author!
