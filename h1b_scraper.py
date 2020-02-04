'''
Class for scraping h1-b database
'''

import urllib
import warnings
import pandas as pd
from bs4 import BeautifulSoup


class HTMLTableParser:
    '''
    Class used to parse html tables at a specified url
    '''
    def parse(self, url):
        '''
        parses data from html table at url
        '''
        if not isinstance(url, str):
            return
        soup = self.read_url(url)
        return self.obtain_tables(soup)

    def batch_parse(self, url_list):
        '''
        runs parse over a list of urls
        '''
        assert isinstance(url_list, list)
        tables = []
        for url in url_list:
            tables.append(self.parse(url))
        return pd.concat(tables)

    def read_url(self, url):
        '''
        provides beatiful soup object of url
        '''
        response = urllib.request.urlopen(url)
        page_source = response.read()
        return BeautifulSoup(page_source, 'lxml')

    def obtain_tables(self, soup):
        '''
        obtains html tables from soup object of url
        '''
        tables = pd.DataFrame(columns=['name', 'value'])
        for table in soup.find_all('table'):
            if 'id' not in table:
                table['id'] = "None"
            tables.loc[len(tables)] = (table['id'], self.parse_html_table(table))
        return tables

    def parse_html_table(self, table_):
        '''
        run during obtain_tables method to parse html table
        and add row to pandas df
        '''
        rows = table_.findAll(lambda tag: tag.name == 'tr')
        data = []
        columns = None
        for row in rows:
            cells = row.findAll("td")
            if cells:
                data.append([cell.find(text=True) for cell in cells])
            else:
                new_columns = [element.find(text=True) for element in row.findAll("th")]
                if not new_columns:
                    continue
                if columns is None:
                    columns = new_columns
                else:
                    raise Exception("Column titles exist at multiple rows")

        df_table = pd.DataFrame(data)
        if len(columns) == len(df_table.columns):
            df_table.columns = columns
        else:
            warnings.warn("Column titles do not match the number of columns \
                            for the table with id: " + table_['id'])
        return df_table

class H1bScraper():
    '''
    Class to scrape H1-B database
    '''
    def __init__(self):
        self.parser = HTMLTableParser()
    def scrape(self, years, jobs):
        '''
        Scrapes H1-B database for year in years and job in jobs
        '''
        assert isinstance(years, (list, tuple)), "years should be list or tuple"
        assert isinstance(jobs, (list, tuple)), "jobs should be list or tuple"
        tables = pd.DataFrame(columns=['Year', 'Job Title', 'Table'])
        for year in years:
            for job in jobs:
                url_str = "https://h1bdata.info/index.php?em=&job=%s&city=&year=%d"
                url = url_str % (job.replace(' ', '+'), year)
                ## The H1B info website only contains one table
                table_url = self.parser.parse(url).iloc[0, 1]
                if table_url.shape[0] == 0:
                    table_url = None
                tables.loc[len(tables)] = (year, job, table_url)
        def str2int(df_store, column):
            if df_store is None:
                return
            if column not in df_store.columns:
                return
            df_store.loc[:, column] = df_store[column].apply(lambda x: int(x.replace(',', '')))
        tables['Table'].apply(lambda x: str2int(x, 'BASE SALARY'))
        return tables

    def extract_specific_table(self, tables, year, job):
        '''
        pulls the table of individuals for a particular year-job combo
        '''
        assert isinstance(year, int)
        assert isinstance(job, str)
        mask = (tables['Year'] == year) & (tables['Job Title'] == job)
        return tables.loc[mask, 'Table'].iloc[0]

if __name__ == '__main__':
    SCRAPER = H1bScraper()
    YEARS = [year for year in range(2017, 2019)]
    JOBS = ["Software Engineer", "Data Scientist"]
    TABLES = SCRAPER.scrape(YEARS, JOBS)
    ALL_TABLES = []

    for yr_ in YEARS:
        for job_ in JOBS:
            table_result = SCRAPER.extract_specific_table(TABLES, yr_, job_)
            ALL_TABLES.append(table_result)

    DF_TOTAL = pd.concat(ALL_TABLES, ignore_index=True)
    DF_TOTAL.to_csv('./salary_data.csv')
