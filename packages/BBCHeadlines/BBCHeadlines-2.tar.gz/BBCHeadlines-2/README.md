# BBCNews
A python package to get news from BBC.

### Installation

    pip3 install BBCHeadlines

### Usage
Print headlines:
 
    # Import BBCHeadlines
    from BBCHeadlines import articles

    # Print the title of article #article_num five times. article_num increases by one every time the loop is increased, starting at zero.
    for article_num in range (5):
        print(articles.title()[article_num])
Print info on first article:
    
    # Import library
    from BBCHeadlines import articles
    # We'll get info on the first article
    article_num = 0

    # Print article title
    print('Title: ' + articles.title()[article_num])
    # Print article description
    print('Description: ' + articles.description()[article_num])
    # Print article link
    print('Link: ' + articles.link()[article_num])
We can put this into a loop to get headlines with info on the articles:

    # Import library
    from BBCHeadlines import articles

    # Print info on article #article_num five times. article_num increases by one every time the loop is increased, starting at zero.
    for article_num in range (5):
        # Print article title
        print('Title: ' + articles.title()[article_num])
        # Print article description
        print('Description: ' + articles.description()[article_num])
        # Print article link
        print('Link: ' + articles.link()[article_num])
