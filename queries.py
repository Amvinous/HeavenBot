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


def get_trending():
    animeset = []
    query = """{
  Page(perPage: 12) {
    media(type: ANIME, status: RELEASING, sort: TRENDING_DESC) {
      title {
        userPreferred
      }
      nextAiringEpisode {
        episode
        airingAt
      }
    }
  }
}"""

    url = "https://graphql.anilist.co"

    response = rq.post(url, json={'query': query}).json()

    data = response["data"]["Page"]["media"]
    for media in data:
        if media["nextAiringEpisode"] is not None:
            next_episode = media["nextAiringEpisode"]["episode"]
            title = media["title"]["userPreferred"]
            unix = media["nextAiringEpisode"]["airingAt"]
        else:
            continue
        processed_data = {"title": title, "next episode": next_episode, "unix": unix}
        animeset.append(processed_data)
    return animeset


def emotions(emotion, type="sfw"):
    response = rq.get(f'https://api.waifu.pics/{type}/{emotion}')
    url = response.json()["url"]
    return url
