
# these tests are pretty bad, mostly to make sure no exceptions are thrown

import requests
import time
from riotwatcher import RiotWatcher, NORTH_AMERICA, wait

key = '<YOUR KEY HERE>'
# if summoner doesnt have ranked teams, teams tests will fail
# if summoner doesnt have ranked stats, stats tests will fail
# these are not graceful failures, so try to use a summoner that has them
summoner_name = 'YOUR NAME HERE'

w = RiotWatcher(key)

def test_get_all_champions():
    wait(w)
    temp = w.get_all_champions()
    wait(w)
    r = requests.get('https://na.api.pvp.net/api/lol/na/v1.2/champion/?freeToPlay=False&api_key=' + key)

    return temp == r.json()

def test_get_champion():
    wait(w)
    temp = w.get_all_champions()
    wait(w)
    w.get_champion(temp['champions'][0]['id'])
    

def test_current_game():
    wait(w)
    player = w.get_featured_games()['gameList'][0]['participants'][0]['summonerName']
    wait(w)
    player_id = w.get_summoner(name=player)['id']
    wait(w)
    w.get_current_game(player_id)


def test_featured_games():
    wait(w)
    w.get_featured_games()


def test_game(summoner):
    wait(w)
    w.get_recent_games(summoner['id'])


def test_league(summoner):
    wait(w)
    w.get_league(summoner_ids=[summoner['id'], ])
    wait(w)
    w.get_league_entry(summoner_ids=[summoner['id'], ])
    wait(w)
    w.get_challenger()
    wait(w)
    w.get_master()


def test_static():
    temp = w.static_get_champion_list()
    w.static_get_champion(temp['data'][list(temp['data'])[0]]['id'])
    temp = w.static_get_item_list()
    w.static_get_item(temp['data'][list(temp['data'])[0]]['id'])
    temp = w.static_get_mastery_list()
    w.static_get_mastery(temp['data'][list(temp['data'])[0]]['id'])
    w.static_get_realm()
    temp = w.static_get_rune_list()
    w.static_get_rune(temp['data'][list(temp['data'])[0]]['id'])
    temp = w.static_get_summoner_spell_list()
    w.static_get_summoner_spell(temp['data'][list(temp['data'])[0]]['id'])
    w.static_get_versions()


def test_status():
    w.get_server_status()
    w.get_server_status(region=NORTH_AMERICA)


def test_match(match):
    wait(w)
    w.get_match(match['matchId'])


def test_match_history(summoner):
    wait(w)
    ms = w.get_match_history(summoner['id'])
    return ms['matches'][0]


def test_stats(summoner):
    wait(w)
    w.get_stat_summary(summoner['id'])
    wait(w)
    w.get_ranked_stats(summoner['id'])


def test_summoner(summoner_name):
    wait(w)
    s = w.get_summoner(name=summoner_name)
    wait(w)
    w.get_summoner(_id=s['id'])
    wait(w)
    w.get_mastery_pages([s['id'], ])
    wait(w)
    w.get_rune_pages([s['id'], ])
    wait(w)
    w.get_summoner_name([s['id'], ])
    return s


def test_team(summoner):
    wait(w)
    t = w.get_teams_for_summoner(summoner['id'])
    wait(w)
    w.get_team(t[0]['fullId'])


def main():
    test_static()
    print('static tests passed')
    test_status()
    print('status tests passed')
    result = test_get_all_champions()
    print('get all champion test passed:', result)
    test_get_champion()
    print('get champion test passed')
    test_featured_games()
    print('featured games tests passed')
    test_current_game()
    print('current games tests passed')
    s = test_summoner(summoner_name)
    print('summoner tests passed')
    test_game(s)
    print('game tests passed')
    test_league(s)
    print('league tests passed')
    test_stats(s)
    print('stats tests passed')
    test_team(s)
    print('team tests passed')
    m = test_match_history(s)
    print('match history tests passed')
    test_match(m)
    print('match passed')
    print('all tests passed, w00t. if only they were better tests...')


if __name__ == '__main__':
    main()
