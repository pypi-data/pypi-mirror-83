"""
Requests Osu!Ripple API\n
Written in Python by ```NateTH```
"""

class get:
    """
    This is a get class.
    """
    def user(self, username=None):
        """
        Returns user data was Python dictionary.
        ```md
        PARAMETERS
        accuracy : returns user accuracy
        count100 : returns user count100
        count300 : returns user count300
        count50 : returns user count50
        count_rank_a : returns how many time that user have A rank
        count_rank_s : returns how many time that user have S rank
        count_rank_ss : returns how many time that user have SS rank
        country : returns user country
        events : returns user events
        level : returns user level
        playcount : returns how many time that user have play ripple
        pp_country_rank : returns user country rank
        pp_rank : returns user rank
        pp_raw : returns user raw
        ranked_score : returns user ranked score
        total_score : returns user total score
        user_id : returns user id
        username : returns username
        ```

        """
        import requests
        text = requests.get(f"https://ripple.moe/api/get_user?u={self}")
        import json
        a = text.text.strip("][")
        x = json.loads(a)
        return x
    
    def beatmaps(self, id=None):
        """
        Returns beatmap data was Python dictionary.
        ```md
        PARAMETERS
        approved : returns beatmap approved
        approved_date : returns beatmap approved date
        artist : returns beatmap artist
        beatmap_id : returns beatmap beatmap id
        beatmapset_id : returns beatmap beatmap set id
        bpm : returns beatmap bpm
        creator : returns beatmap creator
        diff_approach : returns beatmap difficulty approach
        diff_drain : returns beatmap difficulty drain
        diff_overall : returns beatmap difficulty overall
        diff_size : returns beatmap difficulty size
        difficultyrating : returns beatmap difficulty rating
        favourite_count : returns beatmap favourite count
        file_md5 : returns beatmap file md5
        genre_id : returns beatmap genre id
        hit_length : returns beatmap hit length
        language_id : returns beatmap language id
        last_update : returns beatmap last update datetime
        max_combo : returns beatmap max combo
        mode : returns beatmap mode
        passcount : returns beatmap passcount
        playcount : returns beatmap playcount
        source : returns beatmap source
        tags : returns beatmap tags
        title : returns beatmap title
        total_length : returns beatmap total length
        version : returns beatmap version
        ```

        """
        import requests
        text = requests.get(f"https://ripple.moe/api/get_beatmaps?b={self}")
        import json
        a = text.text.strip("][")
        x = json.loads(a)
        return x