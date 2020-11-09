create database music;

use music;

create table artists(
id int unsigned auto_increment not null,
name varchar(255),
primary key(id)
);

create table albums(
id int unsigned auto_increment not null,
title varchar(255),
artist_id int unsigned references artists(id),
primary key(id)
);

create table genres(
id int unsigned auto_increment not null,
name varchar(255) unique,
primary key(id)
);

create table tracks(
id int unsigned auto_increment not null,
name varchar(255),
artist_id int unsigned references artists(id),
album_id int unsigned references albums(id),
genre_id int unsigned references genres(id),
primary key(id)
);

create table users(
id int unsigned auto_increment not null,
username varchar(255),
password varchar(255),
primary key(id)
);

create table subscriptions(
id int unsigned auto_increment not null,
user_id int unsigned references users(id),
is_enabled bool default null,
sub_date datetime,
primary key(id)
);

create table playlists(
id int unsigned auto_increment not null,
title varchar(255),
user_id int unsigned references users(id),
primary key(id)
);

create table playlists_tracks(
id int unsigned auto_increment not null,
playlist_id int unsigned references playlists(id),
track_id int unsigned references tracks(id),
primary key(id)
);

insert into genres (name) values ('Rock');
insert into genres (name) values ('Hip-hop');
insert into genres (name) values ('Pop');
insert into genres (name) values ('Rap');

insert into artists (name) values ('AC/DC');
insert into artists (name) values ('Queen');
insert into artists (name) values ('Cardi B');
insert into artists (name) values ('Nicki Minaj');
insert into artists (name) values ('Taylor Swift');
insert into artists (name) values ('Ariana Grande');
insert into artists (name) values ('A$AP Ferg');
insert into artists (name) values ('Drake');

insert into albums (title, artist_id) values ('Black Ice', 1);
insert into albums (title, artist_id) values ('Back In Black', 1);
insert into albums (title, artist_id) values ('Hot Space', 2);
insert into albums (title, artist_id) values ('Bohemian Rhapsody', 2);
insert into albums (title, artist_id) values ('Invasion of Privacy', 3);
insert into albums (title, artist_id) values ('Gangsta Bitch Music', 3);
insert into albums (title, artist_id) values ('Queen', 4);
insert into albums (title, artist_id) values ('The Pinkprint', 4);
insert into albums (title, artist_id) values ('Lover', 5);
insert into albums (title, artist_id) values ('1989', 5);
insert into albums (title, artist_id) values ('thank u, next', 6);
insert into albums (title, artist_id) values ('Dangerous Woman', 6);
insert into albums (title, artist_id) values ('Still Striving', 7);
insert into albums (title, artist_id) values ('Floor Seats', 7);
insert into albums (title, artist_id) values ('Scorpion', 8);
insert into albums (title, artist_id) values ('Views', 8);

insert into tracks (name, artist_id, album_id, genre_id) values ('War Machine', 1, 1, 1);
insert into tracks (name, artist_id, album_id, genre_id) values ('Rock N Roll Train', 1, 1, 1);
insert into tracks (name, artist_id, album_id, genre_id) values ('Back In Black', 1, 2, 1);
insert into tracks (name, artist_id, album_id, genre_id) values ('Back Chat', 2, 3, 1);
insert into tracks (name, artist_id, album_id, genre_id) values ('Under Pressure', 2, 3, 1);
insert into tracks (name, artist_id, album_id, genre_id) values ('Bohemian Rhapsody', 2, 4, 1);
insert into tracks (name, artist_id, album_id, genre_id) values ('I\'m in Love with My Car', 2, 4, 1);
insert into tracks (name, artist_id, album_id, genre_id) values ('Get up 10', 3, 5, 2);
insert into tracks (name, artist_id, album_id, genre_id) values ('She Bad', 3, 5, 2);
insert into tracks (name, artist_id, album_id, genre_id) values ('Rollin', 3, 6, 2);
insert into tracks (name, artist_id, album_id, genre_id) values ('Pull Up', 3, 6, 2);
insert into tracks (name, artist_id, album_id, genre_id) values ('LLC', 4, 7, 2);
insert into tracks (name, artist_id, album_id, genre_id) values ('Barbie Dreams', 4, 7, 2);
insert into tracks (name, artist_id, album_id, genre_id) values ('I Lied', 4, 8, 2);
insert into tracks (name, artist_id, album_id, genre_id) values ('All Things Go', 4, 8, 2);
insert into tracks (name, artist_id, album_id, genre_id) values ('The Man', 5, 9, 3);
insert into tracks (name, artist_id, album_id, genre_id) values ('The Archer', 5, 9, 3);
insert into tracks (name, artist_id, album_id, genre_id) values ('Style', 5, 10, 3);
insert into tracks (name, artist_id, album_id, genre_id) values ('Bad Blood', 5, 10, 3);
insert into tracks (name, artist_id, album_id, genre_id) values ('imagine', 6, 11, 3);
insert into tracks (name, artist_id, album_id, genre_id) values ('needy', 6, 11, 3);
insert into tracks (name, artist_id, album_id, genre_id) values ('Moonlight', 6, 12, 3);
insert into tracks (name, artist_id, album_id, genre_id) values ('Into You', 6, 12, 3);
insert into tracks (name, artist_id, album_id, genre_id) values ('Awww Yeah', 7, 13, 4);
insert into tracks (name, artist_id, album_id, genre_id) values ('Plain Jane', 7, 13, 4);
insert into tracks (name, artist_id, album_id, genre_id) values ('Jet Lag', 7, 14, 4);
insert into tracks (name, artist_id, album_id, genre_id) values ('Ride', 7, 14, 4);
insert into tracks (name, artist_id, album_id, genre_id) values ('Nonstop', 8, 15, 4);
insert into tracks (name, artist_id, album_id, genre_id) values ('Survival', 8, 15, 4);
insert into tracks (name, artist_id, album_id, genre_id) values ('Hype', 8, 16, 4);
insert into tracks (name, artist_id, album_id, genre_id) values ('Redemption', 8, 16, 4);

insert into users (username, password) values ('user', 'ee11cbb19052e40b07aac0ca060c23ee');
insert into users (username, password) values ('user2', '7e58d63b60197ceb55a1c487989a3720');

insert into playlists (title, user_id) values ('My playlist', 1);
insert into playlists (title, user_id) values ('I like it', 1);
insert into playlists (title, user_id) values ('Favorite music', 2);
insert into playlists (title, user_id) values ('Mmm', 2);

insert into playlists_tracks (playlist_id, track_id) values (1, 1);
insert into playlists_tracks (playlist_id, track_id) values (1, 2);
insert into playlists_tracks (playlist_id, track_id) values (1, 3);
insert into playlists_tracks (playlist_id, track_id) values (1, 4);
insert into playlists_tracks (playlist_id, track_id) values (2, 5);
insert into playlists_tracks (playlist_id, track_id) values (2, 6);
insert into playlists_tracks (playlist_id, track_id) values (3, 24);
insert into playlists_tracks (playlist_id, track_id) values (3, 25);
insert into playlists_tracks (playlist_id, track_id) values (3, 26);
insert into playlists_tracks (playlist_id, track_id) values (3, 27);
insert into playlists_tracks (playlist_id, track_id) values (4, 28);
insert into playlists_tracks (playlist_id, track_id) values (4, 29);
insert into playlists_tracks (playlist_id, track_id) values (4, 30);

insert into subscriptions (user_id, is_enabled, sub_date) values (1, true, '2020-11-1');
insert into subscriptions (user_id, is_enabled, sub_date) values (2, false, '2020-09-15');