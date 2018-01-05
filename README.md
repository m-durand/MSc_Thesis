# Beer

Aprendizaje reforzado aplicado a un modelo basado en agentes jugando _The Beer Distribution Game_.

La estructura básica de este repositorio es:

1. `aux_documents` contiene los documentos de creación de la demanda del consumidor y la oferta de los campos.
2. `code` contiene tanto el código para el modelo, como el código para las visualizaciones. En la subcarpeta `model` se pueden encontrar:
* `beer_distribution_game.ipynb`, en el cual puede consultarse el progreso en el modelo de agentes aprendiendo - contiene visualizaciones interactivas en _Bokeh_, por lo que el rendering en la interfaz web de _Github_ no es ideal
* Todos los demás archivos .py, que son el código real, sobre el que estoy trabajando actualmente; el archivo principal es `clean_run.py`
3. `tesis_tex` contiene el código para generar el archivo `.tex` final. Utiliza el mismo formato que usé para la tesis de licenciatura. En la subcarpeta `figures` pueden consultarse algunas visualizaciones resultantes. Asimismo, existe un pdf con la versión actual, para no tener que compilar localmente.
4. `biblio` contiene bibliografía, la carpeta debe ser eliminada cuando el repo se vuelva público.
