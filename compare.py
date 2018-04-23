# import pickle
import shelve
import time

from factoring.interfaces import get_factor_bqm, submit_factor_bqm, postprocess_factor_response
# from factoring.fixed_embedding import factor


if __name__ == '__main__':
    shelf = shelve.open("shelf/embedding1524512692.62")
    embedding = shelf['embedding']
    shelf.close()
    for trial in range (1000):
        bqm = get_factor_bqm(49)
        response, embedding = submit_factor_bqm(bqm,embedding) # comment out input embedding to generate new one
        output49 = postprocess_factor_response(response, 49)

        bqm = get_factor_bqm(21)
        response, _ = submit_factor_bqm(bqm, embedding)
        output21 = postprocess_factor_response(response, 21)

        bqm = get_factor_bqm(12)
        response, _ = submit_factor_bqm(bqm, embedding)
        output12 = postprocess_factor_response(response, 12)

        shelf = shelve.open("embedding1524512692.62/output%s" % time.time())
        shelf['output49'] = output49
        shelf['output21'] = output21
        shelf['output12'] = output12
        shelf['embedding'] = embedding
        shelf.close()

        # output = factor(P)
        # with open("pickle/fixed%s" % time.time(), "wb") as f:
        #     pickle.dump(output, f)

# import os
# import pandas as pd
# from collections import defaultdict

# d = defaultdict(list)

# for filename in os.listdir('.'):
#     # if filename.startswith('output'):
#     shelf = shelve.open(filename)
#     d['percent49'].append(sum([x['percentageOfOccurrences'] for x in shelf['output49']['results'] if x['valid']]))
#     d['percent21'].append(sum([x['percentageOfOccurrences'] for x in shelf['output21']['results'] if x['valid']]))
#     d['percent12'].append(sum([x['percentageOfOccurrences'] for x in shelf['output12']['results'] if x['valid']]))
#     for k, v in shelf['embedding'].items():
#         d[k].append(len(v))
#     d['filename'].append(filename)
#     shelf.close()

# df = pd.DataFrame(data=d)
# df['minpercent'] = df[['percent49', 'percent21', 'percent12']].min(axis=1)
# df = df.sort_values('minpercent')
# # df = df[(df.T != 0).all()]
# pd.set_option('expand_frame_repr', False)
# pd.set_option('max_columns', 50)

