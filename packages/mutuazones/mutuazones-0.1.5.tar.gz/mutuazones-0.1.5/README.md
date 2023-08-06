## Objetivo
Permite definir de una forma unificada el acceso a las zonas definidas en la arquitectrura de analítica avanzada de Mutua Tienerfeña.

Se han definido las siguientes zonas de trabajo.

* **lz** - Landing Zone. Son los datos que llegan desde el operacional. Pendiente de ser revisados y formatados para la silver.
* **sz** - Silver Zone. Son los datos limpios, preparados para poder cruzarse utilizarse en los correspondientes modelos.
* **gz** - Golden Zone. Son los datos asociados a los resutlados de los modelos definitivos.

## Forma de uso

En los cuadernos de python, se debe realizar lo siguiente.

Para acceder a los dataframes (pandas) almacenados en una zona<lz>:

```python
from mutuazones import lz

lz.df_names
```

Para guardar nuevos data frames en una zona<sz> 

```python
from mutuazones import sz

df_clientes = sz.load_df('clientes')
 ...
sz.save_df('clientes_con_coche')
```

## Ejecución del los test

Se requiere instalar las librerías dependientes.

```bash
python -m pip install -r requirements.txt
```

Así como conectarse a una BD con la LZ ya creada.

Para ello utilizar e fichero .envrc (con dirp) o suministrar las credenciales en los propios test.

## Publicar nueva versión

Para publicar nueva versión en Pypi ejecutar los siguientes comandos. El primer genera la distribución correspondiente. El segundo sube/actualiza la distribución en Pypi

```bash
python3 setup.py sdist bdist_wheel
python3 -m twine upload  dist/*
```

Posteriormente, donde se use, actualizar la librería:

```bash
sudo -H pip3 install --upgrade mutuazones
```