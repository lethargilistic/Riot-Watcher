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


    # Get all champions tests
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

    def test_get_all_champions_for_numeric_arg(self):
        #with self.assertRaises(LoLException):
        numeric_arg_json = self.w.get_all_champions(free_to_play=345)
        wait(self.w)
        no_arg_json = self.w.get_all_champions()

        self.assertEqual(no_arg_json, numeric_arg_json)

    #Get Champion Tests
    def test_get_champion_for_extant_champ(self):
        champID = 81 #Ezreal         
        method_json = self.w.get_champion(champID)

        wait(self.w)
        r = requests.get('https://na.api.pvp.net/api/lol/na/v1.2/champion/' + str(champID) + '?api_key=' + self.key)
        correct_json = r.json()
        
        self.assertEqual(correct_json, method_json)
        
    def test_get_champion_for_nonexistant_champ(self):
        with self.assertRaises(LoLException):
            self.w.get_champion(420)

    #Freatured Games Test
    def test_featured_games(self):
        #This test may fail if one of the featured games ends after the method_json call and before the correct_json call.

        method_json = self.w.get_featured_games()

        wait(self.w)
        r = requests.get('https://na.api.pvp.net/observer-mode/rest/featured?api_key=' + self.key)
        correct_json = r.json()
        
        #Compare the game length vals. Second game should be longer.
        self.assertEqual(len(correct_json['gameList']), len(method_json['gameList']))

        first_game_ids = set()
        second_game_ids = set()
        for game in range(len(method_json['gameList'])):
            first_game_ids.add(method_json['gameList'][game]['gameId'])
            second_game_ids.add(correct_json['gameList'][game]['gameId'])

        not_shared_games = first_game_ids ^ second_game_ids #symmetric difference
        self.assertEqual(0, len(not_shared_games) % 2, "If there is any difference, there must be a unique game in both sets, so the difference will always be of equal size.")
                
        first_game_ids = first_game_ids - not_shared_games
        second_game_ids = second_game_ids - not_shared_games
        
        shared_games = first_game_ids & second_game_ids #intersection

        game_length_diffs = list()
        ids = list()
        #for each of the shared games
        for game_id in shared_games:
            first_len = 0
            #find an id in the first to get len
            for game in range(len(method_json['gameList'])):
                if method_json['gameList'][game]['gameId'] == game_id:
                    first_len = method_json['gameList'][game]['gameLength']
                    break
            second_len = 0
            
            #find an id in the second to get len
            for game in range(len(correct_json['gameList'])):
                if correct_json['gameList'][game]['gameId'] == game_id:
                    second_len = correct_json['gameList'][game]['gameLength']
                    break
                
            #compare
            game_length_diffs.append(second_len - first_len)
            ids.append(game_id)

        game_and_diff_debug_str = ''
        for i in range(len(ids)):
            game_and_diff_debug_str += str(ids[i]) + " " + str(game_length_diffs[i]) + "\n"

        for diff in game_length_diffs:
            self.assertGreaterEqual(0, diff, "The second poll of the API should have longer game lengths (negative diff), but it seems like this is somehow not guaranteed on Riot's end? \n\n\nGame ID\ttime diff (should be negative)\n" + game_and_diff_debug_str + "\n\nFirst game (method)\n\n" + str(method_json) + '\n\nSecond game (correct)\n\n' + str(correct_json))

        #test the whole json, aside from the game length
        game_length_regex = r"'gameLength':\s*\d+,"
        method_json = re.sub(game_length_regex, "", str(method_json))
        correct_json = re.sub(game_length_regex, "", str(correct_json))
        self.assertEqual(correct_json, method_json)
        
if __name__ == '__main__':
    unittest.main()
