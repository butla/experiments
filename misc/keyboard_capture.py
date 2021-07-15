import keyboard

print('Press esc to stop recording keys.')
recorded = keyboard.record(until='esc')
for r in recorded:
    print(r.name, r.scan_code, r.event_type)
