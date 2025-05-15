import pandas as pd
import os

def normalizar_texto(serie):
    '''
    Convierte la serie a string, la pone en minúsculas, elimina espacios
    extremos y reemplaza ciertos caracteres.
    '''
    return (serie.astype(str)
                .str.strip()
                .str.lower()
                .str.replace('_', ' ', regex=False)
                .str.replace('-', ' ', regex=False)
                .str.replace(',', '', regex=False)
                .str.replace('$', '', regex=False)
                .str.replace('.00', '', regex=False)
                .str.strip())

def convertir_fecha(fecha_series):
    '''
    Intenta convertir la serie de fechas a datetime usando dos formatos,
    combinando ambos resultados.
    '''
    fmt1 = pd.to_datetime(fecha_series, format='%d/%m/%Y', errors='coerce')
    fmt2 = pd.to_datetime(fecha_series, format='%Y/%m/%d', errors='coerce')
    return fmt1.combine_first(fmt2)

def pregunta_01():
    '''
    Realice la limpieza del archivo 'files/input/solicitudes_de_credito.csv'.
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en 'files/output/solicitudes_de_credito.csv'

    '''

    archivo_entrada = 'files/input/solicitudes_de_credito.csv'
    archivo_salida = 'files/output/solicitudes_de_credito.csv'

    df = pd.read_csv(archivo_entrada, sep=';', index_col=0, encoding='UTF-8')
    
    df.dropna(inplace=True)
    
    df['sexo'] = df['sexo'].str.lower().str.strip()
    df['sexo'] = df['sexo'].apply(lambda x: 'm' if x.startswith('m') else ('f' if x.startswith('f') else x))
    
    df['tipo_de_emprendimiento'] = df['tipo_de_emprendimiento'].str.lower().str.strip()
    
    df['barrio'] = df['barrio'].str.lower().str.replace('_', ' ', regex=False).str.replace('-', ' ', regex=False)
    
    df['idea_negocio'] = df['idea_negocio'].str.lower().str.replace('_', ' ', regex=False).str.replace('-', ' ', regex=False).str.strip()
    
    df['monto_del_credito'] = (df['monto_del_credito']
                               .str.strip()
                               .str.replace('$', '', regex=False)
                               .str.replace(',', '', regex=False)
                               .str.replace('.00', '', regex=False))
    df['monto_del_credito'] = pd.to_numeric(df['monto_del_credito'], errors='coerce')
    
    df['línea_credito'] = df['línea_credito'].str.lower().str.replace('_', ' ', regex=False).str.replace('-', ' ', regex=False).str.strip()
    
    fecha1 = pd.to_datetime(df['fecha_de_beneficio'], format='%d/%m/%Y', errors='coerce')
    fecha2 = pd.to_datetime(df['fecha_de_beneficio'], format='%Y/%m/%d', errors='coerce')
    df['fecha_de_beneficio'] = fecha1.combine_first(fecha2)
    
    df['comuna_ciudadano'] = pd.to_numeric(df['comuna_ciudadano'], errors='coerce', downcast='integer')
    
    df['estrato'] = df['estrato'].astype(int)
    
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    
    df = df[df['sexo'].isin(['m', 'f'])]
    
    os.makedirs(os.path.dirname(archivo_salida), exist_ok=True)
    
    df.to_csv(archivo_salida, sep=';', index=False)

if __name__ == '__main__':
    print(pregunta_01())