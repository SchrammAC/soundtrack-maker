library(tidyverse)
library(rvest)

#artists <- tibble(artist = c("queen", "The-rolling-stones","cage-the-elephant", "Queens-of-the-stone-age", "Foo-fighters", "Beyonce", "Drake", "Eminem", "Post-malone", "Kanye-west", "Kacey-musgraves", "Chris-stapleton", "Florida-georgia-line", "Luke-combs", "johnny-cash"), genre = c("rock", "rock", "rock", "rock", "rock", "hiphop", "hiphop", "hiphop", "hiphop", "hiphop", "country", "country", "country", "country", "country"))
#artists <- tibble(artist = c("The-rolling-stones","drake"), genre = c("rock", "hiphop"))
#Format the link to navigate to the artists genius webpage
artists <- tibble(artist = c("The-rolling-stones", "Foo-fighters"), genre = c("rock", "rock"))
genius_urls <- paste0("https://genius.com/artists/",artists$artist)

#Initialize a tibble to store the results
artist_lyrics <- tibble()

# Outer loop to get the song links for each artist 
for (i in 1:2) {
  genius_page <- read_html(genius_urls[i])
  song_links <- html_nodes(genius_page, ".mini_card_grid-song a") %>%
    html_attr("href") 
  
  #Inner loop to get the Song Name and Lyrics from the Song Link    
  for (j in 1:20) {
    
    # Get lyrics
    lyrics_scraped <- read_html(song_links[j]) %>%
      html_nodes("div.lyrics p") %>%
      html_text()
    
    # Get song name
    song_name <- read_html(song_links[j]) %>%
      html_nodes("h1.header_with_cover_art-primary_info-title") %>%
      html_text()
    
    # Save the details to a tibble
#    artist_lyrics <- rbind(artist_lyrics, tibble(Rank = top_artists$Rank[i],
#                                                 Artist = top_artists$Artist[i],
#                                                 Song = song_name,
#                                                 Lyrics = lyrics_scraped ))
    
    artist_lyrics <- rbind(artist_lyrics, tibble(Artist = artists$artist[i],
                                                 Song = song_name,
                                                 Genre = artists$genre[i],
                                                 Lyrics = gsub('\n',' ',lyrics_scraped) ))    
    
    # Insert a time lag - to prevent me from getting booted from the site :)
    Sys.sleep(10)
  }
} 

#Inspect the results
artist_lyrics