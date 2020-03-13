# !/usr/bin/python2
import requests
from datetime import datetime
# import urlparse
import urllib
import urllib.parse as urlparse
# import dropbox
import csv
from bs4 import BeautifulSoup

USERNAME = ""
PASSWORD = ""
pin = [1, 2, 3, 4]
FILENAME = "bank.csv"
# start_date = urllib.quote_plus(datetime(2017, 5, 15).strftime("%d/%m/%Y"))
# end_date = urllib.quote_plus(datetime.today().strftime("%d/%m/%Y"))

ROOT_URL = "https://www.open24.ie/online"
LOGIN_URL = "https://www.pnc.com/en/personal-banking.html"
FORM_ENDPOINT_URL = "https://www.open24.ie/online/"
FORM2_ENDPOINT_URL = "https://www.open24.ie/online/Login/Step2"
TX_ENDPOINT = "https://www.open24.ie/online/Accounts/Details/RecentTransactions"


def get_data(session, url):
    result = session.get(url)
    return BeautifulSoup(result.content, "html.parser")


def post_data(session, url, data):
    result = session.post(url, data=data, headers=dict(referer=LOGIN_URL))
    return BeautifulSoup(result.content, "html.parser")


"""
 Finds out which digits are requested from PIN
"""


def get_pin_digits(soup):
    t1 = int(soup.find("label", {'for': 'login-digit-1'}).string.replace("Digit ", "")) - 1
    t2 = int(soup.find("label", {'for': 'login-digit-2'}).string.replace("Digit ", "")) - 1
    t3 = int(soup.find("label", {'for': 'login-digit-3'}).string.replace("Digit ", "")) - 1
    return t1, t2, t3


"""
 Gets the Verification token used to submit forms
"""


def get_verif_token(soup):
    return soup.find("input", {'name': '__RequestVerificationToken'}).get('value')


"""
 Gets the account UUID generated on login
"""


def get_acct_id(soup):
    acct_id_url = soup.find("h2", {'class': 'heading-general'}).contents[0]['href']
    url_data = urlparse.urlparse(acct_id_url)
    query = urlparse.parse_qs(url_data.query)
    acct_id = query["accountId"][0]
    return acct_id


def main():
    session_requests = requests.session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    soup = session_requests.get(LOGIN_URL, headers=headers)


    # Get login csrf token
    # soup = get_data(session_requests, LOGIN_URL)
    print(soup)

    # authenticity_token = get_verif_token(soup)
    #
    # # Create payload
    # payload = {
    #     "__RequestVerificationToken": authenticity_token,
    #     "section": "",
    #     "login-number": USERNAME,
    #     "login-password": PASSWORD,
    # }
    #
    # # Perform initial login
    # soup = post_data(session_requests, LOGIN_URL, payload)
    # authenticity_token = get_verif_token(soup)
    # t1, t2, t3 = get_pin_digits(soup)
    #
    # # Create payload
    # payload = {
    #     "__RequestVerificationToken": authenticity_token,
    #     "login-digit-1": pin[t1],
    #     "login-digit-2": pin[t2],
    #     "login-digit-3": pin[t3]
    # }
    #
    # # Perform 2nd login
    # soup = post_data(session_requests, FORM2_ENDPOINT_URL, payload)
    #
    # avail_funds = soup.find("span", {'class': 'fund-1'}).string.encode('ascii', 'ignore')
    # cur_bal = soup.find("span", {'class': 'fund-2'}).string.encode('ascii', 'ignore')
    #
    # acct_id = get_acct_id(soup)
    # print("Available Funds: ", avail_funds)
    # print("Current Balance: ", cur_bal)
    # print("Account ID: ", acct_id)
    #
    # url = 'https://www.open24.ie/online/Accounts/Details/RecentTransactions?accountId=' + acct_id + '&from-date=' + start_date + '&to-date=' + end_date
    # soup = get_data(session_requests, url)
    # valid_trs = [item for item in soup.find_all('tr') if "data-uid" in item.attrs]
    #
    # outputFile = open(FILENAME, 'w')
    # outputWriter = csv.writer(outputFile, lineterminator='\n')
    # outputWriter.writerow(['Date', 'Desc', 'In', 'Out', 'Total'])
    #
    # for tr in valid_trs:
    #     date = datetime.strptime(tr.find("td", {'class': 'date'}).string, '%d %b %y').strftime('%d-%b-%y')
    #     desc = tr.find("td", {'class': 'desc'}).string
    #     if desc is None:
    #         desc = tr.find("td", {'class': 'desc'}).find('a', {'class': 'underline'}).string
    #     desc = str(desc).strip()
    #     tds = tr.findAll("td", {'class': 'currency'})
    #     monin = tds[0].string
    #     monout = tds[1].string
    #     total = tds[2].string
    #     outputWriter.writerow([date, desc, monin, monout, total])
    # outputFile.close()
    #

if __name__ == '__main__':
    main()
