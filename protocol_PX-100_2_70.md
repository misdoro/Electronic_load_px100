# PX-100 ELECTRONIC LOAD


This document applies to PX-100 Electronic load version 2.70 with rs-232 TTL serial interface.

# Electrical diagram

Any USB TTL Serial adapter should do. Both 3.3V and 5V IO levels work. I used FT232 adapter from A.


| LOAD | RS-232 TTL adapter |
| -- | -- |
| GND | GND |
| TXD | RXD |
| RXD | TXD |

# Connection settings

Electronic load uses 9600 baud 8N1 (8 bits, no parity, 1 stop bit) configuration with no flow control.

# Binary protocol

Electronic load uses a binary protocol with 7-bytes control frames sent by host and either 1 or 7 bytes response frames. All other data is ignored, until the next command is received.
No line end characters is sent or expected.

The control frame looks like:
```
  0xB1 0xB2 CMD D1 D2 0xB3 0xB4
```

with 2 header bytes `0xB1 0xB2` and 2 trailing bytes `0xB3 0xB4`

Data format of control commands differs from the query commands.

## Control commands
Control commands start with `0x0*` and the unit responds with 1 byte `0x6F`

First data byte carries the integer part, second data byte carries a fraction * 100

So 1.23 V will be tranmitted as 0x01 0x17 hexadecimal.

| Command | Data | Description |
| -- | -- | -- |
| 0x01 | 0x0100 - ON \ 0x0000 OFF | Enable or disable the load 
| 0x02 | D1.D2  | Set cutoff voltage
| 0x03 | D1.D2  | Set current
| 0x04 | 16-bit unsigned integer | Set timeout in seconds
| 0x05 | 0x0000 | Reset counters


## Query commands
Query commands start with `0x1*` and the unit responds with 7 bytes:

```
  0xCA 0xCB D1 D2 D3 0xCE 0xCF
```
Request data bytes should be send as 0x00.

Response data format varies.

| Command | Response Data | Description |
| -- | -- | --
| 0x10 | 0x000000 OFF 0x000001 ON | Load enabled ?
| 0x11 | 24-bit integer | Voltage reading, mV
| 0x12 | 24-bit integer | Current reading, mA
| 0x13 | D1 hours, D2 minutes, D3 seconds | Elapsed or remaining time
| 0x14 | 24-bit integer | Capacity, mAH
| 0x15 | 24-bit integer | Capacity, mWH
| 0x16 | 24-bit integer | Mosfet temperature, °C
| 0x17 | 24-bit integer | Current setting, AH * 100, 1.23A would be sent as 123
| 0x18 | 24-bit integer | Cutoff voltage setting, V*100, 3.21V will be sent as 321
| 0x19 | D1 hours, D2 minutes, D3 seconds | Timer setting

