movie_info
==========

Queries IMDB for information on a movie

Movie Info is a work in progress, the end state is to be able to look at a movie folder and return information on your collection. 
Movies can then be sorted and grouped based on user ratings, genre, actor, etc. <p><p>

To use:<p>
<code> python wtftowatch.py "MOVIE TO SEARCH" (-d) </code><p>
The '-d' will enable debug mode, creating a log of the HTML output for testing purposes if the program crashes <p>

3rd Party libraries are:
- [BS4](http://www.crummy.com/software/BeautifulSoup/) <p>
      <code>pip install beautifulsoup4</code>
  or
      <code>easy_install beautifulsoup4</code>

---
To Do:
- Work on getDirectory()
- Work on conformString() to strip useless information before the request
- Transfer the Movie to a class structure
- Error checking for 404's or not connected to internet
