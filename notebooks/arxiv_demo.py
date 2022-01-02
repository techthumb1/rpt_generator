import pandas as pd
import arxivscraper
import arxivscraper.arxivscraper as ax



# scraper = arxivscraper.Scraper(category='cs.CV', data_from='2017-01-01', date_until='2017-01-31')
scraper = arxivscraper.Scraper(category='physics:cond-mat', date_from='2017-05-27',date_until='2017-06-07')

output = scraper.scrape()

cols = ['title','id','abstract','categories','doi','created','updated','authors','url']
df = pd.DataFrame(output, columns=cols)
# df.to_csv('arxiv_scraper_output.csv', index=False)

scraper = ax.Scraper(category='stat',date_from='2017-08-01',date_until='2017-08-10',t=10, filters={'categories':['stat.ml'],'abstract':['learning']})
output = scraper.scrape()

cols = ['title','id','abstract','categories','doi','created','updated','authors','url']
df = pd.DataFrame(output, columns=cols)


"Citations: Mahdi Sadjadi (2017). arxivscraper:Zendo. http://doi.org/10.5281/zenodo.889853"