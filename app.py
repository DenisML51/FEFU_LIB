from flask import Flask, session

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.run(host='0.0.0.0', port=5000, debug=True)

from controllers import index, new_reader, search
#, statistics