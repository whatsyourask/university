use music;

-- Select playlists with certain user id
select 
	title 
from 
	playlists 
where 
	user_id = 2;

-- Select all tracks with format track: name, artist_name, album_title ordered by track name
select 
	tracks.name,
    artists.name as artist_name,
    albums.title as album_title
from 
	tracks,
    artists,
    albums
where 
	tracks.artist_id = artists.id and
	tracks.album_id = albums.id
order by 
	tracks.name;
      
-- With left join but ordered by artist_name
select 
	tracks.name,
    artists.name as artist_name,
    albums.title as album_title
from 
	tracks 
left join artists on 
	tracks.artist_id = artists.id
left join albums on 
	tracks.album_id = albums.id
order by 
	artist_name;

-- Select all tracks which genre is Rap
select tracks.name,
       artists.name as artist_name,
       albums.title as album_title
from 
	tracks, 
    artists, 
    albums, 
    genres
where 
	tracks.artist_id = artists.id and 
	tracks.album_id = albums.id and 
	tracks.genre_id = genres.id and 
	genres.name = 'Rap';
      
-- Select all tracks in playlist with playlist_id
select 
	tracks.name,
	artists.name as artist_name,
	albums.title as album_title
from 
	playlists_tracks
left join tracks on 
	playlists_tracks.track_id = tracks.id
left join artists on 
	tracks.artist_id = artists.id
left join albums on
	tracks.album_id = albums.id
where 
	playlists_tracks.playlist_id = 1;

-- Select all albums of specified artist
select 
	albums.title
from 
	albums,
    artists
where 
	albums.artist_id = artists.id and
	albums.artist_id = 2;

-- Select count of tracks in each playlist
select 
	playlists.title,
    count(*) as tracks_count
from 
	playlists_tracks,
    playlists
where 
	playlists_tracks.playlist_id = playlists.id
group by 
	playlists_tracks.playlist_id;