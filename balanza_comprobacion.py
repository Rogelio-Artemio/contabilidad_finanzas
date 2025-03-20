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
        "Balanza de Comprobación"  # Última opción
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