from flask import render_template
from flask_cors import CORS
import connexion

# Create the application instance
app = connexion.App(__name__, specification_dir='./')

# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yml')
CORS(app.app)
# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5004/
    :return:        the rendered template 'home.html'
    """
    return render_template('home.html')

if __name__ == '__main__':
    #
    # UPGRADE WEBSERVER PORT
    #
    app.run(host='0.0.0.0', port=5004, debug=True)