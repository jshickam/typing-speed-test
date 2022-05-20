import requests

class SentenceGenerator():
    def __init__(self):
        self.endpoint = "http://metaphorpsum.com/sentences/"

    def get_random(self, sentences):
        """Returns the number of random sentences requested
           sentences: Integer - number of sentences to generate
        """
        response = requests.get(self.endpoint + str(sentences))
        response.raise_for_status()
        random_string = response.text
        return random_string