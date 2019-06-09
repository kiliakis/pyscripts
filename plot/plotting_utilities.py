import matplotlib.pyplot as plt
import numpy as np
import subprocess
import re


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


def get_stats_from_metrics(metrics_to_calc, metric_formulas, regexp='([a-zA-Z0-9_%]+)'):
    stats = set()
    for metric in metrics_to_calc:
        f = metric_formulas[metric]
        matches = re.compile(regexp).findall(f)
        for m in matches:
            stats.add(m)
    return list(stats)


def get_data_per_kernel_no_scan(h, data, stats_to_keep, require_conversion, warnings=False):
    # The first for loop creates all the keys
    # The second assigns to each key the value.
    tempdir = {}
    for r in data:
        if r[h.index('metric')] == 'kernel_name':
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



def get_data_per_kernel_with_scan(h, data, stats_to_keep, require_conversion, warnings=False):
    # The first for loop creates all the keys
    # The second assigns to each key the value.
    tempdir = {}
    for r in data:
        if r[h.index('metric')] == 'kernel_name':
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


def get_traces_per_kernel_with_scan(h, data, warnings=False):
    datadir = {}
    for r in data:
        app = r[h.index('app_and_args')]
        config = r[h.index('config')]
        kname = r[h.index('kernel_name')]
        ids = r[h.index('kernel_ids')]
        cycles = r[h.index('cycles')].split('|')
        if (len(cycles)) == 0 or (cycles[0] == ''):
            if warnings:
                print('WARNING Trace problem with {}:{}'.format(app, kname))
            continue
        if 'active_threads' in h:
            active_threads = r[h.index('active_threads')].split('|')
            shader_cores = r[h.index('shader_cores')]
        else:
            active_threads = r[h.index('warps')].split('|')
            shader_cores = 0
        # metric = 'active_threads'
        key = '{}/{}'.format(app, kname)
        if key not in datadir:
            datadir[key] = {}
        if config not in datadir[key]:
            datadir[key][config] = {
                'x': np.array(cycles, int) - int(cycles[0]),
                'y': np.array(active_threads, int)}
    return datadir


def evaluate_metrics_no_scan(datadir, metrics_to_calc, metrics_formulas, constants={}, warnings=False):
    metricsdic = {}
    for m_name in metrics_to_calc:
        m_formula = metrics_formulas[m_name]
        # metricsdic[m_name] = {}
        for k_name, stats in datadir.items():
            res = m_formula
            for s, val in stats.items():
                res = res.replace(s, str(np.mean(np.array(val, float))))
            for s, val in constants.items():
                res = res.replace(s, val)
            try:
                res = eval(res)
            except Exception as e:
                if warnings:
                    print('WARNING {}:{} had the value {} and raised {}'.format(m_name, k_name,
                                                                                res, e))
                # print(e)
                continue
            # if res < 0:
            #     print('WARNING!', res, k_name, stats)
            if m_name not in metricsdic:
                metricsdic[m_name] = {}
            metricsdic[m_name][k_name] = res
    return metricsdic


def evaluate_metrics_with_scan(datadir, metrics_to_calc, metrics_formulas, constants={}, warnings=False):
    metricsdic = {}
    for m_name in metrics_to_calc:
        m_formula = metrics_formulas[m_name]
        metricsdic[m_name] = {}
        for k_name, metrics in datadir.items():
            metricsdic[m_name][k_name] = {}
            for stat, configs in metrics.items():
                for config, val in configs.items():
                    if config not in metricsdic[m_name][k_name]:
                        metricsdic[m_name][k_name][config] = m_formula
                    metricsdic[m_name][k_name][config] = metricsdic[m_name][k_name][config].replace(
                        stat, str(np.mean(np.array(val, float))))

    temp_dir = dict(metricsdic)
    for m_name, kernels in temp_dir.items():
        for k_name, configs in kernels.items():
            for config, res in configs.items():
                # if 'shaders' in res:
                    # print(m_name, k_name, config)
                for c, val in constants.items():
                    res = res.replace(c, val)
                try:
                    res = eval(res)
                except Exception as e:
                    if warnings:
                        print('WARNING: {}:{}:{} had the value {} and raised {}'.format(
                            m_name, k_name, config, res, e))
                    metricsdic[m_name][k_name][config] = float('nan')
                    continue
                metricsdic[m_name][k_name][config] = res

    return metricsdic


def get_figdic_with_scan(metricdic_lst, basedic=None, metrics_to_norm=[],
                         knobs_to_keep=None, knobs_to_sort=None, warnings=False):
    figdic = {}
    if not isinstance(metricdic_lst, (list,)):
        metricdic_lst = [metricdic_lst]

    for metricdic in metricdic_lst:
        for metric in metricdic.keys():
            for app in metricdic[metric].keys():
                for conf in metricdic[metric][app].keys():
                    val = metricdic[metric][app][conf]
                    if basedic and (metric in metrics_to_norm):
                        # Check that the same config exists in the other dir.
                        if (metric in basedic) and (app in basedic[metric]):
                            if conf in basedic[metric][app]:
                                val_base = float(basedic[metric][app][conf])
                            else:
                                val_base = np.mean(
                                    [float(v) for v in basedic[metric][app].values()])
                        else:
                            if warnings:
                                print('WARNING {}:{} not in basedic'.format(
                                    metric, app))
                            continue
                    else:
                        val_base = 1

                    if np.isnan(val_base) or np.isnan(val):
                        continue

                    matches = re.compile('([a-z]+)_([a-z\d_]+)').findall(conf)

                    if not matches:
                        matches = re.compile('([a-z]+)(\d+:?\d*)').findall(conf)
                        # matches = re.compile('([a-z]+)(\d+)').findall(conf)
                        if not matches:
                            if warnings:
                                print('{}:{} Problem with matching the expression {}'.format(
                                    app, metric, conf))
                            continue

                    # for i in range(len(matches)):
                    knob = ','.join([m[0] for m in matches])
                    # knob = ','.join([m[0] for m in matches])
                    if knobs_to_keep and (knob not in knobs_to_keep):
                        continue
                    if app not in figdic:
                        figdic[app] = {}
                    if metric not in figdic[app]:
                        figdic[app][metric] = {}
                    if knob not in figdic[app][metric]:
                        figdic[app][metric][knob] = {'x': [], 'y': []}

                    x = ','.join([m[1] for m in matches])
                    y = float(metricdic[metric][app][conf]) / float(val_base)
                    if not np.isnan(y):
                        figdic[app][metric][knob]['x'].append(x)
                        figdic[app][metric][knob]['y'].append(y)

    for app in figdic.keys():
        for metric in figdic[app].keys():
            for knob, vals in figdic[app][metric].items():
                x = np.array(vals['x'])
                y = np.array(vals['y'])
                if knobs_to_keep and knobs_to_sort:
                    sort_with = knobs_to_sort[knobs_to_keep.index(knob)]
                    sort_indices = [knob.split(',').index(k) for k in sort_with]
                else:
                    sort_indices = [0]
                try:
                    indices = [i[0] for i in sorted(enumerate(x),
                                                    key=lambda a: [int(a[1].split(',')[j]) for j in sort_indices])]
                except:
                    indices = [i[0] for i in sorted(enumerate(x),
                                                    key=lambda a: [a[1].split(',')[j] for j in sort_indices])]

                x, y = x[indices], y[indices]
                figdic[app][metric][knob]['x'] = x
                figdic[app][metric][knob]['y'] = y
    return figdic


def get_figdic_with_scan_knob_first(metricdic_lst, basedic=None, metrics_to_norm=[],
                                    knobs_to_keep=None, knobs_to_sort=None, warnings=False):
    figdic = {}
    if not isinstance(metricdic_lst, (list,)):
        metricdic_lst = [metricdic_lst]

    for metricdic in metricdic_lst:
        for metric in metricdic.keys():
            for app in metricdic[metric].keys():
                for conf in metricdic[metric][app].keys():
                    val = metricdic[metric][app][conf]
                    if basedic and (metric in metrics_to_norm):
                        # Check that the same config exists in the other dir.
                        if (metric in basedic) and (app in basedic[metric]):
                            if conf in basedic[metric][app]:
                                val_base = float(basedic[metric][app][conf])
                            else:
                                val_base = np.mean(
                                    [float(v) for v in basedic[metric][app].values()])
                        else:
                            if warnings:
                                print('WARNING {}:{} not in basedic'.format(
                                    metric, app))
                            continue
                    else:
                        val_base = 1

                    if np.isnan(val_base) or np.isnan(val):
                        continue

                    knob = conf
                    if knobs_to_keep and (knob not in knobs_to_keep):
                        continue
                    if metric not in figdic:
                        figdic[metric] = {}
                    if knob not in figdic[metric]:
                        figdic[metric][knob] = {'x': [], 'y': []}

                    x = app
                    y = float(metricdic[metric][app][conf]) / float(val_base)
                    if not np.isnan(y):
                        figdic[metric][knob]['x'].append(x)
                        figdic[metric][knob]['y'].append(y)

    for metric in figdic.keys():
        for knob, vals in figdic[metric].items():
            x = np.array(vals['x'])
            y = np.array(vals['y'])
            indices = np.argsort(y)
            figdic[metric][knob]['x'] = x[indices]
            figdic[metric][knob]['y'] = y[indices]

    return figdic


def extract_knob(string, knob):
    rec = '-?{}_(\w+)-?'.format(knob)
    rec = re.compile(rec)
    match = rec.search(string)
    if match:
        return string.replace(match.group(0), ''), match.group(1)
    else:
        return string, None


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


def dictify(h, data, key_names, cols, prefixes=None):
    d = {}
    if prefixes is None:
        prefixes = len(key_names) * ['']
    for r in data:
        key = ''
        for k in key_names:
            key += prefixes[key_names.index(k)] + r[h.index(k)]
        if key not in d:
            d[key] = {}
        for col in cols:
            assert col in h, '{} not in header'.format(col)
            if col not in d[key]:
                d[key][col] = []
            d[key][col].append(r[h.index(col)])
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


def get_values(v, h, s):
    return np.array(v[:, h.index(s)], float)


def get_plots(h, data, key_names, exclude=[]):
    d = {}
    for r in data:
        match = True
        key = ''
        for k, v in key_names.items():
            if v is None:
                key += r[h.index(k)] + '-'
            elif r[h.index(k)] in v:
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
