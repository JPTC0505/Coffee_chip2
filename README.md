# ☕ Coffee Chip: ASIC Coffee Bean Quality Classifier

![License](https://img.shields.io/badge/license-Apache--2.0-blue)
![GDS](https://img.shields.io/badge/GDS-Generated-green)
![Status](https://img.shields.io/badge/Status-Verified-success)

## Overview
The **Coffee Chip** is a dedicated hardware classifier designed for the coffee industry. It processes real-time data from a color-to-frequency sensor (TCS3200) to categorize coffee beans into three stages: **Unripe, Optimal, or Overripe**. 

Unlike software-based solutions running on general-purpose microcontrollers, this ASIC implements the classification logic directly in digital gates, ensuring high speed, low power consumption, and deterministic latency.

---

## 🛠 How it Works

The chip operates as a specialized frequency processor and comparison engine:

### 1. Frequency-to-Digital Conversion
The sensor sends a square wave where the frequency is proportional to light intensity. The chip uses a **26-bit internal counter** to measure the number of pulses within a precise time window.

### 2. Multi-Channel Processing
Using a Finite State Machine (FSM), the chip cycles through different color filters:
* **Red Filter:** To detect the ripeness levels.
* **Green Filter:** To detect chlorogenic acids and unripe traits.

### 3. Classification Logic
The measured frequencies are compared against programmable or static thresholds:
* **Greenish (Unripe):** High green component.
* **Bright Red (Optimal):** High red component with low green ratio.
* **Dark/Black (Overripe):** Low frequency across all channels (low reflection).

### 4. Configuration Modes
* **Static Mode:** Uses physical pins to select between common pre-set coffee varieties.
* **Dynamic Mode:** Features a **UART Receiver** allowing a master controller to update thresholds on-the-fly to adapt to different coffee species (Arabica vs. Robusta) or roasting levels.

---

## 🚀 How to Test

Follow these steps to verify the chip's functionality:

1.  **Hardware Connection:**
    * Connect a **50 MHz** clock to the `clk` pin.
    * Connect the **TCS3200 sensor's OUT** pin to `ui[0]`.
    * Connect `uo[0:3]` to the sensor's control pins (S0-S3) for automatic filter switching.
2.  **Reset:** Pull `rst_n` low for at least 10 cycles to clear internal counters and reset the FSM.
3.  **Operation:**
    * Place a coffee bean sample in front of the sensor.
    * Observe the output pins `uo[4:6]` which correspond to the classification LEDs.
4.  **Verification:**
    * **Optimal Bean:** LED at `uo[5]` should light up.
    * **Unripe Bean:** LED at `uo[4]` should light up.
    * **Overripe/Empty:** LED at `uo[6]` should light up.

---

## 🔌 External Hardware

To build a complete sorting machine, you will need:

| Component | Purpose | Connection |
|-----------|---------|------------|
| **TCS3200** | Color-to-Frequency Sensor | `ui[0]` (Input) & `uo[0:3]` (Control) |
| **LED Array** | Visual Indicators | `uo[4]`, `uo[5]`, `uo[6]` |
| **UART Bridge** | Threshold Calibration | `ui[1]` |
| **Logic Analyzer**| Signal Debugging | Monitor `uo[7]` (Cycle Done pulse) |

---

## 📁 Project Structure

* `/src`: Contains the Verilog source code, including the UART receiver, frequency counter, and the top-level module.
* `/test`: Python testbench using Cocotb for automated verification.
* `/docs`: Detailed technical documentation and GDS renders.

---
## Hardware Interface and Pinout

The following diagram illustrates the physical connection between the Coffee Chip ASIC and the external sensing/actuation hardware.

```text
               __________________________________________
              |                                          |
              |            COFFEE CHIP (ASIC)            |
              |__________________________________________|
              |                    |                     |
   [ INPUTS ] |     PIN NAME       |      PIN NAME       | [ OUTPUTS ]
   -----------|--------------------|---------------------|------------
    50MHz CLK |--> [clk]           |            [uo_0] --|--> Sensor S2
    Active L  |--> [rst_n]         |            [uo_1] --|--> Sensor S3
   Sensor OUT |--> [ui_0] (Input)  |            [uo_2] --|--> Sensor S0
    UART RX   |--> [ui_1] (Config) |            [uo_3] --|--> Sensor S1
              |                    |            [uo_4] --|--> LED Unripe
              |                    |            [uo_5] --|--> LED Optimal
              |                    |            [uo_6] --|--> LED Overripe
              |                    |            [uo_7] --|--> Sync Pulse
   -----------|--------------------|---------------------|------------
              |____________________|_____________________|
                        |                    |
                 [ COLOR SENSOR ]      [ INDICATORS ]
                 (TCS3200 / RGB)       (LEDs / Relay)

## 📐 Implementation Details

* **Process:** Sky130 PDK (130nm) via TinyTapeout.
* **Clock Frequency:** Optimized for 50 MHz.
* **Interface:** Standard PMOD-compatible IO mapping.

---
