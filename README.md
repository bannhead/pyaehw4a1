# pyaeh-w4a1
Python module and client for Hisense AEH-W4A1 wifi module 

## Usage
### Read all commands
	python -m pyaehw4a1 --host IP_ADDRESS

### Send update command
	python -m pyaehw4a1 --host IP_ADDRESS --command COMMAND

## Supported commands
- on
- off
- mode_(cool, heat, fan, dry)
- speed_(mute, low, med, max, auto)
- temp_$1_C ($1 from 16 to 32)
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


Heavily based on https://github.com/JonasPed/pydanfoss-air work!
