#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Sistema de Reservaciones para un Hotel

from datetime import datetime, timedelta

# Clases de habitaciones con precios predefinidos
class Habitacion:
    def __init__(self, tipo, capacidad, precio):
        self.tipo = tipo
        self.capacidad = capacidad
        self.precio = precio

class HabitacionDoble(Habitacion):
    def __init__(self):
        super().__init__("Habitacion Doble", 2, 900.00)

class Suite(Habitacion):
    def __init__(self):
        super().__init__("Suite", 4, 2000.00)

# Clase Cliente
class Cliente:
    def __init__(self, nombre, correo):
        self.nombre = nombre
        self.correo = correo
        self.reservas = []

# Clase Reserva
class Reserva:
    def __init__(self, cliente, habitaciones, fecha_inicio, noches):
        self.cliente = cliente
        self.habitaciones = habitaciones
        self.fecha_inicio = datetime.strptime(fecha_inicio, "%d-%m-%Y")
        self.fecha_fin = self.fecha_inicio + timedelta(days=noches)
        self.noches = noches

    def calcular_total(self):
        return sum(h.precio for h in self.habitaciones)

    def generar_resumen(self):
        total_habitaciones = len(self.habitaciones)
        total_personas = sum(h.capacidad for h in self.habitaciones)
        total_precio = self.calcular_total()

        detalles_precio = "\n".join(f"[1]  {h.tipo:<25} {h.precio:.2f}$" for h in self.habitaciones)

        resumen = f"""¡Hola {self.cliente.nombre}! aqui tienes los detalles de tu reserva:

Check-in:    {self.fecha_inicio.strftime('%d-%m-%Y')}
Check out:   {self.fecha_fin.strftime('%d-%m-%Y')}

Reservaste   [{self.noches}] noches, [{total_habitaciones}] habitaciones, [{total_personas}] personas

Detalles de reserva
""" + "\n".join(f"[1]  {h.tipo}" for h in self.habitaciones) + f"""

E-mail de contacto   [{self.cliente.correo}]

Detalles del precio:
{detalles_precio}
----------------------------------------------
Total:                           {total_precio:.2f}$"""

        return resumen

    def guardar_resumen(self, archivo_salida="output.txt"):
        with open(archivo_salida, "w", encoding="utf-8") as file:
            file.write(self.generar_resumen())
        print("Archivo de salida generado: output.txt")



def parser(documento):
    with open(documento, "r", encoding="utf-8") as file:
        lineas = [line.strip() for line in file if line.strip()]  # Elimina espacios en blanco extra

    cliente = None
    nombre = correo = fecha_inicio = ""
    noches = 0
    habitaciones = []

    flag_nombre = False
    flag_habitaciones = False

    for linea in lineas:
        if flag_nombre:
            nombre = linea
            flag_nombre = False
        elif "Nombre del cliente" in linea:
            flag_nombre = True
        elif "correo" in linea:
            correo = lineas[lineas.index(linea) + 1]
        elif "numero de noches" in linea:
            try:
                # Verifica si la línea siguiente es el número de noches
                noches = int(lineas[lineas.index(linea) + 1].strip())  # Elimina cualquier espacio extra
            except ValueError:
                print(f"Error al leer el número de noches en la línea: {linea}")
        elif "fecha inicio" in linea:
            try:
                
                fecha_inicio = lineas[lineas.index(linea) + 1].strip()  
        
                datetime.strptime(fecha_inicio, "%d-%m-%Y")  
            except (IndexError, ValueError):
                print(f"Error al leer la fecha en la línea: {linea}")
        elif "habitacion doble" in linea.lower():
            habitaciones.append(HabitacionDoble())
        elif "suite" in linea.lower():
            habitaciones.append(Suite())

    if nombre and correo and fecha_inicio and noches > 0 and habitaciones:
        cliente = Cliente(nombre, correo)
        return Reserva(cliente, habitaciones, fecha_inicio, noches)
    else:
        raise ValueError("Error en el input.txt: Faltan datos importantes.")


try:
    reserva = parser("reserva.txt")
    reserva.guardar_resumen()
except Exception as e:
    print(e)


