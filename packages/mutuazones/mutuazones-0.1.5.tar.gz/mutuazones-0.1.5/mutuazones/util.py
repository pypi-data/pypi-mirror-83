# def sage(df_siniesage):
#     """Devuelve el dataframe resultante de la limpieza de siniesage, de una anualidad concreta"""

#     import pandas as pd
#     import numpy as np

#     col = ['tipo_reg',
#        't_pol',
#        't_pdo',
#        'pnb',
#        'imp_sto',
#        'tot_sto',
#        'tot_plz',
#        'sexo',
#        'antig_carnet',
#        'edad',
#        'primer_efecto',
#        'anualidades',
#        'antiguedad_poliza',
#        'antiguedad_matric',
#        'tipo_cob',
#        'zona',
#        'categoria',
#        'id_hoja',
#        'bns100',
#        'bns_inicial',
#        'tomador_id',
#        'tomador_nif',
#        'nro_pol',
#        'tot_polizas_div',
#        'tot_polizas_veh',
#        'flota',
#        'fch_anula']

#     datos = df_siniesage[col]
#     # Realizamos el filtro de las cancelaciones
#     datos = datos.loc[datos.tipo_reg != 'CAN']
#     # Realizamos las agrupaciones de los campos calculados indexado por póliza
#     # Realizamos el cálculo de los valores acumulados: pnb,imp_sto,tot_sto,tot_plz
#     datos_plz = pd.pivot_table(datos,
#                           index = ['nro_pol'],
#                           values = ['pnb','imp_sto','tot_sto','tot_plz'],
#                           aggfunc = np.sum,
#                           fill_value = 0,
#                           margins = True)

#     # no añadimos los campos tot_polizas_veh y tot_polizas_div por evitar errores concepto cliente o duplicidad pólizas

#     #Seleccionamos las pólizas vivas
#     #No tener en cuenta las pólizas que sólo tienen registro de APE -> solo vamos a contar con pólizas con periodos PRD&RNV
#     pol_vivas = pd.DataFrame(datos['nro_pol'].loc[(datos.tipo_reg == 'PLZ') & (datos.t_pdo!= 'APE') & (datos.fch_anula.isnull())]).drop_duplicates()

#     # Creamos el Merge
#     dataset = pd.merge(pol_vivas,datos_plz,how = 'left',left_on = pol_vivas.nro_pol, right_on = datos_plz.index).drop('key_0',axis=1)

#     col_desc = ['tipo_reg',
#        't_pol',
#        't_pdo',
#        'sexo',
#        'antig_carnet',
#        'edad',
#        'primer_efecto',
#        'anualidades',
#        'antiguedad_poliza',
#        'antiguedad_matric',
#        'tipo_cob',
#        'zona',
#        'categoria',
#        'id_hoja',
#        'bns100',
#        'bns_inicial',
#        'tomador_id',
#        'tomador_nif',
#        'nro_pol',
#        'tot_polizas_div',
#        'tot_polizas_veh',
#        'flota',
#        'fch_anula']

#     # Parte PLZ sin APE para la descripción de la póliza
#     desc_plz = datos[col_desc].loc[(datos.tipo_reg == 'PLZ') & (datos.t_pdo != 'APE') & (datos.fch_anula.isnull())].drop_duplicates()
#     # Realizamos el merge
    
#     dataset = pd.merge(dataset,desc_plz,how = 'left',left_on = dataset.nro_pol, right_on = desc_plz.nro_pol).drop('key_0',axis=1)

#     # Reindexamos y eliminamos la duplicidad del campo póliza
#     df = dataset
#     df= df.set_index('nro_pol_x')
#     df.index.names = ['nro_pol']
#     df = df.drop('nro_pol_y',axis=1)

#     # Creo la variable póliza viva
#     df['Churn'] = 0

#     #################################################### CANCELACIONES ##############################################
#     #Creamos la bbdd de cancelaciones

#     # Seleccionamos las columnas

#     datos_can = df_siniesage[col]

#     # Creamos la tabla de canceladas
#     canceladas = datos_can.loc[datos_can.tipo_reg == 'CAN']

#     # Realizamos las agrupaciones de los campos calculados indexado por póliza
#     # Realizamos el cálculo de los valores acumulados: pnb,imp_sto,tot_sto,tot_plz

#     datos_can_agg = pd.pivot_table(canceladas,
#                           index = ['nro_pol'],
#                           values = ['pnb','imp_sto','tot_sto','tot_plz'],
#                           aggfunc = np.sum,
#                           fill_value = 0,
#                           margins = True)

#     #Seleccionamos las pólizas vivas
#     #No tener en cuentalas pólizas que sólo tienen registro de APE -> solo vamos a contar con pólizas con periodos PRD&RNV

#     pol_can = pd.DataFrame(canceladas['nro_pol']).drop_duplicates()

#     # Creamos el Merge

#     dataset_can = pd.merge(pol_can,datos_can_agg,how = 'left',left_on = pol_can.nro_pol, right_on = datos_can_agg.index).drop('key_0',axis=1)

#     # Realizamos el cambio de signo

#     dataset_can['pnb'] = (-1)*dataset_can['pnb']
#     dataset_can['imp_sto'] = (-1)*dataset_can['imp_sto']
#     dataset_can['tot_plz'] = (-1)*dataset_can['tot_plz']
#     dataset_can['tot_sto'] = (-1)*dataset_can['tot_sto']

#     # Añadimos la descripción del riesgo usando "canceladas"

#     desc_can = canceladas[col_desc]
#     dataset_can = pd.merge(dataset_can,desc_can,how = 'left',left_on = dataset_can.nro_pol, right_on = desc_can.nro_pol).drop('key_0',axis=1)

#     # Reindexamos y eliminamos la duplicidad del campo póliza
#     df_can = dataset_can
#     df_can= df_can.set_index('nro_pol_x')
#     df_can.index.names = ['nro_pol']
#     df_can = df_can.drop('nro_pol_y',axis=1)

#     # Creo la variable póliza viva
#     df_can['Churn'] = 1

#     ## Creamos el dataset completo con df y df_can

#     return pd.concat([df,df_can])