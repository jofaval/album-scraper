"""
Spanish translations
"""

from typing import Dict


STRINGS: Dict[str, str] = {
    'ERRORS': {
        'GET_PAGE': 'No se ha podido recuperar el contenido de la página: {{url}}',
        'GET_IMG': 'No se ha podido recuperar el contenido de la imagen: {{url}}',
        'INVALID_URL': 'Url para la imagen "{{filename}}" no ha sido encontada o es inválida, URL: {{url}}',
        'IMAGE_DIDNT_DOWNLOAD': 'No se ha podido descargar la imágen {{img}}',
        'PARSE_ERROR': 'Error de parseo',
        'CORRPUT_IMAGE_FOUND': 'Imágen corrupta o faltante encontrada {{chapter}} {{index}}{{extension}} {{filesize}})',
        'INVALID_CHAPTER_URL': 'La URL del capítulo "{{chapter_url}}" no se ha detectado como válida, asegurese de que empieza por http[s]://',
    },
    'CHAPTERS': {
        'GET_ALL': 'Se intentan recuperar todos los capítulos, empezando a partir del: {{start_at}}',
        'CHAPTER_DOWNLOAD_STARTS': 'Se va a descargar el contenido del capítulo {{chapter_url}}',
        # 'TOTAL_CHAPTERS_RETRIEVED': 'Se han recuperado un total de {{total_chapter_links}} enalces'
        'TOTAL_CHAPTERS_RETRIEVED': 'Se ha(n) recuperado un total de {{chapter_links}} capítulo(s)',
        'TOTAL_CORRUPTED_CHAPTERS': 'Capítulos incompletos o corruptos {{total_incomplete_chapters}} capítulo(s)\n {{incomplete_chapters}}',
        'CORRUPT_CHAPTERS_DETECTION':
        "|----------------------------------|\n"
            + "| Detección de capítulos corruptos |\n"
            + "|----------------------------------|\n",
        'PROGRESS_PERCENTAGE': 'Porcentaje de descarga del capítulo ({{title}}), {{percentage}} ({{index}}{{URL_SEPARATOR}}{{total_imgs}})',
    },
    'IMAGES': {
        'IMAGE_SUCCESS': 'Se ha descargado la imagen {{filename}}',
        'FOUND_TOTAL_IMAGES': 'Se ha(n) encontrado {{total_imgs}} imágen(es)',
        'IMAGES_DOWNLOADED': 'Ya se han descargado todas las imágenes del capítulo',
        'NOT_DOWNLOADED': 'No se ha(n) podido descargar {{not_downloaded}} imágen(es)',
        'ANALYZING_IMAGES': 'Analizando las imágenes del capítulo {{chapter}}',
        'IMAGE_ATTEMPT': 'Se intenta descargar la imagen "{{url}}", intento: ({{attempt}}/{{max_retries}})',
    },
    'THREADS': {
        'WAIT_ALL': 'Se espera a que terminen el resto de hilos',
    },
    'UPDATES': {
        'NEWS': 'Las novedades son {{updates}}',
        'DOWNLOAD_PROMPT': '¿Descargar las novedades? Sí=s: ',
        'CHOSEN_OPTION': 'Se ha elegido la opción {{option}}',
        'NOT_DOWNLOADING_NEWS': '\nNo se descargarán las novedades\n',
        'NEWS_DOWNLOADED': '\nSe han descargado las novedades\n',
    }
}
