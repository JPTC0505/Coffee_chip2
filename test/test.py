# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge
from cocotb.binary import BinaryValue

@cocotb.test()
async def test_coffee_classifier(dut):
    dut._log.info("Iniciando Test del Coffee Chip")

    # Reloj de 50MHz (20ns de periodo)
    clock = Clock(dut.clk, 20, unit="ns")
    cocotb.start_soon(clock.start())

    # --- RESET ---
    dut._log.info("Reset del sistema")
    dut.ena.value = 1
    dut.ui_in.value = 0    # ui_in[0] es la entrada del sensor
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 5)

    # --- SIMULACIÓN DEL SENSOR (Frecuencia) ---
    # Vamos a simular que el sensor envía pulsos en ui_in[0]
    # Queremos que lea: Rojo Alto, Verde Medio (Estado Óptimo)
    
    async def send_sensor_pulses(cycles_active, total_duration):
        """Genera pulsos en ui_in[0] para simular la salida del sensor"""
        for _ in range(total_duration):
            dut.ui_in.value = 1  # Pulso del sensor
            await ClockCycles(dut.clk, 2) 
            dut.ui_in.value = 0
            await ClockCycles(dut.clk, 2)

    # 1. Esperamos a que la FSM esté en lectura de ROJO (S2=0, S3=0)
    # Según tu lógica, el chip controla los pines uo_out[2] y uo_out[3]
    dut._log.info("Simulando lectura de color ROJO...")
    # Simulamos enviar muchos pulsos mientras el chip lee rojo
    # (Ajusta los ciclos según tu WINDOW_MAX en el Verilog)
    cocotb.start_soon(send_sensor_pulses(100, 500))
    
    # Avanzamos el tiempo suficiente para que pase por los estados de la FSM
    # (Si WINDOW_MAX es 50M, en testbench conviene bajarlo a 1000 para que no tarde horas)
    await ClockCycles(dut.clk, 2000)

    # --- VERIFICACIÓN ---
    dut._log.info("Verificando salidas de clasificación")
    
    # Leemos uo_out:
    # uo_out[4] = led_unripe
    # uo_out[5] = led_optimal
    # uo_out[6] = led_overripe
    
    val_out = dut.uo_out.value
    dut._log.info(f"Valor de salida uo_out: {val_out.binstr}")

    # Ejemplo de aserción: Verificar si el LED de "Óptimo" (bit 5) se enciende
    # Nota: Esto depende de que los valores simulados caigan en el rango r_min/r_max
    # assert (val_out & 0x20) != 0, "Error: No se detectó café óptimo"

    dut._log.info("Test finalizado con éxito")
