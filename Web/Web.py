'''from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask.ext.jsonpify import jsonify

import os.path


class BestandAPI(Resource):
    def __init__(self, **kwargs):
        self.bestand = kwargs['bestand']

    def get(self):
        func = request.args.get('func')
        partition = int(request.args.get('partition'))
        image = int(request.args.get('image'))

        if 'hashlist' in func:

            return jsonify(
                self.bestand.generate_hashlist_api(image, partition))

        if 'ziplist' in func:
            return jsonify(self.bestand.generate_ziplist_api(image, partition))


class MainAPI(Resource):
    def __init__(self, **kwargs):
        self.main = kwargs['main']

    def get(self):
        command = str(request.args.get('command'))
        img_json = []
        for num in range(len(self.main.images)):
            image = self.main.images[num]

            partitions = image.ewf_img_info.get_partitions()
            part_json = []
            for part in partitions:
                part_json.append({'addr': part.addr,
                                  'desc': part.desc,
                                  'size': part.size,
                                  'dirs': len(part.dirs),
                                  'files': len(part.files)})

            img_json.append({'id': num,
                             'path': image.image_path,
                             'partities': part_json,
                             'size': image.ewf_img_info.get_size()})
        return jsonify(img_json)

    def post(self):
        json_data = request.get_json(force=True)
        result = {'result': 'failed'}
        if 'path' in json_data:
            try:
                if os.path.isfile(json_data['path']):
                    print '[+] Adding Image: ' + json_data['path']
                    self.main.add_image(json_data['path'])
                    result = {'result': 'success'}
                else:
                    result = {'result': 'Unknown File'}
            except:
                pass
            return jsonify(result)


class Socket():
    def __init__(self, port, name, main):
        self.port = port
        self.name = name
        self.main = main

    def run(self, debug):
        print '[+] Starting WebAPI \'' + \
            self.name + '\' on port ' + str(self.port)
        app = Flask(self.name)
        api = Api(app)

        api.add_resource(BestandAPI, '/bestand',
                         resource_class_kwargs={'bestand': self.main.bestand})
        api.add_resource(MainAPI, '/main',
                         resource_class_kwargs={'main': self.main})

        app.run(port=self.port, debug=debug, use_reloader=False)
'''