import requests as rq


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
