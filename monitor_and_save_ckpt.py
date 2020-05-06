import argparse, time, os, sys
print(sys.version)
from datetime import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials
def get_drive():
    # to reset authentication on colab, comment in below
    #!rm -f /content/adc.json
    gauth = None
    try:
        auth.authenticate_user()
        gauth = GoogleAuth()
        gauth.credentials = GoogleCredentials.get_application_default()
    except:
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
    return GoogleDrive(gauth)
def upload_file_to_drive(drive, path, params=None):
    f = None
    if params is None:
        f = drive.CreateFile()
    else:
        f = drive.CreateFile(params)
    f.SetContentFile(path)
    f.Upload()
def create_folder_under_id_on_drive(drive, id, name):
    folder_metadata = {'parents': [{'id': id}], 'title' : name, 'mimeType' : 'application/vnd.google-apps.folder'}
    folder = drive.CreateFile(folder_metadata)
    folder.Upload()
    return folder['id']
def list_drive_folder(drive, id):
    file_list = drive.ListFile({'q': f"'{id}' in parents and trashed=false"}).GetList()
    ret = []
    for f in file_list:
        ret.append({ 'title': f['title'], 'id': f['id'] })
    return ret
def delete_file_from_drive(drive, id):
    drive.CreateFile({'id': id}).Delete()
def upload_file(drive, name, folder_id):
    print(f'uploading {name}...')
    try:
        upload_file_to_drive(drive, name, {'parents': [{'id': folder_id}]})
    except:
        print(f'failed to upload {name}!')
parser = argparse.ArgumentParser()
parser.add_argument('--root', required=True)
parser.add_argument('--save_root_id', required=True)
args = parser.parse_args()
drive = get_drive()
latest_index = -1
while True:
    try:
        os.chdir(args.root)
    except:
        time.sleep(10)
        continue
    name = datetime.now().strftime('%Y%m%d%H%M%S')
    print(f'start uploading to {name}...', flush=True)
    folder_id = create_folder_under_id_on_drive(
        drive, args.save_root_id, name
    )
    for p in os.listdir():
        if not os.path.isfile(os.path.join(args.root, p)):
            continue
        upload_file(drive, p, folder_id)
    os.chdir('/tmp')
    for p in ['monitor.log', 'main.log']:
        upload_file(drive, p, folder_id)
    print(f'end upload to {name}...', flush=True)
    fs = list_drive_folder(drive, args.save_root_id)
    fs = sorted(fs, key=lambda x: x['title'])[::-1][4:]
    for f in fs:
        delete_file_from_drive(drive, f['id'])
    print(f'end delete old folders', flush=True)
    time.sleep(30 * 60)
