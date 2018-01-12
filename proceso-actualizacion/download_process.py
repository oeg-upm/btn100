"""
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
  This file is part of the BTN100 catalogue transformation project:
    http://centrodedescargas.cnig.es/CentroDescargas/buscadorCatalogo.do?codFamilia=BT100
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
    LICENCE INFORMATION:

    Esta obra está bajo un Licencia Creative Commons Atribución 4.0 Internacional (http://creativecommons.org/licenses/by/4.0/).

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

"""

__author__ = 'Miguel Angel Garcia (ma-garcia)'

import configparser
import zipfile
import urllib.request
import os
import subprocess
import logging
import filecmp

# create logger with 'spam_application'
logger = logging.getLogger('download_process')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('download_process.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


# Read config file from execution folder
config = configparser.ConfigParser()
config.read('settings.conf')

# URLS
urls = config.get('URLS', 'urls').split(',')

# IDS to be excluded
excluded_ids = config.get('IDS', 'excluded_ids').split(',')
graph_id = config.get('IDS', 'graph_id')

# WORKING DIRS
temp_dir = config.get('BASEDIRS', 'tempDir')
work_dir = config.get('BASEDIRS', 'workDir')
geokettle_dir = config.get('BASEDIRS', 'geokettle')
github_dir = config.get('BASEDIRS', 'githubDir')
virtuoso_dir = config.get('BASEDIRS', 'virtuosoDir')
sameas_dir = config.get('BASEDIRS', 'sameAsDir')

# VIRTUOSO DATA
userVirt = config.get('VIRTUOSO', 'user')
passVirt = config.get('VIRTUOSO', 'password')
isqlPort = config.get('VIRTUOSO', 'isqlPort')

# GITHUB DATA
update = config.get('GITHUB', 'update')
user_git = config.get('GITHUB', 'user_git')
pass_git = config.get('GITHUB', 'pass_git')
git_rep = config.get('GITHUB', 'git_rep')
git_dir = config.get('GITHUB', 'git_dir')


# retrieve name of the folder from url
def folder_name(url):
    init = url.rindex('/')+1
    end = url.rindex('.')
    name = url[init:end]
    return name


# download zip file and extract to temp folder
def download_extract(url, name):
    try:
        print('Downloading '+str(url))
        urllib.request.urlretrieve(url, temp_dir + name + '.zip')
        zip_ref = zipfile.ZipFile(temp_dir + name + '.zip') # create zipfile object
        zip_ref.extractall(temp_dir + name) # extract file to dir
        zip_ref.close()
        os.remove(temp_dir + name + '.zip')
        return 0
    except:
        print('Error downloading '+str(url))
        return 1
    raise


logger.info("================================= START PROCESS =================================")
os.chdir(github_dir)
if (update == 'Y'):
    res = subprocess.getoutput('git pull -v --progress  "origin" ')
    logger.info('Actualizamos el directorio GIT-->'+str(res))
    print('pullres-->'+str(res))

logger.info("Procesamos las siguientes URLs:"+str(urls))
print("Procesamos las siguientes URLs:"+str(urls))
folders = []
errors = []
for url in urls:
    name = folder_name(url)
    if not download_extract(url, name):
        folders.append(name)
    else:
        errors.append(name)

if errors.__sizeof__()>0:
    logger.error("Error downloading the following elements:")
    for error in errors:
        logger.error(error)


# extract element ids to be processed from folders list
def extract_id(folders):
    ids = []
    for folder in folders:
        list = os.listdir(temp_dir + folder)
        for elem in list:
            id = elem[:elem.rindex('.')]
            if not ids.__contains__((id,folder)):
                ids.append((id,folder))

    return ids


ids = extract_id(folders)
logger.info("Procesamos los siguientes elementos: " + str(ids))
print("Procesamos los siguientes elementos-->" + str(ids))


# function to decided if an id has to be processed
def must_be_updated(f1, f2):
    if not os.path.exists(f2) or filecmp.cmp(f1, f2, False):
        return True
    else:
        return False


# Check which IDs must be updated, those who shape file is different from the downloaded version
# or those who shape file is not present in the working directory
to_be_updated = []
for id in ids:

    # if filecmp.cmp(temp_dir+id[1] + '/'+id[0] + '.shp', work_dir+id[0] + '/'+id[0] + '.shp', False):
    if must_be_updated(temp_dir+id[1] + '/'+id[0] + '.shp', work_dir+id[0] + '/'+id[0] + '.shp'):
        command = 'mv ' + temp_dir + id[1] + '/' + id[0] + '.* ' + work_dir + id[0]
        print(command)
        status = subprocess.getstatusoutput(command)
        print(status)
        to_be_updated.append(id[0])
        command = 'rm ' + temp_dir + id[1] + '/' + id[0] + '.* '
        print(status)

logger.info("Elementos a procesar-->"+str(to_be_updated))

# Remove temp folders
for folder in folders:
    command = 'rm -r ' + temp_dir + folder
    print(command)
    status = subprocess.getstatusoutput(command)
    print(status)


# Extract the ktr files in the working folder
def extract_ktr(folder):
    ktrs = []
    print(work_dir + folder)
    list = os.listdir(work_dir + folder)
    for elem in list:
        if elem.__contains__('.ktr'):
            ktrs.append(elem)
    return ktrs


os.chdir(geokettle_dir)
print(os.listdir(geokettle_dir))
ids_updated = []
for id in to_be_updated:

    # Generate ttl files with Geokettle tool
    ktrs = extract_ktr(id)
    print('Ficheros ktr para [' + id + ']===>'+str(ktrs))
    logger.info('Ficheros ktr para [' + id + ']===>'+str(ktrs))
    to_update = 0
    for ktr in ktrs:
        output = subprocess.getstatusoutput(geokettle_dir+'/pan.sh -file="'+work_dir+id+'/'+ktr+'" -level=Detailed -norep')
        print('outputGK['+ktr+']-->'+str(output[0]))
        to_update = to_update or output[0]

    if (not to_update):
        ids_updated.append(id)
        # Update Virtuoso information
        os.chdir(virtuoso_dir)
        logger.info('Empezamos la carga de--->'+str(id))
        status = subprocess.getstatusoutput('bin/isql -S '+isqlPort+' -U '+userVirt+' -P '+passVirt+' verbose=on banner=off prompt=off echo=ON errors=stdout exec="DELETE FROM RDF_QUAD WHERE G = DB.DBA.RDF_MAKE_IID_OF_QNAME (\'' + graph_id + id + '\'); DELETE FROM DB.DBA.LOAD_LIST as d WHERE d.ll_graph=\'' + graph_id + id + '\'"')
        logger.info("DeleteGraph-->"+str(status))

        #/opt/virtuoso-7/default/bin/isql -S "$1" -U dba verbose=on banner=off prompt=off echo=ON errors=stdout exec="ld_dir_all(('$2'), '*.ttl', '$3'); rdf_loader_run(); checkpoint;"
        status = subprocess.getstatusoutput('bin/isql -S '+isqlPort+' -U '+userVirt+' -P '+passVirt+' verbose=on banner=off prompt=off echo=ON errors=stdout exec="ld_dir_all((\''+work_dir+id+'\'), \'*.ttl\', \'' + graph_id + id + '\'); rdf_loader_run(); checkpoint;"')
        logger.info("LoadFolder-->"+str(status))

        # if shape file is bigger than 100 MB, it is splitted in files of 90MB to be able of loading them in GitHub
        # files larger than 100MB can't be uploaded to GitHub unless GLFS is used. GLFS is a pay service
        if id in excluded_ids:
            os.chdir(work_dir+id)
            cpsplit = subprocess.getstatusoutput('split --bytes=90m '+id+'.shp')
            print('cpsplit-->'+str(cpsplit))
            os.chdir(geokettle_dir)

        # Move files generated from working directory to github directory
        cpres_text = 'cp -r '+work_dir+id+' ' + github_dir + git_dir
        print("CPRES-->" + cpres_text)
        cpres = subprocess.getstatusoutput(cpres_text)
        print("cpres-->"+str(cpres))
        if id in excluded_ids:
            cprm = subprocess.getstatusoutput('rm ' + github_dir + git_dir + id + '/' + id + '.shp')
            print('cprm-->'+str(cprm))
    else:
        logger.error('Error procesando los ficheros ktr del ID--->'+str(id))
        print('Error procesando los ficheros ktr del ID--->'+str(id))


    logger.info('Terminado el procesamiento de--->'+str(id))
    print('Terminado el procesamiento de--->'+str(id))

# sameAs files are loaded after the loading process
os.chdir(virtuoso_dir)
logger.info('Empezamos la carga de los ficheros sameAs')
status = subprocess.getstatusoutput('bin/isql -S '+isqlPort+' -U '+userVirt+' -P '+passVirt+' verbose=on banner=off prompt=off echo=ON errors=stdout exec="DELETE FROM RDF_QUAD WHERE G = DB.DBA.RDF_MAKE_IID_OF_QNAME (\'' + graph_id +'sameas\'); DELETE FROM DB.DBA.LOAD_LIST as d WHERE d.ll_graph=\'' + graph_id + 'sameas\'"')
logger.info("DeleteGraphSameAs-->"+str(status))

#/opt/virtuoso-7/default/bin/isql -S "$1" -U dba verbose=on banner=off prompt=off echo=ON errors=stdout exec="ld_dir_all(('$2'), '*.ttl', '$3'); rdf_loader_run(); checkpoint;"
status = subprocess.getstatusoutput('bin/isql -S '+isqlPort+' -U '+userVirt+' -P '+passVirt+' verbose=on banner=off prompt=off echo=ON errors=stdout exec="ld_dir_all((\''+sameas_dir+'\'), \'*.ttl\', \'' + graph_id + 'sameas\'); rdf_loader_run(); checkpoint;"')
logger.info("LoadFolderSameAs-->"+str(status))

# if there are ids to be updated, commit to GitHub repository is made
if ids_updated.__sizeof__()>0 and update == 'Y':
    logger.info("Actualizados los siguientes elementos:"+str(ids_updated))
    print("Actualizados los siguientes elementos:"+str(ids_updated))
    os.chdir(github_dir)
    # res = subprocess.getoutput('git pull -v --progress  "origin" ')
    # print('pullres-->'+str(res))

    resadd = subprocess.getoutput('git add -A')
    print("resadd-->"+str(resadd))

    resadd = subprocess.getoutput('git commit -m "Actualizados los siguientes elementos: ' + str(ids_updated) + '"')
    print("rescommit-->"+str(resadd))

    resadd = subprocess.getoutput('git push https://' + user_git + ':' + pass_git + '@' + git_rep + ' --all')
    print("rescommit-->"+str(resadd))

    logger.info("Actualizado repositorio GitHub")
else:
    logger.info("No hay elementos que actualizar en el repositorio")

logger.info("================================= END PROCESS =================================")
