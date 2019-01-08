# Picture-Scraper

A picture scraper based on a basketball forum HUPU, which I personally browse often. 
The scaper is designed with the use of asyncrohnes mechanism and multiprocessing, usually taking around 3 minutes to download all pictures of the posts in a single page of url. 

The speed is ultimately determined by lots of factor, such as internet speed, cpu effiency, size of pictures etc. 
Users are allowed to input different page numbers to be scraped. Also, change the path after clone.

A little modification needs to be done if users want to scrape a different type of url address. Probably inspect the desired webpage source at first, and then modify the keywords regarding lookup with the libraries.

![wx20190107-211715](https://user-images.githubusercontent.com/39290810/50813856-b4b3be00-12e5-11e9-8b2f-ec9210eaa0f9.png)
