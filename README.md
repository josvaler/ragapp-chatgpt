## ragapp-chatgpt: Convierte tus documentos en conversaciones con chatGPT

Esta version requiere que crees un archivo .env con las siguientes variables:

>OPENAI_API_KEY= "tu_api_key"

Una vez tengas el archivo.env, ejecuta el siguiente comando en la terminal:

>pip install -r requirements.txt

Es posible que tengas que instalar algunas librerias de python, como faiss_cpu no detectada por pipreqs. 

Esta libreria acelera mucho la consulta, si tienes GPU  instalar faiss_gpu, pero no es obligatorio y afecta en partiular a esta linea del codigo:

>knowledge_base = FAISS.from_texts(chunks, embeddings)

La libreria de FAISS es una libreria que permite hacer consultas y funciona muy bien con GPU, la deteccion es automática. En caso que no tengas GPU, puedes usar la libreria faiss_cpu.

Se hizo un refactoring del codigo con las nuevas funcionalidades:

1. Historial de preguntas:
2. Persistencia de sesiones de conversacion 
3. Carga de variables de entorno desde un archivo.env


Para ejecutar la aplicacion:

>streamlit run app.py

Jose Valerio

:link:[LinkedIn](https://www.linkedin.com/in/josvaler/)

:link:[Comprame un cafe](https://buymeacoffee.com/josevalerio)
