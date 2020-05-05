import os, shutil, copy, json, cv2, uuid, argparse
parser = argparse.ArgumentParser()
parser.add_argument('--vott_root', required=True)
parser.add_argument('--pascal_root', required=True)
args = parser.parse_args()
def get_anno_obj_xml_data(name, bndbox):
    return f"""<object>
		<name>{name}</name>
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>{bndbox[0]}</xmin>
			<ymin>{bndbox[1]}</ymin>
			<xmax>{bndbox[2]}</xmax>
			<ymax>{bndbox[3]}</ymax>
		</bndbox>
    </object>"""
def get_anno_xml_data(aid, width, height, objs):
    obj_xmls = '\n'.join([get_anno_obj_xml_data(*obj) for obj in objs])
    return f"""<annotation>
	<folder>VOC2012</folder>
	<filename>{aid}.jpg</filename>
	<source>
		<database>The VOC2007 Database</database>
		<annotation>PASCAL VOC2007</annotation>
		<image>flickr</image>
	</source>
	<size>
		<width>{width}</width>
		<height>{height}</height>
		<depth>3</depth>
	</size>
        {obj_xmls}
	<segmented>0</segmented>
    </annotation>"""
vott_path = f'{args.vott_root}/vott-aug-target'
vott_file_path = f'{vott_path}/trafficlight-aug.vott'
vott_data = None
pascal_root_path = args.pascal_root
pascal_path = f'{pascal_root_path}/myVOCdevkit/VOC2012'
pascal_anno_path = f'{pascal_path}/Annotations'
pascal_imgset_path = f'{pascal_path}/ImageSets/Main'
pascal_jpg_path = f'{pascal_path}/JPEGImages'
shutil.rmtree(pascal_path, ignore_errors=True)
for p in [pascal_anno_path, pascal_imgset_path, pascal_jpg_path]:
    os.makedirs(p)
with open(vott_file_path) as f:
    vott_data = json.loads(f.read())
classes = ['aeroplane', 'bicycle']
imgset = []
ind = 0
for aid in vott_data['assets']:
    print(ind)
    imgset.append(aid)
    a = vott_data['assets'][aid]
    path = a['path'].split(':')[1]
    width = a['size']['width']
    height = a['size']['height']
    objs = []
    ad = None
    with open(f'{vott_path}/{aid}-asset.json') as f:
        ad = json.loads(f.read())
    for reg in ad['regions']:
        name = classes[0] if reg['tags'][0] == 'green' else classes[1]
        bb = reg['boundingBox']
        l = bb['left']
        t = bb['top']
        r = l + bb['width']
        b = t + bb['height']
        obj = [name, [int(round(x)) for x in [l, t, r, b]]]
        objs.append(obj)
    xml = get_anno_xml_data(aid, width, height, objs)
    with open(f'{pascal_anno_path}/{aid}.xml', 'w') as f:
        f.write(xml)
    shutil.copyfile(path, f'{pascal_jpg_path}/{aid}.jpg')
    ind += 1
for p in ['train', 'val']:
    timgset = [x for x in imgset if x.endswith(f'_{p}.jpg')]
    with open(f'{pascal_imgset_path}/aeroplane_{p}.txt', 'w') as f:
        f.write('\n'.join([f'{x} -1' for x in timgset]))
# os.system(f'cd {pascal_root_path}; tar -cvf myVOCdevkit.tar myVOCdevkit; rm -rf myVOCdevkit')
# shutil.move(f'{pascal_root_path}/myVOCdevkit.tar', f'/home/zb/Dropbox (skewers)/Apps/tm-work/myVOCdevkit.tar')
