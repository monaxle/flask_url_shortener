from flask import Flask, render_template, request, redirect, flash, url_for, abort, session,jsonify
import json
import os, random, string

app = Flask(__name__)
app.secret_key = "af4tgarag4gaa4gar"
APP_ROOT = os.getcwd()


@app.route('/')
def index():
    return render_template('index.html', active='active', sess=session.keys())


@app.route('/get_url', methods=['GET', 'POST'])
def get_url():
    if request.method == 'POST':
        urls = {}

        if os.path.exists('urls.json'):
            with open('urls.json') as url_file:
                urls = json.load(url_file)

        if request.form['o_url'] in urls.keys():
            flash('Shorten URL Name already exist')
            with open('urls.json') as url_file:
                r_url = random_url()
                jsn = json.load(url_file)
                while r_url in jsn.keys():
                    r_url = random_url()
            flash("Suggestion: " + r_url)
            if 'inputurl' in request.form.keys():
                return redirect('/')
            else:
                return redirect('/file-shorten')

        if 'inputurl' in request.form.keys():
            urls[request.form['o_url']] = {'url': request.form['inputurl']}
        else:
            f = request.files['input_file']
            if f.filename.split('.')[1] in ['jpg', 'jpeg', 'png', 'gif']:
                f_name = request.form['o_url'] + random_url() + '.' + f.filename.split('.')[1]
                f.save(os.path.join(APP_ROOT, 'static/' + f_name))
                urls[request.form['o_url']] = {'file': f_name}
            else:
                flash('Sorry! wrong file type')
                return redirect(url_for('file_shortner'))

        with open('urls.json', 'w') as json_file:
            json.dump(urls, json_file)
            session[request.form['o_url']] = True
        return render_template('shorten_url.html', short_url=request.form['o_url'])
    return redirect('/')

@app.route('/file-shorten')
def file_shortner():
    return render_template('file_shortner.html', active1='active',sess=session.keys())


@app.route('/<string:link>')
def link_to_url(link):
    if os.path.exists('urls.json'):
        with open('urls.json') as url:
            url_dict = json.load(url)
            if link in url_dict.keys():
                if 'url' in url_dict[link]:
                    return redirect(url_dict[link]['url'])
                else:
                    pass
                    f = url_for('static', filename=url_dict[link]['file'])
                    return redirect(f)
    return abort(404)


@app.errorhandler(404)
def page_not_found(error):
    err = '404: Requested page not found'
    return render_template('index.html', err404=err), 404

@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))

def random_url():
    r_str = string.ascii_letters + string.digits
    r_url = ''.join(random.choice(r_str) for i in range(6))
    return r_url


if __name__ == '__main__':
    app.run(debug=True)
