### README ###

Los siguientes archivos constituyen el primer prototipo del backend del proyecto
SafePet. A continuacion se describen los codigos implementados

## insert.py
Script para agregar datos (fotos de narices) a la aplicacion. Lee las imagenes que se
encuentran el la ruta indicada en IMAGES_PATH, transformando la imagen en el vector 
correspondiente, que se almacena en './npyData_original/'. Adicionalmente recalcula el
subespacio de componentes principales (teniendo en cuenta el nuevo dato ingresado) y
proyecta toda la data almacenada hasta ahora (archivos en './npyData_original/') en este
nuevo subespacio. Cada una de los datos/narices proyectadas en el subespacio se almacenan
en la matriz './reduced_dogs.npy' (cada dato en un fila) y tambien se almacena el subespacio
de componentes principales en './pc_matrix.npy'.

## masterpet.py
Al iniciar masterpet.py carga en memoria principal los datos originales, los datos reducidos
(con pca), la matriz de componentes principales y computa el objeto de la clase NearestNeighbors
necesario para aplicar el algoritmo KNN.
El programa principal provee de dos comandos basicos:
> insert image.jpg
> search image.jpg
donde el argumento de insert y search es una imagen que se encuentra en el directorio donde
corre la aplicación o el directorio en la variable IMAGES_PATH y TEST_PATH respectivamente.
En el caso de insert, inserta individualmente la imagen indicada siguiendo el mismo procedimiento
que el script anterior.
En el caso de search, este realiza una busqueda de las narices mas semejantes a la de la imagen
que se entrega en el argumento. La busqueda se realiza en primer lugar convirtiendo la imagen en un
vector, para luego aplicarle la proyección en los componentes principales (reducción de dimensiones).
Posteriormente, a esta data reducida se le aplica KNN (K-Nearest Neighbors) obteniendo los indices
de los dos vecinos más cercanos y las distancias correspondientes. Finalmente se muestran los fotos
correspondientes.

## Librerias
Para la aplicación de PCA se ocupa sklearn.decomposition.PCA con el numero de componentes indicados
en la variable NCOMPONENTS. KNN se aplica por medio de sklearn.neighbors.NearestNeighbors con numero
de vecino indicados en la variable NEIGHBORS.

## Datos
Los datos con los cuales trabaja la aplicación pueden encontrarse en
https://www.dropbox.com/sh/pe6u5p6ke8ehh5z/AADOdF8rFoQYm59uFLThJ5Wsa?dl=0
