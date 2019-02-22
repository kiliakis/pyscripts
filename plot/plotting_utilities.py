import matplotlib.pyplot as plt
import numpy as np
import subprocess


def save_and_crop(fig, name, *args, **kw):
    fig.savefig(name, *args, **kw)
    if 'pdf' not in name:
        return
    try:
        subprocess.call(['pdfcrop', name, name])
    except FileNotFoundError as e:
        print(e)


def import_results(file):
    d = np.genfromtxt(file, dtype='str')
    return d.tolist()


def sort_based_on_order(order, major_arr, *minor_arrs):
    j = 0
    for i in range(len(order)):
        try:
            idx = list(major_arr).index(order[i])
        except Exception as e:
            continue
        # idx = np.where(major_arr == order[i])[0]
        # print(idx)
        # if len(idx) == 0:
        #     continue
        major_arr[j], major_arr[idx] = major_arr[idx], major_arr[j]
        for arr in minor_arrs:
            arr[j], arr[idx] = arr[idx], arr[j]
        j += 1


def get_data_per_kernel_no_scan(h, data, stats_to_keep, require_conversion):
    # The first for loop creates all the keys
    # The second assigns to each key the value.
    tempdir = {}
    for r in data:
        if r[h.index('metric')] == 'kernel_launch_uid':
            tempdir['{}/{}'.format(r[h.index('app_and_args')],
                                   r[h.index('config')])] = r[h.index('valuelist')].split('|')
    datadir = {}
    for r in data:
        metric = r[h.index('metric')]
        if metric in stats_to_keep:
            app = r[h.index('app_and_args')]
            config = r[h.index('config')]
            vals = r[h.index('valuelist')].split('|')
            if metric in require_conversion:
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
    return datadir


def get_data_per_kernel_with_scan(h, data, stats_to_keep, require_conversion):
    # The first for loop creates all the keys
    # The second assigns to each key the value.
    tempdir = {}
    for r in data:
        if r[h.index('metric')] == 'kernel_launch_uid':
            tempdir['{}/{}'.format(r[h.index('app_and_args')],
                                   r[h.index('config')])] = r[h.index('valuelist')].split('|')
    datadir = {}
    for r in data:
        metric = r[h.index('metric')]
        if metric in stats_to_keep:
            app = r[h.index('app_and_args')]
            config = r[h.index('config')]
            vals = r[h.index('valuelist')].split('|')
            if metric in require_conversion:
                vals = np.array(vals, float)
                vals[1:] = vals[1:] - vals[:-1]
                vals = np.array(vals, str)
            for name, val in zip(tempdir['{}/{}'.format(app, config)],
                                 vals):
                key = '{}/{}'.format(app, name)
                if key not in datadir:
                    datadir[key] = {}
                if metric not in datadir[key]:
                    datadir[key][metric] = {}
                if config not in datadir[key][metric]:
                    datadir[key][metric][config] = []
                datadir[key][metric][config].append(val)
    return datadir


def evaluate_metrics_no_scan(datadir, metrics_to_calc, metrics_formulas, constants={}):
    metricsdir = {}
    for m_name in metrics_to_calc:
        m_formula = metrics_formulas[m_name]
        # metricsdir[m_name] = {}
        for k_name, stats in datadir.items():
            res = m_formula
            for s, val in stats.items():
                res = res.replace(s, str(np.mean(np.array(val, float))))
            for s, val in constants.items():
                res = res.replace(s, val)
            try:
                res = eval(res)
            except Exception as e:
                print('WARNING {}:{} had the value {} and raised {}'.format(m_name, k_name,
                                                                            res, e))
                # print(e)
                continue
            # if res < 0:
            #     print('WARNING!', res, k_name, stats)
            if m_name not in metricsdir:
                metricsdir[m_name] = {}
            metricsdir[m_name][k_name] = res
    return metricsdir


def evaluate_metrics_with_scan(datadir, metrics_to_calc, metrics_formulas, constants={}):
    metricsdir = {}
    for m_name in metrics_to_calc:
        m_formula = metrics_formulas[m_name]
        metricsdir[m_name] = {}
        for k_name, metrics in datadir.items():
            metricsdir[m_name][k_name] = {}
            for stat, configs in metrics.items():
                for config, val in configs.items():
                    if config not in metricsdir[m_name][k_name]:
                        metricsdir[m_name][k_name][config] = m_formula
                    metricsdir[m_name][k_name][config] = metricsdir[m_name][k_name][config].replace(
                        stat, str(np.mean(np.array(val, float))))

    temp_dir = dict(metricsdir)
    for m_name, kernels in temp_dir.items():
        for k_name, configs in kernels.items():
            for config, res in configs.items():
                # if 'shaders' in res:
                    # print(m_name, k_name, config)
                for c, val in constants.items():
                    res = res.replace(c, val)
                try:
                    res = eval(res)
                except NameError as e:
                    print('WARNING: {} for {}:{}:{}'.format(
                        e, m_name, k_name, config))
                    metricsdir[m_name][k_name][config] = float('nan')
                    continue
                metricsdir[m_name][k_name][config] = res

    return metricsdir


def color_y_axis(ax, color):
    """Color your axes."""
    for t in ax.get_yticklabels():
        t.set_color(color)
    return None


def annotate(ax, A, B, **kwargs):
    for x, y in zip(A, B):
        # ax.annotate('%.2f, %.2f' % (x, y), xy=(
        ax.annotate('%.0f' % (y), xy=(
            x, y), textcoords='data', **kwargs)


def annotate_min(A, B):
    y = min(B)
    i = B.index(y)
    plt.subplot().annotate('%.2e' % float(y), xy=(A[i], y), size='large')


# def annotate_max(A, B):
#     y = max(B)
#     i = B.index(y)

#     plt.subplot().annotate('%.2e' % float(y), xy=(A[i], y), size='large')


def annotate_max(ax, A, B, **kwargs):
    y = max(B)
    i = list(B).index(y)
    ax.annotate('%.0f' % float(y), xy=(A[i], y), **kwargs)


def group_by(header, list1, key_names, prefixes=None):
    d = {}
    if prefixes is None:
        prefixes = len(key_names) * ['']
    for r in list1:
        key = ''
        for k in key_names:
            key += prefixes[key_names.index(k)] + r[header.index(k)]
        if key not in d:
            d[key] = []
        d[key] += [r]

    return d


def data_to_dir(header, data, key_names, keep_only=None):
    d = {}
    header = list(header)
    for r in data:
        r = list(r)
        tempd = d
        for k in key_names[:-1]:
            if r[header.index(k)] not in tempd:
                tempd[r[header.index(k)]] = {}
            tempd = tempd[r[header.index(k)]]
        if keep_only:
            tempd[r[header.index(key_names[-1])]] = [r[i]
                                                     for i in range(len(r)) if header[i] in keep_only]
        else:
            tempd[r[header.index(key_names[-1])]] = r

    return d


def get_plots(h, data, key_names, exclude=[]):
    d = {}
    for r in data:
        match = True
        key = ''
        for k, v in key_names.items():
            if r[h.index(k)] in v:
                key += r[h.index(k)] + '-'
            else:
                match = False
                break
        if match:
            key = key[:-1]

            if any(all(x in key for x in excl) for excl in exclude):
                continue
            if key not in d:
                d[key] = []
            d[key] += [r]
            # d[key] = np.append(d[key], np.array(r), axis=0)
    for k, v in d.items():
        d[k] = np.array(v)
    return d

# def new_group_by(header, data, key_names, d={}):
#     if not key_names:
#         return d
#     # d = {}
#     key = key_names[0]
#     idx = header.index(key)
#     for r in data:
#         if r[idx] not in d:
#             d[r[idx]] = []
#         d[r[idx]] += [r]
#     # print(d)
#     for k, v in d.items():
#         d[k] = new_group_by(header, v, key_names[1:], d[k])

#     return d


def keep_only(header, dir1, to_keep):
    d = {}
    for k, values in dir1.items():
        if k not in d:
            d[k] = []
        for h in to_keep:
            c = header.index(h)
            list1 = []
            for v in values:
                list1.append(v[c])
            d[k].append(list1)
    return d


def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000
    # add more suffixes if you need them
    return '%d%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


def autolabel(ax, rects, rounding=None, ha='left', **kwargs):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        if rounding:
            height = round(height, rounding)
        string = str(height)
        if height < 1.:
            string = string[1:]
        # if (height > 1.) and integer:
        #     val = '%d' % round(height)
        # else:
        #     val = '%.1lf' % float(height)
        ax.text(rect.get_x(), 1.0 * height,
                string,
                ha=ha, va='bottom', **kwargs)


def plot_lines_from_dir(plotDir, fig=None, x=None, normalize=None, xlabel='', ylabel='',
                        title='', linestyle='-', marker='.', loc='best',
                        show=True, image_name='image.png', xlim=None,
                        ylim=None, xticks=None, ret=False,
                        figsize=()):

    if fig is None:
        fig = plt.figure(figsize=figsize)
    plt.grid(True, which='major', alpha=0.5)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)
    plots = []
    for k, v in plotDir.items():
        if x is None:
            x = np.arange(len(v))

        y = v
        if normalize is not None:
            y = normalize / y
        plots.append(
            plt.plot(x, y, linestyle=linestyle, marker=marker, label=k))

    if xticks is not None:
        plt.xticks(x, xticks)
    plt.legend(loc=loc, fancybox=True, framealpha=0.5)
    plt.tight_layout()
    if ret:
        return plt.gca()
    plt.savefig(image_name, bbox_inches='tight')
    if(show):
        plt.show()
    plt.close()
