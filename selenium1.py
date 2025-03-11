from selenium import webdriver #Automatización de navegadores
import time #Para los Sleeps
import os #Para manejar archivos
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from glob import glob #Para buscar archivos en un directorio
import gspread #Para trabajar con Google Sheets
import streamlit as st #Para la interfaz de usuario
from google.oauth2.service_account import Credentials #Para autenticación con Google Sheets
import pandas as pd #Para convertir a formato google sheets.
import subprocess #Para llamar otro codigo dentro del prinicipal

DOWNLOAD_PATH = "/Users/fernandomartinez/Downloads" #Download path para los exceles (Ahí se guardsarán, cambie según su necesidad).

" GOOGLE API PERMISOS Y TAL"
SERVICE_ACCOUNT_FILE = "file.json" #Agregar el file.json adecuado.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

" PARA PASARLE EL SfRjDfk4z5gONM2lx4nIHEET AL CUAL PASARÁ EL EXCEL"
SHEET_ID = "1JYvt8rXfsdPwMhXQh7mYV2USqGOkhjWBoCi9wkQ6nHc" #SE OBTIENE DADO EL URL DEL SHEET
sheet = client.open_by_key(SHEET_ID).sheet1 


def get_excel_file(folder, extension = "xlsx"):
    files = glob(os.path.join(folder, f"*.{extension}"))
    if not files:
        return None
    return max(files, key = os.path.getctime)

def download_excel_from_cognito():
    driver = webdriver.Chrome()

    driver.get("https://www.cognitoforms.com/itesm7/formatodesolicitud/entries/1-all-entries") #Cambiar por el Cognito que necesiten.

    time.sleep(2)

    google_button = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Continue with Google')]]"))
    )

    google_button.click()

    time.sleep(3)

    driver.switch_to.window(driver.window_handles[1])

    email_field = driver.find_element(By.XPATH, "//input[@type='email']")
    email_field.send_keys("Correo")
    email_field.send_keys(Keys.RETURN)
    time.sleep(5)

    driver.switch_to.window(driver.window_handles[1])
    email_field2 = driver.find_element(By.XPATH, "//input[@placeholder='Usuario']")
    email_field2.send_keys("Usuario")
    # --- Enter Password ---
    password_field = driver.find_element(By.XPATH, "//input[@placeholder='Contrasena']")
    password_field.send_keys("Ingresar contraseña")
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)

    driver.switch_to.window(driver.window_handles[1])

    confirm_button = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Continuar')]]"))
    )

    confirm_button.click()

    time.sleep(10)

    driver.switch_to.window(driver.window_handles[0])

    print("Se cambió de ventana")
    actions_button = WebDriverWait(driver, 60).until( 
        EC.element_to_be_clickable((By.XPATH, "//div[@class='c-additional-actions']//div[@class='toggle-on']"))  #el xpath los encontré tanto con inspect element, como con selenium IDE y selectors Hub, que me auxiliaron.
    )
    actions_button.click()
    #esperar
    time.sleep(5)

    element = driver.find_element(By.CSS_SELECTOR, '.entry-view-actions__menu--dropdown .el-submenu:nth-child(4) > .el-submenu__title')

    # Click!
    driver.execute_script("arguments[0].click();", element) #lo forzo por javascript porque con .click() no jala!
    time.sleep(5)

    element2 = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.el-menu--popup-right-start > .el-menu-item:nth-child(3) > .flyout-menu__item'))
    )
    driver.execute_script("arguments[0].click();", element2) #Lo mismo de antes, aqui se descarga ya el excel.

    time.sleep(15)

    latest_file = get_excel_file(DOWNLOAD_PATH)
    if latest_file:
        print(f"Archivo Descargado!: {latest_file}")
    else:
        print("No se descargó!")
    
    close = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.c-modal-button-bar:nth-child(3) .c-modal-button'))
    )

    close.click()
    time.sleep(5)
    driver.quit() #Se cierra selenium.
    
    return latest_file

def upload_excel_to_sheet(excel_path):
    try: 
        df_dict = pd.read_excel(excel_path, sheet_name=None)  # Retorna un diccionario con el nombre de la hoja como clave y el DataFrame como valor

        # Iterar sobre cada hoja
        for sheet_name, df in df_dict.items():
            # Reemplazar NaN con ""
            df = df.fillna("")

            # Convertir columnas de tipo Timestamp a string
            for col in df.select_dtypes(include=["datetime64"]):
                df[col] = df[col].astype(str)

            # Convertir DataFrame a lista de listas
            data = [df.columns.tolist()] + df.values.tolist()

            # Verificar si la hoja ya existe en Google Sheets y actualizarla
            try:
                sheet_instance = client.open_by_key(SHEET_ID).worksheet(sheet_name)
            except gspread.exceptions.WorksheetNotFound:
                # Si la hoja no existe, crear una nueva
                sheet_instance = client.open_by_key(SHEET_ID).add_worksheet(title=sheet_name, rows="100", cols="20")

            # Limpiar y actualizar la hoja
            sheet_instance.clear()
            sheet_instance.update(range_name="A1", values=data)

            print(f"Se agregó la información de la hoja '{sheet_name}' al Google Sheet")
    except Exception as e:
        print(f"Error: {e}")

#Interfaz de usuario de streamlit
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
                background-color: white;
        }
        .stButton{
            display: flex;
            justify-content: center;
        }
        div.stButton > button:first-child {
            background-color: #ff8502 !important; /* naranja de la inclusión */
            color: white !important;
            font-size: 18px !important;
            border-radius: 10px !important;
            padding: 10px 20px !important; /* lo hace más amplio el margen */
            border: none !important; /* si no se ve feo al seleccionar */
        }

        /* Button hover effect */
        div.stButton > button:first-child:hover {
            background-color: #d96d00 !important; /* Más naranja */
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h1 style="color: #dd1d83;">Hola, bienvenido al sistema de evaluación de OSCs.</h1>', unsafe_allow_html=True)

st.markdown(
    """ 
    <p style="color:black; font-size:20px;">
    Por favor, asegúrese de que la fecha límite para subir respuestas al Cognito Forms <b> ya haya pasado </b>.
    </p>
    
    <p style="color:black; font-size:20px;">
    Para enviar a procesar la información, de click al botón de abajo, y posteriormente, dar click a "calificar mediante IA", <b>para la evaluación </b>.
    </p>
    """,
    unsafe_allow_html=True
)

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

st.image("logosecretaria.jpg", caption="Descripción de la imagen", use_column_width=True)

if not st.session_state.button_clicked:
    if st.button("Enviar información"):
        st.balloons()
        file_path = download_excel_from_cognito()
        if file_path:
            upload_excel_to_sheet(file_path)
            st.success("Se ha enviado la información correctamente")
        else:
            st.error("No se pudo descargar el archivo")
        
        st.session_state.button_clicked = True

#De esta manera, el botón de IA solo se enseñará cuando el primer proceso haya terminado.
if st.session_state.button_clicked:  
    if st.button("Calificar mediante IA"):
        st.balloons()
        time.sleep(10) #PARA TEMAS DE QUE NO SOBREPASE LIMITE DE API!
        second_script_path = "/Users/fernandomartinez/pruebaselenium/grades/eficiencia/gpteficiencia" #NO CONFUNDIR CON EFICIENCIA.PY
        try:
            subprocess.Popen(["python3", second_script_path])
            st.success("Calificando...")
        except:
            st.error("Hubo un problema calificando: {e}")