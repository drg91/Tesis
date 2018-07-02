# Tesis de grado FCEFyN Ing Computacion

#### Garbiglia, Diego Rodrigo

### Script para crear dataset de imagenes para reconocimiento

Entrar a la pagina de Microsoft Azure

https://azure.microsoft.com/en-us/try/cognitive-services/?api=bing-image-search-api

Apretar en Get Api Key


[img1]: https://www.pyimagesearch.com/wp-content/uploads/2018/04/deep_learning_dataset_get_api_key-768x452.jpg "Microsoft Azure"

### Instalar dependencias

```shell
$ pip install requests
```
Crear carpeta para los dataset

```shell
$ mkdir dataset/vacas
```

## Ejecutar script

```shell
$ python3 search_bing_api.py --query "vacas" --output dataset/vacas
```
