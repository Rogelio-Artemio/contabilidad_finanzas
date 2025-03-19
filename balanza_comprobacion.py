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

# Función para la Balanza de Comprobación
def balanza_comprobacion():
    st.write("### Balanza de Comprobación")

    # Calcular totales
    total_circulante, total_no_circulante, total_capital, total_activo, total_pasivo, total_pasivo_capital = calcular_totales(st.session_state.data, st.session_state.pasivo_data)

    # Mostrar los totales de la Balanza de Comprobación
    st.write("#### Totales de la Balanza de Comprobación")
    st.write(f"**Total Activo:** ${total_activo:,.2f}")
    st.write(f"**Total Pasivo + Capital:** ${total_pasivo_capital:,.2f}")
    st.write(f"**Diferencia:** ${total_activo - total_pasivo_capital:,.2f}")

# Funciones para las otras operaciones (esqueletos)
def compra_credito_efectivo():
    st.write("### Compra a Crédito-Efectivo")
    st.write("Aquí puedes registrar una compra realizada parcialmente a crédito y parcialmente en efectivo.")
    # Agrega aquí la lógica para compra a crédito-efectivo

def renta():
    st.write("### Renta")
    st.write("Aquí puedes registrar un gasto por renta.")
    # Agrega aquí la lógica para renta

def venta():
    st.write("### Venta")
    st.write("Aquí puedes registrar una venta.")
    # Agrega aquí la lógica para venta

def papelería():
    st.write("### Papelería")
    st.write("Aquí puedes registrar gastos de papelería.")
    # Agrega aquí la lógica para papelería

def libro_diario():
    st.write("### Libro Diario")
    st.write("Aquí puedes ver el libro diario con todas las transacciones registradas.")
    # Agrega aquí la lógica para el libro diario

def libro_mayor():
    st.write("### Libro Mayor")
    st.write("Aquí puedes ver el libro mayor con los saldos de cada cuenta.")
    # Agrega aquí la lógica para el libro mayor

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
    papelería()
elif opcion == "Libro Diario":
    libro_diario()
elif opcion == "Libro Mayor":
    libro_mayor()
elif opcion == "Balanza de Comprobación":
    balanza_comprobacion()