# eprice-package
This package alows the user to get an e-commerce product's **title** and **price** as **tuple** according to the user's input **url**. The user shall then use the data scraped to track, compare or even real time track the prices without having to worry about scraping and cleaning the data.

### List of e-commerce websites that can be requested through this package:

    1.Amazon
    2.Flipkart
    3.Snapdeal
    4.Alibaba
    5.Reliance digital

### Importing and using the package:

Additionaly it requires the following packages:
    1.lxml
    2.requests
    3.beautifulsoup4

### Importing and using the package:

``` python
from eprice_pkg import eprice

Title,Price=eprice.getAmazon(url)

Title,Price=eprice.getAlibaba(url)

Title,Price=eprice.getFlipkart(url)

Title,Price=eprice.getSnapdeal(url)

Title,Price=eprice.getReliancedigital(url)
```

#### NOTE: be aware of the region you request for because the functions retunrs the prices acording to the url the user searches for.
#### NOTE: be aware of the quantity while providing the link from alibaba.



[Source files](https://github.com/Zero-Autumn/eprice-package.git)

##### Thanks <3
