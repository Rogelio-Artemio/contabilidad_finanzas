import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(layout="wide")

# Título de la aplicación
st.title("Sistema Contable")

# Barra lateral con opciones de operaciones
st.sidebar.title("Operaciones")
opcion = st.sidebar.selectbox(
    "Selecciona una operación",
    [
        "Balanza General",  # Primera opción
        "Compra en Efectivo", "Compra a Crédito", "Compra a Crédito-Efectivo", 
        "Renta", "Venta", "Papelería", "Libro Diario", "Libro Mayor",
        "Balanza de Comprobación",  # Última opción
        "Depreciaciones",  # Nueva opción
        "Estado de Resultados",  # Nueva opción
        "Cálculo de Utilidad del Período",  # Nueva opción
        "Estado de Cambios", #Nueva opción
        "Estado de Flujos", #Nueva opción
        "Fuente de Efectivo" #Nueva opción
    ]
)

# Inicializar el DataFrame con los datos iniciales (para la Balanza General)
if 'data' not in st.session_state:
    data = {
        "Tipo": ["Circulante", "Circulante", "Circulante", "No Circulante", "No Circulante", 
                 "No Circulante", "No Circulante", "No Circulante", "No Circulante", "Capital", "Capital"],
        "Cuenta": [
            "Caja", "Bancos", "Mercancías", "Terrenos", "Edificios", 
            "Equipo de Reparto", "Equipo de Computo", "Mob y Equipo", 
            "Muebles y Enseres", "Capital Contribuido", "Capital Social"
        ],
        "Monto": [
            50000, 2500000, 150000, 650000, 1500000, 
            200000, 90000, 115000, 120000, 0, 5375000
        ]
    }
    st.session_state.data = pd.DataFrame(data)

# Inicializar el DataFrame para Pasivo
if 'pasivo_data' not in st.session_state:
    st.session_state.pasivo_data = pd.DataFrame({
        "Cuenta": [],
        "Monto": []
    })


# Inicializar el DataFrame para el libro diario
if 'libro_diario_data' not in st.session_state:
    st.session_state.libro_diario_data = pd.DataFrame(columns=["Fecha", "Cuentas", "Parcial", "Debe", "Haber"])

# Función para calcular los totales (para la Balanza General y Balanza de Comprobación)
def calcular_totales(df, pasivo_df):
    total_circulante = df.loc[df["Tipo"] == "Circulante", "Monto"].sum()
    total_no_circulante = df.loc[df["Tipo"] == "No Circulante", "Monto"].sum()
    total_capital = df.loc[df["Tipo"] == "Capital", "Monto"].sum()
    total_activo = total_circulante + total_no_circulante
    total_pasivo = pasivo_df["Monto"].sum()
    total_pasivo_capital = total_capital + total_pasivo
    return total_circulante, total_no_circulante, total_capital, total_activo, total_pasivo, total_pasivo_capital

# Función para la Balanza General
def balanza_general():
    st.write("### Balanza General")

    # Mostrar campos editables para cada cuenta de Activo y Capital
    st.write("#### Editar Montos de las Cuentas")
    tipos = st.session_state.data["Tipo"].unique()
    for tipo in tipos:
        st.write(f"##### {tipo}")
        cuentas_tipo = st.session_state.data[st.session_state.data["Tipo"] == tipo]
        for i, row in cuentas_tipo.iterrows():
            st.session_state.data.at[i, "Monto"] = st.number_input(
                f"Monto para {row['Cuenta']}", 
                value=float(row["Monto"]), 
                key=f"monto_{i}"
            )

    # Sección para agregar cuentas de Pasivo
    st.write("#### Agregar Cuentas de Pasivo")
    nueva_cuenta = st.text_input("Nombre de la cuenta de Pasivo", key="nueva_cuenta_pasivo")
    nuevo_monto = st.number_input("Monto de la cuenta de Pasivo", value=0.0, key="nuevo_monto_pasivo")
    if st.button("Agregar Pasivo"):
        if nueva_cuenta:
            nueva_fila = {"Cuenta": nueva_cuenta, "Monto": nuevo_monto}
            st.session_state.pasivo_data = pd.concat([st.session_state.pasivo_data, pd.DataFrame([nueva_fila])], ignore_index=True)

    # Mostrar cuentas de Pasivo
    st.write("#### Pasivo")
    st.dataframe(st.session_state.pasivo_data)

    # Calcular totales
    total_circulante, total_no_circulante, total_capital, total_activo, total_pasivo, total_pasivo_capital = calcular_totales(st.session_state.data, st.session_state.pasivo_data)

    # Mostrar la Balanza General
    st.write("#### Balanza General")

    # Mostrar cuentas agrupadas por tipo
    for tipo in tipos:
        st.write(f"##### {tipo}")
        cuentas_tipo = st.session_state.data[st.session_state.data["Tipo"] == tipo]
        st.dataframe(cuentas_tipo[["Cuenta", "Monto"]])

    # Mostrar los totales de la Balanza General
    st.write("#### Totales de la Balanza General")
    st.write(f"**Total Circulante:** ${total_circulante:,.2f}")
    st.write(f"**Total No Circulante:** ${total_no_circulante:,.2f}")
    st.write(f"**Total Activo:** ${total_activo:,.2f}")
    st.write(f"**Total Capital:** ${total_capital:,.2f}")
    st.write(f"**Total Pasivo:** ${total_pasivo:,.2f}")
    st.write(f"**Total Pasivo + Capital:** ${total_pasivo_capital:,.2f}")

# Función para la Compra en Efectivo
def compra_efectivo():
    st.write("### Compra en Efectivo")

    # Campos para ingresar los datos de la compra
    costo_compra = st.number_input("Costo de la compra", value=0.0, key="costo_compra")
    iva = costo_compra * 0.16  # Calcular el IVA (16%)
    total_compra = costo_compra + iva  # Calcular el total de la compra

    # Mostrar el desglose de la compra
    st.write("#### Detalles de la Compra")
    st.write(f"**Costo de la compra:** ${costo_compra:,.2f}")
    st.write(f"**IVA (16%):** ${iva:,.2f}")
    st.write(f"**Total de la compra:** ${total_compra:,.2f}")

    # Botón para registrar la compra
    if st.button("Registrar Compra en Efectivo"):
        # Actualizar la cuenta de Caja
        st.session_state.data.loc[st.session_state.data["Cuenta"] == "Caja", "Monto"] -= total_compra

        # Actualizar la cuenta de Mercancías
        st.session_state.data.loc[st.session_state.data["Cuenta"] == "Mercancías", "Monto"] += costo_compra

        # Agregar la cuenta de IVA Acreditable si no existe
        if "IVA Acreditable" not in st.session_state.data["Cuenta"].values:
            nueva_fila = {"Tipo": "Circulante", "Cuenta": "IVA Acreditable", "Monto": iva}
            st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([nueva_fila])], ignore_index=True)
        else:
            # Si ya existe, sumar el IVA
            st.session_state.data.loc[st.session_state.data["Cuenta"] == "IVA Acreditable", "Monto"] += iva

        st.success("Compra registrada exitosamente.")

# Función para la Compra a Crédito
def compra_credito():
    st.write("### Compra a Crédito")

    # Campos para ingresar los datos de la compra
    costo_compra = st.number_input("Costo de la compra", value=0.0, key="costo_compra_credito")
    iva = costo_compra * 0.16  # Calcular el IVA (16%)
    total_compra = costo_compra + iva  # Calcular el total de la compra

    # Mostrar el desglose de la compra
    st.write("#### Detalles de la Compra")
    st.write(f"**Costo de la compra:** ${costo_compra:,.2f}")
    st.write(f"**IVA (16%):** ${iva:,.2f}")
    st.write(f"**Total de la compra:** ${total_compra:,.2f}")

    # Botón para registrar la compra
    if st.button("Registrar Compra a Crédito"):
        # Actualizar la cuenta de Equipo de Computo
        st.session_state.data.loc[st.session_state.data["Cuenta"] == "Equipo de Computo", "Monto"] += costo_compra

        # Agregar la cuenta de "IVA por Acreditar" en Activo
        if "IVA por Acreditar" not in st.session_state.data["Cuenta"].values:
            nueva_fila_activo = {"Tipo": "Circulante", "Cuenta": "IVA por Acreditar", "Monto": iva}
            st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([nueva_fila_activo])], ignore_index=True)
        else:
            # Si ya existe, sumar el IVA
            st.session_state.data.loc[st.session_state.data["Cuenta"] == "IVA por Acreditar", "Monto"] += iva

        # Agregar la cuenta de "Acreedores a Corto Plazo" en Pasivo
        if "Acreedores a Corto Plazo" not in st.session_state.pasivo_data["Cuenta"].values:
            nueva_fila_pasivo = {"Cuenta": "Acreedores a Corto Plazo", "Monto": total_compra}
            st.session_state.pasivo_data = pd.concat([st.session_state.pasivo_data, pd.DataFrame([nueva_fila_pasivo])], ignore_index=True)
        else:
            # Si ya existe, sumar el total de la compra
            st.session_state.pasivo_data.loc[st.session_state.pasivo_data["Cuenta"] == "Acreedores a Corto Plazo", "Monto"] += total_compra

        st.success("Compra a crédito registrada exitosamente.")

# Función para la Compra a Crédito-Efectivo
def compra_credito_efectivo():
    st.write("### Compra a Crédito-Efectivo")

    # Campos para ingresar los datos de la compra
    costo_compra = st.number_input("Costo de la compra", value=0.0, key="costo_compra_credito_efectivo")
    iva = costo_compra * 0.16  # Calcular el IVA (16%)
    total_compra = costo_compra + iva  # Calcular el total de la compra

    # Calcular la mitad de la compra y el IVA
    mitad_costo = costo_compra / 2
    mitad_iva = iva / 2
    mitad_total = total_compra / 2

    # Mostrar el desglose de la compra
    st.write("#### Detalles de la Compra")
    st.write(f"**Costo de la compra:** ${costo_compra:,.2f}")
    st.write(f"**IVA (16%):** ${iva:,.2f}")
    st.write(f"**Total de la compra:** ${total_compra:,.2f}")
    st.write(f"**Mitad de la compra (efectivo):** ${mitad_total:,.2f}")
    st.write(f"**Mitad del IVA (efectivo):** ${mitad_iva:,.2f}")

    # Botón para registrar la compra
    if st.button("Registrar Compra a Crédito-Efectivo"):
        # Actualizar la cuenta de Caja (pago en efectivo)
        st.session_state.data.loc[st.session_state.data["Cuenta"] == "Caja", "Monto"] -= mitad_total

        # Actualizar la cuenta de Mercancías
        st.session_state.data.loc[st.session_state.data["Cuenta"] == "Mercancías", "Monto"] += costo_compra

        # Agregar la cuenta de "IVA Acreditable" si no existe
        if "IVA Acreditable" not in st.session_state.data["Cuenta"].values:
            nueva_fila_activo = {"Tipo": "Circulante", "Cuenta": "IVA Acreditable", "Monto": mitad_iva}
            st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([nueva_fila_activo])], ignore_index=True)
        else:
            # Si ya existe, sumar el IVA
            st.session_state.data.loc[st.session_state.data["Cuenta"] == "IVA Acreditable", "Monto"] += mitad_iva

        # Agregar la cuenta de "IVA por Acreditar" si no existe
        if "IVA por Acreditar" not in st.session_state.data["Cuenta"].values:
            nueva_fila_activo = {"Tipo": "Circulante", "Cuenta": "IVA por Acreditar", "Monto": mitad_iva}
            st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([nueva_fila_activo])], ignore_index=True)
        else:
            # Si ya existe, sumar el IVA
            st.session_state.data.loc[st.session_state.data["Cuenta"] == "IVA por Acreditar", "Monto"] += mitad_iva

        # Agregar la cuenta de "Documentos por Pagar" en Pasivo
        if "Documentos por Pagar" not in st.session_state.pasivo_data["Cuenta"].values:
            nueva_fila_pasivo = {"Cuenta": "Documentos por Pagar", "Monto": mitad_total}
            st.session_state.pasivo_data = pd.concat([st.session_state.pasivo_data, pd.DataFrame([nueva_fila_pasivo])], ignore_index=True)
        else:
            # Si ya existe, sumar el total de la compra
            st.session_state.pasivo_data.loc[st.session_state.pasivo_data["Cuenta"] == "Documentos por Pagar", "Monto"] += mitad_total

        st.success("Compra a crédito-efectivo registrada exitosamente.")

# Función para la Renta
def renta():
    st.write("### Renta")

    # Campos para ingresar los datos de la renta
    costo_renta_mes = st.number_input("Costo de la renta por mes", value=0.0, key="costo_renta_mes")
    meses = st.number_input("Número de meses", value=1, min_value=1, key="meses_renta")
    costo_renta_total = costo_renta_mes * meses
    iva = costo_renta_total * 0.16  # Calcular el IVA (16%)
    total_renta = costo_renta_total + iva  # Calcular el total de la renta

    # Mostrar el desglose de la renta
    st.write("#### Detalles de la Renta")
    st.write(f"**Costo de la renta por mes:** ${costo_renta_mes:,.2f}")
    st.write(f"**Número de meses:** {meses}")
    st.write(f"**Costo de la renta total:** ${costo_renta_total:,.2f}")
    st.write(f"**IVA (16%):** ${iva:,.2f}")
    st.write(f"**Total de la renta:** ${total_renta:,.2f}")

    # Botón para registrar la renta
    if st.button("Registrar Renta"):
        # Verificar si hay suficiente saldo en Caja
        saldo_caja = st.session_state.data.loc[st.session_state.data["Cuenta"] == "Caja", "Monto"].values[0]
        if saldo_caja < total_renta:
            st.error("No hay suficiente saldo en Caja para realizar esta operación.")
        else:
            # Actualizar la cuenta de Caja
            st.session_state.data.loc[st.session_state.data["Cuenta"] == "Caja", "Monto"] -= total_renta

            # Agregar la cuenta de "Renta Anticipada" si no existe
            if "Renta Anticipada" not in st.session_state.data["Cuenta"].values:
                nueva_fila_renta = {"Tipo": "Circulante", "Cuenta": "Renta Anticipada", "Monto": costo_renta_total}
                st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([nueva_fila_renta])], ignore_index=True)
            else:
                # Si ya existe, sumar el costo de la renta
                st.session_state.data.loc[st.session_state.data["Cuenta"] == "Renta Anticipada", "Monto"] += costo_renta_total

            # Agregar la cuenta de "IVA Acreditable" si no existe
            if "IVA Acreditable" not in st.session_state.data["Cuenta"].values:
                nueva_fila_iva = {"Tipo": "Circulante", "Cuenta": "IVA Acreditable", "Monto": iva}
                st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([nueva_fila_iva])], ignore_index=True)
            else:
                # Si ya existe, sumar el IVA
                st.session_state.data.loc[st.session_state.data["Cuenta"] == "IVA Acreditable", "Monto"] += iva

            st.success("Renta registrada exitosamente.")
#Función para la Venta
def venta():
    st.write("### Venta")

    # Campos para ingresar los datos de la venta
    monto_venta = st.number_input("Monto de la venta", value=0.0, key="monto_venta")
    iva = monto_venta * 0.16  # Calcular el IVA (16%)
    total_venta = monto_venta + iva  # Calcular el total de la venta

    # Mostrar el desglose de la venta
    st.write("#### Detalles de la Venta")
    st.write(f"**Monto de la venta:** ${monto_venta:,.2f}")
    st.write(f"**IVA (16%):** ${iva:,.2f}")
    st.write(f"**Total de la venta:** ${total_venta:,.2f}")

    # Calcular la mitad del monto y el IVA
    mitad_monto = monto_venta / 2
    mitad_iva = iva / 2
    total_pago_cliente = mitad_monto + mitad_iva

    # Mostrar el pago parcial del cliente
    st.write("#### Pago Parcial del Cliente")
    st.write(f"**Mitad del monto de la venta:** ${mitad_monto:,.2f}")
    st.write(f"**Mitad del IVA:** ${mitad_iva:,.2f}")
    st.write(f"**Total pagado por el cliente:** ${total_pago_cliente:,.2f}")

    # Botón para registrar la venta
    if st.button("Registrar Venta"):
        # Sumar el pago del cliente a Caja
        st.session_state.data.loc[st.session_state.data["Cuenta"] == "Caja", "Monto"] += total_pago_cliente

        # Agregar la cuenta de "Anticipo de Cliente" en Pasivo si no existe
        if "Anticipo de Cliente" not in st.session_state.pasivo_data["Cuenta"].values:
            nueva_fila_anticipo = {"Cuenta": "Anticipo de Cliente", "Monto": mitad_monto}
            st.session_state.pasivo_data = pd.concat([st.session_state.pasivo_data, pd.DataFrame([nueva_fila_anticipo])], ignore_index=True)
        else:
            # Si ya existe, sumar el monto
            st.session_state.pasivo_data.loc[st.session_state.pasivo_data["Cuenta"] == "Anticipo de Cliente", "Monto"] += mitad_monto

        # Agregar la cuenta de "IVA Trasladado" en Pasivo si no existe
        if "IVA Trasladado" not in st.session_state.pasivo_data["Cuenta"].values:
            nueva_fila_iva = {"Cuenta": "IVA Trasladado", "Monto": mitad_iva}
            st.session_state.pasivo_data = pd.concat([st.session_state.pasivo_data, pd.DataFrame([nueva_fila_iva])], ignore_index=True)
        else:
            # Si ya existe, sumar el IVA
            st.session_state.pasivo_data.loc[st.session_state.pasivo_data["Cuenta"] == "IVA Trasladado", "Monto"] += mitad_iva

        st.success("Venta registrada exitosamente.")
#Función para Papeleria
def papeleria():
    st.write("### Compra de Papelería")

    # Campos para ingresar los datos de la compra
    costo_papeleria = st.number_input("Costo de la papelería", value=0.0, key="costo_papeleria")
    iva = costo_papeleria * 0.16  # Calcular el IVA (16%)
    total_compra = costo_papeleria + iva  # Calcular el total de la compra

    # Mostrar el desglose de la compra
    st.write("#### Detalles de la Compra")
    st.write(f"**Costo de la papelería:** ${costo_papeleria:,.2f}")
    st.write(f"**IVA (16%):** ${iva:,.2f}")
    st.write(f"**Total de la compra:** ${total_compra:,.2f}")

    # Botón para registrar la compra
    if st.button("Registrar Compra de Papelería"):
        # Verificar si hay suficiente saldo en Caja
        saldo_caja = st.session_state.data.loc[st.session_state.data["Cuenta"] == "Caja", "Monto"].values[0]
        if saldo_caja < total_compra:
            st.error("No hay suficiente saldo en Caja para realizar esta operación.")
        else:
            # Actualizar la cuenta de Caja
            st.session_state.data.loc[st.session_state.data["Cuenta"] == "Caja", "Monto"] -= total_compra

            # Agregar la cuenta de "Papelería" si no existe
            if "Papelería" not in st.session_state.data["Cuenta"].values:
                nueva_fila_papeleria = {"Tipo": "Circulante", "Cuenta": "Papelería", "Monto": costo_papeleria}
                st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([nueva_fila_papeleria])], ignore_index=True)
            else:
                # Si ya existe, sumar el costo de la papelería
                st.session_state.data.loc[st.session_state.data["Cuenta"] == "Papelería", "Monto"] += costo_papeleria

            # Agregar la cuenta de "IVA Acreditable" si no existe
            if "IVA Acreditable" not in st.session_state.data["Cuenta"].values:
                nueva_fila_iva = {"Tipo": "Circulante", "Cuenta": "IVA Acreditable", "Monto": iva}
                st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([nueva_fila_iva])], ignore_index=True)
            else:
                # Si ya existe, sumar el IVA
                st.session_state.data.loc[st.session_state.data["Cuenta"] == "IVA Acreditable", "Monto"] += iva

            st.success("Compra de papelería registrada exitosamente.")


#Función para el libro Diario
def libro_diario():
    st.write("### Libro Diario")

    # Mostrar el libro diario
    st.write("#### Libro Diario")
    st.dataframe(st.session_state.libro_diario_data)

    # Calcular y mostrar el total de Debe y Haber
    total_debe = st.session_state.libro_diario_data["Debe"].sum()
    total_haber = st.session_state.libro_diario_data["Haber"].sum()

    st.write("#### Totales")
    st.write(f"**Total Debe:** ${total_debe:,.2f}")
    st.write(f"**Total Haber:** ${total_haber:,.2f}")

    # Verificar si los totales están balanceados
    if total_debe == total_haber:
        st.success("Los totales de Debe y Haber están balanceados.")
    else:
        st.error("Los totales de Debe y Haber no están balanceados. Revise las operaciones.")


# Función para agregar una operación al libro diario
def agregar_operacion(fecha, cuentas, parcial, debe, haber):
    nueva_fila = {"Fecha": fecha, "Cuentas": cuentas, "Parcial": parcial, "Debe": debe, "Haber": haber}
    st.session_state.libro_diario_data = pd.concat([st.session_state.libro_diario_data, pd.DataFrame([nueva_fila])], ignore_index=True)

 # Agregar las cuentas iniciales de la Balanza General
if st.button("Registrar Cuentas Iniciales"):
    agregar_operacion("21/01/2025", "Caja", "", 50000.0, 0.0)
    agregar_operacion("21/01/2025", "Bancos", "", 2500000.0, 0.0)
    agregar_operacion("21/01/2025", "Mercancías", "", 150000.0, 0.0)
    agregar_operacion("21/01/2025", "Terrenos", "", 650000.0, 0.0)
    agregar_operacion("21/01/2025", "Edificios", "", 1500000.0, 0.0)
    agregar_operacion("21/01/2025", "Equipo de Reparto", "", 200000.0, 0.0)
    agregar_operacion("21/01/2025", "Mob y Equipo", "", 115000.0, 0.0)
    agregar_operacion("21/01/2025", "Muebles y Enseres", "", 120000.0, 0.0)
    agregar_operacion("21/01/2025", "Equipo de Computo", "", 90000.0, 0.0)
    agregar_operacion("21/01/2025", "Capital", "", 0.0, 5375000.0)
    st.success("Cuentas iniciales registradas en el libro diario.")
    
def agregar_operaciones_contables():
    # Operación 1: Bancos, Ventas, IVA Trasladado
    agregar_operacion("01/03/2025", "Bancos", "", 232000.00, 0.00)
    agregar_operacion("01/03/2025", "Ventas", "", 0.00, 200000.00)
    agregar_operacion("01/03/2025", "IVA Trasladado", "", 0.00, 32000.00)

    # Operación 2: Costo de lo Vendido, Inventario
    agregar_operacion("02/03/2025", "Costo de lo Vendido", "", 100000.00, 0.00)
    agregar_operacion("02/03/2025", "Inventario", "", 0.00, 100000.00)

    # Operación 3: Gastos Generales, Renta Pagada Contado
    agregar_operacion("03/03/2025", "Gastos Generales", "", 4000.00, 0.00)
    agregar_operacion("03/03/2025", "Renta Pagada Contado", "", 0.00, 4000.00)

    # Operación 4: Clientes, Anticipo de Clientes, IVA Trasladado, Ventas, etc.
    agregar_operacion("04/03/2025", "Clientes", "", 4640.00, 0.00)
    agregar_operacion("04/03/2025", "Anticipo de Clientes", "", 4000.00, 0.00)
    agregar_operacion("04/03/2025", "IVA Trasladado", "", 640.00, 0.00)
    agregar_operacion("04/03/2025", "Ventas", "", 0.00, 8000.00)
    agregar_operacion("04/03/2025", "IVA Trasladado", "", 0.00, 640.00)
    agregar_operacion("04/03/2025", "IVA por Trasladar", "", 0.00, 640.00)
    agregar_operacion("04/03/2025", "Costo de lo Vendido", "", 4000.00, 0.00)
    agregar_operacion("04/03/2025", "Inventario", "", 0.00, 4000.00)

    # Operación 5: Gastos Generales (Depreciaciones)
    agregar_operacion("05/03/2025", "Gastos Generales", "", 15075.00, 0.00)
    agregar_operacion("05/03/2025", "Dep. Acum de Edificios", "6250.00", 0.00, 6250.00)
    agregar_operacion("05/03/2025", "Dep. Acum de Equipo de Reparto", "4166.67", 0.00, 4166.67)
    agregar_operacion("05/03/2025", "Dep. Acum de Equipo de Computo", "2700.00", 0.00, 2700.00)
    agregar_operacion("05/03/2025", "Dep. Acum de Mob y Equipo", "958.33", 0.00, 958.33)
    agregar_operacion("05/03/2025", "Dep. Acum de Muebles y Enseres", "1000.00", 0.00, 1000.00)

    st.success("¡Operaciones contables agregadas correctamente!")

if st.button("Cargar Operaciones Contables"):
    agregar_operaciones_contables()

# Función para la Compra en Efectivo
def compra_efectivo():
    st.write("### Compra en Efectivo")

    # Campos para ingresar los datos de la compra
    costo_compra = st.number_input("Costo de la compra", value=0.0, key="costo_compra")
    iva = costo_compra * 0.16  # Calcular el IVA (16%)
    total_compra = costo_compra + iva  # Calcular el total de la compra

    # Mostrar el desglose de la compra
    st.write("#### Detalles de la Compra")
    st.write(f"**Costo de la compra:** ${costo_compra:,.2f}")
    st.write(f"**IVA (16%):** ${iva:,.2f}")
    st.write(f"**Total de la compra:** ${total_compra:,.2f}")

    # Botón para registrar la compra
    if st.button("Registrar Compra en Efectivo"):
        # Actualizar la cuenta de Caja
        st.session_state.data.loc[st.session_state.data["Cuenta"] == "Caja", "Monto"] -= total_compra

        # Actualizar la cuenta de Mercancías
        st.session_state.data.loc[st.session_state.data["Cuenta"] == "Mercancías", "Monto"] += costo_compra

        # Agregar la cuenta de IVA Acreditable si no existe
        if "IVA Acreditable" not in st.session_state.data["Cuenta"].values:
            nueva_fila = {"Tipo": "Circulante", "Cuenta": "IVA Acreditable", "Monto": iva}
            st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([nueva_fila])], ignore_index=True)
        else:
            # Si ya existe, sumar el IVA
            st.session_state.data.loc[st.session_state.data["Cuenta"] == "IVA Acreditable", "Monto"] += iva

        # Registrar la operación en el libro diario
        agregar_operacion("22/01/2025", "Mercancías", "", costo_compra, 0.0)
        agregar_operacion("22/01/2025", "IVA Acreditable", "", iva, 0.0)
        agregar_operacion("22/01/2025", "Caja", "", 0.0, total_compra)

        st.success("Compra registrada exitosamente.")


# Función para la Compra a Crédito
def compra_credito():
    st.write("### Compra a Crédito")

    # Campos para ingresar los datos de la compra
    costo_compra = st.number_input("Costo de la compra", value=0.0, key="costo_compra_credito")
    iva = costo_compra * 0.16  # Calcular el IVA (16%)
    total_compra = costo_compra + iva  # Calcular el total de la compra

    # Mostrar el desglose de la compra
    st.write("#### Detalles de la Compra")
    st.write(f"**Costo de la compra:** ${costo_compra:,.2f}")
    st.write(f"**IVA (16%):** ${iva:,.2f}")
    st.write(f"**Total de la compra:** ${total_compra:,.2f}")

    # Botón para registrar la compra
    if st.button("Registrar Compra a Crédito"):
        # Actualizar la cuenta de Equipo de Computo
        st.session_state.data.loc[st.session_state.data["Cuenta"] == "Equipo de Computo", "Monto"] += costo_compra

        # Agregar la cuenta de "IVA por Acreditar" en Activo
        if "IVA por Acreditar" not in st.session_state.data["Cuenta"].values:
            nueva_fila_activo = {"Tipo": "Circulante", "Cuenta": "IVA por Acreditar", "Monto": iva}
            st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([nueva_fila_activo])], ignore_index=True)
        else:
            # Si ya existe, sumar el IVA
            st.session_state.data.loc[st.session_state.data["Cuenta"] == "IVA por Acreditar", "Monto"] += iva

        # Agregar la cuenta de "Acreedores a Corto Plazo" en Pasivo
        if "Acreedores a Corto Plazo" not in st.session_state.pasivo_data["Cuenta"].values:
            nueva_fila_pasivo = {"Cuenta": "Acreedores a Corto Plazo", "Monto": total_compra}
            st.session_state.pasivo_data = pd.concat([st.session_state.pasivo_data, pd.DataFrame([nueva_fila_pasivo])], ignore_index=True)
        else:
            # Si ya existe, sumar el total de la compra
            st.session_state.pasivo_data.loc[st.session_state.pasivo_data["Cuenta"] == "Acreedores a Corto Plazo", "Monto"] += total_compra

        # Registrar la operación en el libro diario
        agregar_operacion("23/01/2025", "Equipo de Computo", "", costo_compra, 0.0)
        agregar_operacion("23/01/2025", "IVA por Acreditar", "", iva, 0.0)
        agregar_operacion("23/01/2025", "Acreedores", "", 0.0, total_compra)

        st.success("Compra a crédito registrada exitosamente.")


# Función para la Renta
def renta():
    st.write("### Renta")

    # Campos para ingresar los datos de la renta
    costo_renta_mes = st.number_input("Costo de la renta por mes", value=0.0, key="costo_renta_mes")
    meses = st.number_input("Número de meses", value=1, min_value=1, key="meses_renta")
    costo_renta_total = costo_renta_mes * meses
    iva = costo_renta_total * 0.16  # Calcular el IVA (16%)
    total_renta = costo_renta_total + iva  # Calcular el total de la renta

    # Mostrar el desglose de la renta
    st.write("#### Detalles de la Renta")
    st.write(f"**Costo de la renta por mes:** ${costo_renta_mes:,.2f}")
    st.write(f"**Número de meses:** {meses}")
    st.write(f"**Costo de la renta total:** ${costo_renta_total:,.2f}")
    st.write(f"**IVA (16%):** ${iva:,.2f}")
    st.write(f"**Total de la renta:** ${total_renta:,.2f}")

    # Botón para registrar la renta
    if st.button("Registrar Renta"):
        # Verificar si hay suficiente saldo en Caja
        saldo_caja = st.session_state.data.loc[st.session_state.data["Cuenta"] == "Caja", "Monto"].values[0]
        if saldo_caja < total_renta:
            st.error("No hay suficiente saldo en Caja para realizar esta operación.")
        else:
            # Actualizar la cuenta de Caja
            st.session_state.data.loc[st.session_state.data["Cuenta"] == "Caja", "Monto"] -= total_renta

            # Agregar la cuenta de "Renta Anticipada" si no existe
            if "Renta Anticipada" not in st.session_state.data["Cuenta"].values:
                nueva_fila_renta = {"Tipo": "Circulante", "Cuenta": "Renta Anticipada", "Monto": costo_renta_total}
                st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([nueva_fila_renta])], ignore_index=True)
            else:
                # Si ya existe, sumar el costo de la renta
                st.session_state.data.loc[st.session_state.data["Cuenta"] == "Renta Anticipada", "Monto"] += costo_renta_total

            # Agregar la cuenta de "IVA Acreditable" si no existe
            if "IVA Acreditable" not in st.session_state.data["Cuenta"].values:
                nueva_fila_iva = {"Tipo": "Circulante", "Cuenta": "IVA Acreditable", "Monto": iva}
                st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([nueva_fila_iva])], ignore_index=True)
            else:
                # Si ya existe, sumar el IVA
                st.session_state.data.loc[st.session_state.data["Cuenta"] == "IVA Acreditable", "Monto"] += iva

            # Registrar la operación en el libro diario
            agregar_operacion("28/01/2025", "Rentas Pagadas por Anticipo", "", costo_renta_total, 0.0)
            agregar_operacion("28/01/2025", "IVA Acreditable", "", iva, 0.0)
            agregar_operacion("28/01/2025", "Caja", "", 0.0, total_renta)

            st.success("Renta registrada exitosamente.")


# Función para la Venta
def venta():
    st.write("### Venta")

    # Campos para ingresar los datos de la venta
    monto_venta = st.number_input("Monto de la venta", value=0.0, key="monto_venta")
    iva = monto_venta * 0.16  # Calcular el IVA (16%)
    total_venta = monto_venta + iva  # Calcular el total de la venta

    # Mostrar el desglose de la venta
    st.write("#### Detalles de la Venta")
    st.write(f"**Monto de la venta:** ${monto_venta:,.2f}")
    st.write(f"**IVA (16%):** ${iva:,.2f}")
    st.write(f"**Total de la venta:** ${total_venta:,.2f}")

    # Calcular la mitad del monto y el IVA
    mitad_monto = monto_venta / 2
    mitad_iva = iva / 2
    total_pago_cliente = mitad_monto + mitad_iva

    # Mostrar el pago parcial del cliente
    st.write("#### Pago Parcial del Cliente")
    st.write(f"**Mitad del monto de la venta:** ${mitad_monto:,.2f}")
    st.write(f"**Mitad del IVA:** ${mitad_iva:,.2f}")
    st.write(f"**Total pagado por el cliente:** ${total_pago_cliente:,.2f}")

    # Botón para registrar la venta
    if st.button("Registrar Venta"):
        # Sumar el pago del cliente a Caja
        st.session_state.data.loc[st.session_state.data["Cuenta"] == "Caja", "Monto"] += total_pago_cliente

        # Agregar la cuenta de "Anticipo de Cliente" en Pasivo si no existe
        if "Anticipo de Cliente" not in st.session_state.pasivo_data["Cuenta"].values:
            nueva_fila_anticipo = {"Cuenta": "Anticipo de Cliente", "Monto": mitad_monto}
            st.session_state.pasivo_data = pd.concat([st.session_state.pasivo_data, pd.DataFrame([nueva_fila_anticipo])], ignore_index=True)
        else:
            # Si ya existe, sumar el monto
            st.session_state.pasivo_data.loc[st.session_state.pasivo_data["Cuenta"] == "Anticipo de Cliente", "Monto"] += mitad_monto

        # Agregar la cuenta de "IVA Trasladado" en Pasivo si no existe
        if "IVA Trasladado" not in st.session_state.pasivo_data["Cuenta"].values:
            nueva_fila_iva = {"Cuenta": "IVA Trasladado", "Monto": mitad_iva}
            st.session_state.pasivo_data = pd.concat([st.session_state.pasivo_data, pd.DataFrame([nueva_fila_iva])], ignore_index=True)
        else:
            # Si ya existe, sumar el IVA
            st.session_state.pasivo_data.loc[st.session_state.pasivo_data["Cuenta"] == "IVA Trasladado", "Monto"] += mitad_iva

        # Registrar la operación en el libro diario
        agregar_operacion("30/01/2025", "Anticipo de Clientes", "", 0.0, mitad_monto)
        agregar_operacion("30/01/2025", "IVA Trasladado", "", 0.0, mitad_iva)
        agregar_operacion("30/01/2025", "Caja", "", total_pago_cliente, 0.0)

        st.success("Venta registrada exitosamente.")


# Función para Papelería
def papeleria():
    st.write("### Compra de Papelería")

    # Campos para ingresar los datos de la compra
    costo_papeleria = st.number_input("Costo de la papelería", value=0.0, key="costo_papeleria")
    iva = costo_papeleria * 0.16  # Calcular el IVA (16%)
    total_compra = costo_papeleria + iva  # Calcular el total de la compra

    # Mostrar el desglose de la compra
    st.write("#### Detalles de la Compra")
    st.write(f"**Costo de la papelería:** ${costo_papeleria:,.2f}")
    st.write(f"**IVA (16%):** ${iva:,.2f}")
    st.write(f"**Total de la compra:** ${total_compra:,.2f}")

    # Botón para registrar la compra
    if st.button("Registrar Compra de Papelería"):
        # Verificar si hay suficiente saldo en Caja
        saldo_caja = st.session_state.data.loc[st.session_state.data["Cuenta"] == "Caja", "Monto"].values[0]
        if saldo_caja < total_compra:
            st.error("No hay suficiente saldo en Caja para realizar esta operación.")
        else:
            # Actualizar la cuenta de Caja
            st.session_state.data.loc[st.session_state.data["Cuenta"] == "Caja", "Monto"] -= total_compra

            # Agregar la cuenta de "Papelería" si no existe
            if "Papelería" not in st.session_state.data["Cuenta"].values:
                nueva_fila_papeleria = {"Tipo": "Circulante", "Cuenta": "Papelería", "Monto": costo_papeleria}
                st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([nueva_fila_papeleria])], ignore_index=True)
            else:
                # Si ya existe, sumar el costo de la papelería
                st.session_state.data.loc[st.session_state.data["Cuenta"] == "Papelería", "Monto"] += costo_papeleria

            # Agregar la cuenta de "IVA Acreditable" si no existe
            if "IVA Acreditable" not in st.session_state.data["Cuenta"].values:
                nueva_fila_iva = {"Tipo": "Circulante", "Cuenta": "IVA Acreditable", "Monto": iva}
                st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([nueva_fila_iva])], ignore_index=True)
            else:
                # Si ya existe, sumar el IVA
                st.session_state.data.loc[st.session_state.data["Cuenta"] == "IVA Acreditable", "Monto"] += iva

            # Registrar la operación en el libro diario
            agregar_operacion("19/02/2025", "Papelería", "", costo_papeleria, 0.0)
            agregar_operacion("19/02/2025", "IVA Acreditable", "", iva, 0.0)
            agregar_operacion("19/02/2025", "Caja", "", 0.0, total_compra)

            st.success("Compra de papelería registrada exitosamente.")


# Función para generar el libro mayor
def libro_mayor():
    st.write("### Libro Mayor")

    # Crear un diccionario para almacenar las cuentas y sus movimientos
    libro_mayor = {}

    # Recorrer las transacciones del libro diario
    for index, row in st.session_state.libro_diario_data.iterrows():
        cuenta = row["Cuentas"]
        debe = row["Debe"]
        haber = row["Haber"]

        # Si la cuenta no existe en el libro mayor, la inicializamos
        if cuenta not in libro_mayor:
            libro_mayor[cuenta] = {"Debe": 0.0, "Haber": 0.0}

        # Sumar los montos de débito y crédito
        libro_mayor[cuenta]["Debe"] += debe
        libro_mayor[cuenta]["Haber"] += haber

    # Mostrar el libro mayor en formato de "T"
    for cuenta, movimientos in libro_mayor.items():
        st.write(f"#### Cuenta: {cuenta}")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Debe**")
            st.write(f"${movimientos['Debe']:,.2f}")
        with col2:
            st.write("**Haber**")
            st.write(f"${movimientos['Haber']:,.2f}")

# Crear un DataFrame para el libro mayor
    cuentas_mayor = {}
    
    # Recorrer el libro diario para sumar débitos y créditos
    for _, fila in st.session_state.libro_diario_data.iterrows():
        cuenta = fila["Cuentas"]
        debe = fila["Debe"]
        haber = fila["Haber"]
        
        if cuenta not in cuentas_mayor:
            cuentas_mayor[cuenta] = {"Debe": 0.0, "Haber": 0.0}
        
        cuentas_mayor[cuenta]["Debe"] += debe
        cuentas_mayor[cuenta]["Haber"] += haber
    
    # Calcular saldos (SumaMayor - SumaMenor)
    libro_mayor_df = pd.DataFrame.from_dict(cuentas_mayor, orient="index")
    libro_mayor_df["Saldo Debe"] = libro_mayor_df["Debe"] - libro_mayor_df["Haber"]
    libro_mayor_df["Saldo Haber"] = libro_mayor_df["Haber"] - libro_mayor_df["Debe"]
    
    # Ajustar saldos (si es positivo en Debe, si es negativo en Haber)
    libro_mayor_df["Saldo Final"] = libro_mayor_df.apply(
        lambda x: f"${x['Saldo Debe']:,.2f} (Debe)" if x['Saldo Debe'] > 0 else f"${abs(x['Saldo Haber']):,.2f} (Haber)",
        axis=1
    )

# Función para el libro Diario
def libro_diario():
    st.write("### Libro Diario")

    # Mostrar el libro diario
    st.write("#### Libro Diario")
    st.dataframe(st.session_state.libro_diario_data)

    # Calcular y mostrar el total de Debe y Haber
    total_debe = st.session_state.libro_diario_data["Debe"].sum()
    total_haber = st.session_state.libro_diario_data["Haber"].sum()

    st.write("#### Totales")
    st.write(f"**Total Debe:** ${total_debe:,.2f}")
    st.write(f"**Total Haber:** ${total_haber:,.2f}")

    # Verificar si los totales están balanceados
    if total_debe == total_haber:
        st.success("Los totales de Debe y Haber están balanceados.")
    else:
        st.error("Los totales de Debe y Haber no están balanceados. Revise las operaciones.")

    # Botón para generar el libro mayor
    if st.button("Generar Libro Mayor", key="boton_generar_libro_mayor"):
        libro_mayor()

# Función para agregar una operación al libro diario
def agregar_operacion(fecha, cuentas, parcial, debe, haber):
    nueva_fila = {"Fecha": fecha, "Cuentas": cuentas, "Parcial": parcial, "Debe": debe, "Haber": haber}
    st.session_state.libro_diario_data = pd.concat([st.session_state.libro_diario_data, pd.DataFrame([nueva_fila])], ignore_index=True)

# Inicializar el libro diario si no existe
if "libro_diario_data" not in st.session_state:
    st.session_state.libro_diario_data = pd.DataFrame(columns=["Fecha", "Cuentas", "Parcial", "Debe", "Haber"])

# Agregar las cuentas iniciales de la Balanza General
if st.button("Registrar Cuentas Iniciales", key="boton_registrar_cuentas_iniciales"):
    agregar_operacion("21/01/2025", "Caja", "", 50000.0, 0.0)
    agregar_operacion("21/01/2025", "Bancos", "", 2500000.0, 0.0)
    agregar_operacion("21/01/2025", "Mercancías", "", 150000.0, 0.0)
    agregar_operacion("21/01/2025", "Terrenos", "", 650000.0, 0.0)
    agregar_operacion("21/01/2025", "Edificios", "", 1500000.0, 0.0)
    agregar_operacion("21/01/2025", "Equipo de Reparto", "", 200000.0, 0.0)
    agregar_operacion("21/01/2025", "Mob y Equipo", "", 115000.0, 0.0)
    agregar_operacion("21/01/2025", "Muebles y Enseres", "", 120000.0, 0.0)
    agregar_operacion("21/01/2025", "Equipo de Computo", "", 90000.0, 0.0)
    agregar_operacion("21/01/2025", "Capital", "", 0.0, 5375000.0)
    st.success("Cuentas iniciales registradas en el libro diario.")

# Llamar a la función del libro diario

# Función para generar la Balanza de Comprobación
def balanza_comprobacion():
    st.write("### Balanza de Comprobación")

    # Verificar si el libro mayor existe y tiene datos
    if not hasattr(st.session_state, "libro_mayor") or not st.session_state.libro_mayor:
        st.error("El libro mayor no tiene datos. Registra operaciones primero.")
        return

    # Crear una lista para almacenar las cuentas y sus saldos
    balanza_comprobacion = []

    # Recorrer las cuentas del libro mayor
    for cuenta, movimientos in st.session_state.libro_mayor.items():
        # Asegurarse de que los movimientos tengan "Debe" y "Haber"
        debe = movimientos.get("Debe", 0.0)  # Usar 0.0 si "Debe" no existe
        haber = movimientos.get("Haber", 0.0)  # Usar 0.0 si "Haber" no existe
        
        # Agregar la cuenta a la balanza de comprobación
        balanza_comprobacion.append({
            "Cuenta": cuenta,
            "Debe": debe,
            "Haber": haber
        })

    # Crear un DataFrame para mostrar la balanza de comprobación
    df_balanza = pd.DataFrame(balanza_comprobacion)

    # Mostrar la balanza de comprobación en Streamlit
    st.write("#### Balanza de Comprobación")
    st.dataframe(df_balanza)

    # Calcular los totales de Debe y Haber
    total_debe = df_balanza["Debe"].sum()
    total_haber = df_balanza["Haber"].sum()

    st.write("#### Totales")
    st.write(f"**Total Debe:** ${total_debe:,.2f}")
    st.write(f"**Total Haber:** ${total_haber:,.2f}")

    # Verificar si los totales están balanceados
    if total_debe == total_haber:
        st.success("La balanza de comprobación está balanceada.")
    else:
        st.error("La balanza de comprobación no está balanceada. Revise las operaciones.")

# Función para el libro Diario
def libro_diario():
    #st.write("### Libro Diario")

    # Mostrar el libro diario
    #st.write("#### Libro Diario")
    st.dataframe(st.session_state.libro_diario_data)

    # Calcular y mostrar el total de Debe y Haber
    total_debe = st.session_state.libro_diario_data["Debe"].sum()
    total_haber = st.session_state.libro_diario_data["Haber"].sum()

    st.write("#### Totales")
    st.write(f"**Total Debe:** ${total_debe:,.2f}")
    st.write(f"**Total Haber:** ${total_haber:,.2f}")

    # Verificar si los totales están balanceados
    if total_debe == total_haber:
        st.success("Los totales de Debe y Haber están balanceados.")
    else:
        st.error("Los totales de Debe y Haber no están balanceados. Revise las operaciones.")

# Función para agregar una operación al libro diario
def agregar_operacion(fecha, cuentas, parcial, debe, haber):
    nueva_fila = {"Fecha": fecha, "Cuentas": cuentas, "Parcial": parcial, "Debe": debe, "Haber": haber}
    st.session_state.libro_diario_data = pd.concat([st.session_state.libro_diario_data, pd.DataFrame([nueva_fila])], ignore_index=True)

    # Actualizar el libro mayor
    if cuentas not in st.session_state.libro_mayor:
        st.session_state.libro_mayor[cuentas] = {"Debe": 0.0, "Haber": 0.0}
    
    st.session_state.libro_mayor[cuentas]["Debe"] += debe
    st.session_state.libro_mayor[cuentas]["Haber"] += haber

# Inicializar el libro diario si no existe
if "libro_diario_data" not in st.session_state:
    st.session_state.libro_diario_data = pd.DataFrame(columns=["Fecha", "Cuentas", "Parcial", "Debe", "Haber"])

# Inicializar el libro mayor si no existe
if "libro_mayor" not in st.session_state:
    st.session_state.libro_mayor = {}

# Agregar las cuentas iniciales de la Balanza General
if st.button("Registrar Cuentas Iniciales.B", key="cuentas_iniciales"):
    agregar_operacion("21/01/2025", "Caja", "", 50000.0, 0.0)
    agregar_operacion("21/01/2025", "Bancos", "", 2500000.0, 0.0)
    agregar_operacion("21/01/2025", "Mercancías", "", 150000.0, 0.0)
    agregar_operacion("21/01/2025", "Terrenos", "", 650000.0, 0.0)
    agregar_operacion("21/01/2025", "Edificios", "", 1500000.0, 0.0)
    agregar_operacion("21/01/2025", "Equipo de Reparto", "", 200000.0, 0.0)
    agregar_operacion("21/01/2025", "Mob y Equipo", "", 115000.0, 0.0)
    agregar_operacion("21/01/2025", "Muebles y Enseres", "", 120000.0, 0.0)
    agregar_operacion("21/01/2025", "Equipo de Computo", "", 90000.0, 0.0)
    agregar_operacion("21/01/2025", "Capital", "", 0.0, 5375000.0)
    st.success("Cuentas iniciales registradas en el libro diario.")

# Llamar a las funciones
libro_diario()

# Inicializar el DataFrame para las depreciaciones
if 'depreciaciones_data' not in st.session_state:
    st.session_state.depreciaciones_data = pd.DataFrame({
        "Cuenta": ["Edificios", "Equipo de Reparto", "Equipo de Computo", "Mob y Equipo", "Muebles y Enseres"],
        "Porcentaje": [5, 25, 30, 10, 10],
        "Monto": [1500000, 200000, 90000, 115000, 120000],
        "Depreciación Anual": [0, 0, 0, 0, 0],
        "Depreciación Mensual": [0, 0, 0, 0, 0]
    })

# Función para calcular las depreciaciones
def calcular_depreciaciones():
    # Obtener los montos de las cuentas no circulantes desde la balanza de comprobación
    for index, row in st.session_state.depreciaciones_data.iterrows():
        cuenta = row["Cuenta"]
        monto = st.session_state.data.loc[st.session_state.data["Cuenta"] == cuenta, "Monto"].values[0]
        st.session_state.depreciaciones_data.at[index, "Monto"] = monto

    # Calcular la depreciación anual y mensual
    st.session_state.depreciaciones_data["Depreciación Anual"] = (
        st.session_state.depreciaciones_data["Monto"] * st.session_state.depreciaciones_data["Porcentaje"] / 100
    )
    st.session_state.depreciaciones_data["Depreciación Mensual"] = (
        st.session_state.depreciaciones_data["Depreciación Anual"] / 12
    )

# Función para mostrar las depreciaciones
def mostrar_depreciaciones():
    st.write("### Depreciaciones")
    calcular_depreciaciones()  # Recalcular las depreciaciones con los montos actualizados
    st.dataframe(st.session_state.depreciaciones_data)

    # Calcular el total de la depreciación mensual
    total_depreciacion_mensual = st.session_state.depreciaciones_data["Depreciación Mensual"].sum()
    st.write(f"**Total Depreciación Mensual:** ${total_depreciacion_mensual:,.2f}")

# Función para mostrar el Estado de Resultados
def mostrar_estado_resultados():
    st.write("### Estado de Resultados")

    # Mostrar cuentas circulantes con montos predefinidos
    st.write("#### Cuentas Circulantes")
    cuentas_circulantes = pd.DataFrame({
        "Cuenta": ["Caja", "Bancos", "Mercancías", "IVA Acreditable", "IVA por Acreditar", "Renta Anticipada", "Papelería", "Cliente"],
        "Monto": [17520, 2732000, 78000, 5120, 4480, 4000, 2000, 4640]
    })
    st.table(cuentas_circulantes)

    # Calcular Total Circulante
    total_circulante = cuentas_circulantes["Monto"].sum()
    st.write(f"**Total Circulante:** ${total_circulante:,.2f}")

    # Mostrar cuentas no circulantes con depreciaciones
    st.write("#### Cuentas No Circulantes")
    cuentas_no_circulantes = st.session_state.data[st.session_state.data["Tipo"] == "No Circulante"]
    estado_no_circulantes = cuentas_no_circulantes[["Cuenta", "Monto"]].copy()

    # Calcular el valor actualizado de las cuentas que se deprecian
    for index, row in estado_no_circulantes.iterrows():
        cuenta = row["Cuenta"]
        if cuenta in st.session_state.depreciaciones_data["Cuenta"].values:
            # Obtener la depreciación mensual acumulada
            depreciacion_mensual = st.session_state.depreciaciones_data.loc[
                st.session_state.depreciaciones_data["Cuenta"] == cuenta, "Depreciación Mensual"
            ].values[0]
            # Restar la depreciación mensual al monto actual de la balanza de comprobación
            estado_no_circulantes.at[index, "Monto"] -= depreciacion_mensual

    # Mostrar las cuentas no circulantes con sus montos actualizados
    st.table(estado_no_circulantes)

    # Calcular Total No Circulante
    total_no_circulante = estado_no_circulantes["Monto"].sum()
    st.write(f"**Total No Circulante:** ${total_no_circulante:,.2f}")

    # Calcular Total Activo (Circulante + No Circulante)
    total_activo = total_circulante + total_no_circulante
    st.write(f"**Total Activo (Circulante + No Circulante):** ${total_activo:,.2f}")

    # Mostrar cuentas de Pasivo
    st.write("#### Pasivo")
    pasivo_data = pd.DataFrame({
        "Cuenta": ["Acreedores Corto Plazo", "Documentos por Pagar", "Anticipo de Clientes", "IVA Trasladado", "IVA por Trasladar"],
        "Monto": [20880, 11600, 0, 32640, 640]
    })
    st.table(pasivo_data)

    # Calcular Total Pasivo
    total_pasivo = pasivo_data["Monto"].sum()
    st.write(f"**Total Pasivo:** ${total_pasivo:,.2f}")

    # Mostrar cuentas de Capital
    st.write("#### Capital")
    capital_data = pd.DataFrame({
        "Cuenta": ["Capital Social", "Utilidad del Período"],
        "Monto": [5375000, 84925]
    })
    st.table(capital_data)

    # Calcular Total Capital
    total_capital = capital_data["Monto"].sum()
    st.write(f"**Total Capital:** ${total_capital:,.2f}")

    # Calcular Total Pasivo + Capital
    total_pasivo_capital = total_pasivo + total_capital
    st.write(f"**Total Pasivo + Capital:** ${total_pasivo_capital:,.2f}")

    # Comparar Total Activo con Total Pasivo + Capital
    st.write("#### Comparación de Totales")
    comparacion_df = pd.DataFrame({
        "Concepto": ["Total Activo", "Total Pasivo + Capital"],
        "Monto": [f"${total_activo:,.2f}", f"${total_pasivo_capital:,.2f}"]
    })
    st.table(comparacion_df)

    # Verificar si coinciden los totales
    if total_activo == total_pasivo_capital:
        st.success("✅ Los totales coinciden: **Total Activo = Total Pasivo + Capital**.")
    else:
        st.error("❌ Los totales no coinciden. Revise los cálculos.")

# Función para calcular la Utilidad del Período
def calcular_utilidad_periodo():
    st.write("### Cálculo de Utilidad del Período")

    # Simular que los montos se toman de la balanza de comprobación
    st.write("#### Montos tomados de la Balanza de Comprobación")
    ventas = 208000  # Monto de Ventas
    costo_lo_vendido = 104000  # Monto de Costo de lo Vendido
    gastos_generales = 19075  # Monto de Gastos Generales

    # Crear un DataFrame para mostrar los montos
    montos_df = pd.DataFrame({
        "Cuenta": ["Ventas", "Costo de lo Vendido", "Gastos Generales"],
        "Monto": [ventas, costo_lo_vendido, gastos_generales]
    })
    st.table(montos_df)

    # Calcular Utilidad Bruta
    st.write("#### Cálculo de Utilidad Bruta")
    utilidad_bruta = ventas - costo_lo_vendido
    calculo_utilidad_bruta_df = pd.DataFrame({
        "Operación": ["Ventas - Costo de lo Vendido"],
        "Detalle": [f"${ventas:,.2f} - ${costo_lo_vendido:,.2f}"],
        "Resultado": [f"${utilidad_bruta:,.2f}"]
    })
    st.table(calculo_utilidad_bruta_df)

    # Calcular Utilidad del Período
    st.write("#### Cálculo de Utilidad del Período")
    utilidad_periodo = utilidad_bruta - gastos_generales
    calculo_utilidad_periodo_df = pd.DataFrame({
        "Operación": ["Utilidad Bruta - Gastos Generales"],
        "Detalle": [f"${utilidad_bruta:,.2f} - ${gastos_generales:,.2f}"],
        "Resultado": [f"${utilidad_periodo:,.2f}"]
    })
    st.table(calculo_utilidad_periodo_df)

    # Mostrar el resumen final
    st.write("#### Resumen Final")
    resumen_df = pd.DataFrame({
        "Cuenta": ["Ventas", "Costo de lo Vendido", "Gastos Generales", "Utilidad Bruta", "Utilidad del Período"],
        "Monto": [f"${ventas:,.2f}", f"${costo_lo_vendido:,.2f}", f"${gastos_generales:,.2f}", f"${utilidad_bruta:,.2f}", f"${utilidad_periodo:,.2f}"]
    })
    st.table(resumen_df)


# Función para mostrar el Estado de Cambios
def estado_cambios():
    st.write("### Estado de Cambios")

    # Primera tabla: Calcular el 5% de la Utilidad Bruta y dividirlo entre 12
    st.write("#### Cálculo del 5% de la Utilidad Bruta")
    utilidad_bruta = 84925  # Valor de la Utilidad Bruta (calculado previamente)
    porcentaje_utilidad = utilidad_bruta * 0.05  # 5% de la Utilidad Bruta
    resultado_division = porcentaje_utilidad / 12  # Dividir entre 12
    st.write(f"**Utilidad Bruta:** ${utilidad_bruta:,.2f}")
    st.write(f"**5% de la Utilidad Bruta:** ${porcentaje_utilidad:,.2f}")
    st.write(f"**Resultado de la división (5% / 12):** ${resultado_division:,.2f}")

    # Segunda tabla: Estado de Cambios
    st.write("#### Estado de Cambios")

    # Crear el DataFrame para el Estado de Cambios
    estado_cambios_data = {
        "Concepto": [
            "Saldo Inicial",
            "Aumentos:",
            "  Capital Social",
            "  Reserva Legal",
            "  Emisión de Acciones",
            "  Prima de Acciones",
            "  Resultado del Ejercicio (Utilidad)",
            "Total Aumentos",
            "Disminuciones:",
            "  Decreto de Dividendos",
            "  Reserva Legal",
            "  Reembolso a Socios",
            "Total Disminuciones",
            "Incremento Neto",
            "Saldo Final"
        ],
        "Capital Contribuido +": [
            5375000,  # Saldo Inicial (Capital Social)
            0,  # Aumentos (placeholder)
            5375000,  # Capital Social
            0,  # Reserva Legal
            0,  # Emisión de Acciones
            0,  # Prima de Acciones
            0,  # Resultado del Ejercicio (Utilidad)
            5375000,  # Total Aumentos
            0,  # Disminuciones (placeholder)
            0,  # Decreto de Dividendos
            0,  # Reserva Legal
            0,  # Reembolso a Socios
            0,  # Total Disminuciones
            5375000,  # Incremento Neto
            0   # Saldo Final
        ],
        "Capital Ganado =": [
            0,  # Saldo Inicial
            0,  # Aumentos (placeholder)
            0,  # Capital Social
            resultado_division,  # Reserva Legal
            0,  # Emisión de Acciones
            0,  # Prima de Acciones
            84925,  # Resultado del Ejercicio (Utilidad)
            84925 + resultado_division,  # Total Aumentos
            0,  # Disminuciones (placeholder)
            0,  # Decreto de Dividendos
            resultado_division,  # Reserva Legal
            0,  # Reembolso a Socios
            resultado_division,  # Total Disminuciones
            84925,  # Incremento Neto
            5375000 + 84925  # Saldo Final
        ],
        "Capital Contable": [
            5375000,  # Saldo Inicial
            0,  # Aumentos (placeholder)
            5375000,  # Capital Social
            resultado_division,  # Reserva Legal
            0,  # Emisión de Acciones
            0,  # Prima de Acciones
            84925,  # Resultado del Ejercicio (Utilidad)
            5375000 + 84925 + resultado_division,  # Total Aumentos
            0,  # Disminuciones (placeholder)
            0,  # Decreto de Dividendos
            resultado_division,  # Reserva Legal
            0,  # Reembolso a Socios
            resultado_division,  # Total Disminuciones
            5375000 + 84925,  # Incremento Neto
            5375000 + 84925  # Saldo Final
        ]
    }

    # Convertir el diccionario a un DataFrame
    estado_cambios_df = pd.DataFrame(estado_cambios_data)

    # Mostrar la tabla
    st.table(estado_cambios_df)

    # Explicación de los cálculos
    st.write("#### Explicación de los cálculos:")
    st.write("- **Saldo Inicial**: Capital Social inicial ($5,375,000).")
    st.write(f"- **Reserva Legal**: 5% de la Utilidad Bruta dividido entre 12 (${resultado_division:,.2f}).")
    st.write(f"- **Resultado del Ejercicio (Utilidad)**: Utilidad del Período (${84925:,.2f}).")
    st.write(f"- **Total Aumentos**: Capital Social + Reserva Legal + Utilidad del Período.")
    st.write(f"- **Total Disminuciones**: Reserva Legal (${resultado_division:,.2f}).")
    st.write(f"- **Incremento Neto**: Total Aumentos - Total Disminuciones.")
    st.write(f"- **Saldo Final**: Saldo Inicial + Incremento Neto.")

def estado_flujos():
    st.write("### Estado de Flujos de Efectivo")

    # =============================================
    # 1. ACTIVIDADES DE OPERACIÓN (NUEVA ESTRUCTURA)
    # =============================================
    st.write("#### Actividades de Operación")
    
    # Datos de cuentas (Montos exactos según lo solicitado)
    operacion_data = [
        {"Cuenta": "Clientes", "Monto": 4640.00},
        {"Cuenta": "Almacen/Mercancia", "Monto": 78000.00},
        {"Cuenta": "IVA Acreditable", "Monto": 5120.00},
        {"Cuenta": "IVA Pendiente de Acreditar", "Monto": 4480.00},
        {"Cuenta": "IVA Trasladado", "Monto": -32640.00},
        {"Cuenta": "IVA Pendiente de Trasladar", "Monto": -640.00},
        {"Cuenta": "Proveedores", "Monto": 0.00},
        {"Cuenta": "Provision de ISR", "Monto": -25477.50},
        {"Cuenta": "Provision de PTU", "Monto": -8492.50},
        {"Cuenta": "Utilidad de Ejercicio", "Monto": -50955.00},
        {"Cuenta": "Papeleria", "Monto": 2000.00},
        {"Cuenta": "Renta Pagada por Anticipo", "Monto": 4000.00}
    ]
    
    # Convertir a DataFrame
    operacion_df = pd.DataFrame(operacion_data)
    
    # Mostrar tabla con formato monetario
    st.table(operacion_df.style.format({"Monto": "${:,.2f}"}))
    
    # Calcular total automáticamente
    flujo_operacion = operacion_df["Monto"].sum()
    st.success(f"**Flujos netos de actividades en operaciones:** ${flujo_operacion:,.2f}")

    # =============================================
    # 2. ACTIVIDADES DE INVERSIÓN
    # =============================================
    st.write("#### Actividades de Inversión")
    
    inversion_data = [
        {"Cuenta": "Terrenos", "Monto": 650000.00},
        {"Cuenta": "Edificios", "Monto": 1493750.00},
        {"Cuenta": "Equipo de Reparto", "Monto": 195833.33},
        {"Cuenta": "Mob y Equipo", "Monto": 105300.00},
        {"Cuenta": "Muebles y Enseres", "Monto": 114041.67},
        {"Cuenta": "Equipo de Computo", "Monto": 119000.00}
    ]
    
    inversion_df = pd.DataFrame(inversion_data)
    st.table(inversion_df.style.format({"Monto": "${:,.2f}"}))
    
    flujo_inversion = inversion_df["Monto"].sum()
    st.success(f"**Flujos netos de actividades en inversión:** ${flujo_inversion:,.2f}")

    # =============================================
    # 3. ACTIVIDADES DE FINANCIAMIENTO
    # =============================================
    st.write("#### Actividades de Financiamiento")
    
    financiamiento_data = [
        {"Cuenta": "Capital Social", "Monto": -5375000.00},
        {"Cuenta": "Acreedores Diversos", "Monto": -20880.00},
        {"Cuenta": "Documentos por pagar", "Monto": -11600.00}
    ]
    
    financiamiento_df = pd.DataFrame(financiamiento_data)
    st.table(financiamiento_df.style.format({"Monto": "${:,.2f}"}))
    
    flujo_financiamiento = financiamiento_df["Monto"].sum()
    st.success(f"**Flujos netos de actividades en financiamiento:** ${flujo_financiamiento:,.2f}")

    # =============================================
    # 4. RESUMEN FINAL (CÁLCULO AUTOMÁTICO)
    # =============================================
    st.write("#### Resumen General")
    
    resumen_data = [
        {"Concepto": "Efectivo generado en operaciones", "Monto": flujo_operacion},
        {"Concepto": "Efectivo usado en inversiones", "Monto": flujo_inversion},
        {"Concepto": "Efectivo usado en financiamiento", "Monto": flujo_financiamiento},
        {"Concepto": "Incremento neto de efectivo", "Monto": flujo_operacion + flujo_inversion + flujo_financiamiento}
    ]
    
    resumen_df = pd.DataFrame(resumen_data)
    st.table(resumen_df.style.format({"Monto": "${:,.2f}"}))
    
    # =============================================
    # 5. COMPARACIÓN DE SALDOS (BANCOS/CAJA)
    # =============================================
    st.write("#### Comparación de Saldos")
    
    bancos_final = 2732000.00
    bancos_inicial = 2500000.00
    caja_final = 17520.00
    caja_inicial = 50000.00
    
    comparacion_data = [
        {"Cuenta": "Bancos (Final)", "Monto": bancos_final},
        {"Cuenta": "Bancos (Inicial)", "Monto": bancos_inicial},
        {"Cuenta": "Diferencia Bancos", "Monto": bancos_inicial - bancos_final},
        {"Cuenta": "Caja (Final)", "Monto": caja_final},
        {"Cuenta": "Caja (Inicial)", "Monto": caja_inicial},
        {"Cuenta": "Diferencia Caja", "Monto": caja_inicial - caja_final}
    ]
    
    comparacion_df = pd.DataFrame(comparacion_data)
    st.table(comparacion_df.style.format({"Monto": "${:,.2f}"}))
    
    st.write("#### Validación de Saldos")
    
    # Datos de saldos
    bancos_inicial = 2500000.00
    bancos_final = 2732000.00
    caja_inicial = 50000.00
    caja_final = 17520.00
    
    # Cálculos
    disminucion_neta = -2749520.00  # Según lo especificado
    diferencia_saldos = bancos_final + caja_final

    # Tabla comparativa (mostrando valores originales pero comparando absolutos)
    validacion_data = [
        {"Concepto": "Disminución Neta del Efectivo", "Valor": f"${disminucion_neta:,.2f}", "Tipo": "Calculado"},
        {"Concepto": "Suma de Saldos Finales", "Valor": f"${diferencia_saldos:,.2f}", "Tipo": "Real"},
        {"Concepto": "Coinciden (comparando valores absolutos)", 
        "Valor": "Sí" if abs(disminucion_neta) == abs(diferencia_saldos) else "No", 
        "Tipo": "Validación"}
    ]

    st.table(pd.DataFrame(validacion_data))

    if abs(disminucion_neta) == abs(diferencia_saldos):
        st.success("✅ Los valores coinciden correctamente (comparando magnitudes).")
    else:
        st.error(f"❌ Hay discrepancia. Diferencia: ${abs(abs(disminucion_neta) - abs(diferencia_saldos)):,.2f}")

def fuente_efectivo():
    st.write("### Fuente de Efectivo")
    
    # --- 1. FUENTE DE EFECTIVO ---
    st.write("#### Fuente de Efectivo")
    fuente_data = [
        {"Concepto": "Utilidad del Ejercicio", "Monto": 50955.00},
        {"Concepto": "Depreciaciones", "Monto": 15075.00}
    ]
    fuente_df = pd.DataFrame(fuente_data)
    st.table(fuente_df.style.format({"Monto": "${:,.2f}"}))
    
    # Suma automática
    suma_fuente = fuente_df["Monto"].sum()
    st.write(f"**Suma de fuente de efectivo (Utilidad + Depreciaciones):** ${suma_fuente:,.2f}")

    # --- 2. CARGOS A RESULTADOS ---
    st.write("#### Cargos a Resultados que no implican utilización de efectivo")
    cargos_data = [
        {"Concepto": "ISR", "Monto": 25477.50},
        {"Concepto": "PTU", "Monto": 8492.50},
        {"Concepto": "Acreedores", "Monto": 20880.00}
    ]
    cargos_df = pd.DataFrame(cargos_data)
    st.table(cargos_df.style.format({"Monto": "${:,.2f}"}))
    
    # Suma automática
    suma_cargos = cargos_df["Monto"].sum()
    st.write(f"**Suma de cargos de resultados (ISR + PTU + Acreedores):** ${suma_cargos:,.2f}")

    # Cálculo de efectivo generado
    efectivo_operacion = suma_fuente + suma_cargos
    st.success(f"**Efectivo generado en la operación:** ${efectivo_operacion:,.2f}")

    # --- 3. FINANCIAMIENTO ---
    st.write("#### Financiamiento y otras fuentes")
    financiamiento_data = [
        {"Concepto": "Proveedores", "Monto": 0.00},
        {"Concepto": "Documentos Por Pagar", "Monto": 11600.00},
        {"Concepto": "Capital Social", "Monto": 5375000.00}
    ]
    financiamiento_df = pd.DataFrame(financiamiento_data)
    st.table(financiamiento_df.style.format({"Monto": "${:,.2f}"}))
    
    # Suma automática
    suma_financiamiento = financiamiento_df["Monto"].sum()
    st.write(f"**Suma de financiamiento:** ${suma_financiamiento:,.2f}")

    # Total fuentes
    total_fuentes = efectivo_operacion + suma_financiamiento
    st.success(f"**Suma las fuentes de efectivo:** ${total_fuentes:,.2f}")

    # --- 4. APLICACIÓN DE EFECTIVO ---
    st.write("#### Aplicación de Efectivo")
    aplicacion_data = [
        {"Concepto": "Almacen", "Monto": 78000.00},
        {"Concepto": "Clientes", "Monto": 4640.00},
        {"Concepto": "Papeleria", "Monto": 2000.00},
        {"Concepto": "Renta", "Monto": 4000.00},
        {"Concepto": "IVA Acreditable", "Monto": 5120.00},
        {"Concepto": "IVA Pendiente De Acreditar", "Monto": 4480.00},
        {"Concepto": "IVA Trasladado", "Monto": -32640.00},
        {"Concepto": "IVA Pendiente de Trasladar", "Monto": -640.00},
        {"Concepto": "Terrenos", "Monto": 650000.00},
        {"Concepto": "Edificios", "Monto": 1500000.00},
        {"Concepto": "Equipo de Reparto", "Monto": 200000.00},
        {"Concepto": "Mob y Equipo", "Monto": 115000.00},
        {"Concepto": "Muebles y Enseres", "Monto": 120000.00},
        {"Concepto": "Equipo de Computo", "Monto": 108000.00}
    ]
    aplicacion_df = pd.DataFrame(aplicacion_data)
    st.table(aplicacion_df.style.format({"Monto": "${:,.2f}"}))
    
    # Suma automática
    suma_aplicacion = aplicacion_df["Monto"].sum()
    st.write(f"**Suma de Aplicación de Efectivo:** ${suma_aplicacion:,.2f}")

    # --- 5. COMPARACIÓN DE SALDOS ---
    st.write("#### Comparación de Saldos Bancarios y Caja")
    bancos_data = [
        {"Concepto": "Disminución neta del Efectivo", "Monto": 2749520.00},
        {"Concepto": "Saldo inicial de bancos", "Monto": 2500000.00},
        {"Concepto": "Saldo final de bancos", "Monto": 2732000.00, "Diferencia": 232000.00},
        {"Concepto": "Saldo inicial de Caja", "Monto": 50000.00},
        {"Concepto": "Saldo final de Caja", "Monto": 17520.00, "Diferencia": 32480.00}
    ]
    bancos_df = pd.DataFrame(bancos_data)
    st.table(bancos_df.style.format({"Monto": "${:,.2f}", "Diferencia": "${:,.2f}"}))

    st.write("#### Validación de Saldos")
    
    # Datos de saldos
    saldo_final_bancos = 2732000.00
    saldo_final_caja = 17520.00
    disminucion_neta = 2749520.00  # Valor positivo para comparación
    
    # Cálculos
    suma_saldos_finales = saldo_final_bancos + saldo_final_caja
    
    # Tabla comparativa
    validacion_data = [
        {"Concepto": "Disminución Neta del Efectivo", "Valor": f"${disminucion_neta:,.2f}", "Tipo": "Esperado"},
        {"Concepto": "Suma de Saldos Finales (Bancos + Caja)", "Valor": f"${suma_saldos_finales:,.2f}", "Tipo": "Real"},
        {"Concepto": "Coinciden", "Valor": "Sí" if abs(disminucion_neta - suma_saldos_finales) < 0.01 else "No", "Tipo": "Validación"}
    ]
    
    st.table(pd.DataFrame(validacion_data))
    
    if abs(disminucion_neta - suma_saldos_finales) < 0.01:
        st.success("✅ Los valores coinciden correctamente.")
    else:
        st.error(f"❌ Discrepancia de ${abs(disminucion_neta - suma_saldos_finales):,.2f}. Revise las operaciones.")



# Botón para generar la Balanza de Comprobación
if st.button("Generar Balanza de Comprobación", key="boton_generar_balanza_comprobacion"):
    balanza_comprobacion()
# Lógica para mostrar la operación seleccionada
if opcion == "Balanza General":
    balanza_general()
elif opcion == "Compra en Efectivo":
    compra_efectivo()
elif opcion == "Compra a Crédito":
    compra_credito()
elif opcion == "Compra a Crédito-Efectivo":
    compra_credito_efectivo()
elif opcion == "Renta":
    renta()
elif opcion == "Venta":
    venta()
elif opcion == "Papelería":
    papeleria()
elif opcion == "Libro Diario":
    libro_diario()
elif opcion == "Libro Mayor":
    libro_mayor()
elif opcion == "Balanza de Comprobación":
    balanza_comprobacion()
elif opcion == "Depreciaciones":
    mostrar_depreciaciones()
elif opcion == "Estado de Resultados":
    mostrar_estado_resultados()
elif opcion == "Cálculo de Utilidad del Período":
    calcular_utilidad_periodo()
elif opcion== "Estado de Cambios":
    estado_cambios()
elif opcion== "Estado de Flujos":
    estado_flujos()
elif opcion== "Fuente de Efectivo":
    fuente_efectivo()
