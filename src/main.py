import tkinter as tk
from tkinter import ttk

def show_text():
    input_text = text_field.get("1.0", tk.END)  # Obtener todo el texto del campo de texto
    lines = input_text.strip().split("\n")  # Dividir el texto en líneas
    
    if len(lines) < 2:
        output_text_field.config(state=tk.NORMAL)
        output_text_field.delete("1.0", tk.END)
        output_text_field.insert(tk.END, "Error: Debe ingresar al menos dos líneas para N y M.\n")
        output_text_field.config(state=tk.DISABLED)
        return
    
    try:
        N = int(lines[0])  # Cantidad de químicos a la venta
        M = int(lines[1])  # Cantidad de materias primas del problema
        if N < 0 or M < 0:
            raise ValueError
    except ValueError:
        output_text_field.config(state=tk.NORMAL)
        output_text_field.delete("1.0", tk.END)
        output_text_field.insert(tk.END, "Error: Las primeras dos líneas deben ser enteros no negativos.\n")
        output_text_field.config(state=tk.DISABLED)
        return
    
    if len(lines) < 2 + N + M:
        output_text_field.config(state=tk.NORMAL)
        output_text_field.delete("1.0", tk.END)
        output_text_field.insert(tk.END, "Error: No hay suficientes líneas para los productos y materias primas.\n")
        output_text_field.config(state=tk.DISABLED)
        return
    
    productos = []
    numero_producto = dict()
    for i in range(2, 2 + N):
        partes = lines[i].split()
        if len(partes) != 2 + M:
            output_text_field.config(state=tk.NORMAL)
            output_text_field.delete("1.0", tk.END)
            output_text_field.insert(tk.END, f"Error: La línea {i + 1} no tiene el formato correcto para un producto.\n")
            output_text_field.config(state=tk.DISABLED)
            return
        nombre = partes[0]
        try:
            precio = int(partes[1])
            cantidades = list(map(int, partes[2:]))
            if precio < 0 or any(cantidad < 0 for cantidad in cantidades):
                raise ValueError
        except ValueError:
            output_text_field.config(state=tk.NORMAL)
            output_text_field.delete("1.0", tk.END)
            output_text_field.insert(tk.END, f"Error: La línea {i + 1} contiene valores no enteros o negativos.\n")
            output_text_field.config(state=tk.DISABLED)
            return
        productos.append((nombre, precio, cantidades))
        numero_producto[nombre] = i - 1
    
    materias_primas = []
    for i in range(2 + N, 2 + N + M):
        partes = lines[i].split()
        if len(partes) != 3:
            output_text_field.config(state=tk.NORMAL)
            output_text_field.delete("1.0", tk.END)
            output_text_field.insert(tk.END, f"Error: La línea {i + 1} no tiene el formato correcto para una materia prima.\n")
            output_text_field.config(state=tk.DISABLED)
            return
        nombre = partes[0]
        try:
            costo = int(partes[1])
            disponibilidad = int(partes[2])
            if costo < 0 or disponibilidad < 0:
                raise ValueError
        except ValueError:
            output_text_field.config(state=tk.NORMAL)
            output_text_field.delete("1.0", tk.END)
            output_text_field.insert(tk.END, f"Error: La línea {i + 1} contiene valores no enteros o negativos.\n")
            output_text_field.config(state=tk.DISABLED)
            return
        materias_primas.append((nombre, costo, disponibilidad))
    
    restricciones = {}
    for i in range(2 + N + M, len(lines)):
        partes = lines[i].split()
        if len(partes) != 3:
            output_text_field.config(state=tk.NORMAL)
            output_text_field.delete("1.0", tk.END)
            output_text_field.insert(tk.END, f"Error: La línea {i + 1} no tiene el formato correcto para una restricción.\n")
            output_text_field.config(state=tk.DISABLED)
            return
        nombre = partes[0]
        tipo = partes[1].lower()
        try:
            valor = int(partes[2])
            if valor < 0:
                raise ValueError
        except ValueError:
            output_text_field.config(state=tk.NORMAL)
            output_text_field.delete("1.0", tk.END)
            output_text_field.insert(tk.END, f"Error: La línea {i + 1} contiene valores no enteros o negativos.\n")
            output_text_field.config(state=tk.DISABLED)
            return
        if nombre not in restricciones:
            restricciones[nombre] = {}
        if tipo in restricciones[nombre]:
            output_text_field.config(state=tk.NORMAL)
            output_text_field.delete("1.0", tk.END)
            output_text_field.insert(tk.END, f"Error: La restricción de {nombre} tiene más de un valor {tipo}.\n")
            output_text_field.config(state=tk.DISABLED)
            return
        restricciones[nombre][tipo] = valor
    
    # Validar que el mínimo sea menor que el máximo
    for nombre, restriccion in restricciones.items():
        if "minimo" in restriccion and "maximo" in restriccion:
            if restriccion["minimo"] > restriccion["maximo"]:
                output_text_field.config(state=tk.NORMAL)
                output_text_field.delete("1.0", tk.END)
                output_text_field.insert(tk.END, f"Error: El valor mínimo para {nombre} es mayor que el valor máximo.\n")
                output_text_field.config(state=tk.DISABLED)
                return
    
    output_text_field.config(state=tk.NORMAL)  # Habilitar edición temporalmente
    output_text_field.delete("1.0", tk.END)  # Limpiar el campo de texto de salida
    
    output_text_field.insert(tk.END, f"N (Cantidad de químicos): {N}\n")
    output_text_field.insert(tk.END, f"M (Cantidad de materias primas): {M}\n")
    
    output_text_field.insert(tk.END, "Código\n\n")
    output_text_field.insert(tk.END, "var int: z;\n") # declaración de la variable que almacena la función objetivo
    
    for i in range(N): # declaración de variables
        output_text_field.insert(tk.END, f"var int: x{i+1}; % {productos[i][0]}\n")
    
    output_text_field.insert(tk.END, "\n")
    Z = "constraint z = "
    for i in range(N):
        Z += f"{productos[i][1]} * x{i+1} + "
    Z = Z[:-3] + ";" # muestra la función objetivo
    
    output_text_field.insert(tk.END, f"\n{Z}\n\n")
    
    output_text_field.insert(tk.END, "\n")
    
    for i in range(N):
        output_text_field.insert(tk.END, f"constraint x{i+1} >= 0;\n") # restricciones de No negatividad
    
    output_text_field.insert(tk.END, "\n")
    
    for j in range(M): # muestra las restricciones de disponibilidad de las materias primas
        rest = "constraint "
        for i in range(N):
            rest += f"{productos[i][2][j]}*x{i+1} + "
        rest = rest[:-3] + f" <= {materias_primas[j][2]};\n"
        output_text_field.insert(tk.END, rest)
    
    output_text_field.insert(tk.END, "\n")
        
    # demandas minimas y máximas
    for restriccion in restricciones:
        if "minimo" in restricciones[restriccion]:
            output_text_field.insert(tk.END, f"constraint x{numero_producto[restriccion]} >= {restricciones[restriccion]['minimo']};\n")
        if "maximo" in restricciones[restriccion]:
            output_text_field.insert(tk.END, f"constraint x{numero_producto[restriccion]} <= {restricciones[restriccion]['maximo']};\n")
    
    
    output_text_field.insert(tk.END, "\n")
    
    output_text_field.insert(tk.END, "solve maximize z;\n")
    
    output_text_field.insert(tk.END, "\n")
    
    result = ""
    for i in range(N):
        result += f'"\\n{productos[i][0]}=", show(x{i+1}), '
    result = result[:-2]
    output_text_field.insert(tk.END, f"output[{result}];\n\n")
    
    output_text_field.insert(tk.END, 'output["\\nZ= ",show(z)];\n')
    output_text_field.insert(tk.END, "\n")
    
    output_text_field.config(state=tk.DISABLED)  # Deshabilitar edición

# creo la ventana
root = tk.Tk()
root.title("Ingrese los datos")

# creo un campo de texto
text_field = tk.Text(root, width=100, height=12)
text_field.pack(pady=10)

# creo una botón para mostrar el texto
show_button = ttk.Button(root, text="Mostrar texto", command=show_text)
show_button.pack(pady=10)

# creo un campo de texto para mostrar el texto resultante
output_text_field = tk.Text(root, width=100, height=12, state=tk.DISABLED)
output_text_field.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()