import itertools
import re
import unicodedata
import pkg_resources
from utils.tokenizacion import tokenizar, destokenizar


def remover_acentos(texto):
    """Quita los acentos (tildes, diéresis, virgulilla) de un texto de entrada. Esta reemplaza \
    cada carácter con acento en el texto por su equivalente sin acento.

    :param texto: (str) Texto al que se le quieren quitar los acentos.
    :return: (str) Texto sin acentos después de la limpieza.
    """
    try:
        texto = unicode(texto, 'utf-8')
    except NameError:
        pass
    texto = unicodedata.normalize('NFD', texto)\
        .encode('ascii', 'ignore')\
        .decode("utf-8")
    return str(texto)

def remover_stopwords(texto, lista_palabras = [], lista_expresiones = [],
        ubicacion_archivo=None, tokenizador=None):
    """Quita las palabras y expresiones determinadas de un texto. Esta función quita del texto de entrada, \
    palabras específicas contenidas en `lista_palabras`, o expresiones de palabras contenidas en `lista_expresiones`.

    :param texto: (str) Texto al cual se le quitarán palabras y expresiones contenidas en `lista_palabras` \
    y `lista_expresiones`.
    :param lista_palabras: (list) Parámetro opcional. Lista de palabras que se quieren quitar del texto. Por ejemplo, \
        la lista `['hola', 'de', 'a']` eliminará esas palabras.
    :param lista_expresiones: (list) Parámetro opcional. Lista de expresiones que se quieren quitar al texto. \
        A diferencia de `lista_palabras`, esta puede contener palabras compuestas. Por ejemplo, \
        ['San juan de Dios', 'Distrito Capital, 'fuente de agua']; esta lista quitará esas palabras \
        compuestas del texto de entrada.
    :param ubicacion_archivo: (str) Valor por defecto: None. Ubicación del archivo plano que contiene la lista de palabras \
        y/o lista de palabras separadas por espacios, comas o saltos de línea. En \
        caso contrario no es necesario especificar los parametros `lista_palabras` y `lista_expresiones`.
    :param tokenizador: Valor por defecto: None. Objeto encargado de la tokenización y detokenización \
        de textos. Si el valor es 'None', se utilizará por defecto una instancia de la clase *TokenizadorNLTK*.        
    :return: (str) Texto sin las palabras y expresiones incluidas en la limpieza.
    """
    if ubicacion_archivo:
        lista_palabras, lista_expresiones = cargar_stopwords(ubicacion_archivo)
    # Quitar las expresiones no deseadas
    for expresion in set(lista_expresiones):
        texto = texto.replace(expresion, ' ')
    # Dejar solo las palabras que no aparecen en la lista de palabras no
    # deseadas
    tokens = tokenizar(texto, tokenizador)
    texto = destokenizar([p for p in tokens if p not in set(lista_palabras)], tokenizador)
    # Reemplaza espacios múltiples por un solo espacio
    texto = re.sub(r" +", " ", texto)
    return texto

def remover_palabras_cortas(texto, n_min):
    """Quita las palabras en el texto con longitud estrictamente menor a `n_min`.

    :param texto: (str) Texto de entrada al que se quitarán las palabras menores a `n_min`.
    :param n_min: (int) Longitud mínima de las palabras aceptadas en el texto de entrada.
    :return: (str) Texto sin las palabras de longitud menor a `n_min`.
    """
    palabras = texto.split(' ')
    return ' '.join([palabra for palabra in palabras if len(palabra) >= n_min])

def limpieza_basica(texto, quitar_numeros=True):
    """Limpieza básica del texto. Esta función realiza una limpieza básica del texto de entrada, \
    transforma todo el texto a letras minúsculas, quita signos de puntuación y caracteres \
    especiales, remueve espacios múltiples dejando solo espacio sencillo y caracteres \
    de salto de línea o tabulaciones.

    :param texto: (str) Texto de entrada al que se le aplicará la limpieza básica.
    :param quitar_numeros: (bool) {True, False} Valor por defecto: True. \
        Indica si desea quitar los números dentro del texto.
    :return: (str) Texto después de la limpieza básica.
    """
    # Texto a minúsculas
    texto = texto.lower()
    # Pone un espacio antes y después de cada signo de puntuación
    texto = re.sub(r"([\.\",\(\)!\?;:])", " \\1 ", texto)
    # Quita caracteres especiales del texto.
    # RegEx adaptada de https://stackoverflow.com/a/56280214
    if quitar_numeros:
        texto = re.sub(r'[^ a-zA-ZÀ-ÖØ-öø-ÿ]+', ' ', texto)
    else:
        texto = re.sub(r'[^ a-zA-ZÀ-ÖØ-öø-ÿ0-9]+', ' ', texto)
    # Reemplaza espacios múltiples por un solo espacio
    texto = re.sub(r" +", " ", texto)
    # Quitar espacios, tabs y enters en los extremos del texto
    texto = texto.strip(' \t\n\r')
    return texto

def limpieza_texto(texto, lista_palabras=[], lista_expresiones=[],
        ubicacion_archivo=None, n_min=0, quitar_numeros=True,
        quitar_acentos=False, tokenizador=None, momento_stopwords='ambos'):
    """Limpieza completa de texto. Esta función hace una limpieza exhaustiva del texto de entrada. \
    Es capaz de quitar palabras y expresiones contenidas en `lista_palabras` y `lista_expresiones`, \
    quita acentos de las palabras, números y palabras de longitud menor a `n_min`.

    :param texto: (str) Texto de entrada al que se le aplicará el proceso de limpieza.
    :param lista_palabras: (list) Parámetro opcional. Lista de palabras que se quieren quitar del texto. Por ejemplo, \
        la lista `['hola', 'de', 'a']` eliminará esas palabras.
    :param lista_expresiones: (list) Parámetro opcional. Lista de expresiones que se quieren quitar al texto. \
        A diferencia de `lista_palabras`, esta puede contener expresiones compuestas. Por ejemplo, \
        ['San juan de Dios', 'Distrito Capital, 'fuente de agua']; esta lista quitará esas expresiones \
        del texto de entrada.
    :param ubicacion_archivo: (str) Valor por defecto: None. Parámetro opcional. Indica la ubicación del archivo \
        plano que contiene la lista de palabras y/o expresiones separadas por comas o saltos de línea. \
        Si se usa este parámetro, no se tendrán en cuenta los parámetros `lista_palabras` y `lista_expresiones`.
    :param n_min: (int) Parámetro opcional. Longitud mínima de las palabras aceptadas en el texto de entrada.
    :param quitar_numeros: (bool) {True, False} Valor por defecto: True. Si `False`, no se quitan los números dentro \
        del texto de entrada
    :param quitar_acentos: (bool) {True, False} Valor por defecto: False. Opción para determinar si se quitan \
        acentos (tildes, diéresis, virgulilla) del texto.
    :param tokenizador: Valor por defecto: None. Objeto encargado de la tokenización y detokenización \
        de textos al momento de quitar stopwords. Si el valor es 'None', se utilizará por defecto una instancia \
        de la clase *TokenizadorNLTK*.
    :param momento_stopwords: (str) {'antes', 'después', 'ambos'} Valor por defecto: 'ambos'. Indica en qué \
        momento remover las *stopwords* del texto. Las opciones son hacerlo antes o después \
        de las demás operaciones de limpieza del texto de entrada, eligiendo los valores "antes" o "después", \
        respectivamente (la función acepta los valores con o sin tildes y/o mayúsculas). También es posible remover \
        stopwords de los textos tanto antes como despúes de las otras operaciones de limpieza, al asignar el valor \
        "ambos" a este parámetro. Cualquier otro valor que se asigne a este parámetro ocasionará que no se haga \
        remoción de stopwords en el texto.
    :return: (str) Texto después de la limpieza completa.
    """
    # Estandarizar parámetro de momento_stopwords
    momento_stopwords = remover_acentos(momento_stopwords).lower()
    # Quitar palabras y expresiones no deseadas. Se hace al texto original porque la palabra/expresión
    # a remover puede tener tildes/mayúsculas/signos o estar compuesta por palabras cortas
    if momento_stopwords in ('antes', 'ambos'):
        texto = remover_stopwords(texto, lista_palabras, lista_expresiones, 
                                ubicacion_archivo, tokenizador)
    # Se verifica si se desean quitar acentos/tildes
    if quitar_acentos:
        texto = remover_acentos(texto)
    # Limpieza básica del texto
    texto = limpieza_basica(texto, quitar_numeros)
    # Quita palabras cortas y palabras pertenecientes a una lista específica
    texto = remover_palabras_cortas(texto, n_min)
    # Se quitan stopwords de nuevo, por si habían palabras que después de su limpieza quedan en
    # la lista de palabras/expresiones no deseadas
    if momento_stopwords in ('despues', 'ambos'):
        texto = remover_stopwords(texto, lista_palabras, lista_expresiones, 
                                ubicacion_archivo, tokenizador)
    return texto

def limpiar_extremos(texto):
    """Quita los espacios presentes al inicio y al final de una cadena de texto.

    :param texto: (str) Cadena de texto de entrada.
    :return: (str) Cadena de texto sin espacios en el inicio y en el final.
    """
    return texto[::-1].rstrip()[::-1].rstrip()

def quitar_repetidos(texto, sep='|', remover_espacios=True):
    """Función para quitar frases o palabras repetidas que están separadas por un \
    caracter en específico.

    :param texto: (str) Texto de entrada.
    :param sep: (str) Valor por defecto: '|'. Separador determinado para encontrar palabras repetidas.
    :param remover_espacios: (bool) {True, False} Valor por defecto: True. Si True quita los espacios \
        presentes al inicio y al final de una palabra.
    :return: (str) Texto sin palabras o expresiones repetidas.
    """
    lista = texto.split(sep)
    if remover_espacios:
        lista = [limpiar_extremos(i) for i in lista]
    # Para preservar el orden de aparición. Tomado de https://stackoverflow.com/a/58666031
    seen = set()
    lista = [i for i in lista if not (i in seen or seen.add(i))]
    return ' '.join(lista)

def cargar_stopwords(ubicacion_archivo, encoding='utf8'):
    """Función para cargar las listas de palabras y expresiones que se desean \
    eliminar de un texto a partir de un archivo plano.

    :param ubicacion_archivo: (str) Ubicación del archivo plano que contiene la lista de palabras \
        y/o lista de palabras separadas por espacios, comas o saltos de línea.
    :param encoding: (str) Valor por defecto 'utf-8'. Codificación del archivo de texto. 
    :return: (tuple) Tupla que contiene: |br|

        |ul|  |li| lista_palabras (list): Lista que contiene las palabras que se desean quitar en un texto. |/li|
        |li| lista_expresiones (list): Lista que contiene las expresiones que se desean quitar de un texto. |/li|  |/ul|
    """
    lista_palabras = []
    lista_expresiones = []
    with open(ubicacion_archivo, encoding=encoding) as fp:
        line = fp.readline()
        while line:
            linea = line.strip().split(',')
            for i in linea:
                i = limpiar_extremos(i)
                if len(i.split(' ')) > 1:
                    lista_expresiones.append(i)
                else:
                    lista_palabras.append(i)
            line = fp.readline()
    return lista_palabras, lista_expresiones

def lista_stopwords(lenguaje='es'):
    """Genera una lista de stopwords (palabras que se quieren quitar de un texto). \
    Función que genera una lista de stopwords de un idioma predeterminado.

    :param lenguaje: (str) Valor por defecto: 'es' (Español). Define el lenguaje de las stopwords. \
        Para mayor información, consultar la sección de :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`.
    :return: (list) Lista de palabras stopwords del idioma seleccionado.
    """
    from lenguajes import definir_lenguaje
    lenguaje = definir_lenguaje(lenguaje, False)

    from nltk.corpus import stopwords
    try:
        sw = stopwords.words(lenguaje)
    except:
        import nltk
        nltk.download("stopwords") 
        sw = stopwords.words(lenguaje)
    # Si se quieren en español, se intenta sacar las stopwords
    # desde la lista predfinida que viene con la librería
    if lenguaje == 'spanish':
        try:
            ruta = pkg_resources.resource_filename(
                __name__, 'data/listas_stopwords/sw_es.txt')
            sw = cargar_stopwords(ruta, 'latin-1')[0]
        except BaseException:
            pass
    # Quitar elemento vacío de la lista, si está
    if '' in sw:
        sw.remove('')   
    # Devolver stopwords
    return sw

def lista_nombres(tipo='todos'):
    """Genera lista de nombres más comunes del español. Retorna lista con los nombres \
    más comunes, tanto para hombre y mujer del idioma español. La función permite generar \
    lista de nombres solo de mujeres o solo de hombres con el parámetro `tipo`.

    :param tipo: (str) {'todos', 'mujeres', 'hombres'} Valor por defecto: 'todos'. \
        Permite generar una lista de nombres de: solo mujeres (`tipo='mujeres'`), \
        solo nombres de hombres (`tipo='hombres'`) o ambos (`tipo='todos'`).
    :return: (list) Lista de nombres en español.
    """
    if tipo.lower() in ['m', 'masculino', 'hombre', 'hombres']:
        ruta = pkg_resources.resource_filename(
            __name__, 'data/listas_stopwords/nombres_hombres.txt')
        return cargar_stopwords(ruta)
    elif tipo.lower() in ['f', 'femenino', 'mujer', 'mujeres']:
        ruta = pkg_resources.resource_filename(
            __name__, 'data/listas_stopwords/nombres_mujeres.txt')
        return cargar_stopwords(ruta)
    elif tipo == 'todos':
        ruta = pkg_resources.resource_filename(
            __name__, 'data/listas_stopwords/nombres_ambos.txt')
        lista_todos = list(cargar_stopwords(ruta))
        lista_hombres = lista_nombres('hombre')
        lista_mujeres = lista_nombres('mujer')
        for i in range(2):
            lista_todos[i] += lista_hombres[i] + lista_mujeres[i]
            lista_todos[i] = sorted(list(set(lista_todos[i])))

        return lista_todos[0], lista_todos[1]
    else:
        print(
            'Por favor ingresar un tipo válido de nombres ("hombres", "mujeres" o "todos").')
        return [], []

def lista_apellidos():
    """Genera lista de apellidos más comunes del español.

    :return: (list) Lista de apellidos más comunes del español.
    """
    ruta = pkg_resources.resource_filename(
        __name__, 'data/listas_stopwords/apellidos.txt')
    return cargar_stopwords(ruta)

def lista_geo_colombia(tipo='todos'):
    """Genera lista de nombres de municipios y departamentos de Colombia.

    :param tipo: (str) {'todos', 'municipios', 'departamentos'} Valor por defecto 'todos'. \
        'todos' genera una lista de nombres de municipios y departamentos de Colombia, \
        'municipios' genera nombres solo de municipios y 'departamentos' genera nombres \
        solo de departamentos.
    :return: (list) Lista de nombres de municipios, departamentos o ambos.
    """
    ruta_mun = pkg_resources.resource_filename(
        __name__, 'data/listas_stopwords/municipios_col.txt')
    ruta_dep = pkg_resources.resource_filename(
        __name__, 'data/listas_stopwords/departamentos_col.txt')
    if tipo == 'todos':
        palabras = sorted(list(set(cargar_stopwords(ruta_mun)[
            0] + cargar_stopwords(ruta_dep)[0])))
        expresiones = sorted(list(set(cargar_stopwords(ruta_mun)[
            1] + cargar_stopwords(ruta_dep)[1])))
        return palabras, expresiones
    elif tipo.lower() in ['municipios', 'mun', 'm']:
        return cargar_stopwords(ruta_mun)
    elif tipo.lower() in ['departamentos', 'dep', 'd']:
        return cargar_stopwords(ruta_dep)
    else:
        print('Por favor ingresar un tipo válido de lugares ("municipios", "departamentos" o "todos").')
        return [], []