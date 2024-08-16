# 1. Selecciona la imagen base de Airflow
FROM apache/airflow:2.5.0

# 2. Establece la variable de entorno para desactivar la creación de ejemplos en Airflow
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

# 3. Copia el archivo requirements.txt al contenedor
COPY requirements.txt /requirements.txt

# 4. Instala las dependencias adicionales que mencionas en requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# 5. Copia los DAGs, plugins, y configuraciones al contenedor
COPY dags/ /opt/airflow/dags/
COPY plugins/ /opt/airflow/plugins/
COPY config/ /opt/airflow/config/

# 6. Exponer el puerto 8080 para acceder a la interfaz web de Airflow
EXPOSE 8080

# 7. Comando por defecto para iniciar el servidor web de Airflow
CMD ["airflow", "webserver"]

#8. Copiar los elementos de la aplicación a docker.
COPY log.txt /log.txt
COPY main.py /main.py
COPY artist_top_tracks.sqlite /artist_top_tracks.sqlite
