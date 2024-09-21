import sys, time
import requests, bs4
import threading, logging
import smtplib
from random import *

# constants
WAIT_INTERVAL = 120
LOG_FILE = 'stockPriceLog.txt'
SMTP_HOST = 'smtp.gmail.com'
SMTP_TLS_PORT = 587

def main():
    """
    Clear the log, set up logging, log a start message
    Retrieve the list of stock symbols from the command
    line
    Start up a thread for each stock listed
    Sleep a little to allow the stock prices to be logged
    Have the user enter CTRL-C to stop the program.
    """

    open(LOG_FILE, 'w').close()
    logging.basicConfig(filename=LOG_FILE,
                        level=logging.INFO,
                        format=' %(asctime)s %(message)s ')
    logging.info("StockWatcher - start program")

    # For Step B: Add in CODE HERE to get the
    #     stock symbols from the command line,
    #     instead of using the hardcoded list

    if len(sys.argv) > 1:
        stock_list = sys.argv[1:]
    else:
        print("Error: No stocks being watched.")
        logging.info("Error: No stocks being watched.")
        sys.exit()

    # stock_list = ["MSFT", "GOOG", "AAPL", "AMZN"]

    for i in range(len(stock_list)):
        stock = stock_list[i].upper()
        print("Begin watch for " + stock)
        thread = threading.Thread(target = get_quote,
                                  args = (stock, ))
        thread.setDaemon(True)
        thread.start()

    time.sleep(5)   # Sleep for threads to print msgs

    # Need a try-except to catch the ctrl-c
    try:
        input("\nHit CTRL-C to stop recording.\n\n")
    except:
        pass

    logging.info("StockWatcher = end program")

def get_quote(symbol):
    """
    Get a stock quote for the given stock symbol using
    Python requests and BeautifulSoup modules.
    Determine the availability of webpage
    Request the quote every WAIT_INTERVAL minutes until the
    user ends the program with CTRL-C
    Compare current quote with previous quote and send
    text when different.
    """

    # For Step C: Replace CODE HERE to get the stock
    #     prices from the Yahoo Finance website using
    #     requests and Beautiful Soup, instead of
    #     using the hardcoded list

    # prices = ['20', '25', '30', '30', '30', '20']
    # price = prices[0]
    # prev_price = '10'

    url = "https://finance.yahoo.com/quote/{}?p={}".format(symbol, symbol)

    # Requests and BeautifulSoup statements
    resp = requests.get(url)
    stocks = bs4.BeautifulSoup(resp.text, "html.parser")
    bs_elem = stocks.find(class_='Trsdu(0.3s)')

    if bs_elem is not None:

        # Price retrieval statements
        price = bs_elem.getText()
        price = price.replace(',', '')
        price = float(price.strip())

        # Set up previous price for checking
        # whether or not to send text
        prev_price = price
    else:
        print("Symbol " + symbol + " not found.")
        sys.exit()

    text = "Start watching {}: Price: {:.2f}".format(symbol, price)
    print(text)
    logging.info(text)

    while True:
        try:
            # Add Requests and BeautifulSoup statements
            # Add Price retrieval statements

            price = price + random()
            logging.info("{}\t{:.2f}".format(symbol, price))

            if price != prev_price:
                text = "{} now at {:.2f} was at {:.2f}".format(symbol, price, prev_price)
                print(text)
                send_email(text)
                prev_price = price

            time.sleep(WAIT_INTERVAL)

        except Exception:
            text = "Connection Problem with " + symbol
            print(text)
            time.sleep(WAIT_INTERVAL)

    i = 0   # not needed with steps C and D

    # Start watching and continue until CTRL-Break

    while True:

        # Get Price with steps A and B only
        # Steps C and D use requests and Beautiful Soup

        price = prices[i % 6]

        # Send price for symbol to log

        logging.info(symbol + "\t" + price)

        i = i + 1  # not needed with Steps C and D

        # Check for price difference and send email,
        # if different

        if price != prev_price:
            text = symbol + " now at " + price + \
                   "; was " + prev_price
            print(text)
            send_email(text)
            prev_price = price

        time.sleep(WAIT_INTERVAL)

def send_email(msg):
    """
    For now, this program just prints a message
    The code that sends the email is in Step D
    """

    print("sendEmail: " + msg)

main()