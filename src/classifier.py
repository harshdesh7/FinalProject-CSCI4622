import tensorflow as tf
from tensorflow import keras
import numpy as np
import os
from bottle import route, request, run, static_file, template
import base64


@route('/', method='GET')
def serve():
    return static_file('index.html', root='')

@route('/classify', method='POST')
def classify_img():
    data = request.files.get('data')
    name, ext = os.path.splitext(data.filename)
    if ext not in ('.png', '.jpg', '.jpeg'):
        return static_file('error.html', root='')
    bytes = data.file.read()
    d64 = base64.b64encode(bytes)
    im = tf.image.decode_jpeg(bytes, channels=3)
    proc = tf.image.resize(im, [192,192]) / 255
    proc = tf.reshape(proc, [1,192,192,3])
    pred = mod.predict(proc)
    ind = np.argmax(pred, axis=-1)
    label = CLASSES[ind[0]]
    return template('''<!DOCTYPE html>
<html>
	<head>
		<title>Flower Type</title>
	</head>
	<body>

		<h1>{{label}}</h1>
		<img src="data:image/png;base64,{{n}}", width="192", height="192">
		<form action="/" method="get" enctype="multipart/form-data">
  			<input value="Home Page" type="submit" />
		</form>

	</body>
</html>''', label=label, n=d64)

if __name__ == '__main__':

    mod = keras.models.load_model('final_model.h5')

    CLASSES = ['pink primrose',    'hard-leaved pocket orchid', 'canterbury bells', 'sweet pea',     'wild geranium',     'tiger lily',           'moon orchid',              'bird of paradise', 'monkshood',        'globe thistle',         # 00 - 09
           'snapdragon',       "colt's foot",               'king protea',      'spear thistle', 'yellow iris',       'globe-flower',         'purple coneflower',        'peruvian lily',    'balloon flower',   'giant white arum lily', # 10 - 19
           'fire lily',        'pincushion flower',         'fritillary',       'red ginger',    'grape hyacinth',    'corn poppy',           'prince of wales feathers', 'stemless gentian', 'artichoke',        'sweet william',         # 20 - 29
           'carnation',        'garden phlox',              'love in the mist', 'cosmos',        'alpine sea holly',  'ruby-lipped cattleya', 'cape flower',              'great masterwort', 'siam tulip',       'lenten rose',           # 30 - 39
           'barberton daisy',  'daffodil',                  'sword lily',       'poinsettia',    'bolero deep blue',  'wallflower',           'marigold',                 'buttercup',        'daisy',            'common dandelion',      # 40 - 49
           'petunia',          'wild pansy',                'primula',          'sunflower',     'lilac hibiscus',    'bishop of llandaff',   'gaura',                    'geranium',         'orange dahlia',    'pink-yellow dahlia',    # 50 - 59
           'cautleya spicata', 'japanese anemone',          'black-eyed susan', 'silverbush',    'californian poppy', 'osteospermum',         'spring crocus',            'iris',             'windflower',       'tree poppy',            # 60 - 69
           'gazania',          'azalea',                    'water lily',       'rose',          'thorn apple',       'morning glory',        'passion flower',           'lotus',            'toad lily',        'anthurium',             # 70 - 79
           'frangipani',       'clematis',                  'hibiscus',         'columbine',     'desert-rose',       'tree mallow',          'magnolia',                 'cyclamen ',        'watercress',       'canna lily',            # 80 - 89
           'hippeastrum ',     'bee balm',                  'pink quill',       'foxglove',      'bougainvillea',     'camellia',             'mallow',                   'mexican petunia',  'bromelia',         'blanket flower',        # 90 - 99
           'trumpet creeper',  'blackberry lily',           'common tulip',     'wild rose']

    run(host='0.0.0.0', port=8080)