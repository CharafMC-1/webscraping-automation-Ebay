# webscraping-automation-Ebay


Methodology: 

- Created a Github repo to automate the scrapping method
- Write the scrapping script and the YAML file 
- Leave the scrapping for 2 days then work on the scrapped Dataset
- Cleaned the Dataset and use it the for EDA

Analysis for EDA:

Section 1(Time Series Analysis):
Although the scraper was scheduled to run every 3 hours, the chart shows that all deals were captured around 5 AM.
This likely means that the timestamp recorded corresponds to the scraping execution time, not the actual deal posting time on eBay.
As a result, there’s no visible variation across hours, and the time data mainly reflects when the scraper retrieved the listings.

Section 2(Price and Discount Analysis):

The price histogram and boxplot show that most products are priced under $500, with a few expensive outliers reaching around $4000. This indicates a right-skewed distribution, meaning most deals are low-priced tech items with some high-end exceptions.
The scatter plot (Original vs Price) reveals a strong positive correlation — higher original prices generally lead to higher sale prices, confirming consistent pricing logic.
Finally, the discount distribution shows that many items have low or no discounts, but a smaller portion receive moderate to high discounts (20–60%), reflecting selective promotional pricing on certain products.

Section 3(Shipping Information Analysis):
The chart shows that almost all listings (91 out of 92) have their shipping details marked as “Shipping info unavailable.”
Only one product specifies an actual shipping option (“Free 2–4 day delivery”), suggesting that shipping data was mostly missing or not displayed on the source pages during scraping.
This highlights a data limitation future runs could include more detailed scraping to capture shipping terms accurately.

Section 4(Text Analysis on Product Titles):
The keyword frequency chart shows that Apple-related products dominate the listings, followed by iPhone, while other keywords like Tablet, Laptop, and Samsung appear much less frequently.
This suggests the dataset is heavily centered on Apple devices, especially iPhones, with relatively few listings for other brands or product types.

Section 5(Price Difference Analysis):
The histogram shows that most items have small or zero absolute discounts, while a smaller group has a significant savings of over $200–$500.
This suggests that while many deals are listed near their original price, some high-value items receive large sales.

Section 6(Discount):
The top 5 deals show discounts ranging from about 60% to 85%, with products like Soundcore Earbuds, Sigma Lens Converter, and Apple iPhones offering the largest reductions.
These listings represent major promotional deals, where high original prices were significantly lowered.


Challenges: 
- Internet issues so while working on scrapping it got inturrepted several times
- Some data where hard to get (Shipping info)

Potential Improvement: 
- Apply multithreading so the process of scrapping will be faster specially for that related to URLs