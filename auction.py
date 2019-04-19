import re
import time
import numpy as np
class Bid:

    auction_id = -1
    price = -1
    creative = None
    dim = (0,0)
    ad_id = -1
    ad_name = ''

    def __init__(self, cpm = -1, cr=None, dim=(0,0), ad_id=-1, ad_name=''):
        self.price = cpm
        self.creative = cr
        self.dim = dim
        self.ad_id = ad_id
        self.ad_name = ad_name

    def __str__(self):
        return str([self.auction_id, self.price, self.creative, self.dim, self.ad_id, self.ad_name])

    def __repr__(self):
        return str([self.auction_id, self.price, self.creative, self.dim, self.ad_id, self.ad_name])
class Auction:

    auction_id = -1
    datetime = None
    site = ''
    ad_unit = ''
    bids = []

    def __init__(self, auc_id = -1, datetime = None, site= '', ad_unit = '', bids = []):
        self.auction_id = auc_id
        self.datetime = datetime
        self.site = site
        self.ad_unit = ad_unit
        self.bids = bids

    def add_bid(self, b):
        self.bids.append(b)

    def get_winning_bid(self):
        max = -1
        i = -1
        for bid in self.bids:
            if bid.price > max:
                i = bid
                max = bid.price

        return bid

    def get_avg_bid(self):
        sum =0
        num=0
        if len(self.bids )==0:
            return -1
        for bid in self.bids:
            sum+=bid.price
            num+=1

        return sum/num

    def __str__(self):
        return str([self.auction_id, self.datetime, self.site, self.ad_unit, self.bids])

    def __repr__(self):
        return str([self.auction_id, self.datetime, self.site, self.ad_unit, self.bids])

    def __lt__(self, other):
        return self.datetime<other.datetime

def merge_auctions(a_list):
    bids = []
    for auction in a_list:
        bids  = bids+auction.bids

    a_new = Auction(-1, a_list[0].datetime, a_list[0].site, -1, bids)
    return a_new


def is_num(n):
    try:
        float(n)
        return True
    except:
        return False

def get_num_val(response, var_name, val_offset):
    vals = []

    for match in re.finditer(var_name, response):
        i=1
        val_start = match.end()+val_offset
        val = -1
        while True:
            val_string = response[val_start:(val_start+i)]
            if is_num(val_string):
                val = float(val_string)
                i+=1
                continue
            else:
                break
        vals.append(val)
    return vals

def get_str_val(response, var_name, str_offset):
    vals = []
    for match in re.finditer(var_name, response):
        i=1
        val_start = match.end()+str_offset
        val = -1
        while True:
            val_string = response[val_start:(val_start+i)]
            if val_string.replace(' ', '').isalnum():
                val = val_string
                i+=1
                continue
            else:
                break
        vals.append(val)
    return vals

#each var argument is a unique identifier for the value you're looking for - make sure there is no conflict or this will mess up
#val_offset is number of characters to skip after identifier for numeric values; in the case of cygnus, there's a ':' character so offset =1
#str_offset is number of characters to skip for non-numeric values; in the case of cygnus, there's ':/"' so I set it to 3.
def parse_response(row, response, price_var = '/"price/"', cid_var = '/"cid/"' , dim_vars = ['/"w/"','/"h/"'], adname_var = '/"advbrand/"', adid_var = '/"advbrandid/"', val_offset = 1, str_offset=3):

    prices = get_num_val(response, price_var, val_offset)
    cids = get_str_val(response, cid_var, str_offset)
    w = get_num_val(response, dim_vars[0], val_offset)
    h = get_num_val(response, dim_vars[1], val_offset)
    dims = [(w[i],h[i]) for i in range(0, len(w))]
    adids = get_num_val(response, adid_var, val_offset)
    adnames = get_str_val(response, adname_var, str_offset)

    bids = []


    for i in range(min(len(prices), len(cids), len(w), len(h), len(adids), len(adnames))):
        bids.append(Bid(prices[i], cids[i], dims[i], adids[i],adnames[i]))

    t=time.strptime(row[1].replace("-",""), "%Y%m%dT%H:%M:%S.%fZ")
    return (Auction(datetime=t, site=row[2], bids = bids))
