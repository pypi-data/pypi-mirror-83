import requests
from enum import IntEnum

class Mods(IntEnum):
	NOMOD = 0
	NOFAIL = 1 << 0
	EASY = 1 << 1
	TOUCHSCREEN = 1 << 2
	HIDDEN = 1 << 3
	HARDROCK = 1 << 4
	SUDDENDEATH = 1 << 5
	DOUBLETIME = 1 << 6
	RELAX = 1 << 7
	HALFTIME = 1 << 8
	NIGHTCORE = 1 << 9
	FLASHLIGHT = 1 << 10
	AUTOPLAY = 1 << 11
	SPUNOUT = 1 << 12
	RELAX2 = 1 << 13
	PERFECT = 1 << 14
	KEY4 = 1 << 15
	KEY5 = 1 << 16
	KEY6 = 1 << 17
	KEY7 = 1 << 18
	KEY8 = 1 << 19
	KEYMOD = 1 << 20
	FADEIN = 1 << 21
	RANDOM = 1 << 22
	LASTMOD = 1 << 23
	KEY9 = 1 << 24
	KEY10 = 1 << 25
	KEY1 = 1 << 26
	KEY3 = 1 << 27
	KEY2 = 1 << 28
	SCOREV2 = 1 << 29

def readableMods(m: int) -> str:
	"""
	Return a string with readable std mods.
	Used to convert a mods number for oppai
	:param m: mods bitwise number
	:return: readable mods string, eg HDDT
	"""

	if not m: return ''

	r = []
	if m & Mods.NOFAIL:      r.append('NF')
	if m & Mods.EASY:        r.append('EZ')
	if m & Mods.TOUCHSCREEN: r.append('TD')
	if m & Mods.HIDDEN:      r.append('HD')
	if m & Mods.HARDROCK:    r.append('HR')
	if m & Mods.DOUBLETIME:  r.append('DT')
	if m & Mods.RELAX:       r.append('RX')
	if m & Mods.HALFTIME:    r.append('HT')
	if m & Mods.NIGHTCORE:   r.append('NC')
	if m & Mods.FLASHLIGHT:  r.append('FL')
	if m & Mods.SPUNOUT:     r.append('SO')
	if m & Mods.SCOREV2:     r.append('V2')
	d = ''.join(r)
	return d.replace('DT','') if 'NC' in d else d

def calc_acc(mode, count_300, count_100, count_50, count_miss, count_katu = 0, count_geki = 0):
	if mode == 0:
		total = sum((int(count_300), int(count_100), int(count_50), int(count_miss)))
		d = 100.0 * sum((
		int(count_50) * 50.0,
		int(count_100) * 100.0,
		int(count_300) * 300.0
		)) / (total * 300.0)
		return round(d, 2)
	elif mode == 1:
		total = sum((int(count_300), int(count_100), int(count_miss)))
		d = 100.0 * sum((
		int(count_100) * 150.0,
		int(count_300) * 300.0
		)) / (total * 300.0)
		return round(d, 2)
	elif mode == 2:
		return 0 # CTB
	elif mode == 3:
		return 0 # MANIA
	else:
		return 0

class osu():

	def __init__(self, api_base = 'bancho', bancho_api_key = '', letters = None) -> None:
		"""
		Hello!\n
		This class allows you to get the following\n
		recent scores | best scores | scores | beatmap info | mapid's | user's stats\n
		Coolest thing about this is, it returns the same formatted dictionary for the servers supported.\n
		Remember that this is still a working progress!\n
		TODO:\n
			Move to bancho api v2 at some point\n
			Accuracy on bancho for modes like Catch the Beat and Mania\n
		\n
		This is how you can use this class!
		------------------------
		from coverosu import osu
		
		osu = osu(api_base='bancho', bancho_api_key='Osu Api Key')

		stats = osu.profile('[Cover]')

		for stat in stats:
			print(f'{stat}: {stats[stat]}')
		------------------------
		\n
		To get more information about each function, you can simply do\n
		------------------------
		from coverosu import osu
		osu = osu()
		print(osu.profile.__doc__)
		------------------------
		"""
		self.api_base = api_base
		self.bancho_api_key = bancho_api_key if bancho_api_key != '' else print("No api key was provided! Can't use bancho api")
		self.letters = letters if letters != None else print("No letters where provided! Can't process any letter links. (This is for discord embeds)")

	def get_mapid(self, string):
		"""
		Parsers the beatmap ID from a string.\n
		Such as "https://akatsuki.pw/b/123 guys check out my map!".\n
		This function returns a list of all the ids provided. (Removes duplicates!)\n
		Note that this doesn't determine if an id is a set or an individual map.
		"""
		links = [
			'https://akatsuki.pw/b/', 
			'https://akatsuki.pw/d/',
			'https://osu.ppy.sh/b/',
			'https://osu.ppy.sh/d/',
			'https://osu.ppy.sh/beatmapsets/',
			'https://osu.gatari.pw/b/',
			'https://osu.gatari.pw/d/',
			'https://ripple.moe/b/',
			'https://ripple.moe/b/',
			]
		beatmapid = []
		for _link in links:
			if _link in string:
				if _link != 'https://osu.ppy.sh/beatmapsets/':
					string = string.split(_link)
				else:
					string = " ".join(string.split(_link)).replace('#','').split('/')
				for strr in string:
					_beatmapid = []
					for char in strr:
						if char.isnumeric():
							_beatmapid.append(char)
						if char == ' ' and strr.index(char) != 0:
							break
					beatmapid.append("".join(_beatmapid))
					try:
						beatmapid.remove('')
					except:
						pass

		return list(dict.fromkeys(beatmapid))

	def get_beatmap(self, beatmapid, mode = 0, maptype = 'b'):
		"""
		Gets beatmap information from the beatmap ID.\n
		Required:\n
			Osu! API Key: You can find an api key here -> https://osu.ppy.sh/p/api/\n
		Optional:\n
			maptype: if you provided a set ID, you can put 's' as the maptype, if you didn't you can set it to 'b'. The maptype by default is 'b'\n
			mode: 0 is std, 1 is taiko, 2 is ctb, 3 is mania
		"""
		base_api = "https://osu.ppy.sh/api"
		params = {
			'k': self.bancho_api_key,
			'm': mode,
			maptype: beatmapid,
			'a': 1
		}
		_beatmapinfo = requests.get(f"{base_api}/get_beatmaps?", params=params)
		if not _beatmapinfo:
			raise Exception("Map couldn't be found.")
		return _beatmapinfo.json()[0]
		
	def get_scores(self, userid, beatmapid, mode = 0, relax = 0, limit = 0):
		"""
		Gets a user's score on a specific map using their user ID and the beatmap ID\n

		Required:\n
			(Kind of optional) Osu! API Key: If your api base is bancho (by default) then you will need an api key where you can find here -> https://osu.ppy.sh/p/api/\n
			userid: Example, 40626 (40626 being the user ID)\n
			beatmapid: Example, https://akatsuki.pw/b/2514777 (2514777 being the user ID)\n
		Optional:\n
			relax: 1 if you want a relax score (only supported on relax servers) and 0 if you don't\n
			mode: 0 is std, 1 is taiko, 2 is ctb, 3 is mania\n
			limit: If a user has multiple scores on a map, you can literate through them using this! Setting limit to 1 will get the user's 2nd best play on the map
		"""
		if 'bancho' in self.api_base:
			with requests.Session() as e:
				base_api = "https://osu.ppy.sh/api"
				params = {
					'k': self.bancho_api_key,
					'b': beatmapid,
					'u': userid,
					'm': mode,
					'type': 'id' if isinstance(userid, int) else 'string' 
				}
				_stats = e.get(f'{base_api}/get_scores?', params=params)
				stats = _stats.json()
				if not _stats or len(stats) == 0:
					raise Exception("Coudn't find a score on this map for this user.")
				stats = stats[limit - 1 if limit > 0 else limit]
				params = {
					'k': self.bancho_api_key,
					'b': beatmapid
				}
				_beatmapinfo = e.get(f"{base_api}/get_beatmaps?", params=params)
				if not _beatmapinfo:
					raise Exception("Map couldn't be found.")
				beatmapinfo = _beatmapinfo.json()[0]
				return {
					'beatmap_id':beatmapid,
					'beatmapset_id': beatmapinfo['beatmapset_id'],
					'artist': beatmapinfo['artist'],
					'title': beatmapinfo['title'],
					'version': beatmapinfo['version'],
					'ar': beatmapinfo['diff_approach'],
					'od': beatmapinfo['diff_overall'],
					'difficultyrating': round(float(beatmapinfo['difficultyrating']), 2),
					'score': stats['score'],
					'maxcombo': stats['maxcombo'],
					'fullcombo': beatmapinfo['max_combo'],
					'count_50': stats['count50'],
					'count_100': stats['count100'],
					'count_300': stats['count300'],
					'pp': round(float(stats['pp']), 2) if stats['pp'] != '0' else stats['pp'],
					'count_miss': stats['countmiss'],
					'enabled_mods': 'NM' if readableMods(int(stats['enabled_mods'])) == '' else readableMods(int(stats['enabled_mods'])),
					'intmods': int(stats['enabled_mods']),
					'rank': self.letters.get(stats['rank']) if self.letters else stats['rank'],
					'accuracy': calc_acc(mode, stats['count300'], stats['count100'], stats['count50'], stats['countmiss']),
					'avatar_url': "http://s.ppy.sh/a/" + str(self.profile(userid)['userid'])
				}
		
		elif 'akatsuki' in self.api_base:
			base_api = "https://akatsuki.pw/api/v1"
			params = {
				'u': userid if isinstance(userid, int) else self.profile(userid)['userid'],
				'm': mode,
				'rx': relax,
				'b': beatmapid
			}
			_stats = requests.get(f"{base_api}/get_scores?", params=params)
			if not _stats:
				raise Exception("User Coudn't be found.")
			stats = _stats.json()[limit - 1 if limit > 0 else limit]
			beatmapinfo = self.get_beatmap(beatmapid=beatmapid, mode=mode)
			return {
				'beatmap_id': beatmapinfo['beatmap_id'],
				'beatmapset_id': beatmapinfo['beatmapset_id'],
				'artist': beatmapinfo['artist'],
				'title': beatmapinfo['title'],
				'version': beatmapinfo['version'],
				'ar': beatmapinfo['diff_approach'],
				'od': beatmapinfo['diff_overall'],
				'difficultyrating': round(float(beatmapinfo['difficultyrating']), 2),
				'score': stats['score'],
				'maxcombo': stats['maxcombo'],
				'fullcombo': beatmapinfo['max_combo'],
				'count_50': stats['count50'],
				'count_100': stats['count100'],
				'count_300': stats['count300'],
				'pp': round(float(stats['pp']), 2) if stats['pp'] != '0' else stats['pp'],
				'count_miss': stats['countmiss'],
				'enabled_mods': 'NM' if readableMods(int(stats['enabled_mods'])) == '' else readableMods(int(stats['enabled_mods'])),
				'intmods': int(stats['enabled_mods']),
				'rank': self.letters.get(stats['rank']) if self.letters else stats['rank'],
				'accuracy': calc_acc(mode, stats['count300'], stats['count100'], stats['count50'], stats['countmiss']),
				'avatar_url': "http://a.akatsuki.pw/" + str(stats['user_id'])
			}
		
		elif 'ripple' in self.api_base:
			base_api = "https://ripple.moe/api/v1"
			params = {
				'u': userid if isinstance(userid, int) else self.profile(userid)['userid'],
				'mode': mode,
				'relax': relax,
				'b': beatmapid
			}
			_stats = requests.get(f"{base_api}/get_scores?", params=params)
			if not _stats:
				raise Exception("User Coudn't be found.")
			stats = _stats.json()[limit - 1 if limit > 0 else limit]
			beatmapinfo = self.get_beatmap(beatmapid=beatmapid, mode=mode)
			return {
				'beatmap_id': beatmapinfo['beatmap_id'],
				'beatmapset_id': beatmapinfo['beatmapset_id'],
				'artist': beatmapinfo['artist'],
				'title': beatmapinfo['title'],
				'version': beatmapinfo['version'],
				'ar': beatmapinfo['diff_approach'],
				'od': beatmapinfo['diff_overall'],
				'difficultyrating': round(float(beatmapinfo['difficultyrating']), 2),
				'score': stats['score'],
				'maxcombo': stats['maxcombo'],
				'fullcombo': beatmapinfo['max_combo'],
				'count_50': stats['count50'],
				'count_100': stats['count100'],
				'count_300': stats['count300'],
				'pp': round(float(stats['pp']), 2) if stats['pp'] != '0' else stats['pp'],
				'count_miss': stats['countmiss'],
				'enabled_mods': 'NM' if readableMods(int(stats['enabled_mods'])) == '' else readableMods(int(stats['enabled_mods'])),
				'intmods': int(stats['enabled_mods']),
				'rank': self.letters.get(stats['rank']) if self.letters else stats['rank'],
				'accuracy': calc_acc(mode, stats['count300'], stats['count100'], stats['count50'], stats['countmiss']),
				'avatar_url': "http://a.ripple.moe/" + str(stats['user_id'])
			}
		
		elif 'gatari' in self.api_base:
			base_api = "https://api.gatari.pw"
			params = {
				'u': self.profile(userid)['userid'] if isinstance(userid, str) else userid,
				'mode': mode,
				'b': beatmapid
			}
			_stats = requests.get(f"{base_api}/beatmap/user/score?", params=params)
			if not _stats:
				raise Exception("User Coudn't be found.")
			stats = _stats.json()['score']
			beatmapinfo = self.get_beatmap(beatmapid=beatmapid, mode=mode)
			return {
				'beatmap_id': beatmapinfo['beatmap_id'],
				'beatmapset_id': beatmapinfo['beatmapset_id'],
				'artist': beatmapinfo['artist'],
				'title': beatmapinfo['title'],
				'version': beatmapinfo['version'],
				'ar': beatmapinfo['diff_approach'],
				'od': beatmapinfo['diff_overall'],
				'difficultyrating': round(float(beatmapinfo['difficultyrating']), 2),
				'score': stats['score'],
				'maxcombo': stats['max_combo'],
				'fullcombo': beatmapinfo['max_combo'],
				'count_50': stats['count_50'],
				'count_100': stats['count_100'],
				'count_300': stats['count_300'],
				'pp': round(float(stats['pp']), 2) if stats['pp'] != 0 else stats['pp'],
				'count_miss': stats['count_miss'],
				'enabled_mods': 'NM' if readableMods(int(stats['mods'])) == '' else readableMods(int(stats['mods'])),
				'intmods': int(stats['mods']),
				'rank': self.letters.get(stats['ranking']) if self.letters else stats['ranking'],
				'accuracy': round(float(stats['accuracy']), 2),
				'avatar_url': f"http://a.gatari.pw/{str(self.profile(userid)['userid'])}"
			}

	def profile(self, userid, mode = 0, relax = 0):
		"""
		Gets a user's stats\n
		\n
		Required:\n
			(Kind of optional) Osu! API Key: If your api base is bancho (by default) then you will need an api key where you can find here -> https://osu.ppy.sh/p/api/\n
			userid: Example, 40626 (40626 being the user ID)\n
		Optional:\n
			relax: 1 if you want a relax score (only supported on relax servers) and 0 if you don't\n
			mode: 0 is std, 1 is taiko, 2 is ctb, 3 is mania
		"""
		if 'bancho' in self.api_base:
			base_api = "https://osu.ppy.sh/api"
			params = {
				'k': self.bancho_api_key,
				'u': userid,
				'm': mode,
				'type': 'id' if isinstance(userid, int) else 'string' 
			}
			_stats = requests.get(f"{base_api}/get_user?", params=params)
			if not _stats:
				raise Exception("User Coudn't be found.")
			try:
				stats = _stats.json()[0]
			except:
				raise Exception("No score could be found")
			return {
				'userid': stats['user_id'],
				'username': stats['username'],
				'join_date': stats['join_date'],
				'global_rank': stats['pp_rank'],
				'playcount': stats['playcount'],
				'ranked_score': stats['ranked_score'],
				'total_score': stats['total_score'],
				'level': round(float(stats['level']), 2),
				'pp': round(float(stats['pp_raw']), 2),
				'accuracy': round(float(stats['accuracy']), 2),
				'country': stats['country'],
				'country_rank': stats['pp_country_rank'],
				'avatar_url': "http://s.ppy.sh/a/" + str(stats['user_id'])
			}

		elif 'akatsuki' in self.api_base:
			base_api = "https://akatsuki.pw/api/v1"
			gamemodes = ['std', 'taiko', 'ctb', 'mania']
			params = {
				'id' if isinstance(userid, int) else 'name': userid,
				'm': mode,
			}
			_stats = requests.get(f"{base_api}/users/full?", params=params)
			if not _stats:
				raise Exception("User Coudn't be found.")
			stats = _stats.json()
			game_stats = stats['stats'][relax][gamemodes[mode]]
			return {
				'userid': stats['id'],
				'username': stats['username'],
				'join_date': stats['registered_on'],
				'global_rank': game_stats['global_leaderboard_rank'],
				'playcount': game_stats['playcount'],
				'ranked_score': game_stats['ranked_score'],
				'total_score': game_stats['total_score'],
				'level': round(float(game_stats['level'])),
				'pp': game_stats['pp'],
				'accuracy': round(float(game_stats['accuracy'])),
				'country': stats['country'],
				'country_rank': game_stats['country_leaderboard_rank'],
				'avatar_url': "https://a.akatsuki.pw/" + str(stats['id'])
			}

		elif 'ripple' in self.api_base:
			base_api = "https://ripple.moe/api/v1"
			gamemodes = ['std', 'taiko', 'ctb', 'mania']
			params = {
				'id' if isinstance(userid, int) else 'name': userid,
				'm': mode,
				'relax': relax
			}
			_stats = requests.get(f"{base_api}/users/full?", params=params)
			if not _stats:
				raise Exception("User Coudn't be found.")
			stats = _stats.json()
			game_stats = stats[gamemodes[mode]]
			return {
				'userid': stats['id'],
				'username': stats['username'],
				'join_date': stats['registered_on'],
				'global_rank': game_stats['global_leaderboard_rank'],
				'playcount': game_stats['playcount'],
				'ranked_score': game_stats['ranked_score'],
				'total_score': game_stats['total_score'],
				'level': round(float(game_stats['level'])),
				'pp': game_stats['pp'],
				'accuracy': round(float(game_stats['accuracy'])),
				'country': stats['country'],
				'country_rank': game_stats['country_leaderboard_rank'],
				'avatar_url': "https://a.ripple.moe/" + str(stats['id'])
			}
		
		elif 'gatari' in self.api_base:
			base_api = "https://api.gatari.pw"
			params = {
				'u': userid,
			}
			_userinfo = requests.get(f"{base_api}/users/get?", params=params)
			if not _userinfo:
				raise Exception("User Coudn't be found.")
			userinfo = _userinfo.json()['users'][0]
			params = {
				'u': userid,
				'mode': mode
			}
			_stats = requests.get(f"{base_api}/user/stats?", params=params)
			if not _stats:
				raise Exception("User Coudn't be found.")
			stats = _stats.json()['stats']
			return {
				'userid': userinfo['id'],
				'username': userinfo['username'],
				'join_date': userinfo['registered_on'],
				'global_rank': stats['rank'], 
				'playcount': stats['playcount'], 
				'ranked_score': stats['ranked_score'], 
				'total_score': stats['total_score'], 
				'level': stats['level'], 
				'pp': stats['pp'],  
				'accuracy': round(float(stats['avg_accuracy'])),
				'country': userinfo['country'],
				'country_rank': stats['country_rank'],
				'avatar_url': "https://a.gatari.pw/" + str(userinfo['id'])
			}
		
		else:
			raise Exception("Coudn't find a valid server")

	def recent_score(self, userid, mode = 0, relax = 0, limit = 0):
		"""
		Gets a user's recent score\n
		\n
		Required:\n
			(Kind of optional) Osu! API Key: If your api base is bancho (by default) then you will need an api key where you can find here -> https://osu.ppy.sh/p/api/\n
			userid: Example, 40626 (40626 being the user ID)\n
		Optional:\n
			relax: 1 if you want a relax score (only supported on relax servers) and 0 if you don't\n
			mode: 0 is std, 1 is taiko, 2 is ctb, 3 is mania\n
			limit: If a user has multiple scores on a map, you can literate through them using this! Setting limit to 1 will get the user's 2nd best play on the map
		"""
		if 'bancho' in self.api_base:
			with requests.Session() as e: 
				base_api = "https://osu.ppy.sh/api"
				params = {
					'k': self.bancho_api_key,
					'u': userid,
					'm': mode,
					'type': 'id' if isinstance(userid, int) else 'string' 
				}
				_stats = e.get(f"{base_api}/get_user_recent?", params=params)
				if not _stats:
					raise Exception("User Coudn't be found.")
				try:
					stats = _stats.json()[limit - 1 if limit > 0 else limit]
				except:
					raise Exception("Couldn't find score.")
				if stats['rank'] != 'F':
					params = {
						'k': self.bancho_api_key,
						'b': stats['beatmap_id'],
						'u': userid,
						'm': mode,
						'type': 'id' if isinstance(userid, int) else 'string' 
					}
					_info = e.get(f'{base_api}/get_scores?', params=params)
					if not _info or len(_info.json()) == 0:
						stats['pp'] = 0
						stats['complete'] = 'No'
					else:
						info = _info.json()
						for score in info:
							if score['score'] == stats['score'] and score['maxcombo'] == stats['maxcombo'] and score['count50'] == stats['count50'] and score['count100'] == stats['count100'] and score['count300'] == stats['count300'] and score['countmiss'] == stats['countmiss'] and score['countkatu'] == stats['countkatu'] and score['countgeki'] == stats['countgeki'] and score['perfect'] == stats['perfect'] and score['enabled_mods'] == stats['enabled_mods'] and score['enabled_mods'] == stats['enabled_mods'] and score['rank'] == stats['rank']:
								stats['pp'] = score['pp']
								stats['complete'] = 'Yes'
							else:
								stats['pp'] = 0
								stats['complete'] = 'No'
				else:
					stats['pp'] = 0
					stats['complete'] = 'No'
				
				params = {
					'k': self.bancho_api_key,
					'b': stats['beatmap_id']
				}
				_beatmapinfo = e.get(f"{base_api}/get_beatmaps?", params=params)
				if not _beatmapinfo:
					raise Exception("Map couldn't be found.")
				beatmapinfo = _beatmapinfo.json()[0]
				try:
					return {
						'beatmap_id': stats['beatmap_id'],
						'beatmapset_id': beatmapinfo['beatmapset_id'],
						'artist': beatmapinfo['artist'],
						'title': beatmapinfo['title'],
						'version': beatmapinfo['version'],
						'ar': beatmapinfo['diff_approach'],
						'od': beatmapinfo['diff_overall'],
						'difficultyrating': round(float(beatmapinfo['difficultyrating']), 2),
						'score': stats['score'],
						'maxcombo': stats['maxcombo'],
						'fullcombo': beatmapinfo['max_combo'],
						'count_50': stats['count50'],
						'count_100': stats['count100'],
						'count_300': stats['count300'],
						'pp': round(float(stats['pp']), 2) if stats['pp'] != '0' else stats['pp'],
						'count_miss': stats['countmiss'],
						'enabled_mods': 'NM' if readableMods(int(stats['enabled_mods'])) == '' else readableMods(int(stats['enabled_mods'])),
						'intmods': int(stats['enabled_mods']),
						'rank': self.letters.get(stats['rank']) if self.letters else stats['rank'],
						'Map_Completed': stats['complete'],
						'accuracy': calc_acc(mode, stats['count300'], stats['count100'], stats['count50'], stats['countmiss']),
						'avatar_url': "http://s.ppy.sh/a/" + str(self.profile(userid)['userid'])
					}
				except:
					raise Exception("Couldn't find recent score in the past 24 hours!")

		elif 'akatsuki' in self.api_base:
			base_api = "https://akatsuki.pw/api/v1"
			gamemodes = ['std', 'taiko', 'ctb', 'mania']
			params = {
				'id' if isinstance(userid, int) else 'name': userid,
				'mode': mode,
				'rx': relax
			}
			_stats = requests.get(f"{base_api}/users/scores/recent?", params=params)
			if not _stats:
				raise Exception("User Coudn't be found.")
			try:
				stats = _stats.json()['scores'][limit - 1 if limit > 0 else limit]
			except:
				raise Exception("Couldn't find score.")
			return {
				'beatmap_id': stats['beatmap']['beatmap_id'],
				'beatmapset_id': stats['beatmap']['beatmapset_id'],
				'artist': stats['beatmap']['song_name'].split('-')[0][:-1],
				'title': "".join(stats['beatmap']['song_name'].split('-')[1]).split('[')[0][:-1][1:],
				'version': stats['beatmap']['song_name'].split('[')[1][:-1],
				'ar': stats['beatmap']['ar'],
				'od': stats['beatmap']['od'],
				'difficultyrating': round(float(stats['beatmap']['difficulty2'][gamemodes[mode]]), 2),
				'score': stats['score'],
				'maxcombo': stats['max_combo'],
				'fullcombo': stats['beatmap']['max_combo'],
				'count_50': stats['count_50'],
				'count_100': stats['count_100'],
				'count_300': stats['count_300'],
				'pp': round(float(stats['pp']), 2) if stats['pp'] != '0' else stats['pp'],
				'count_miss': stats['count_miss'],
				'enabled_mods': 'NM' if readableMods(int(stats['mods'])) == '' else readableMods(int(stats['mods'])),
				'intmods': int(stats['mods']),
				'rank': self.letters.get(stats['rank']) if self.letters else stats['rank'],
				'Map_Completed': 'No' if stats['completed'] == 0 else 'Yes',
				'accuracy': round(float(stats['accuracy']), 2) if float(stats['accuracy']) else stats['accuracy'],
				'avatar_url': "http://a.akatsuki.pw/" + str(self.profile(userid)['userid'])
			}

		elif 'ripple' in self.api_base:
			base_api = "https://ripple.moe/api/v1"
			gamemodes = ['std', 'taiko', 'ctb', 'mania']
			params = {
				'id' if isinstance(userid, int) else 'name': userid,
				'm': mode,
				'relax': relax
			}
			_stats = requests.get(f"{base_api}/users/scores/recent?", params=params)
			if not _stats:
				raise Exception("User Coudn't be found.")
			try:
				stats = _stats.json()['scores'][limit - 1 if limit > 0 else limit]
			except:
				raise Exception("Couldn't find score.")
			return {
				'beatmap_id': stats['beatmap']['beatmap_id'],
				'beatmapset_id': stats['beatmap']['beatmapset_id'],
				'artist': stats['beatmap']['song_name'].split('-')[0][:-1],
				'title': "".join(stats['beatmap']['song_name'].split('-')[1]).split('[')[0][:-1][1:],
				'version': stats['beatmap']['song_name'].split('[')[1][:-1],
				'ar': stats['beatmap']['ar'],
				'od': stats['beatmap']['od'],
				'difficultyrating': round(float(stats['beatmap']['difficulty2'][gamemodes[mode]]), 2),
				'score': stats['score'],
				'maxcombo': stats['max_combo'],
				'fullcombo': stats['beatmap']['max_combo'],
				'count_50': stats['count_50'],
				'count_100': stats['count_100'],
				'count_300': stats['count_300'],
				'pp': round(float(stats['pp']), 2) if stats['pp'] != '0' else stats['pp'],
				'count_miss': stats['count_miss'],
				'enabled_mods': 'NM' if readableMods(int(stats['mods'])) == '' else readableMods(int(stats['mods'])),
				'intmods': int(stats['mods']),
				'rank': self.letters.get(stats['rank']) if self.letters else stats['rank'],
				'Map_Completed': 'No' if stats['completed'] == 0 else 'Yes',
				'accuracy': round(float(stats['accuracy']), 2) if float(stats['accuracy']) else stats['accuracy'],
				'avatar_url': "http://a.ripple.moe/" + str(self.profile(userid)['userid'])
			
			}
		
		elif 'gatari' in self.api_base:
			base_api = "https://api.gatari.pw"
			params = {
				'id': self.profile(userid)['userid'] if isinstance(userid, str) else userid,
				'mode': mode,
				'f': 0
			}
			_stats = requests.get(f"{base_api}/user/scores/recent?", params=params)
			if not _stats:
				raise Exception("User Coudn't be found.")
			try:
				stats = _stats.json()['scores'][limit - 1 if limit > 0 else limit]
			except:
				raise Exception("Couldn't find score.")
			return {
				'beatmap_id': stats['beatmap']['beatmap_id'],
				'beatmapset_id': stats['beatmap']['beatmapset_id'],
				'artist': stats['beatmap']['artist'],
				'title': stats['beatmap']['title'],
				'version': stats['beatmap']['version'],
				'ar': stats['beatmap']['ar'],
				'od': stats['beatmap']['od'],
				'difficultyrating': round(float(stats['beatmap']['difficulty']), 2),
				'score': stats['score'],
				'maxcombo': stats['max_combo'],
				'fullcombo': stats['beatmap']['fc'],
				'count_50': stats['count_50'],
				'count_100': stats['count_100'],
				'count_300': stats['count_300'],
				'pp': round(float(stats['pp']), 2) if stats['pp'] != 0 else stats['pp'],
				'count_miss': stats['count_miss'],
				'enabled_mods': 'NM' if readableMods(int(stats['mods'])) == '' else readableMods(int(stats['mods'])),
				'intmods': int(stats['mods']),
				'rank': self.letters.get(stats['ranking']) if self.letters else stats['ranking'],
				'Map_Completed': 'No' if stats['completed'] == 0 else 'Yes',
				'accuracy': round(float(stats['accuracy']), 2) if float(stats['accuracy']) else stats['accuracy'],
				'avatar_url': f"http://a.gatari.pw/{str(self.profile(userid)['userid'])}"
			}

		else:
			raise Exception("Coudn't find a valid server")

	def best_score(self, userid, mode = 0, relax = 0, limit = 0):
		"""
		Gets a user's best score\n

		Required:\n
			(Kind of optional) Osu! API Key: If your api base is bancho (by default) then you will need an api key where you can find here -> https://osu.ppy.sh/p/api/\n
			userid: Example, 40626 (40626 being the user ID)\n
		Optional:\n
			relax: 1 if you want a relax score (only supported on relax servers) and 0 if you don't\n
			mode: 0 is std, 1 is taiko, 2 is ctb, 3 is mania\n
			limit: If a user has multiple scores on a map, you can literate through them using this! Setting limit to 1 will get the user's 2nd best play on the map
		"""
		if 'bancho' in self.api_base:
			with requests.Session() as e:
				base_api = "https://osu.ppy.sh/api"
				params = {
					'k': self.bancho_api_key,
					'u': userid,
					'm': mode,
					'type': 'id' if isinstance(userid, int) else 'string'
				}
				_stats = e.get(f"{base_api}/get_user_best?", params=params)
				if not _stats:
					raise Exception("User Coudn't be found.")
				try:
					stats = _stats.json()[limit - 1 if limit > 0 else limit]
				except:
					raise Exception("Couldn't find score.")
				params = {
					'k': self.bancho_api_key,
					'b': stats['beatmap_id']
				}
				_beatmapinfo = e.get(f"{base_api}/get_beatmaps?", params=params)
				if not _beatmapinfo:
					raise Exception("Map couldn't be found.")
				beatmapinfo = _beatmapinfo.json()[0]
				try:
					return {
						'beatmap_id': stats['beatmap_id'],
						'beatmapset_id': beatmapinfo['beatmapset_id'],
						'artist': beatmapinfo['artist'],
						'title': beatmapinfo['title'],
						'version': beatmapinfo['version'],
						'ar': beatmapinfo['diff_approach'],
						'od': beatmapinfo['diff_overall'],
						'difficultyrating': round(float(beatmapinfo['difficultyrating']), 2),
						'score': stats['score'],
						'maxcombo': stats['maxcombo'],
						'fullcombo': beatmapinfo['max_combo'],
						'count_50': stats['count50'],
						'count_100': stats['count100'],
						'count_300': stats['count300'],
						'pp': round(float(stats['pp']), 2) if stats['pp'] != '0' else stats['pp'],
						'count_miss': stats['countmiss'],
						'enabled_mods': 'NM' if readableMods(int(stats['enabled_mods'])) == '' else readableMods(int(stats['enabled_mods'])),
						'intmods': int(stats['enabled_mods']),
						'rank': self.letters.get(stats['rank']) if self.letters else stats['rank'],
						'accuracy': calc_acc(mode=mode, count_300=stats['count300'], count_100=stats['count100'], count_50=stats['count50'], count_miss=stats['countmiss'], count_katu=stats['countkatu'], count_geki=stats['countgeki']),
						'avatar_url': "http://s.ppy.sh/a/" + str(self.profile(userid)['userid'])
					}
				except:
					raise Exception("No plays were found.")

		elif 'akatsuki' in self.api_base:
			base_api = "https://akatsuki.pw/api/v1"
			gamemodes = ['std', 'taiko', 'ctb', 'mania']
			params = {
				'id' if isinstance(userid, int) else 'name': userid,
				'mode': mode,
				'rx': relax
			}
			_stats = requests.get(f"{base_api}/users/scores/best?", params=params)
			if not _stats:
				raise Exception("User Coudn't be found.")
			try:
				stats = _stats.json()['scores'][limit - 1 if limit > 0 else limit]
			except:
				raise Exception("Couldn't find score.")
			return {
				'beatmap_id': stats['beatmap']['beatmap_id'],
				'beatmapset_id': stats['beatmap']['beatmapset_id'],
				'artist': stats['beatmap']['song_name'].split('-')[0][:-1],
				'title': "".join(stats['beatmap']['song_name'].split('-')[1]).split('[')[0][:-1][1:],
				'version': stats['beatmap']['song_name'].split('[')[1][:-1],
				'ar': stats['beatmap']['ar'],
				'od': stats['beatmap']['od'],
				'difficultyrating': round(float(stats['beatmap']['difficulty2'][gamemodes[mode]]), 2),
				'score': stats['score'],
				'maxcombo': stats['max_combo'],
				'fullcombo': stats['beatmap']['max_combo'],
				'count_50': stats['count_50'],
				'count_100': stats['count_100'],
				'count_300': stats['count_300'],
				'pp': round(float(stats['pp']), 2) if stats['pp'] != '0' else stats['pp'],
				'count_miss': stats['count_miss'],
				'enabled_mods': 'NM' if readableMods(int(stats['mods'])) == '' else readableMods(int(stats['mods'])),
				'intmods': int(stats['mods']),
				'rank': self.letters.get(stats['rank']) if self.letters else stats['rank'],
				'accuracy': round(float(stats['accuracy']), 2) if float(stats['accuracy']) else stats['accuracy'],
				'avatar_url': "http://a.akatsuki.pw/" + str(self.profile(userid)['userid'])
			}

		elif 'ripple' in self.api_base:
			base_api = "https://ripple.moe/api/v1"
			gamemodes = ['std', 'taiko', 'ctb', 'mania']
			params = {
				'id' if isinstance(userid, int) else 'name': userid,
				'm': mode,
				'relax': relax
			}
			_stats = requests.get(f"{base_api}/users/scores/best?", params=params)
			if not _stats:
				raise Exception("User Coudn't be found.")
			try:
				stats = _stats.json()['scores'][limit - 1 if limit > 0 else limit]
			except:
				raise Exception("Couldn't find score.")
			return {
				'beatmap_id': stats['beatmap']['beatmap_id'],
				'beatmapset_id': stats['beatmap']['beatmapset_id'],
				'artist': stats['beatmap']['song_name'].split('-')[0][:-1],
				'title': "".join(stats['beatmap']['song_name'].split('-')[1]).split('[')[0][:-1][1:],
				'version': stats['beatmap']['song_name'].split('[')[1][:-1],
				'ar': stats['beatmap']['ar'],
				'od': stats['beatmap']['od'],
				'difficultyrating': round(float(stats['beatmap']['difficulty2'][gamemodes[mode]]), 2),
				'score': stats['score'],
				'maxcombo': stats['max_combo'],
				'fullcombo': stats['beatmap']['max_combo'],
				'count_50': stats['count_50'],
				'count_100': stats['count_100'],
				'count_300': stats['count_300'],
				'pp': round(float(stats['pp']), 2) if stats['pp'] != '0' else stats['pp'],
				'count_miss': stats['count_miss'],
				'enabled_mods': 'NM' if readableMods(int(stats['mods'])) == '' else readableMods(int(stats['mods'])),
				'rank': self.letters.get(stats['rank']) if self.letters else stats['rank'],
				'accuracy': round(float(stats['accuracy']), 2) if float(stats['accuracy']) else stats['accuracy'],
				'intmods': int(stats['mods']),
				'avatar_url': "http://a.ripple.moe/" + str(self.profile(userid)['userid'])
			}
		
		elif 'gatari' in self.api_base:
			base_api = "https://api.gatari.pw"
			params = {
				'id': self.profile(userid)['userid'] if isinstance(userid, str) else userid,
				'mode': mode,
			}
			_stats = requests.get(f"{base_api}/user/scores/best?", params=params)
			if not _stats:
				raise Exception("User Coudn't be found.")
			try:
				stats = _stats.json()['scores'][limit - 1 if limit > 0 else limit]
			except:
				raise Exception("Couldn't find score.")
			return {
				'beatmap_id': stats['beatmap']['beatmap_id'],
				'beatmapset_id': stats['beatmap']['beatmapset_id'],
				'artist': stats['beatmap']['artist'],
				'title': stats['beatmap']['title'],
				'version': stats['beatmap']['version'],
				'ar': stats['beatmap']['ar'],
				'od': stats['beatmap']['od'],
				'difficultyrating': round(float(stats['beatmap']['difficulty']), 2),
				'score': stats['score'],
				'maxcombo': stats['max_combo'],
				'fullcombo': stats['beatmap']['fc'],
				'count_50': stats['count_50'],
				'count_100': stats['count_100'],
				'count_300': stats['count_300'],
				'pp': round(float(stats['pp']), 2) if stats['pp'] != 0 else stats['pp'],
				'count_miss': stats['count_miss'],
				'enabled_mods': 'NM' if readableMods(int(stats['mods'])) == '' else readableMods(int(stats['mods'])),
				'intmods': int(stats['mods']),
				'rank': self.letters.get(stats['ranking']) if self.letters else stats['ranking'],
				'accuracy': round(float(stats['accuracy']), 2) if float(stats['accuracy']) else stats['accuracy'],
				'avatar_url': f"http://a.gatari.pw/{str(self.profile(userid)['userid'])}"
			}

		else:
			raise Exception("Coudn't find a valid server")