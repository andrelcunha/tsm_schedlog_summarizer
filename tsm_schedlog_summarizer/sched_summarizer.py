
SCHEDLOG = ""

DICT_TITLES = {
    'TOTAL_OBJ_INSPECT': ['Total number of objects inspected', []],
    'TOTAL_OBJ_BACK_UP': ['Total number of objects backed up', []],
    'TOTAL_OBJ_UPDATED': ['Total number of objects updated', []],
    'TOTAL_OBJ_REBOUND': ['Total number of objects rebound', []],
    'TOTAL_OBJ_DELETED': ['Total number of objects deleted', []],
    'TOTAL_OBJ_EXPIRED': ['Total number of objects expired', []],
    'TOTAL_OBJ_FAILED': ['Total number of objects failed', []],
    'TOTAL_BYTES_INSPECT': ['Total number of bytes inspected', []],
    'TOTAL_BYTES_TRANSFERRED': ['Total number of bytes transferred', []],
    'DATA_TRANSFER_TIME': ['Data transfer time', []],
    'NETWORK_DATA_TRANSFER_RATE': ['Network data transfer rate', []],
    'AGGREGATE_DATA_TRANSFER_RATE': ['Aggregate data transfer rate', []],
    'OBJ_COMPRESSED_BY': ['Objects compressed by', []],
    'TOTAL_DATA_REDUCTION_RATIO': ['Total data reduction ratio', []],
    'ELAPSED_PROCESSING_TIME': ['Elapsed processing time', []],
}
DICT_BYTES = dict(B=1, KB=1000, MB=1000000, GB=1000000000, TB=1000000000)
BYTES = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB']


def convert_str(str_value):
    return int(str_value.replace(',', ''))


def convert_byte_unit_2_byte_int(unit_value_str):
    """
    Get a string with a float and byte unit, i.e. MB, and returns a integer value of bytes.
    :param : unit_value_str
    :return: int
    """
    tmp_str = ' '.join(unit_value_str.split())
    value, unit = unit_value_str.split()
    return int(float(value)*DICT_BYTES.get(unit))


def time_str_2_secs_int(time_str):
    hours, minutes, secs = [int(s) for s in time_str.split(':')]
    s = secs + (minutes * 60) + (hours * 3600)
    return s


def analyse_line(line):
    title = line[:line.find(":")]
    value = line.lstrip(title + ":")
    return title, value


def sum_dict_value(d, key, value):
    if d[key][1].__len__().__gt__(0):
        tmp = d[key][1].pop()
    else:
        tmp = 0
    d[key][1].append(tmp + value)

'''
def humanize_byte(value, unit='B'):
    result = value
    tmp = value / 1000
    if not tmp < 1:
        result = tmp
        unit = 'KB'
        tmp = value / 1000000
        if not tmp < 1:
            result = tmp
            unit = 'MB'
            tmp = value / 1000000000
            if not tmp < 1:
                result = tmp
                unit = 'GB'
                if not tmp < 1:
                    result = tmp
                    unit = 'GB'
    return result, unit
'''


def humanize_byte(value, unit='B'):
    index = BYTES.index(unit)
    tmp = value / 1000**index
    print("tmp:{tmp}, index:{index}".format(tmp=tmp, index=index))
    if tmp < 1:
        index = index-1
        result = value / 1000**index
        unit = BYTES[index]
    elif tmp >= 1000 and index < 7:
        unit = BYTES[index+1]
        print(unit)
        return humanize_byte(value, unit)
    else:
        result = tmp
    return result, unit


def humanize_sec(value):
    import math
    tmp_m, hours = math.modf(value / 3600)
    seconds, minutes = math.modf(tmp_m * 60)
    return math.ceil(hours), math.ceil(minutes), math.ceil(seconds)


def main(filename):
    with open(filename, mode='r') as fn:
        for line in fn:
            for d_key, d_value in DICT_TITLES.items():
                d_title = d_value[0]
                value = 0
                if line.find(d_title) > -1:
                    title, raw_value = analyse_line(line)
                    if title.find('objects') > -1:
                        value = convert_str(raw_value)
                        sum_dict_value(DICT_TITLES, d_key, value)
                    elif title.find('bytes') > -1:
                        value += convert_byte_unit_2_byte_int(raw_value.strip().replace(',', ''))
                        sum_dict_value(DICT_TITLES, d_key, value)
                    elif title.find('Data') > -1:
                        value = float(raw_value.replace('sec', ''))
                        sum_dict_value(DICT_TITLES, d_key, value)
                    elif title.find('rate') > -1:
                        value = float(raw_value.replace('KB/sec', '').strip().replace(',', ''))
                        DICT_TITLES[d_key][1].append(value)
                    elif (title.find('compressed') > -1) or (title.find('ratio') > -1):
                        value = float(raw_value.replace('%', '').strip())
                        if value > 0:
                            DICT_TITLES[d_key][1].append(value)
                    elif title.find('Elapsed') > -1:
                        value = time_str_2_secs_int(raw_value)
                        sum_dict_value(DICT_TITLES, d_key, value)
    for d_key, d_value in DICT_TITLES.items():
        d_title = d_value[0]
        unit = ''
        if d_value[1].__len__().__eq__(1):
            value = d_value[1][0]
            if d_title.find('bytes') > -1:
                tmp, u = humanize_byte(value)
                unit = ' '+u
                total = "%.2f" % tmp
            elif d_title.find('Elapsed') > -1:
                hours, minutes, seconds = humanize_sec(value)
                total = "{h}:{m}:{s}".format(h=hours, m=minutes, s=seconds)
            elif d_title.find('Data transfer time') > -1:
                total = "%.2f" % value
                unit = ' secs'
            else:
                total = value
        else:
            try:
                tmp = sum(d_value[1])/len(d_value[1])
                total = "%.2f" % tmp
            except ZeroDivisionError:
                total = 0
            if d_title.find('rate') > -1:
                unit = ' KB/sec'
            elif (d_title.find('compressed') > -1) or (d_title.find('ratio') > -1):
                unit = '%'
        print("{title}: {total}{unit}".format(title=d_value[0], total=total, unit=unit))

if __name__ == '__main__':
    import sys
    file_name = sys.argv[1]
    main(file_name)
