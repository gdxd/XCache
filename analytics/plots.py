import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

site = 'MWT2'
title = site + ' LRU EVNT only'
# title = site + ' FS'
# title = site + ' LRU (files larger than 1GB not cached)'
# title = site + ' LRU (files smaller than 100kB not cached)'
# title = site + ' Clairvoyant'
# title = site + ' LRU prod only'

results = [
    [site + '_1_LRU_results.h5', '1TB'],
    [site + '_2_LRU_results.h5', '2TB'],
    [site + '_5_LRU_results.h5', '5TB'],
    [site + '_10_LRU_results.h5', '10TB'],
    [site + '_20_LRU_results.h5', '20TB'],
    [site + '_30_LRU_results.h5', '30TB'],
    [site + '_40_LRU_results.h5', '40TB'],
    [site + '_50_LRU_results.h5', '50TB'],
    # [site + '_100_LRU_results.h5', '100TB'],
    # [site + '_10000_LRU_results.h5', 'Inf']
]

# results = [
#     [site + '_1_Clairvoyant_results.h5', '1TB'],
#     [site + '_2_Clairvoyant_results.h5', '2TB'],
#     [site + '_5_Clairvoyant_results.h5', '5TB'],
#     [site + '_10_Clairvoyant_results.h5', '10TB'],
#     [site + '_20_Clairvoyant_results.h5', '20TB'],
#     [site + '_30_Clairvoyant_results.h5', '30TB'],
#     [site + '_40_Clairvoyant_results.h5', '40TB'],
#     [site + '_50_Clairvoyant_results.h5', '50TB'],
#     # [site + '_100_Clairvoyant_results.h5', '100TB'],
#     # [site + '_200_Clairvoyant_results.h5', '200TB'],
#     # [site + '_400_Clairvoyant_results.h5', '400TB'],
#     # [site + '_800_Clairvoyant_results.h5', '800TB'],
#     # [site + '_10000_Clairvoyant_results.h5', 'Inf']
# ]

# results = [
#     [site+ '_5_FS_results.h5', '5TB'],
#     [site+ '_10_FS_results.h5', '10TB'],
#     [site+ '_20_FS_results.h5', '20TB'],
#     [site+ '_30_FS_results.h5', '30TB'],
#     [site+ '_40_FS_results.h5', '40TB'],
#     [site+ '_50_FS_results.h5', '50TB'],
#     [site+ '_10000_FS_results.h5', 'Inf']
# ]

df = None
for r in results:
    rdf = pd.read_hdf(r[0])
    rdf.columns = [r[1]]
    print(rdf)
    if df is None:
        df = rdf
    else:
        df = df.join(rdf)

print(df)

rt = df.transpose()
rt['cache hit rate'] = rt['cache hits'] / rt['total accesses'] * 100
rt['cache data delivery'] = rt['delivered from cache'] / rt['delivered data'] * 100
print(rt)


lab = rt.index
ind = np.arange(len(lab))

plt.figure(figsize=(12, 10))
plt.suptitle(title, fontsize=18)

ax1 = plt.subplot(221)
ax1.plot(ind, rt["cache hit rate"], '--bo')
ax1.set_ylabel('from cache [%]', color='b')
ax1.plot(ind, rt["cache data delivery"], '-r+')
ax1.legend()
ax1.grid(axis='y', linestyle='-', linewidth=.5)
plt.xticks(ind, lab)
plt.xlabel('cache size')

ax3 = plt.subplot(222)
# ax2 = plt.twinx()
ax3.plot(ind, rt["cleanups"], '-r+')
ax3.set_ylabel('cleanups', color='r')
ax3.grid(axis='y', linestyle='-', linewidth=.5)
plt.xticks(ind, lab)
plt.xlabel('cache size')

ax4 = plt.subplot(223)
ax4.plot(ind, rt["files in cache"], '-X')
ax4.set_ylabel('files in cache')
ax4.grid(axis='y', linestyle='-', linewidth=.5)
plt.xticks(ind, lab)
plt.xlabel('cache size')


ax5 = plt.subplot(224)
ax5.plot(ind, rt["avg. accesses of cached files"], 'g-x')
ax5.set_ylabel('avg. accesses of cached files')
ax5.grid(axis='y', linestyle='-', linewidth=.5)
plt.xticks(ind, lab)
plt.xlabel('cache size')

plt.savefig(title + '_analysis.png')
plt.show()
#         plt.yscale('log', nonposy='clip')
#         plt.xscale('log', nonposy='clip')
#         plt.hist(df['filesize'], 200)
