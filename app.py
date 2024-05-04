from flask import Flask, request, send_file
import os
import pytube

app = Flask(__name__)

DOWNLOAD_DIRECTORY = "downloads"

def remove_old_videos():
    files = os.listdir(DOWNLOAD_DIRECTORY)
    if len(files) > 10:
        oldest_files = sorted(files, key=lambda x: os.path.getctime(os.path.join(DOWNLOAD_DIRECTORY, x)))[:len(files) - 10]
        for file_name in oldest_files:
            os.remove(os.path.join(DOWNLOAD_DIRECTORY, file_name))

@app.route('/')
def index():
    return open('templates/index.html').read()

@app.route('/download', methods=['GET'])
def download_video():
    video_url = request.args.get('videoUrl')
    quality = request.args.get('quality')
    
    yt = pytube.YouTube(video_url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').first()

    if quality == 'medium':
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').filter(res='360p').first()
    elif quality == 'lowest':
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').last()

    video_file = stream.download(output_path=DOWNLOAD_DIRECTORY)
    remove_old_videos()
    return send_file(video_file, as_attachment=True)

if __name__ == '__main__':
    port = input("Enter port (default is 5000): ")
    if not port:
        port = 5000
    else:
        port = int(port)
    app.run(debug=True, port=port)

