# ncomix

This is a simple module to download comics from "https://www.porncomix.one" using webscrapping. 

This version is the first prototype, more documentation and functionalities will be added soon

## Basic Usage

from ncomix import ncomix

comic = ncomix(url_to_comic)

comic.download() #download pages as images to a folder in current working directory

comic.download_pdf() #download combine pages to single pdf in current working directory

To download to given directory

comic.download(dest=mydir) #download to given directory

comic.download_pdf(dest=mydir)

To get basic info on the comic

print(comix)