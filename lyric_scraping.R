library(tidyverse)
library(rvest)

output_file <- 'trigenre-lyrics-newcountry-190518.csv'
fail_a_file <- 'invalid-artist.csv'
max_songs <- 100

artist_db <- read_csv('country-artist-list-190518.csv', col_names = TRUE, col_types = NULL,
                      locale = default_locale(), na = c("", "NA"), quoted_na = TRUE,
                      quote = "\"", comment = "", trim_ws = TRUE, skip = 0,
                      progress = show_progress(), skip_empty_rows = TRUE)

#Format the link to navigate to the artists genius webpage
#artist_db <- tibble(artist = c("artic-monkeys","Maggie-Rogers"), genre = c("rock","pop"))
artist_urls <- paste0('http://www.songlyrics.com/',artist_db$artist,'-lyrics/')
artist_lyrics <- tibble()

for (i in 1:length(artist_db$artist)) {
  message(str_c('scraping artist ', i, ' of ', length(artist_db$artist) )) #Monitor artist progress
  tryCatch({
    song_nodes <- read_html(artist_urls[i]) %>% # load the html
      html_nodes("#colone-container .tracklist a")
    
    song_titles <-  html_text(song_nodes)
  
    song_links <-  html_attr(song_nodes, name='href')
    if (max_songs > length(song_links)){
      num_songs <- length(song_links)
    } else {
      num_songs <- max_songs
    }
    for(j in 1:num_songs){ 
    #for(j in 42:43){
      
      message(str_c('scraping song ', j, ' of ', num_songs ))#Monitor song progress
      tryCatch({
        # scape the text of a song
        lyrics_scraped <- song_links[j] %>%
          read_html() %>% 
          html_nodes("#songLyricsDiv") %>%
          html_text()
        
        
        # format the song name for the data frame
        song_name <- song_titles[j] %>% 
          str_to_lower() %>% 
          gsub("[^[:alnum:] ]", "", .) %>%
          gsub("[[:space:]]", "_", .)
        
        # add song to lyrics data frame
        artist_lyrics <- rbind(artist_lyrics, tibble(Artist = artist_db$artist[i],
                                                     Song = song_name,
                                                     Genre = artist_db$genre[i],
                                                     Lyrics = gsub('\n',' ',lyrics_scraped) %>%
                                                       gsub('\r',' ',.) %>%
                                                       gsub('"', ' ', .)))
        
        # pause so we don't get banned!
        Sys.sleep(10) 
      },
      error=function(cond) {
        message(paste("No song at:", song_links[j]))
      })
    }
    write.table(artist_lyrics, file = output_file,row.names=FALSE,col.names=FALSE, sep=",", append = TRUE)
    artist_lyrics <- tibble()
  },
  error=function(cond) {
    message(paste("No artist:", artist_db$artist[i]))
    failed_artist <- tibble(Artist = artist_db$artist[i])
    write.table(failed_artist, file = fail_a_file,row.names=FALSE,col.names=FALSE, sep=",", append = TRUE)
  })
}
#Inspect the results

