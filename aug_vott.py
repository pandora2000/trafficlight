import os, shutil, copy, json, cv2, uuid, autoaugment, copy, tensorflow.compat.v1 as tf, numpy as np, argparse
def get_boxes(width, height, regions):
    boxes = []
    for reg in regions:
        box = reg['boundingBox']
        l, t, w, h = [box['left'], box['top'], box['width'], box['height']]
        boxes.append([t / height, l / width, (t + h) / height, (l + w) / width])
    return boxes
new_data_base = {
    "name": "trafficlight-aug",
    "sourceConnection": {
        "name": "aug-source",
        "providerType": "localFileSystemProxy",
        "providerOptions": {
            "encrypted": "eyJjaXBoZXJ0ZXh0IjoiMDY2YmI5Zjk2ZDJlNzNhY2U5YTJiYjY0OGEwYWRkYjFmZTI5YWYwYjlkYmRiMjE3ZDMyZjFhOWUxZTFiZTYwNWQyZjc1MTZlYTYwNGIzZmVkNjA5ZWZjYTc3ZTY4NzgxODg5MWE5YzE1MzRmMTdhODAwNDBjMmNiNTgwMmZhYTRiMWExYTI2NjQ3NWMzMDE2YTdlYWI4MjdjNWZiOGYxMyIsIml2IjoiY2NiNTAwMzhhZGVmYjBjOTljYzk2NDBhYTNjMGI4M2M2YmI4Y2NkMGM2NDY3ODdmIn0="
        },
        "id": "t3rGrkfbx"
    },
    "targetConnection": {
        "name": "aug-target",
        "providerType": "localFileSystemProxy",
        "providerOptions": {
            "encrypted": "eyJjaXBoZXJ0ZXh0IjoiNjU2Yjg4ZTEwZjBhYzhjMWQ4OGU3M2RjZmM3NmRkM2Q0NmQzMDg1MzE0NDgzNGQ5MzllYWYzMmY0NGEzZjg5YWU5MTc5YTQ5MTQ4YjcxNjM4MmE1NTVlODE0MDU1YjQwZmJhOGEzZTViYzVkY2JiM2FkMDdmYzE4MGRkZWQxZDAyNjBiN2M3MTg0NWZkMzIwM2ZhZjcwNWRlMWQ5NDk4MSIsIml2IjoiNTQ0OTIzNGQ1MDc3Y2NhMmJiZDY2NjgyZDMzNWRhODBjNmYyNmNlZGM4NjY3NTQ1In0="
        },
        "id": "_YEEMU0Gv"
    }
}
def main(root_path, limit):
    vott_src_path = f'{root_path}/vott-target'
    vott_src_file_path = f'{vott_src_path}/trafficlight.vott'
    vott_dst_path = f'{root_path}/vott-aug-target'
    vott_dst_img_path = f'{root_path}/vott-aug-source'
    vott_dst_file_path = f'{vott_dst_path}/trafficlight-aug.vott'
    vott_data = None
    for p in [vott_dst_path, vott_dst_img_path]:
        shutil.rmtree(p, ignore_errors=True)
    for p in [vott_dst_path, vott_dst_img_path]:
        os.makedirs(p)
    with open(vott_src_file_path) as f:
        vott_data = json.loads(f.read())
    cpi = 10
    assets = vott_data['assets']
    new_data = copy.deepcopy(vott_data)
    new_assets = {}
    new_data['assets'] = new_assets
    new_data.update(new_data_base)
    ind = 0
    aids = list(assets.keys())
    if limit > -1:
        aids = aids[:limit]
    # TODO: きちんと関連するものは別に分ける
    train_ind = int(round(len(aids) * 0.8))
    for aid in aids:
        print(ind)
        a = assets[aid]
        path = f'{root_path}/target/{a["name"]}'
        print(path)
        nim = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
        height, width = nim.shape[:2]
        im = tf.convert_to_tensor(nim)
        anno = None
        with open(f'{vott_src_path}/{aid}-asset.json') as f:
            anno = json.loads(f.read())
        if len(anno['regions']) == 0:
            boxes = tf.zeros([0, 4])
        else:
            boxes = tf.convert_to_tensor(np.array(get_boxes(width, height, anno['regions']), dtype=np.float32))
        train = ind < train_ind
        for i in range(cpi if train else 1):
            if train:
                # crop入れたいね
                aug_im, aug_boxes = autoaugment.distort_image_with_autoaugment(im, boxes, 'custom')
                nnim = cv2.cvtColor(aug_im.numpy(), cv2.COLOR_RGB2BGR)
                nboxes = aug_boxes.numpy().tolist()
            else:
                nnim = nim
                nboxes = boxes.numpy().tolist()
            naid = f'{str(uuid.uuid1()).replace("-", "")}-{"train" if train else "val"}'
            na = copy.deepcopy(a)
            na['id'] = naid
            na['name'] = f'{naid}.jpg'
            npath = f'{vott_dst_img_path}/{na["name"]}'
            na['path'] = f'file:{npath}'
            nh, nw = nnim.shape[:2]
            na['size'] = {
                'width': nw,
                'height': nh,
            }
            new_assets[naid] = na
            cv2.imwrite(npath, nnim)
            nanno = copy.deepcopy(anno)
            nanno['asset'] = na
            for reg, nbox in zip(nanno['regions'], nboxes):
                t, l, b, r = nbox
                l, t, r, b = [l * nw, t * nh, r * nw, b * nh]
                w, h = [r - l, b - t]
                reg['boundingBox'] = {
                    'left': l,
                    'top': t,
                    'width': w,
                    'height': h
                }
                reg['points'] = [
                    { 'x': l, 'y': t },
                    { 'x': r, 'y': t },
                    { 'x': r, 'y': b },
                    { 'x': l, 'y': b }
                ]
            with open(f'{vott_dst_path}/{naid}-asset.json', 'w') as f:
                f.write(json.dumps(nanno))
        ind += 1
    new_data['lastVisitedAssetId'] = list(new_assets.keys())[0]
    with open(vott_dst_file_path, 'w') as f:
        f.write(json.dumps(new_data))
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True)
    parser.add_argument('--limit', type=int, default=-1, required=True)
    args = parser.parse_args()
    main(args.root, args.limit)
