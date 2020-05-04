# vottで古いプロジェクトを削除し、このプログラムで得られた.vottをopen local projectすればよい
import os, shutil, copy, json, cv2, uuid
template = {
    "name": "trafficlight",
    "securityToken": "trafficlight Token",
    "sourceConnection": {
        "name": "source",
        "providerType": "localFileSystemProxy",
        "providerOptions": {
            "encrypted": "eyJjaXBoZXJ0ZXh0IjoiMjc5OWJiODI1OWE4M2VmZDBiZTMzNWNkYmRlYTFiZTYzM2EyZTRjZmVlYTkzMDAyN2ExZGI0YmNlNTVlZjlkNThmZWYxMTEwZDAxMzk0ODk5Y2UyOWY2MGMyMGJiODcyZGNkNWU2NmQyOTlmM2VjMTAwNWFhYTRhZDA1MjdiMTciLCJpdiI6Ijk3NmNkNDQ4YTM3YjYwODY0MzBhZmYzOTM0ZmZiNTkzNWQzNmY1Mjk5NGNhNWUxMyJ9"
        },
        "id": "dnv6iQedX"
    },
    "targetConnection": {
        "name": "target",
        "providerType": "localFileSystemProxy",
        "providerOptions": {
            "encrypted": "eyJjaXBoZXJ0ZXh0IjoiYzQ3NGFmNDhhNDkyMGY0OWZlNjdhNzg4NzQ3ZGUyMjc1NTc1MTUwNzVhOWE4YzE2MjZhZGMyMzgxZjk3YmFlYWZhZTQ2ZWQ3MTQzNGFlYWY1NzU4NDJhYzdkYzZjNzYxNTNiOTgyNjAxMDg0NTE5NzNjOWNmMTY3NTA0YjNmYTEiLCJpdiI6ImFjNmI1Y2JiNjMzYjExZmU0YzJkOTBjZTZiMjYyYjAwOTZhZDI3ODVjZjVkZjIxZCJ9"
        },
        "id": "BpD-JRS3P"
    },
    "videoSettings": {
        "frameExtractionRate": 15
    },
    "tags": [
        {
            "name": "green",
            "color": "#5db300"
        },
        {
            "name": "red",
            "color": "#e81123"
        }
    ],
    "id": "l_wIMIPuD",
    "activeLearningSettings": {
        "autoDetect": False,
        "predictTag": True,
        "modelPathType": "coco"
    },
    "exportFormat": {
        "providerType": "vottJson",
        "providerOptions": {
            "encrypted": "eyJjaXBoZXJ0ZXh0IjoiZWE2ZWE2ODVmOTc5YzQ5YWJhZmVkZmZkOGNhNTY2NmQwNjYzZTgyNGE1YjhjZjkzODZkMzkyZDliMWVkNzIyOWY3MWE1MzU1NTkzOTRiNjIzZjcyMTJkN2E1NzQxNDkzIiwiaXYiOiIzNjFjZDMwNjliYjlkNTkzM2E2YmM0YmY5ZGY0MWFhNjlkZTliMjU0NWNiYjk3ZGQifQ=="
        }
    },
    "version": "2.1.0",
    "lastVisitedAssetId": "0339a4878f553995313d8a84c6f29d34",
    "assets": {}
}
asset_template = {
    "format": "jpg",
    "id": "ff1b43bed228d17363491d8473066f6d",
    "name": "kouka_06_img000.jpg",
    "path": "file:/home/zb/%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89/trafficlight/%D0%93f%D0%91%5B%D0%93%5E%D0%93Z%D0%93b%D0%93g/kouka_06_img/kouka_06_img000.jpg",
    "size": {
        "width": 1080,
        "height": 1920
    },
    "state": 2,
    "type": 1
}
region_template = {
    "id": "dWQwi37no",
    "type": "RECTANGLE",
    "tags": [
        "green"
    ],
    "boundingBox": {
        "height": 108.5972850678733,
        "width": 349.85915492957747,
        "left": 92.62575452716298,
        "top": 475.656108597285
    },
    "points": [
        {
            "x": 92.62575452716298,
            "y": 475.656108597285
        },
        {
            "x": 442.48490945674047,
            "y": 475.656108597285
        },
        {
            "x": 442.48490945674047,
            "y": 584.2533936651583
        },
        {
            "x": 92.62575452716298,
            "y": 584.2533936651583
        }
    ]
}
mypath = '/home/zb/downloads/trafficlight/files'
target = '/home/zb/works/test/trafficlight/target'
vott_target = '/home/zb/works/test/trafficlight/vott-target'
jpg_files = []
txt_files = []
shutil.rmtree(target, ignore_errors=True)
shutil.rmtree(vott_target, ignore_errors=True)
os.makedirs(target)
os.makedirs(vott_target)
for r, d, f in os.walk(mypath):
    for file in f:
        if '.jpg' in file:
            jpg_files.append(os.path.join(r, file))
        if '.txt' in file:
            txt_files.append(os.path.join(r, file))
# tagとその色の設定
# template['tags'] = []
# for i in range(50):
#     template['tags'].append({
#         'name': f'{i}',
#         'color': '#ffffff'
#     })
d = copy.deepcopy(template)
i = 0
annoi = 0
for jpg_file in jpg_files:
    t = f'{jpg_file[:-4]}.txt'
    k = jpg_file.split('/')
    jf = f'{target}/{k[-2]}__{k[-1]}'
    shutil.copyfile(jpg_file, jf)
    aid = str(uuid.uuid1()).replace('-', '')
    if i == 0:
        d['lastVisitedAssetId'] = aid
    asset = copy.deepcopy(asset_template)
    asset['id'] = aid
    asset['name'] = jf.split('/')[-1]
    asset['path'] = f'file:{jf}'
    im = cv2.imread(jf)
    width, height = im.shape[:2][::-1]
    asset['size'] = {
        'width': width,
        'height': height
    }
    asset['state'] = 1
    asset['type'] = 1
    if t in txt_files:
        annoi += 1
        asset['state'] = 2
        ind = {
            'asset': asset,
            'regions': [],
            'version': d['version']
        }
        with open(t) as f:
            lines = [x.split(' ') for x in f.read().strip().split('\n')]
            for line in lines:
                tag = line[0]
                x, y, w, h = [float(x) for x in line[1:]]
                x = width * x
                y = height * y
                w = width * w
                h = height * h
                if tag == '16' or tag == '15':
                    region = copy.deepcopy(region_template)
                    region['id'] = str(uuid.uuid1()).replace('-', '')
                    region['tags'] = ['green'] if tag == '16' else ['red']
                    # region['tags'] = [tag]
                    l = x - w / 2
                    t = y - h / 2
                    region['boundingBox'] = {
                        'left': l,
                        'top': t,
                        'width': w,
                        'height': h
                    }
                    region['points'] = [
                        { 'x': l, 'y': t },
                        { 'x': l + w, 'y': t },
                        { 'x': l + w, 'y': t + h },
                        { 'x': l, 'y': t + h }
                    ]
                    ind['regions'].append(region)
        with open(f'{vott_target}/{aid}-asset.json', 'w') as f:
            f.write(json.dumps(ind))
        d['assets'][aid] = asset
    i += 1
    print(i)
    print(annoi)
with open(f'{vott_target}/trafficlight.vott', 'w') as f:
    f.write(json.dumps(d))
