import json
import sys

import imdb
import smtplib

import email.utils
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

reload(sys)
sys.setdefaultencoding('utf-8')

NOTIFY_ABOVE_RATING = 7.5

SENDGRID_API_KEY = "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"

def run_checker(scraped_movies):
    imdb_conn = imdb.IMDb()
    good_movies = []
    for scraped_movie in scraped_movies:
        try:
            imdb_movie = get_imdb_movie(imdb_conn, scraped_movie['name'])
            if imdb_movie['rating'] > NOTIFY_ABOVE_RATING:
                good_movies.append(imdb_movie)
        except:
            pass
    if good_movies:
        send_email(good_movies)

def get_imdb_movie(imdb_conn, movie_name):
    results = imdb_conn.search_movie(movie_name)
    movie = results[0]
    imdb_conn.update(movie)
    print("{title} => {rating}".format(**movie))
    return movie

def send_email(movies):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('pascal.kunkler@gmail.com', 'Pascalk_170395')

    sender = 'pascal.kunkler@gmail.com'
    recipient = ['s4jakunk@uni-trier.de']

    # Create the message
    msg = MIMEMultipart('alternative')
    msg['To'] = email.utils.formataddr(('Jan Pascal kunkler', 's4jakunk@uni-trier.de'))
    msg['From'] = email.utils.formataddr(('Pi', 'pi@raspberrypi.local'))
    msg['Subject'] = 'Highly rated movies of the day'

    text = "High rated today:\n"
    html = '''\
    <html>
        <head></head>
        <body>
            <h3>High rated today:</h3><br>
        </body>
    </html>'''

    for movie in movies:
        html += "<p>{title} => {rating}</p>".format(**movie)
        html += '''<p><u>Playtimes:</u></p><br>
                {}'''
        text += "\n{title} => {rating}".format(**movie)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    msg.attach(part1)
    msg.attach(part2)

    server.sendmail(sender, recipient, msg.as_string() )
    print "Sent email with {} movie(s).".format(len(movies))

if __name__ == '__main__':
    movies_json_file = sys.argv[1]
    with open(movies_json_file) as scraped_movies_file:
        movies_file = json.loads(scraped_movies_file.read())
    run_checker(movies_file)
