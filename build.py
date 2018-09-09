import argparse
import hashlib
import os
import re
import subprocess
import sys
import shutil
from datetime import date
import requests

def computeStringTosha256(value):
    m = hashlib.sha256()
    m.update(value)
    return m.hexdigest()

def createFolder(path='output/', name=''):
    directory = path + name
    if not os.path.exists(directory):
        os.makedirs(directory)

def copyFolder(src, dst):
     shutil.copytree(src, dst)

def copyFile(src, dst):
    shutil.copy2(src, dst)

def readFileAsString(src):
    return open(src, 'r').read()

def writeFile(text, path):
    text_file = open(path, "w")
    text_file.write(text)
    text_file.close()

def pyminifier(path):
    return subprocess.check_output(['pyminifier', '--replacement-length=50', '--obfuscate', path])

def removeFolder(path):
    if os.path.exists(path):
        shutil.rmtree(path)

SECRET_KEY = '209jedjslcasjkposaipajclamclja;c'
CLIENT_URL = 'https://client-ingestion-pubsub-dot-panacea-1.appspot.com/remote_update'

def main():

    parser=argparse.ArgumentParser(
        description='''Build Script, this script will generate all the requirement to create the proper files to deployment ''',
        epilog="""All's well that ends well.""")
    parser.add_argument('--credentials', type=str, default=None, help='Path to json credentials JSON file')
    parser.add_argument('--customer_id', type=int, default=None, help='The Customer Id')
    parser.add_argument('--perform_remote_update', type=bool, default=False, help='Remote Update Flag')
    parser.add_argument('--db_name', type=str, nargs='?', default=None, help='Database name')
    parser.add_argument('--db_host', type=str, nargs='?', default=None, help='Database Host')
    parser.add_argument('--db_port', type=int, nargs='?', default=3306, help='Database Port')
    parser.add_argument('--db_user', type=str, nargs='?', default=None, help='Database User')
    parser.add_argument('--db_password', type=str, nargs='?', default=None, help='Database Password')

    args=parser.parse_args()

    assert args.customer_id, "You must specify a --customer_id"
    assert args.credentials, "You must specify  --credentials"

    if (args.customer_id and args.credentials):
        '''
            This means both variable are present in the script
        '''
        customer_id = str(args.customer_id)
        credential = args.credentials
        db_name = args.db_name
        db_host = args.db_host
        db_password = args.db_password
        db_port = args.db_port
        db_user = args.db_user
        perform_remote_update_flag = args.perform_remote_update

        '''
            Generate sha256 from customer id
        '''
        customerSha256 = computeStringTosha256(customer_id)
        '''
            First remove everything before start
        '''
        removeFolder('output/%s/' % customer_id)
        removeFolder('.tmp/%s/' % customer_id)
        '''
            Create tmp folder and ouput folder
        '''
        createFolder(path='.tmp/', name=customer_id)
        createFolder(name=customer_id)

        '''
            Read files as strings
        '''
        centricity_string = readFileAsString('vitalinteraction_centricity_integration.py')
        helper_string = readFileAsString('vitalinteraction_helper.py')
        '''
            Replace sha256 id for customer sha256
        '''
        centricity_string = re.sub(r'[A-Fa-f0-9]{64}', customerSha256, centricity_string)
        helper_string = re.sub(r'[A-Fa-f0-9]{64}', customerSha256, helper_string)

        '''
            Write those files in the tmp folder
        '''
        writeFile(centricity_string, '.tmp/%s/vitalinteraction_client.py' % customer_id)
        writeFile(helper_string, '.tmp/%s/vitalinteraction_helper.py' % customer_id)
        '''
            Minify files
        '''
        created_at_text = ' \'\'\'\n Created at: %s \n \'\'\'\n' % date.today()
        centricity_minified = pyminifier('.tmp/%s/vitalinteraction_client.py' % customer_id)
        helper_minified = pyminifier('.tmp/%s/vitalinteraction_helper.py' % customer_id)
        centricity_minified = centricity_minified.replace('# Created by pyminifier (https://github.com/liftoff/pyminifier)', '')
        helper_minified = helper_minified.replace('# Created by pyminifier (https://github.com/liftoff/pyminifier)', '')
        centricity_minified = created_at_text + centricity_minified
        helper_minified = created_at_text + helper_minified
        centricity_minified = centricity_minified  + created_at_text
        helper_minified = helper_minified + created_at_text

        '''
            Write generated file into the output folder
        '''
        writeFile(centricity_minified, 'output/%s/vitalinteraction_client.py' % customer_id)
        writeFile(helper_minified, 'output/%s/vitalinteraction_helper.py' % customer_id)
        '''
            Copy storage and credentials
        '''
        copyFolder('src/storage', 'output/%s/storage' % customer_id)
        copyFile(credential, 'output/%s/%s' % (customer_id, customerSha256 + '.json'))


        '''
            Updating in server
        '''
        if (perform_remote_update_flag):
            r = requests.post(CLIENT_URL, {
                'key': SECRET_KEY,
                'customerId': int(customer_id),
                'customerHash': customerSha256,
                'credentials': readFileAsString(credential),
                'script': centricity_minified,
                'DB_name': db_name,
                'DB_host': db_host,
                'DB_port': db_port,
                'DB_user': db_user,
                'DB_password': db_password,
            })
            if r.status_code == 200:
                print('Updated successfully')
            else:
                print('We have an error trying to connect into the server')
                print(r.text)
        else:
            print('Flag perform_remote_update is False')

if __name__ == '__main__':
    main()
