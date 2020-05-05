import argparse, time, os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials
def get_drive():
    # to reset authentication, comment in below
    #!rm -f /content/adc.json
    auth.authenticate_user()
    gauth = GoogleAuth()
    gauth.credentials = GoogleCredentials.get_application_default()
    return GoogleDrive(gauth)
def upload_file_to_drive(drive, path):
    f = drive.CreateFile()
    f.SetContentFile(path)
    f.Upload()
parser = argparse.ArgumentParser()
parser.add_argument('--root', required=True)
args = parser.parse_args()
drive = get_drive()
latest_index = -1
while True:
    try:
        os.chdir(args.root)
    except:
        continue
    for p in os.listdir('.'):
        if not p.startswith('model.ckpt-') or not p.endswith('.meta'):
            continue
        index = int(p.split('-')[1].split('.')[0])
        if index <= latest_index:
            continue
        latest_index = index
        ps = []
        for p2 in os.listdir('.'):
            if not p2.startswith(f'model.ckpt-{index}.'):
                continue
            ps.append(p2)
        for p2 in ps:
            upload_file_to_drive(drive, p2)
    time.sleep(30)
