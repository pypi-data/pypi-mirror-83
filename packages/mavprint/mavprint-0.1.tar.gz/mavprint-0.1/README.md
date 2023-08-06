# mavprint

Print mavlink messages to console

## Quickstart

    pip install mavprint
    mavprint --port /dev/ttyACM1 show

## Examples

    # show all messages except BAD_DATA
    $ mavprint show --exclude BAD_DATA

    # show number of messages of each type captured while running
    $ mavprint unique
    ^C
    {   'ACTUATOR_CONTROL_TARGET': 34,
        'ALTITUDE': 11,
        'ATTITUDE': 56,
        'ATTITUDE_QUATERNION': 57,
        'ATTITUDE_TARGET': 10,
        'BAD_DATA': 4,
        'BATTERY_STATUS': 1,
        'ESTIMATOR_STATUS': 6,
        'EXTENDED_SYS_STATE': 3,
        'HEARTBEAT': 2,
        'HIGHRES_IMU': 57,
        'LOCAL_POSITION_NED': 35,
        'PING': 2,
        'SCALED_IMU': 29,
        'SCALED_IMU2': 29,
        'SERVO_OUTPUT_RAW': 22,
        'SYS_STATUS': 2,
        'TIMESYNC': 12,
        'VFR_HUD': 22,
        'VIBRATION': 3}
