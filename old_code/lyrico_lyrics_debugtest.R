library(tidyverse)
library(rvest)

output_file <- 'test-new.csv'
#output_file <- 'fake-lyrics.csv'
max_songs <- 500

artist_db <- read_csv('artist-list.csv', col_names = TRUE, col_types = NULL,
                      locale = default_locale(), na = c("", "NA"), quoted_na = TRUE,
                      quote = "\"", comment = "", trim_ws = TRUE, skip = 0,
                      progress = show_progress(), skip_empty_rows = TRUE)

#Format the link to navigate to the artists genius webpage
artist_db <- tibble(artist = c("artic-monkeys","smurficancity","Maggie-Rogers"), genre_1 = c("rock","jangle","pop"))
#artist_db <- tibble(artist = 'the-beatles', genre_1 = 'rock')
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
    num_songs <- 3
    song_links[2]
    for(j in 1:num_songs){ 
    #for(j in 42:43){
      song_links[2] <- 'http://www.songlyrics.com/britney-spears/wom/anizer-lyrics/'
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
                                                     Genre = artist_db$genre_1[i],
                                                     Lyrics = gsub('\n',' ',lyrics_scraped) %>%
                                                       gsub('\r',' ',.) %>%
                                                       gsub('"', ' ', .)))
        
        # pause so we don't get banned!
        Sys.sleep(10) 
      },
      error=function(cond) {
        message(paste("No song:", song_links[i]))
      })
      
    }
    write.table(artist_lyrics, file = output_file,row.names=FALSE,col.names=FALSE, sep=",", append = TRUE)
    artist_lyrics <- tibble()
  },
  error=function(cond) {
    message(paste("No artist:", artist_db$artist[i]))
  })
  
}
#Inspect the results

