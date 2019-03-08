class Bid:

    auction_id = -1
    cpm = -1
    creative = None
    dim = (0,0)
    advertiser_id = -1
    advertiser_name = ''

    def __init__(self, auc_id = -1, cpm, = -1 cr=None, dim=(0,0), ad_id=-1, ad_name=''):
        self.auction_id=auc_id
        self.cpm = cpm
        self.creative = cr
        self.dim = dim
        self.advertiser_id = ad_id
        self.advertiser_name = ad_name

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

    def add_bid(b):
        bids.append(b)

    def get_winning_bid():
        max = -1
        i = -1
        for bid in bids:
            if bid.cpm > max:
                i = bid
                max = bid.cpm

        return bid 
