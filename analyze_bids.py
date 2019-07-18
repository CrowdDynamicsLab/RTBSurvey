import sys, sqlite3, json, re
from pprint import pprint
import traceback
import matplotlib.pyplot as plt

BASELINE_PAGES = ['www.cnn.com', 'www.foxnews.com/', 'www.engadget.com']

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def parse_bids_from_cygnus_response(content):    
    if content[0] == '"':
        content = content[1:-1]
    if re.match(r'\w+', content):
        content = ')'.join('('.join(content.split('(')[1:]).split(')')[:-1])
    else:
        # content = content.replace('\\"', '"')
        # content = content.replace('\\"', '"')
        pass
    try:
        content_dict = json.loads(content)
    except Exception as e:
        print(content)
        traceback.print_exc()
        return []
    result = []
    if 'seatbid' not in content_dict:
        return result
    for sb in content_dict['seatbid']:
        seat = sb['seat']
        for bid in sb['bid']:
            bid['seat'] = seat
            result.append(bid)
    return result



def get_cygnus_at_site(profile_name, site_pattern):
    result = []
    conn = sqlite3.connect('crawl_data/{}/crawl-data.sqlite'.format(profile_name))
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(
        "SELECT res.visit_id, res.content_hash, res.time_stamp FROM http_responses as res join http_requests as req on req.request_id=res.request_id WHERE res.url like '%cygnus%' AND (req.top_level_url like '%{}/')".format(site_pattern))
    rows = cur.fetchall()
    for row in rows:
        content = row['content_hash']
        bids = parse_bids_from_cygnus_response(content)
        for bid in bids:            
            result.append({
                'raw_bid': bid,
                'time_stamp': row['time_stamp'],
                'source': site_pattern,
                'visit_id': row['visit_id'],
                'price': int(bid['ext']['pricelevel'][1:])/100.0
                })
    conn.close()    
    return result

# given a string profile name, this will go into the database
# and retrieve every bid it can
def get_cygnus_bids_for_profile(profile_name):
    result = []
    result.extend(get_cygnus_at_site(profile_name, 'cnn.com'))
    result.extend(get_cygnus_at_site(profile_name, 'foxnews.com'))
    result.extend(get_cygnus_at_site(profile_name, 'engadget.com'))
    return result

def plot_data_by_visit(profile, source, visits):
    data = []
    for visit_id, prices in visits.items():
        print('visit_id: {}, prices: {}'.format(visit_id, prices))
        data.append(prices)
    fig, ax = plt.subplots()
    ax.set_title('Visits for profile {}, site {}'.format(profile, source))
    ax.boxplot(data)

    plt.show()


def plot_data(data, profile):
    index = {}
    for bid in data:
        source = bid['source']
        if source not in index:
            index[source] = {}
        visit_id = bid['visit_id']
        if visit_id not in index[source]:
            index[source][visit_id] = []
        price = bid['price']
        index[source][visit_id].append(price)
    for source, visits in index.items():
        plot_data_by_visit(profile, source, visits)

        



if __name__ == "__main__":
    cyg_data = get_cygnus_bids_for_profile(sys.argv[1])
    plot_data(cyg_data, sys.argv[1])
