<h1 align="center">Tomoe</h1>

<div align="center">
  A wrapper for bancho.py that emulates osu!api v1 and v2
</div>

<br />

## Table of Contents
- [What is this project about?](#about)
- [Requeriments](#requeriments)
- [Usage](#usage)
- [Handled routes](#handled-routes)

### About
Wrapper that its main use is to make discord bots that make use of the osu!api v1 or v2 compatible with bancho.py

### Requeriments
- Python 3.13
- A working instance of bancho.py
- Access to the bancho.py api and its database

### Usage
- TODO

### Handled routes:
```
- osu!api v1
    /get_user           : Done (Without events)
    /get_beatmaps       : TODO
    /get_scores         : TODO
    /get_user_best      : TODO
    /get_user_recent    : TODO
    /get_replay         : TODO
    /get_match          : Not supported yet

- osu!api v2
    - /api/v2/beatmaps/{beatmap}/scores/users/{user}/all    : Done (Partially)
    - /api/v2/beatmaps/{beatmap}/scores                     : Done (Partially)
    - /api/v2/beatmapsets/lookup                            : Done (Partially)
    - /api/v2/scores                                        : Done (Partially)
    - /api/v2/users/{user}/{mode}                           : Done (Partially)
    - /api/v2/users/{user}/scores/{type}                    : Done (Partially)
```
