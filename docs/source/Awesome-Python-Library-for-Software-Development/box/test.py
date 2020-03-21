from box import Box

movie_box = Box({
    "Robin Hood: Men in Tights": {
        "imdb_stars": 6.7,
        "length": 104,
        "stars": [ {"name": "Cary Elwes", "imdb": "nm0000144", "role": "Robin Hood"},
                   {"name": "Richard Lewis", "imdb": "nm0507659", "role": "Prince John"} ]
    }
})

print(movie_box.Robin_Hood_Men_in_Tights.imdb_stars)


my_box = Box(dict(a=1, b=2))
print(my_box.a)