# Scraping H1-B Visa Database

This branch introduces a few changes:

1. A single module that contains both classes, as well as the example code in a `main` block.

2.  The code has been cleaned using a linter to move from less than a 4/10 rating to 9.53/10 rating via `pylint`.

You can verify the `pylint` results by running

```
pylint h1b_scraper.py
```

3. You may easily run a test after cloning this repository.  Assuming you are running Python 3.x, you should be able to run the following code:

```
git clone https://github.com/mingen-pan/Scraping-H1B-visa-info.git
cd Scraping-H1B-visa-info
git checkout refactor-branch
python h1b_scraper.py
```

The results are now stored in the local repository in a `.csv` file called `salary_data.csv`.

4. I created `titles.json` for you to easily update the titles you want to add into `salary_data_json_results.csv` to be considered in a post analysis. Run the following code to create the `.csv` dataset based on `titles.json`.

```
ipython run_h1b_scraper.py
```


# Scraping-H1B-visa-info (The Original README.md)

The example code can be found on the `example.py`.

This project uses `BeautifulSoup` (aka `bs4`) and `urllib` packages to scrape the H1B visa info website. In order to use this project, it is recommended to run in the `Python3` environment and install the packages `bs4`, `urllib`, and `pandas`.

Download the python files and put them into the current path. Then import the file:
```
from h1b_scraper import H1B_Scraper
```
Run the following code to obtain the DataFrame:
```
scraper = H1B_Scraper()
years = [year for year in range(2017, 2019)] ## get the list [2017, 2018]
jobs = ["Software Engineer", "Data Scientist"] ## Capital or not doesn't matter.
tables = scraper.scrape(years, jobs)
```

The values of this DataFrame `tables` store the H1B visa info of different years and job titles as a Pandas DataFrame Table.

For example:
```
        Year	Job Title	Table
0	2017	Software Engineer	EMPLOYER JOB T...
1	2017	Data Scientist	EMPLOYER \...
2	2018	Software Engineer	EMPLOYER ...
3	2018	Data Scientist	EMPLOYER JOB T...
```

To extract the table given specific year and job title:
```
scraper.extract_specific_table(tables, 2018, "Software Engineer")
```

Then you have the following dataframe:

(Visualization here is bad, but they are well aligned in the dataframe.)
```
        EMPLOYER	JOB TITLE	BASE SALARY	LOCATION	SUBMIT DATE	START DATE	CASE STATUS
0	GOLD SHIELD TECHNOLOGIES LLC	SOFTWARE ENGINEER	36,000	GAINESVILLE, FL	03/22/2018	03/22/2018	DENIED
1	SRIVEN SYSTEMS OF TX INC	SOFTWARE ENGINEER	37,380	MONROE, LA	02/28/2018	08/28/2018	CERTIFIED
2	SPIRIT MANUFACTURING INC	SOFTWARE ENGINEER	49,040	JONESBORO, AR	03/19/2018	09/18/2018	CERTIFIED
3	EASI LLC	SOFTWARE ENGINEER	49,300	TROY, MI	03/15/2018	03/22/2018	CERTIFIED
4	MXN COMMERCE INC	SOFTWARE ENGINEER	53,060	ENGLEWOOD, NJ	03/20/2018	09/19/2018	CERTIFIED
5	STREAMS INC	SOFTWARE ENGINEER	56,000	MEMPHIS, TN	03/19/2018	09/01/2018	CERTIFIED
...	...	...	...	...	...	...	...
20892	FACEBOOK INC	SOFTWARE ENGINEER	260,000	MENLO PARK, CA	05/30/2018	06/11/2018	CERTIFIED
20893	DELAWARE HOTEL GROUP LLC	SOFTWARE ENGINEER	280,000	TRACY, CA	04/12/2018	09/15/2018	CERTIFIED
20894	DROPBOX INC	SOFTWARE ENGINEER	290,000	SAN FRANCISCO, CA	04/12/2018	06/01/2018	CERTIFIED
20895	LEAD IT CORPORATION	SOFTWARE ENGINEER	834,790	WELDON SPRINGS, MO	03/20/2018	09/18/2018	WITHDRAWN

```


Reference: Some code is referred from https://srome.github.io/Parsing-HTML-Tables-in-Python-with-BeautifulSoup-and-pandas/
