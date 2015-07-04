import requests
import unittest
from riotwatcher import RiotWatcher, NORTH_AMERICA, wait

class TestRiotWatcherMethods(unittest.TestCase):

    def setUp(self):
        with open('key.txt', 'r') as keyFile:
            self.key = keyFile.readline()
        with open('name.txt', 'r') as nameFile:
            self.summoner_name = nameFile.readline()
            
        self.w = RiotWatcher(self.key)
        
    def test_get_all_champions(self):
        wait(self.w)
        method_json = self.w.get_all_champions()
        
        wait(self.w)
        r = requests.get('https://na.api.pvp.net/api/lol/na/v1.2/champion/?freeToPlay=False&api_key=' + self.key)
        correct_json = r.json()

        self.assertEqual(correct_json, method_json)


if __name__ == '__main__':
    unittest.main()
