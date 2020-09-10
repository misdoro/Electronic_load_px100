# Electronic_load_px100
150W Electronic load / Battery discharge capacity tester PX-100 protocol and control software.

# Binary protocol

See the [v2.70 binary Protocol description](protocol_PX-100_2_70.md)

# Control software

** Main features:

- Control all load features
- Voltage and Current plot vs time
- Save logs to CSV at exit and at device reset
- Internal resistance measurement at user-defined voltage steps
- Software-defined CC-CV discharge to speed up capacity tests for low current discharge

# Installing

Python is required to run this software. Version 3.6 or newer is required.

Run the following line to install dependencies:
```
pip install --user -r requirements.txt
```

Then run
```
python main.py
```
to execute the control program.

