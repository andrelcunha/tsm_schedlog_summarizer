import os

SCHEDLOG = ""
LIST_TITLES = [
    ['TOTAL_OBJ_INSPECT', ['Total number of objects inspected']],
    ['TOTAL_OBJ_BACK_UP', ['Total number of objects backed up', 0]],
    ['TOTAL_OBJ_UPDATED', ['Total number of objects updated', 0]],
    ['TOTAL_OBJ_REBOUND', ['Total number of objects rebound', 0]],
    ['TOTAL_OBJ_DELETED', ['Total number of objects deleted', 0]],
    ['TOTAL_OBJ_EXPIRED', ['Total number of objects expired', 0]],
    ['TOTAL_OBJ_FAILED', ['Total number of objects failed', 0]],
    ['TOTAL_BYTES_INSPECT', ['Total number of bytes inspected', 0]],
    ['TOTAL_BYTES_TRANSFERRED', ['Total number of bytes transferred', 0]],
    ['DATA_TRANSFER_TIME', ['Data transfer time', 0]],
    ['NETWORK_DATA_TRANSFER_RATE', ['Network data transfer rate', 0]],
    ['AGGREGATE_DATA_TRANSFER_RATE', ['Aggregate data transfer rate', 0]],
    ['OBJ_COMPRESSED_BY', ['Objects compressed by', 0]],
    ['TOTAL_DATA_REDUCTION_RATIO', ['Total data reduction ratio', 0]],
    ['ELAPSED_PROCESSING_TIME', ['Elapsed processing time', 0]],
]

DICT_BYTES = [
    ['B', 1],
    ['KB', 1000],
    ['MB', 1000000],
    ['GB', 1000000000]
]


def remove_title_str(title, line):
    return line.lstrip(LIST_TITLES.get(title)[0])


def convert_str(str_value):
    return int(str_value.replace(',', ''))


def convert_byte_unit_2_byte_int(unit_value_str):
    """
    Get a string with a float and byte unit, like MB, and returns a integer value of bytes.
    :param : unit_value_str
    :return: int
    """
    value, unit = unit_value_str.split(' ')
    return int(float(value)*DICT_BYTES.get(unit))


def time_str_2_secs_int(time_str):
    hours, minutes, secs = [int(s) for s in time_str.split(':')]
    s = (minutes * 60) + (hours * 3600)
    return s


def analyse_line(line):
    title = line[:line.find(":")]
    value = line.lstrip(title + ":")
    return title, value


def sum_dict_value(d, key, value):
    tmp = d[key].pop()
    d[key].append(tmp + value)


def humanize_byte(value):
    result=value
    unit='B'
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
    return result,unit


def humanize_sec(value):
    result=value
    unit='B'
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
    return result,unit


def main(filename):
    with open(filename, mode='r') as fn:
        for line in fn:
            for l_title, l_list in LIST_TITLES.items():
                for ll_title, ll_list in l_list:
                    value = 0
                    if line.find(ll_title) > -1:
                        title, raw_value = analyse_line(line)
                        if title.find('bytes'):
                            value += convert_byte_unit_2_byte_int(raw_value)
                        elif raw_value.find('KB/sec'):
                            value = float(raw_value.rstrip('KB/sec').replace(',', ''))
                        elif title == DICT_TITLES['DATA_TRANSFER_TIME']:
                            value = float(raw_value.rstrip('KB/sec'))
                        sum_dict_value(DICT_TITLES, d_title, value)
                        DICT_TITLES[d_title][1].append(value)
    for d_title, key in DICT_TITLES.items():
        total = 0
        unit = ""
        for value in key[1]:
            if value.find(".") > -1:
                total += float(value)
            else:
                total += int(value)
        if key[0].find('bytes') > -1:
            tmp = total
            total, unit = humanize_byte(tmp)
        print("{title}: {total} {unit}".format(title=key[0], total=total, unit=unit))


if __name__ == '__main__':
    import sys
    file_name = sys.argv[1]
    main(file_name)