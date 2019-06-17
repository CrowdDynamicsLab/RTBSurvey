import sys, sqlite3, json, re
from pprint import pprint



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
        content = content.replace('\\"', '"')
        content = content.replace('\\"', '"')
    content_dict = json.loads(content)
    result = []
    if 'seatbid' not in content_dict:
        return result
    for sb in content_dict['seatbid']:
        seat = sb['seat']
        for bid in sb['bid']:
            bid['seat'] = seat
            result.append(bid)
    return result

# given a string profile name, this will go into the database
# and retrieve every bid it can
def get_cygnus_bids_for_profile(profile_name):
    conn = sqlite3.connect('crawl_data/{}/crawl-data.sqlite'.format(profile_name))
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM http_responses WHERE url like '%cygnus%'")
    rows = cur.fetchall()
    for row in rows:
        content = row['response_content']
        bids = parse_bids_from_cygnus_response(content)
        for bid in bids:
            print bid['ext']['pricelevel']
            print row['referrer']
            print row['time_stamp']
    conn.close()


if __name__ == "__main__":
    get_cygnus_bids_for_profile(sys.argv[1])