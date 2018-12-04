
# Snip 1
# The first for loop creates all the keys
# The second assigns to each key the value.
for infile in args.infiles:
    data = np.genfromtxt(infile, delimiter='\t', dtype=str)
    h, data = list(data[0]), data[1:]
    tempdir = {}
    for r in data:
        if r[h.index('metric')] in 'kernel_name':
            tempdir['{}/{}'.format(r[h.index('app_and_args')],
                                   r[h.index('config')])] = r[h.index('valuelist')].split('|')

    for r in data:
        metric = r[h.index('metric')]
        if metric in locyc['stats_to_keep']:
            app = r[h.index('app_and_args')]
            config = r[h.index('config')]
            vals = r[h.index('valuelist')].split('|')
            if metric in locyc['requires_conversion']:
                vals = np.array(vals, float)
                vals[1:] = vals[1:] - vals[:-1]
                vals = np.array(vals, str)
            for name, val in zip(tempdir['{}/{}'.format(app, config)],
                                 vals):
                key = '{}/{}'.format(app, name)
                if key not in datadir:
                    datadir[key] = {}
                if metric not in datadir[key]:
                    datadir[key][metric] = []
                datadir[key][metric].append(val)


# Snip 2
# This one evaluates metrics specified in a yaml file.
# 
metricsdir = {}
for m_name, m_formula in locyc['metrics_to_calc'].items():
    metricsdir[m_name] = {}
    for k_name, stats in datadir.items():
        res = m_formula
        for s, val in stats.items():
            res = res.replace(s, str(np.mean(np.array(val, float))))
        res = eval(res)
        if res < 0:
            print('WARNING!', res, k_name, stats)
        metricsdir[m_name][k_name] = res