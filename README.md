# Framester

This repository is a movie version for the popular board and party game ['Hitster'](https://hitstergame.com/en-gb/). In this game, you are shown the screenshot of a movie and you need to sort it correctly into your ever increasing timeline.

Thank you for your interest. If you find any bugs or have any improvement ideas, please reach out to me. Have fun playing 😄

## Rules

Before playing the game, you need to add the players (at least 1). Then, the players are assigned one random movie as their starting year. In each consecutive turn, they must choose the correct position in their ever increasing timeline. If the player has chosen a position, the results can be revealed and additional information about the movie are shown. Also, the game automatically evaluates the position. The first player to reach a pre-defined timeline length wins.

## Movies

The movies that are shown are extracted from [IMDBs Top 250 movie list](https://www.imdb.com/chart/top/?ref_=nv_mv_250) (plus ~20 movies added manually by me for testing purposes). For each movie, we save the (english and german) name, the release year, the director(s) and the link to an image. The linked images are found in the [TMDB](https://www.themoviedb.org/). To access TMDB we use [this API](https://github.com/AnthonyBloomer/tmdbv3api).

If you want to update your movie list, you can either do it manually (see the option in the StartupUI) or by importing the current version of the IMDB Top 250 movies. For this, you need your TMDB API Key as follows: Create a file called "credentials.json" in the root folder in which you save both keys provided by TMDB:

```json
{
    "api_key": "api-key-here",
    "req_key": "read-only-api-token-here"
}
```

## Future Improvements

Here are some ideas for future improvements that I may or may not add someday:

- better UI
- add the Token functionality found in the normal Hitster game
- different movie lists to choose from
- remote multiplayer
- increase quality of shown pictures
