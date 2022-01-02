from __future__ import print_function # used to print the future version of the code.
import xml.etree.ElementTree as ET # xml.etree.ElementTree is a module that can parse XML files.
import datetime # datetime is a module that can parse dates.
import time # time is a module that can be used to measure time.
import sys # sys is a module that contains functions for interacting with the interpreter.


PYTHON3 = sys.version_info[0] == 3 # Ensure that the program is running in Python 3.
if PYTHON3:
    from urllib.parse import urlencode # urlencode is a function that encodes a dictionary into a URL query string.
    from urllib.request import urlopen # urlopen is a function that opens a URL and returns a file-like object.
    from urllib.error import HTTPError # HTTPError is a subclass of OSError that indicates HTTP protocol errors.
else:
    from urllib import urlencode # urlencode is a function that encodes a dictionary into a URL query string.
    from urllib2 import HTTPError, urlopen # urlopen is a function that opens a URL and returns a file-like object.
OAI = '{http://www.openarchives.org/OAI/2.0/}' # OAI is a namespace for the OAI-PMH protocol.
ARXIV = '{http://arxiv.org/OAI/arXiv/}' # ARXIV is a namespace for the ArXiv OAI-PMH protocol.
BASE = 'http://export.arxiv.org/oai2?verb=ListRecords&' # BASE is the base URL for the OAI-PMH protocol.

class Record(object): # Record is a class that represents a single OAI-PMH record.
    """
    A class to hold a single record from ArXiv
    Each records contains the following properties:
    object should be of xml.etree.ElementTree.Element.
    """

    def __init__(self, xml_record): # __init__ is a function that is called when a new object is created.  
        """
        if not isinstance(object,ET.Element):
        raise TypeError("")
        """
        self.xml = xml_record  # xml is a property that holds the xml record.
        self.id = self._get_text(ARXIV, 'id')  # id is a property that holds the arXiv id.
        self.url = 'https://arxiv.org/abs/' + self.id # url is a property that holds the arXiv url.
        self.title = self._get_text(ARXIV, 'title') # title is a property that holds the arXiv title.
        self.abstract = self._get_text(ARXIV, 'abstract') # abstract is a property that holds the arXiv abstract. 
        self.cats = self._get_text(ARXIV, 'categories') # cats is a property that holds the arXiv categories.
        self.created = self._get_text(ARXIV, 'created') # created is a property that holds the arXiv created date.
        self.updated = self._get_text(ARXIV, 'updated') # updated is a property that holds the arXiv updated date.
        self.doi = self._get_text(ARXIV, 'doi') # doi is a property that holds the arXiv doi.
        self.authors = self._get_authors() # authors is a property that holds the arXiv authors.

    def _get_text(self, namespace, tag): # _get_text is a function that returns the text of a tag.
        """Extracts text from an xml field"""
        try:
            return self.xml.find(namespace + tag).text.strip().lower().replace('\n', ' ') # strip() removes leading and trailing whitespace.
        except:
            return ''   # return an empty string if the tag is not found.

    def _get_authors(self): # _get_authors is a function that returns the authors of a record.
        authors = self.xml.findall(ARXIV + 'authors/' + ARXIV + 'author') # authors is a list of all the authors.
        authors = [author.find(ARXIV + 'keyname').text.lower() for author in authors] # authors is a list of all the authors' keynames.
        return authors

    def output(self): # output is a function that returns a string of the record.
        d = {'title': self.title,  # d is a dictionary that holds the record's properties.
         'id': self.id,
         'abstract': self.abstract,
         'categories': self.cats,
         'doi': self.doi,
         'created': self.created,
         'updated': self.updated,
         'authors': self.authors,
         'url': self.url}
        return d


class Scraper(object):
    """
    A class to hold info about attributes of scraping,
    such as date range, categories, and number of returned
    records. If `from` is not provided, the first day of
    the current month will be used. If `until` is not provided,
    the current day will be used.
    Paramters
    ---------
    category: str
    The category of scraped records
    data_from: str
    starting date in format 'YYYY-MM-DD'. Updated eprints are included even if
    they were created outside of the given date range. Default: first day of current month.
    date_until: str
    final date in format 'YYYY-MM-DD'. Updated eprints are included even if
    they were created outside of the given date range. Default: today.
    t: int
    Waiting time between subsequent calls to API, triggred by Error 503.
    filter: dictionary
    A dictionary where keys are used to limit the saved results. Possible keys:
    subcats, author, title, abstract. See the example, below.
    Example:
    Returning all eprints from
    """

    def __init__(self, category, date_from=None, date_until=None, t=30, filters={}): # t is the time to wait between subsequent calls to API.
        self.cat = str(category)
        self.t = t
        DateToday = datetime.date.today()
        if date_from is None:
            self.f = str(DateToday.replace(day=1)) # f for first day of the current month.
        else:
            self.f = date_from
        if date_until is None:
            self.u = str(DateToday) 
        else:
            self.u = date_until # u for date_until.
        self.url = BASE + 'from=' + self.f + '&until=' + self.u + '&metadataPrefix=arXiv&set=%s' % self.cat # url is the base URL for the OAI-PMH protocol.
        self.filters = filters # filters is a dictionary where keys are used to limit the saved results. Possible keys: subcats, author, title, abstract.
        if not self.filters: # If filters is empty, then the default value is used.
            self.append_all = True # append_all is a boolean that indicates whether all records should be saved.
        else:
            self.append_all = False # append_all is a boolean that indicates whether all records should be saved.
            self.keys = filters.keys() # keys is a list of keys in the filters dictionary.

    def scrape(self): 
        t0 = time.time() # t0 is the time when the function started.   
        url = self.url
        print(url)  # Prints the URL to the console.
        ds = [] # ds is a list of dictionaries.
        k = 1   # k is the number of records returned by the API.
        while True: 
            print('fetching up to ', 1000 * k, 'records...') # Prints the number of records returned by the API.
            try:
                response = urlopen(url) # response is a file-like object.
            except HTTPError as e: # HTTPError is a subclass of OSError that indicates HTTP protocol errors.
                if e.code == 503: # If the error code is 503, then the server is overloaded and the program waits for a while.
                    to = int(e.hdrs.get('retry-after', 30)) # to is the time to wait before the next call to API.
                    print('Got 503. Retrying after {0:d} seconds.'.format(self.t)) # Prints the time to wait before the next call to API.
                    time.sleep(self.t) # Waits for a while.
                    continue    # Restarts the loop.
                else:
                    raise # e # Raises the error.
            k += 1 # k is incremented by 1 because the next call to API will return 1000 records.
            xml = response.read() # xml is a string.
            root = ET.fromstring(xml) # fromstring is a function that parses an XML string from the given file-like object.
            records = root.findall(OAI + 'ListRecords/' + OAI + 'record') # records is a list of xml.etree.ElementTree.Element.
            for record in records: # For each record in the list of records.
                meta = record.find(OAI + 'metadata').find(ARXIV + 'arXiv') # meta is an xml.etree.ElementTree.Element.
                record = Record(meta).output() # record is a dictionary.
                if self.append_all: # If append_all is True, then the record is appended to the list of dictionaries.
                    ds.append(record) # Appends the record to the list of dictionaries.
                else:
                    save_record = False # save_record is a boolean that indicates whether the record should be saved.
                    for key in self.keys: # For each key in the filters dictionary.
                        for word in self.filters[key]: # For each word in the list of words in the filters dictionary.
                            if word.lower() in record[key]: # If the word is in the record.
                                save_record = True

                    if save_record: # If save_record is True, then the record is appended to the list of dictionaries.
                        ds.append(record) # Appends the record to the list of dictionaries.

            try:
                token = root.find(OAI + 'ListRecords').find(OAI + 'resumptionToken') # token is an xml.etree.ElementTree.Element.
            except:
                return 1
            if token is None or token.text is None: # If token is None or token.text is None, then the program ends.
                break
            else:
                url = BASE + 'resumptionToken=%s' % token.text # resumptionToken + BASE is the URL for the next call to API.

        t1 = time.time()
        print('fetching is completed in {0:.1f} seconds.'.format(t1 - t0))
        print ('Total number of records {:d}'.format(len(ds)))
        return ds


def search_all(df, col, *words): # df is a pandas DataFrame, col is a string, and words is a list of strings.
    """
    Return a sub-DataFrame of those rows whose Name column match all the words.
    source: https://stackoverflow.com/a/22624079/3349443
    """
    return df[np.logical_and.reduce([df[col].str.contains(word) for word in words])] # np.logical_and.reduce is a function that returns True if all the elements in the list are True.


cats = [ # cats is a list of strings.
 'astro-ph', 'cond-mat', 'gr-qc', 'hep-ex', 'hep-lat', 'hep-ph', 'hep-th',
 'math-ph', 'nlin', 'nucl-ex', 'nucl-th', 'physics', 'quant-ph', 'math', 'CoRR', 'q-bio',
 'q-fin', 'stat']
subcats = {'cond-mat': ['cond-mat.dis-nn', 'cond-mat.mtrl-sci', 'cond-mat.mes-hall',
              'cond-mat.other', 'cond-mat.quant-gas', 'cond-mat.soft', 'cond-mat.stat-mech',
              'cond-mat.str-el', 'cond-mat.supr-con'],
 'hep-th': [],'hep-ex': [],'hep-ph': [],
 'gr-qc': [],'quant-ph': [],'q-fin': ['q-fin.CP', 'q-fin.EC', 'q-fin.GN',
           'q-fin.MF', 'q-fin.PM', 'q-fin.PR', 'q-fin.RM', 'q-fin.ST', 'q-fin.TR'],

 'nucl-ex': [],'CoRR': [],'nlin': ['nlin.AO', 'nlin.CG', 'nlin.CD', 'nlin.SI',
          'nlin.PS'],
 'physics': ['physics.acc-ph', 'physics.app-ph', 'physics.ao-ph',
             'physics.atom-ph', 'physics.atm-clus', 'physics.bio-ph', 'physics.chem-ph',
             'physics.class-ph', 'physics.comp-ph', 'physics.data-an', 'physics.flu-dyn',
             'physics.gen-ph', 'physics.geo-ph', 'physics.hist-ph', 'physics.ins-det',
             'physics.med-ph', 'physics.optics', 'physics.ed-ph', 'physics.soc-ph',
             'physics.plasm-ph', 'physics.pop-ph', 'physics.space-ph'],
 'math-ph': [],
 'math': ['math.AG', 'math.AT', 'math.AP', 'math.CT', 'math.CA', 'math.CO',
          'math.AC', 'math.CV', 'math.DG', 'math.DS', 'math.FA', 'math.GM', 'math.GN',
          'math.GT', 'math.GR', 'math.HO', 'math.IT', 'math.KT', 'math.LO', 'math.MP',
          'math.MG', 'math.NT', 'math.NA', 'math.OA', 'math.OC', 'math.PR', 'math.QA',
          'math.RT', 'math.RA', 'math.SP', 'math.ST', 'math.SG'],
 'q-bio': ['q-bio.BM',
           'q-bio.CB', 'q-bio.GN', 'q-bio.MN', 'q-bio.NC', 'q-bio.OT', 'q-bio.PE', 'q-bio.QM',
           'q-bio.SC', 'q-bio.TO'],
 'nucl-th': [],'stat': ['stat.AP', 'stat.CO', 'stat.ML',
          'stat.ME', 'stat.OT', 'stat.TH'],
 'hep-lat': [],'astro-ph': ['astro-ph.GA',
              'astro-ph.CO', 'astro-ph.EP', 'astro-ph.HE', 'astro-ph.IM', 'astro-ph.SR']
 }
