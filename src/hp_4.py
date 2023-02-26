# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
     
    return [datetime.strptime(od, "%Y-%m-%d").strftime('%d %b %Y') for od in old_dates]


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str) or not isinstance(n, int):
        raise TypeError()
    adr = []
    date_start = datetime.strptime(start, '%Y-%m-%d')
    for a in range(n):
        adr.append(date_start + timedelta(days=a))
    return adr


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    vls_len = len(values)
    d_rng = date_range(start_date, vls_len)
    c = list(zip(d_rng, values))
    return c


def util_book(infile):
    
    fields = ("book_uid,isbn_13,patron_id,date_checkout,date_due,date_returned".
              split(','))
    
    with open(infile, 'r') as f:
        infileData = DictReader(f, fieldnames=fields)
        infile_rows = [row for row in infileData]


    return infile_rows.pop(0)
def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    totalfee = defaultdict(float)
    DAT_FORMAT = '%m/%d/%Y'
    data = util_book(infile)
    
    for line in data:
        patron_id = line['patron_id']
        due = datetime.strptime(line['date_due'], DAT_FORMAT)
        returned = datetime.strptime(line['date_returned'], DAT_FORMAT)

        late = (returned - due).days
        
        totalfee[patron_id]+= 0.25 * late if late > 0 else 0.0

    out_list = [
        {'patron_id': p_id, 'late_fees': f'{fees:0.2f}'} for p_id, fees in totalfee.items()
    ]

    with open(outfile, 'w') as f:
        pid_fees = DictWriter(f, ['patron_id', 'late_fees'])
        pid_fees.writeheader()
        pid_fees.writerows(out_list)


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
