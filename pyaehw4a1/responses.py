from enum import Enum

'''
Based on XM rev.3.2.6 from
https://github.com/htqwe22/device/blob/96f355b12da33c1c187f9d31cace1b02abcf2446/src/protocol/protocol.h

Testing AC (multi split unit) has XM rev 4.4.6
'''

class ResponsePacket(Enum):
    correct_3_0 = bytes([
        0xF4, 0xF5, 0x01, 0x40, 0x0B, 0x01, 0x00, 0xFE, 0x01, 0x01, 0x01,
        0x01, 0x00, 0x03, 0x00, 0x01,
        ])
    correct_3_1 = bytes([    
        0xF4, 0xF5, 0x01, 0x40, 0x0B, 0x01, 0x00, 0xFE, 0x01, 0x01, 0x01,
        0x01, 0x00, 0x03, 0x01, 0x01,
        ])
    correct_7_1 = bytes([    
        0xF4, 0xF5, 0x01, 0x40, 0x0F, 0x01, 0x00, 0xFE, 0x01, 0x01, 0x01,
        0x01, 0x00, 0x07, 0x01, 0x01,
        ])
    correct_10_4 = bytes([    
        0xF4, 0xF5, 0x01, 0x40, 0x0D, 0x01, 0x00, 0xFE, 0x01, 0x01, 0x01,
        0x01, 0x00, 0x0A, 0x04, 0x01,
    ])
    correct_101_0 = bytes([
        0xF4, 0xF5, 0x01, 0x40,
        ])
    correct_102_0 = bytes([
        0xF4, 0xF5, 0x01, 0x40, 0x49, 0x01, 0x00, 0xFE, 0x01, 0x01, 0x01,
        0x01, 0x00, 0x66, 0x00, 0x01,
        ])
    correct_102_64 = bytes([
        0xF4, 0xF5, 0x01, 0x40, 0x1C, 0x01, 0x00, 0xFE, 0x01, 0x01, 0x01,
        0x01, 0x00, 0x66, 0x40, 0x01,
        ])


class _Data_102_0(Enum):
    wind_status = (1, 8) # air volume
    sleep_status = (9, 7) # sleep
    mode_status = (17, 4)  # mode  
    run_status = (21, 1)  # Run
    direction_status = (23, 2)  # wind direction
    indoor_temperature_setting = (25, 8) # indoor temperature
    indoor_temperature_status = (33, 8) # indoor temperature
    indoor_pipe_temperature = (41, 8) # indoor tube temperature value
    indoor_humidity_setting = (49, 8) # indoor humidity
    indoor_humidity_status = (57, 8) # indoor humidity
    somatosensory_temperature = (65, 8) # body temperature
    somatosensory_compensation = (73, 5)  # Somatosensory compensation
    somatosensory_compensation_ctrl = (78, 3)  # Somatosensory compensation control
    temperature_compensation = (81, 5)  # temperature compensation
    temperature_Fahrenheit = (87, 1)  # Fahrenheit display
    timer = (89, 8)
    hour = (97, 8)
    minute = (105, 8)
    poweron_hour = (113, 5)
    poweron_minute = (121, 6)
    poweron_status = (128, 1)
    poweroff_hour = (129, 5)
    poweroff_minute = (137, 6)
    poweroff_status = (144, 1)
    drying = (145, 4)
    wind_door = (149, 4)
    up_down = (153, 1)  # Up and down
    left_right = (154, 1)  # Left wind
    nature = (155, 1)  # natural wind
    heat = (156, 1)  # heating wind
    low_power = (157, 1)  # energy saving
    low_electricity = (158, 1)  # Power saving
    efficient = (159, 1)  # efficient
    dual_frequency = (160, 1)  # Double frequency
    dew = (161, 1)  # fresh
    swap = (162, 1)  # Change the wind
    indoor_clear = (163, 1)  # indoor cleaning
    outdoor_clear = (164, 1)  # Outdoor cleaning
    smart_eye = (165, 1)  # wisdom eye
    mute = (166, 1)  # mute
    voice = (167, 1)  # voice
    smoke = (168, 1)  # except smoke
    back_led = (169, 1)  # background light
    display_led = (170, 1)  # display
    indicate_led = (171, 1)  # light
    indoor_led = (172, 1)  # indoor and outdoor switching lights
    filter_reset = (173, 1)  # Filter reset
    left_wind = (174, 1)  # Left wind
    right_wind = (175, 1)  # right wind
    indoor_electric = (176, 1)  # indoor power board
    auto_check = (177, 1)  # Self-test
    time_laps = (178, 1)  # timelapse
    rev23 = (179, 4) 
    sample = (183, 1)  # sample
    indoor_eeprom = (184, 1)  # eeprom
    indoor_temperature_sensor = (185, 1) 
    indoor_temperature_pipe_sensor = (186, 1) 
    indoor_humidity_sensor = (187, 1) 
    indoor_water_pump = (188, 1) 
    indoor_machine_run = (189, 1) 
    indoor_bars = (190, 1) 
    indoor_zero_voltage = (191, 1) 
    indoor_outdoor_communication = (192, 1) 
    display_communication = (193, 1) 
    keypad_communication = (194, 1) 
    wifi_communication = (195, 1) 
    electric_communication = (196, 1) 
    eeprom_communication = (197, 1) 
    rev25 = (198, 3) 
    compressor_frequency = (201, 8)
    compressor_frequency_setting = (209, 8)
    compressor_frequency_send = (217, 8)
    outdoor_temperature = (225, 8)
    outdoor_condenser_temperature = (233, 8)
    compressor_exhaust_temperature = (241, 8)
    target_exhaust_temperature = (249, 8)
    expand_threshold = (257, 8)
    UAB_HIGH = (265, 8)
    UAB_LOW = (273, 8)
    UBC_HIGH = (281, 8)
    UBC_LOW = (289, 8)
    UCA_HIGH = (297, 8)
    UCA_LOW = (305, 8)
    IAB = (313, 8)
    IBC = (321, 8)
    ICA = (329, 8)
    generatrix_voltage_high = (337, 8)
    generatrix_voltage_low = (345, 8)
    IUV = (353, 8)
    rev46 = (361, 3) 
    four_way = (364, 1) 
    outdoor_machine = (365, 1) 
    wind_machine = (366, 3) 
    rev47 = (369, 8)
    rev48 = (377, 8)
    rev49 = (385, 8)
    rev50 = (393, 8)
    rev51 = (401, 8)
    rev52 = (409, 8)
    rev53 = (417, 8)
    rev54 = (425, 8)
    rev55 = (433, 8)
    rev56 = (441, 8)
    def __init__(self, offset, length):
        self.offset = offset
        self.length = length


class _Data_102_64(Enum):
    ONE_KWH_I = (1, 8)
    ONE_KWH_F = (9, 8)
    ONE_KWH_D = (17, 8)
    KWH_DAY = (25, 8)
    KWH_WEEK_H = (33, 8)
    KWH_WEEK_L = (41, 8)
    KWH_MONTH_H = (49, 8)
    KWH_MONTH_L = (57, 8)
    KWH_QUARTER_H = (65, 8)
    KWH_QUARTER_L = (73, 8)
    KWH_HALFYEAR_H = (81, 8)
    KWH_HALFYEAR_L = (89, 8)
    KWH_YEAR_H = (97, 8)
    KWH_YEAR_L = (105, 8)
    KWH_H = (113, 8)
    KWH_SH = (121, 8)
    KWH_SL = (129, 8)
    KWH_L = (137, 8)
    def __init__(self, offset, length):
        self.offset = offset
        self.length = length


class DataPacket(Enum):
    data_102_0 = _Data_102_0
    data_102_64 = _Data_102_64