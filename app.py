from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
app.secret_key = 'random_key'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin@security.com' and password == 'checkdata':
            return redirect('/search_page')
        else:
            return redirect('/')


@app.route('/search_page', methods=['GET', 'POST'])
def search():
    global filename
    folder_path = 'static/car_images'
    if request.method == 'GET':
        return render_template('search.html')
    elif request.method == 'POST':
        search = request.form['search'].lower()
        city_images = []
        for filename in os.listdir(folder_path):
            if search in filename.lower():
                city_images.append(filename)
        if city_images:
            session['city_images'] = city_images
            session['query'] = search
            return redirect('/Result_Page')
        else:
            return redirect('/Not_Found')


@app.route('/Not_Found')
def not_found():
    return render_template('notfound.html')


@app.template_filter("replace_text")
def replace_text_filter(img):
    replaced = img.replace('.png', '')
    parts = replaced.split('_')
    if len(parts) >= 5 and parts[4] == 'npf':
        return {
            'city': parts[0],
            'state': parts[1],
            'date': parts[2],
            'where': parts[3],
            'tag': 'No Placard Found'
        }

    elif len(parts) >= 5 and parts[4] == 'fp':
        return {
            'city': parts[0],
            'state': parts[1],
            'date': parts[2],
            'where': parts[3],
            'tag': 'Fake Placard'
        }

    else:
        return {'filename': replaced}


@app.route('/Result_Page', methods=['GET', 'POST'])
def results():
    images = session.get('city_images', [])
    query = session.get('query', '')
    length = len(session.get('city_images', []))
    return render_template('results.html', images=images, length=length, query=query)


@app.route('/delete_image', methods=['POST'])
def delete_image():
    image_name = request.form.get('image_name')
    file_path = os.path.join('static/car_images', image_name)

    if os.path.exists(file_path):
        os.remove(file_path)

        if 'city_images' in session:
            session['city_images'] = [img for img in session['city_images'] if img != image_name]

    return redirect('/Result_Page')


app.run(host='0.0.0.0', port=2000, debug=True)
