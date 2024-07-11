Basado en el el video de Nechubm. (Gracias) 

# 📚🗨️ PreguntaDOC es ahora ragapp-chatgpt: Convierte tus documentos en conversaciones con chatGPT

Te recomiendo ver el video de Nechu primero para entender mejor el funcionamiento y luego te detengas a ver el código de esta aplicacion con las nuevas funcionalidades.

Por Nechubm: (Video tutorial y demo de la version anterior)
:link: [Video tutorial](https://youtu.be/iDrpdkIHMq8)
:link: [Web demo](https://nechubm-preguntadoc-app-tutorial-ct21ps.streamlit.app/)

A diferencia de la version anterior, esta version requiere que crees un archivo .env con las siguientes variables:

>OPENAI_API_KEY= "tu_api_key"

Una vez tengas el archivo.env, ejecuta el siguiente comando en la terminal:

>pip install -r requirements.txt

Es posible que tengas que instalar algunas librerias de python, como faiss_cpu no detectada por pipreqs. 

Esta libreria acelera mucho la consulta, si tienes GPU  instalar faiss_gpu, pero no es obligatorio y afecta en partiular a esta linea del codigo:

>knowledge_base = FAISS.from_texts(chunks, embeddings)

La libreria de FAISS es una libreria que permite hacer consultas y funciona muy bien con GPU, la deteccion es automática. En caso que no tengas GPU, puedes usar la libreria faiss_cpu.

Se hizo un refactoring del codigo con las nuevas funcionalidades:

1. Historial de preguntas:
2. Empezar una conversacion nueva con el bot:
3. Persistencia de sesiones de conversacion 
4. Carga de variables de entorno desde un archivo.env
5. Limpieza de variable de ingreso de la pregunta luego del submit

Jose Valerio

:link:[LinkedIn](https://www.linkedin.com/in/josvaler/)

:link:[Comprame un cafe](https://buymeacoffee.com/josevalerio)