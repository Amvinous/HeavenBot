import requests as rq


def get_episode(anime):
    query = """query ($search: String) {
      Media(type: ANIME, search: $search, status_in: [RELEASING, NOT_YET_RELEASED]) {
        id
        siteUrl
        episodes
        coverImage {
          color
          large
        }
        title {
          userPreferred
        }
        startDate {
          year
          month
          day
        }
        nextAiringEpisode {
          episode
          airingAt
        }
      }
    }"""
    variables = {"search": anime}
    url = "https://graphql.anilist.co"

    response = rq.post(url, json={'query': query, 'variables': variables}).json()

    data = response["data"]["Media"]
    processed_data = {
        "title": data["title"]["userPreferred"],
        "anime_url": data["siteUrl"],
        "next episode": data["nextAiringEpisode"]["episode"],
        "total episodes": data["episodes"],
        "unix": data["nextAiringEpisode"]["airingAt"],
        "pic": data["coverImage"]["large"]
    }

    return processed_data
