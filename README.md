# OSC_FINAL
Códigos necesarios para correr el proceso, junto con el set de instrucciones para funcionamiento adecuado.

  ## REQUERIMIENTOS

  Se recomienda descargar <b>Visual Studio Code</b> y ahí abrir el código que se descargue de este repositorio.

  Se necesita tener instalado python en su equipo, para ello, se puede visitar la liga aquí adjuntada: [python](https://learn.microsoft.com/es-es/windows/python/beginners)

  Al tener ambos requerimientos instalados, abrir el archivo en Visual Studio Code, dar click a Terminal->Nueva Terminal, y poner:

    py -m ensurepip --upgrade

  Click enter, para instalar el paquete pip.

  Posteriormente, en la misma terminal, ejecutar las siguientes líneas:

    pip install selenium gspread streamlit google-auth pandas
    pip install pandas gspread google-auth openai

## MANUAL DE FUNCIONAMIENTO

  1. Descargar estos archivos en su equipo de cómputo, es fundamental que se descarguen todos.
  2. Antes de continuar, es importante que, desde el portal de Google Cloud Console, aquí se adjunta [la liga al sitio](https://developers.google.com/workspace/guides/create-credentials#api-key), por si los pasos llegan a cambiar en el futuro.
  
    2.1 Ingresar a la terminal de Google Cloud.
  
    2.2 Ingresar a Cuentas de Servicio.
  
    2.3 Ingresar a Claves.
  
    2.4 Dar click en Agregar Clave.
  
    2.5 Crear Clave nueva.
  
    2.6 Formato JSON.
  
    2.7 Cambiar nombre al recién descargado archivo JSON a "file.json". y guardarlo en el directorio donde tienen guardado el código.
  <img width="1162" alt="Screenshot 2025-03-11 at 18 17 57" src="https://github.com/user-attachments/assets/0758a1bc-913b-478f-af5b-a0a4a60e06bd" />
  3. Crear un nuevo archivo de Google Sheets, y a la primera Hoja, renombrarla como <b>Calificaciones</b>, que por default está como sheet1 u hoja1. 
  
  4. Click en Compartir, y dar permiso de editor a cualquiera que tenga el vínculo.
  
  5. Copiar el ID del Google Sheet que recién se creó.<img width="1354" alt="Screenshot 2025-03-11 at 18 28 59"         
  <img width="1162" alt="Screenshot 2025-03-11 at 18 17 57" src="https://github.com/user-attachments/assets/69a56611-bf29-4f33-95ad-d615fa32ccc2" />
  6. Obtener el API personal de openAI, o pedirme a mí que la proporcione: fernandoenriquemtzrdz@gmail.com
  7. En el Código selenium1.py y gpteficiencia.py, buscar las variables:
     
    SHEET ID = SHEET ID QUE OBTUVIMOS AL INICIO.
    ShEET_ID2  = SHEET ID QUE OBTUVIMOS AL INICIO. 
    
  Y sustituir por el Sheet ID que obtuvimos al inicio. OJO: EN COMILLAS, EJEMPLO: 

    SHEET ID = "ID(*#&$^1u23"
    
  8. En el Código selenium1.py y gpteficiencia.py, buscar las variables, con el cuidado de ponerlas entre comillas también.:

    openai.api_key
    openai.OpenAI(api_key="API")

  
  ## EJECUTAR
  Desde la terminal de Visual Studio Code, escribir:

    streamlit run selenium1.py

  Con ello, se desplegará la Interfaz de Usuario, desde donde ya se puede seguir el proceso completo: obtener los datos, y evaluar la dimensión de eficacia.

  <img width="559" alt="Screenshot 2025-03-11 at 19 40 53" src="https://github.com/user-attachments/assets/35655366-2533-44dd-8076-0c0f2cd1c618" />

