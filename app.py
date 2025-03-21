import os
import uuid
from flask import Flask, request, render_template, redirect, url_for, flash
from translate import process_video, UPLOAD_FOLDER

app = Flask(__name__)
app.secret_key = 'secret'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'video' not in request.files:
            flash('Aucun fichier vidéo trouvé')
            return redirect(request.url)
        file = request.files['video']

        if file.filename == '':
            flash('Aucun fichier sélectionné')
            return redirect(request.url)
        
        # Correction : utilisation d'un tuple pour endswith()
        if file and file.filename.lower().endswith(('.mp4', '.mov', '.avi')): # type: ignore
            filename = f'{uuid.uuid4().hex}_{file.filename}'
            video_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(video_path)

            try:
                output_filename = process_video(filename)
                return redirect(url_for('result', filename=output_filename))
            except Exception as e:
                flash(f"Erreur lors du traitement de la vidéo: {str(e)}")
                return redirect(request.url)
        else:
            flash('Le fichier doit être au format .mp4, .mov ou .avi')
            return redirect(request.url)
                
    return render_template('index.html')
            
@app.route('/result/<filename>')
def result(filename):
    # Afficher la vidéo traduite dans une page avec un lecteur vidéo HTML5
    video_url = url_for("static", filename=f"translate/{filename}")
    return render_template("result.html", video_url=video_url)

if __name__ == '__main__':
    app.run(debug=True)
