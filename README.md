Liked the posts by https://www.facebook.com/tamilnaduweatherman/ and each time I had to wait a long time to get recent updates on the weather.

On checking the pics which are posted by Tamilnaduweatherman I observed them to be from Indian Meteorological Department but there were no noticable/searchable links to the radar data on the site, so I wrote a quick hack that generates the recent url and downloads the radar images.

This script right now feeds Chennairadarmaps FB page https://www.facebook.com/Chennairadarmaps-1645977852357208/ every 15 minutes.

```
> pip install -r requirements.txt
> python chennai_radar_maps.py
```
