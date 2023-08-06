"""
Common utilities for DiaParser resources.
"""

import os
import requests
from tqdm import tqdm
from pathlib import Path
import json
import hashlib
import zipfile
import shutil
import logging

from diaparser import __models_version__

logger = logging.getLogger('diaparser')

RELEASE = 'v1.0'
DOWNLOAD_URL = 'https://github.com/Unipisa/diaparser/archive/'
UPLOAD_URL = f'https://uploads.github.com/repos/Unipisa/diaparser/releases/{RELEASE}/assets'
UPLOAD_COMMAND = f'curl -X POST -H "Content-Type: application/zip" {UPLOAD_URL}'

DEFAULT_RESOURCES_URL = DOWNLOAD_URL
DEFAULT_RESOURCES_VERSION = __models_version__
DEFAULT_MODEL_URL = DOWNLOAD_URL

# set home dir for default
HOME_DIR = str(Path.home())
DEFAULT_MODEL_DIR = os.path.join(HOME_DIR, '.cache/diaparser')

# given a language and models path, build a default configuration
def build_default_config(resources, lang, dir, load_list):
    default_config = {}
    for item in load_list:
        processor, package, dependencies = item

        # handle case when processor variants are used
        if package in PROCESSOR_VARIANTS[processor]:
            default_config[f"{processor}_with_{package}"] = True
        # handle case when identity is specified as lemmatizer
        elif processor == LEMMA and package == 'identity':
            default_config[f"{LEMMA}_use_identity"] = True
        else:
            default_config[f"{processor}_model_path"] = os.path.join(
                dir, lang, processor, package + '.pt'
            )

        if not dependencies: continue
        for dependency in dependencies:
            dep_processor, dep_model = dependency
            default_config[f"{processor}_{dep_processor}_path"] = os.path.join(
                dir, lang, dep_processor, dep_model + '.pt'
            )

    return default_config

def ensure_dir(dir):
    """
    Create dir in case it does not exist.
    """
    Path(dir).mkdir(parents=True, exist_ok=True)

def get_md5(path):
    """
    Get the MD5 value of a path.
    """
    data = open(path, 'rb').read()
    return hashlib.md5(data).hexdigest()

def unzip(dir, filename):
    """
    Fully unzip a file `filename` that's in a directory `dir`.
    """
    logger.debug(f'Unzip: {dir}/{filename}...')
    with zipfile.ZipFile(os.path.join(dir, filename)) as f:
        f.extractall(dir)

def get_root_from_zipfile(filename):
    """
    Get the root directory from a archived zip file.
    """
    try:
        zf = zipfile.ZipFile(filename, "r")
    except:
        raise Exception(f"Failed loading zip file at {filename}.")
    assert len(zf.filelist) > 0, \
        f"Zip file at f{filename} seems to be corrupted. Please check it."
    return os.path.dirname(zf.filelist[0].filename)

def file_exists(path, md5):
    """
    Check if the file at `path` exists and match the provided md5 value.
    """
    return os.path.exists(path) and get_md5(path) == md5

def download_file(url, path):
    """
    Download a URL into a file as specified by `path`.
    """
    verbose = logger.level in [0, 10, 20]
    r = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        file_size = int(r.headers.get('content-length'))
        default_chunk_size = 131072
        desc = 'Downloading ' + url
        with tqdm(total=file_size, unit='B', unit_scale=True, \
            disable=not verbose, desc=desc) as pbar:
            for chunk in r.iter_content(chunk_size=default_chunk_size):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    pbar.update(len(chunk))

def request_file(url, path, md5=None):
    """
    A complete wrapper over download_file() that also make sure the directory of
    `path` exists, and that a file matching the md5 value does not exist.
    Args:
        url: of file to retrieve.
        path: where to store result.
        md5: the ecpected md5 of the file.
    """
    ensure_dir(Path(path).parent)
    if file_exists(path, md5):
        logger.info(f'File exists: {path}.')
        return
    download_file(url, path)
    assert(not md5 or file_exists(path, md5))

def maintain_processor_list(resources, lang, package, processors):
    processor_list = {}
    # resolve processor models
    if processors:
        logger.debug(f'Processing parameter "processors"...')
        for key, value in processors.items():
            assert(key in PIPELINE_NAMES)
            assert(isinstance(key, str) and isinstance(value, str))
            # check if keys and values can be found
            if key in resources[lang] and value in resources[lang][key]:
                logger.debug(f'Found {key}: {value}.')
                processor_list[key] = value
            # allow values to be default in some cases
            elif key in resources[lang]['default_processors'] and value == 'default':
                logger.debug(
                    f'Found {key}: {resources[lang]["default_processors"][key]}.'
                )
                processor_list[key] = resources[lang]['default_processors'][key]
            # allow processors to be set to variants that we didn't implement
            elif value in PROCESSOR_VARIANTS[key]:
                logger.debug(
                    f'Found {key}: {value}. '
                    f'Using external {value} variant for the {key} processor.'
                )
                processor_list[key] = value
            # allow lemma to be set to "identity"
            elif key == LEMMA and value == 'identity':
                logger.debug(
                    f'Found {key}: {value}. Using identity lemmatizer.'
                )
                processor_list[key] = value
            # not a processor in the officially supported processor list
            elif key not in resources[lang]:
                logger.debug(
                    f'{key}: {value} is not officially supported by Stanza, '
                    f'loading it anyway.'
                )
                processor_list[key] = value
            # cannot find the package for a processor and warn user
        else:
                logger.warning(
                    f'Can not find {key}: {value} from official model list. '
                    f'Ignoring it.'
                )
    # resolve package
    if package:
        logger.debug(f'Processing parameter "package"...')
        if package == 'default':
            for key, value in resources[lang]['default_processors'].items():
                if key not in processor_list:
                    logger.debug(f'Found {key}: {value}.')
                    processor_list[key] = value
        else:
            flag = False
            for key in PIPELINE_NAMES:
                if key not in resources[lang]: continue
                if package in resources[lang][key]:
                    flag = True
                    if key not in processor_list:
                        logger.debug(f'Found {key}: {package}.')
                        processor_list[key] = package
                    else:
                        logger.debug(
                            f'{key}: {package} is overwritten by '
                            f'{key}: {processors[key]}.'
                        )
            if not flag: logger.warning((f'Can not find package: {package}.'))
    processor_list = [[key, value] for key, value in processor_list.items()]
    processor_list = sort_processors(processor_list)
    return processor_list

def set_logging_level(logging_level, verbose):
    # Check verbose for easy logging control
    if verbose == False:
        logging_level = 'ERROR'
    elif verbose == True:
        logging_level = 'INFO'

    # Set logging level
    logging_level = logging_level.upper()
    all_levels = ['DEBUG', 'INFO', 'WARNING', 'WARN', 'ERROR', 'CRITICAL', 'FATAL']
    if logging_level not in all_levels:
        raise Exception(
            f"Unrecognized logging level for pipeline: "
            f"{logging_level}. Must be one of {', '.join(all_levels)}."
        )
    logger.setLevel(logging_level)
    return logging_level

def process_pipeline_parameters(lang, dir, package, processors):
    # Check parameter types and convert values to lower case
    if isinstance(lang, str):
        lang = lang.strip().lower()
    elif lang is not None:
        raise Exception(
            f"The parameter 'lang' should be str, "
            f"but got {type(lang).__name__} instead."
        )

    if isinstance(dir, str):
        dir = dir.strip()
    elif dir is not None:
        raise Exception(
            f"The parameter 'dir' should be str, "
            f"but got {type(dir).__name__} instead."
        )

    if isinstance(package, str):
        package = package.strip().lower()
    elif package is not None:
        raise Exception(
            f"The parameter 'package' should be str, "
            f"but got {type(package).__name__} instead."
        )

    if isinstance(processors, str):
        # Special case: processors is str, compatible with older verson
        processors = {
            processor.strip().lower(): package \
                for processor in processors.split(',')
        }
        package = None
    elif isinstance(processors, dict):
        processors = {
            k.strip().lower(): v.strip().lower() \
                for k, v in processors.items()
        }
    elif processors is not None:
        raise Exception(
            f"The parameter 'processors' should be dict or str, "
            f"but got {type(processors).__name__} instead."
        )

    return lang, dir, package, processors

# main download function
def download(
        lang='en',
        dir=DEFAULT_MODEL_DIR,
        package='default',
        processors={},
        logging_level='INFO',
        verbose=None,
        resources_url=DEFAULT_RESOURCES_URL,
        resources_version=DEFAULT_RESOURCES_VERSION,
        model_url=DEFAULT_MODEL_URL
    ):
    # set global logging level
    set_logging_level(logging_level, verbose)

    # Download resources.json to obtain latest packages.
    logger.debug('Downloading resource file...')
    # make request
    pretrained_path = os.path.join(dir, 'pretrained.json')
    request_file(
        f'{resources_url}/resources_{resources_version}.json',
        pretrained_path)
    # unpack results
    try:
        models = json.load(open(pretrained_path))
    except:
        raise Exception(
            f'Cannot load model list. Please check your network connection, '
            f'or provided resource url and resource version.'
        )
    if lang not in models:
        raise Exception(f'Unsupported language: {lang}.')
    if 'alias' in models[lang]:
        logger.info(f'"{lang}" is an alias for "{models[lang]["alias"]}"')
        lang = models[lang]['alias']
    lang_name = models[lang].get'lang_name', '')

    # Default: download zipfile and unzip
    logger.info(f'Downloading model for language: {lang} ({lang_name})...')
    request_file(
        f'{url}/{models_version}/{lang}.zip',
        os.path.join(dir, lang, '.zip'),
        md5=models[lang]['md5']
    )
    unzip(os.path.join(dir, lang), 'default.zip')
    # Customize: maintain download list
    else:
        download_list = maintain_processor_list(
            models, lang, package, processors
        )
        download_list = add_dependencies(models, lang, download_list)
        download_list = flatten_processor_list(download_list)
        download_table = make_table(['Processor', 'Package'], download_list)
        logger.info(
            f'Downloading these customized packages for language: '
            f'{lang} ({lang_name})...\n{download_table}'
        )

        # Download packages
        for key, value in download_list:
            try:
                request_file(
                    f'{url}/{models_version}/{lang}/{key}/{value}.pt',
                    os.path.join(dir, lang, key, f'{value}.pt'),
                    md5=models[lang][key][value]['md5']
                )
            except KeyError as e:
                raise Exception(
                    f'Cannot find the following processor and model name combination: '
                    f'{key}, {value}. Please check if you have provided the correct model name.'
                ) from e
    logger.info(f'Finished downloading models and saved to {dir}.')


TOKEN='390e8e11b748bd1f6eeb6847507e7102d4046dc7'

def upload(path, owner='Unipisa', repo='diaparser', version='v1.0', token=TOKEN):
    name = os.path.basename(path)
    GH_ASSET=f"https://uploads.github.com/repos/{owner}/{repo}/releases/{version}/assets?name={name}"
    curl = f'curl --data-binary @"{path}" -H "Authorization: token {token}" -H "Content-Type: application/zip" {GH_ASSET}'
    subprocess.exec(curl)

# examples
# Upload:
# curl --data-binary @/tmp/it_isdt.dbmdz-xxl.zip -H 'Authorization: token 390e8e11b748bd1f6eeb6847507e7102d4046dc7' -H 'Content-Type: application/octet-stream' https://uploads.github.com/repos/Unipisa/diaparser/releases/32726187/assets?name=it_isdt.dbmdz-xxl.zip
# List:
# curl -X GET -H 'Accept: application/vnd.github.v3+json' https://api.github.com/repos/Unipisa/diaparser/releases/32726187/assets
# Delete:
# curl -X DELETE -H 'Authorization: token 390e8e11b748bd1f6eeb6847507e7102d4046dc7' -H 'Accept: application/vnd.github.v3+json' https://api.github.com/repos/Unipisa/diaparser/releases/assets/27145683
