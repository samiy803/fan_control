import subprocess
import time
import re

LOOP_DELAY = 1 # how often to update fanspeed in seconds
DEADZONE = 10 # how much to round the fanspeed to avoid rapid changes
WINDOW_SIZE = 3 # used for smoothing the temperature readings, how many readings to average

SENSORS_CMD = '/usr/bin/sensors'
IPMITOOL_CMD = '/usr/bin/ipmitool'

temp_history = []

def float_to_hex(f: float):
    """
    Converts a number in range 0-100 to 0x00 to 0xff
    """
    return hex(int(f*255/100))

def temp_to_speed(temp: float):
    """
    Converts temperature to fan speed (0 to 100) and rounds to the 
    nearest multiple of DEADZONE to avoid rapid changes.

    Applies a Michaelis Menten curve (probably not the best choice but it gives good values)
    Graph of the curve: https://www.desmos.com/calculator/lngfs9xoon
    """
    if temp > 87:
        return 100 # avoids the asymptote at 94
    
    speed = (-11.60026*temp)/(-94.82565 + temp) # curve
    clamped = min(100, max(0, speed)) # Clamp between 0 and 100
    return round(clamped/DEADZONE)*DEADZONE # Round to nearest DEADZONE

def smooth_temp(temp: float):
    """
    Smooths the temperature readings by averaging the last WINDOW_SIZE readings
    """
    global temp_history
    temp_history.append(temp)
    temp_history = temp_history[-WINDOW_SIZE:]
    return sum(temp_history)/len(temp_history)

def get_temps():
    """
    Get the temperatures of the CPU. Returns a list of the core temperatures
    """
    sensors_output = subprocess.check_output(SENSORS_CMD)
    sensors_output = sensors_output.decode('utf-8')
    print(sensors_output)
    temps = re.findall(r'Core \d+:\s+\+(\d+.\d)', sensors_output)
    return [float(temp) for temp in temps]

def set_fan_speed(speed: int):
    """
    Set the fan speed to the given value.
    Uses the raw IPMI command 0x3a 0x07 {fan_id} {speed} {fan_override}
    Setting fan_override to 0x01 turns off auto mode, and 0x00 turns it back on
    Setting speed to 0x00 does not turn off the fan, but sets it to the lowest speed. Fine for our purposes.
    """
    speed_hex = float_to_hex(speed)
    subprocess.run([IPMITOOL_CMD, 'raw', '0x3a', '0x07', '0x01', speed_hex, '0x01'])
    subprocess.run([IPMITOOL_CMD, 'raw', '0x3a', '0x07', '0x02', speed_hex, '0x01'])
    subprocess.run([IPMITOOL_CMD, 'raw', '0x3a', '0x07', '0x03', speed_hex, '0x01'])

def weighted_average(temps: list):
    """
    Takes a list of temperatures and returns a weighted average where 
    the two highest temperatures are weighted twice as much as the rest.

    If there is less than 2 temperatures, returns the max of the list.
    If any of the temps are over 87, returns max of the list.
    """
    n = len(temps)
    m = max(temps)
    if n < 2 or m > 87:
        return m
    
    temps.sort()
    return (2*temps[-1] + 2*temps[-2] + sum(temps[:-2]))/(n + 2)

def main():
    while True:
        temps = get_temps()
        print(temps)
        avg_temp = weighted_average(temps)
        avg_temp = smooth_temp(avg_temp)
        speed = temp_to_speed(avg_temp)
        set_fan_speed(speed)
        print(f'Temps: {temps}, Avg: {avg_temp}, Speed: {speed}')
        time.sleep(LOOP_DELAY)

if __name__ == '__main__':
    main()