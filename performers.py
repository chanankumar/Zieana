from pydub import AudioSegment
from pydub.playback import play
from os.path import join
import os
import urllib
import urllib.request
import urllib.parse
import re
import webbrowser
import threading
import requests
import json
from pygame import mixer
from multiprocessing.pool import ThreadPool
import random

class Performers:

    def __init__(self):
        self.music_list = [
            "so far away",
            "pray for me kendrick lamar",
            "The weekend reminder",

        ]

    def play(self, file_name):

        path = join(os.getcwd(), 'music', file_name + '.mp3')
        print(path)
        mixer.init()
        mixer.music.load(path)
        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(mixer.music.play)
        async_result.get()

        # song = AudioSegment.from_mp3(path)
        # t = threading.Thread(target=play(song))
        # t.start()

    def stop(self):
        mixer.music.stop()


    def youtube_player(self, search_query):
        query_string = urllib.parse.urlencode({"search_query":search_query})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'href=\"/watch\?v=(.{11})', html_content.read().decode())
        resonse = "http://www.youtube.com/watch?v=" + search_results[0]
        print(resonse)
        webbrowser.open(resonse)

    def playlist(self, name):

        for i in self.music_list:
            if i.lower() == name.lower():
                return True

    def random_play(self):
        index = random.randrange(0, len(self.music_list))
        music_name = self.music_list.pop(index)
        return music_name


    def find_images(self, search_word):
        headers = {'Api-Key': '8z76ceavpadeka7hrkze6kff'}
        r = requests.get(
            'https://api.gettyimages.com/v3/search/images?minimum_size=xx_large&phrase={0}'.format(search_word),
            headers=headers
        )
        data = json.loads(r.text)
        print(data)
        image1 = data['images'][0]['display_sizes'][0]['uri']
        image2 = data['images'][1]['display_sizes'][0]['uri']
        body = {'url': image1}
        requests.post("http://localhost:8080/image", data=json.dumps(body))

        return image1, image2

    def movies(self, search_query ):
        # query_string = urllib.parse.urlencode({"search_query": search_query})
        # html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        # search_results = re.findall(r'href=\"/watch\?v=(.{11})', html_content.read().decode())
        # resonse = "http://www.youtube.com/watch?v=" + search_results[0]
        # body = {'url': resonse}
        # requests.get("http://localhost:8080/statement?text=oh damn nigga")
        # print(resonse)
        # requests.post("http://localhost:8080/video", data=json.dumps(body))
        key = 'e63c785c'
        r = requests.get("http://www.omdbapi.com/?apikey={0}&t={1}".format(key, search_query))
        data = json.loads(r.text)
        print(json.dumps(data, indent=2))

        Title = data['Title']
        Released = data['Released']
        Plot = data['Plot']
        Genere = data['Genre']
        Director = data['Director']
        Cast = data['Actors']
        Poster = data['Poster']
        rating1_name = None
        try:
            rating1_name = data['Ratings'][1]['Source']
            rating1_value = data['Ratings'][1]['Value']
        except:
            pass

        imdbRating = data['imdbRating']

        if rating1_name is not None:
            return (f"{Title} starring {Cast} was Released on {Released}. The plot of the movie is {Plot}. It has a {rating1_name} score of {rating1_value} and The IMDB rating is {imdbRating} ")
        else:
            return (f"{Title} starring {Cast} was Released on {Released}. The plot of the movie is {Plot}. It has a IMDB rating of {imdbRating} ")






if __name__ == '__main__':
    test = Performers()
    data = test.random_play()
    print(data)
