import re
import requests
import unittest
from riotwatcher import RiotWatcher, NORTH_AMERICA, LoLException, wait

class TestRiotWatcherMethods(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        with open('key.txt', 'r') as keyFile:
            self.key = keyFile.readline()
        with open('name.txt', 'r') as nameFile:
            self.summoner_name = nameFile.readline()
            
        self.w = RiotWatcher(self.key)

    def setUp(self):
        wait(self.w)
        
    def test_get_all_champions_for_no_args(self):
        method_json = self.w.get_all_champions()
        
        wait(self.w)
        r = requests.get('https://na.api.pvp.net/api/lol/na/v1.2/champion/?freeToPlay=False&api_key=' + self.key)
        correct_json = r.json()

        self.assertEqual(correct_json, method_json)

    def test_get_all_champions_for_free_to_play(self):
        method_json = self.w.get_all_champions(free_to_play=True)
        
        wait(self.w)
        r = requests.get('https://na.api.pvp.net/api/lol/na/v1.2/champion/?freeToPlay=True&api_key=' + self.key)
        correct_json = r.json()
        
        self.assertEqual(correct_json, method_json)

    def test_get_champion_for_extant_champ(self):
        champID = 81 #Ezreal         
        method_json = self.w.get_champion(champID)

        r = requests.get('https://na.api.pvp.net/api/lol/na/v1.2/champion/' + str(champID) + '?api_key=' + self.key)
        correct_json = r.json()
        
        self.assertEqual(correct_json, method_json)
        
    def test_get_champion_for_nonexistant_champ(self):
        with self.assertRaises(LoLException):
            self.w.get_champion(420)

    def test_featured_games(self):
        #This test may fail if one of the featured games ends after the method_json call and before the correct_json call.
        
        #Have to remove the game length parameters from the json, since those will not match
        #Ideally, test would also make sure that the second game has a larger game length.

        game_length_regex = r"'gameLength':\s*\d+,"
        
        method_json = re.sub(game_length_regex, "", str(self.w.get_featured_games()))

        r = requests.get('https://na.api.pvp.net/observer-mode/rest/featured?api_key=' + self.key)
        correct_json = re.sub(game_length_regex, "", str(r.json()))

        self.assertEqual(correct_json, method_json)

if __name__ == '__main__':
    unittest.main()
