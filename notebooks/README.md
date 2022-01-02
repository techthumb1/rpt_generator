# arXivScraper

An ArXiV scraper to retrieve records from given categories and date range.

## Installation

Use `pip` or `pip3` to install the package:

    pip install arxivscraper
    
or download the source code and run setup.py:

    python setup.py install

To update the module using pip:

    pip install --upgrade arxivscraper

## Usage

To use the package, import the module and create a scraper object:

    from arxivscraper import Scraper

    scraper = Scraper

 
## Configuration

The scraper object can be configured using the following methods:

    scraper.set_categories(categories)
    
   or
   
    scraper.set_start_date(start_date)
    
   or
   
    scraper.set_end_date(end_date)
    
   or
   
    scraper.set_max_results(max_results)
    

## Examples

The following examples show how to use the scraper object to retrieve records.

    scraper.get_records(categories=['cs.AI'], start_date='2019-01-01', end_date='2019-01-31')
   
   additionally:
    
    scraper.get_records(categories=['cs.AI'], start_date='2019-01-01', end_date='2019-01-31', max_results=10)
   
   additionally:
    
    scraper.get_records(categories=['cs.AI'], start_date='2019-01-01', end_date='2019-01-31', 
                        sort_by='lastUpdatedDate', order='descending')
    additionally:
    
    scraper.get_records(categories=['cs.AI'], start_date='2019-01-01', end_date='2019-01-31',
                        sort_by='lastUpdatedDate', order='descending', include_pdf=True, include_abstract=True, include_comments=True, 
                        include_arxiv_url=True, include_doi=True, include_bibtex=True, include_body_text=True, 
                        include_subjects=True,include_authors=True, include_categories=True)


## Without Filtering

You can create use [arxivscraper](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiI0ejC0JL1AhWlj4kEHQmUDGQQFnoECAgQAQ&url=https%3A%2F%2Fgithub.com%2FMahdisadjadi%2Farxivscraper&usg=AOvVaw3N5BkaUh5GkcgYDjtAi6P4) in your scripts. Import [arxivscraper](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiI0ejC0JL1AhWlj4kEHQmUDGQQFnoECAgQAQ&url=https%3A%2F%2Fgithub.com%2FMahdisadjadi%2Farxivscraper&usg=AOvVaw3N5BkaUh5GkcgYDjtAi6P4) and create a scraper to fetch all records:


The following examples show how to use the scraper object to retrieve records without filtering. This is useful if you want to retrieve all records from a given category. The results are sorted by date and the first 10 records are returned.

    scraper.get_records(categories=['cs.AI'])
    scraper.get_records(categories=['cs.AI'], max_results=10)
    scraper.get_records(categories=['cs.AI'], sort_by='lastUpdatedDate', order='descending')


## License

This package is licensed under the [MIT license] and is provided as is.


## Authors


Jason Robinson<br>
Data Science and Machine Learning<br>
[BloomTech](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjx6Pb0zJL1AhVRkokEHeXXD2AQFnoECA0QAQ&url=https%3A%2F%2Fwww.bloomtech.com%2F&usg=AOvVaw0HSetgGz63LaOIA32I_fSN)


