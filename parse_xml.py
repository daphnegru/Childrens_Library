import os
import sys
import json
import matplotlib.pyplot as plt
import collections as cols


def main():
    input_file = os.path.abspath(os.path.realpath(sys.argv[1]))
    my_tags = os.path.abspath(os.path.realpath(sys.argv[2]))
    xml = os.path.abspath(os.path.realpath(sys.argv[3]))
    y = os.path.abspath(os.path.realpath(sys.argv[4]))
    records = parse_records(input_file)
    p = parse_xml(xml)
    tags = parse_my_tag(my_tags)
    to_add = add_my_tag(records, tags)
    good_struct = make_good_struct(p)
    years = parse_years(y)
    no_dup = remove_dups_in_years(years)
    decades = year_to_decade(no_dup)
    add_decade = add_decade_to_record(years, decades)
    added = add_to_hashmap(good_struct, add_decade, to_add)
    needed = print_only_needed(added)
    to_graph = stats(needed)
    create_graph(to_graph)


# this function creates the graphs from a given hashmap table
def create_graph(to_graph):
    plt.rcParams.update({'figure.max_open_warning': 0})
    for key, val in to_graph.items():
        name = "no_name.jpeg"
        plt.figure()
        x_axe = val.keys()
        y_axe = val.values()
        plt.title(key)
        # if the x labels overlap use the next line
        # plt.xticks(rotation=90)
        plt.bar(x_axe, y_axe, width=0.4)
        if len(key) > 1:
            name = key
            name = name + '.jpeg'
        plt.savefig(name)
        plt.cla()


# this function creates the final csv/json files that we use
# we create hashmap that counts how many entries there are from a specific category/decade
# this hashmap are later used to create the graphs
def stats(needed):
    decades_by_tags = {}
    tags_by_decades = {}
    for val in needed.values():
        d = val["decade: "]
        my_tags = val["Daphne's_tag:"]
        if d not in decades_by_tags.keys():
            decades_by_tags[d] = {}
        for i in range(len(my_tags)):
            tag = my_tags[i]
            if tag not in decades_by_tags[d].keys():
                decades_by_tags[d][tag] = 0
            decades_by_tags[d][tag] += 1
            if tag not in tags_by_decades.keys():
                tags_by_decades[tag] = {}
            if d not in tags_by_decades[tag].keys():
                tags_by_decades[tag][d] = 0
            tags_by_decades[tag][d] += 1

    od = cols.OrderedDict(sorted(tags_by_decades.items()))
    new_dict = json.dumps(od)
    temp = json.loads(new_dict)
    tags_by_decades = temp

    od = cols.OrderedDict(sorted(decades_by_tags.items()))
    new_dict = json.dumps(od)
    temp = json.loads(new_dict)
    decades_by_tags = temp

    for key, val in tags_by_decades.items():
        od = cols.OrderedDict(sorted(val.items()))
        new_dict = json.dumps(od)
        sorted_val = json.loads(new_dict)
        tags_by_decades[key] = sorted_val

    for key, val in decades_by_tags.items():
        od = cols.OrderedDict(sorted(val.items()))
        new_dict = json.dumps(od)
        sorted_val = json.loads(new_dict)
        decades_by_tags[key] = sorted_val

    # with open('tags_by_decades.csv', 'w', encoding='utf-16') as csvFile:
    #     for key in tags_by_decades.keys():
    #         csvFile.write("%s- %s\n" % (key, tags_by_decades[key]))
    #
    # with open('decades_by_tags.csv', 'w', encoding='utf-16') as csvFile:
    #     for key in decades_by_tags.keys():
    #         csvFile.write("%s- %s\n" % (key, decades_by_tags[key]))
    #
    # to_save_d = json.dumps(tags_by_decades, ensure_ascii=False, indent=2)
    # with open('tags_by_decades.json', 'w', encoding='utf-16') as jsonFile:
    #     jsonFile.write(to_save_d)
    #
    # to_save_mt = json.dumps(decades_by_tags, ensure_ascii=False, indent=2)
    # with open('decades_by_tags.json', 'w', encoding='utf-16') as jsonFile:
    #     jsonFile.write(to_save_mt)

    return tags_by_decades


# this function finds the first comma, the function part_tags uses it
def find_first_comma(s):
    ans = -1
    for i in range(len(s)):
        if s[i] == ",":
            ans = i
            break
    return ans


# this function parts the tags into an array
def part_tags(s):
    arr = []
    index_of_comma = find_first_comma(s)
    if index_of_comma > 0:
        s = s.split(", ")
        for i in range(len(s)):
            arr.append(s[i])
    elif len(s) > 0 and index_of_comma < 0:
        arr.append(s)
    return arr


# this function creates a hashmap that has the fields: recordID, decade, Daphne's tag
def print_only_needed(added):
    to_print = {}
    for key, val in added.items():
        needed = {"recordID: ": val["recordID: "], "Daphne's_tag:": val["Daphne's_tag:"], "decade: ": val["decade: "]}
        to_print[key] = needed

    # to_save = json.dumps(to_print, ensure_ascii=False, indent=2)
    # with open('onlyNeededForGraphs.json', 'w', encoding='utf-16') as jsonFile:
    #     jsonFile.write(to_save)

    return to_print


# this function maps a record to the decade it was published
def add_decade_to_record(years, decades):
    hashmap = {}
    d = "decade: "
    for key, val in years.items():
        year = val["year: "]
        decade = decades[year]
        val[d] = decade
        years[key] = val
        temp = {"recordID: ": val["recordID: "], d: decade}
        hashmap[key] = temp

        # to_save = json.dumps(hashmap, ensure_ascii=False, indent=2)
        # with open('decades.json', 'w', encoding='utf-16') as jsonFile:
        #     jsonFile.write(to_save)

    return years


# this function finds the record's year of publication
def find_year(s1):
    found = False
    s = s1.split("||")
    word = 0
    index = 0
    for i in range(len(s)):
        temp = s[i]
        for j in range(len(temp)):
            if temp[j] == '1':
                index = j
                word = i
                found = True
                break
            elif temp[j] == '2' and i != 0:
                index = j
                word = i
                found = True
                break
    if found:
        year = s[word][index: (index + 4)]
    else:
        for i in range(len(s)):
            temp = s[i]
            for j in range(len(temp)):
                if temp[j] == "\u05EA":
                    if j < (len(temp) - 1) and temp[j + 1] == "\u05E9":
                        index = j
                        word = i
                        found = True
                        break
        if found:
            year = s[word][index: (index + 4)]
        else:
            year = ""
    return year


# this function parses the years from a given file
def parse_years(years):
    hashmap = {}
    f = open(years, "r", encoding="utf8")
    index = 0
    for line in f:
        s = line.split(";")
        r = s[0].split(" ")
        if "\"" in r[2]:
            first_slash = r[2].rfind("\"")
            record = r[2][1:first_slash]
            year = find_year(s[1])
            val = {"recordID: ": record, "year: ": year}
            hashmap[index] = val
            index += 1

    return hashmap


# this function removes duplicates in years (the list of years)
def remove_dups_in_years(y):
    hashmap = []
    for value in y.values():
        year = value["year: "]
        if year not in hashmap:
            hashmap.append(year)

    return hashmap


# this function maps year of publication to decade
def year_to_decade(no_dup):
    hashmap = {}
    for i in range(len(no_dup)):
        decade = no_dup[i][0:3]
        decade = decade + "0"
        hashmap[no_dup[i]] = decade
    return hashmap


# this function parses the xml given
def parse_xml(xml):
    hashmap = {}
    r = 0
    f = open(xml, "r", encoding="utf8")
    val = {}
    index = 0
    seen = False
    null_or_empty = False
    for line in f:
        s = line.split(":")
        if index == 49:
            hashmap[r] = val
        if "recordID" in s[0]:
            index = 0
            temp = s[1].split(",")
            if "\"" in temp[0]:
                first = temp[0].index("\"")
                first += 1
                last = temp[0].index("\"", first)
                r = temp[0][first:last]
                record = "recordID: " + r
                r = record
                val = {}
                seen = False
            elif "null" in temp[0]:
                val = hashmap[r]
                seen = True
            index += 1

        elif index < 49:
            tag_name_len = s[0].rfind("\"")
            tag_name = s[0][1:tag_name_len]
            name = ""
            s1 = s[1]
            if "null" in s1:
                name = "null"
                null_or_empty = True
            elif "\"\"" in s1:
                name = ""
                null_or_empty = True
            else:
                if len(s) > 2:
                    j = 2
                    temp = s[1].split("\"")
                    name = name + temp[1]
                    for i in range(j, len(s)):
                        temp = s[i].split("\"")
                        name = name + temp[0]
                else:
                    temp = s1.split("\"")
                    name = temp[1]
                null_or_empty = False
            if not seen:
                val[tag_name] = name
            elif seen:
                if not null_or_empty:
                    old = val[tag_name]
                    if name not in old:
                        temp = old + ", " + name
                        val[tag_name] = temp
            index += 1
    return hashmap


# this function creates a hashmap with all the fields of the record
def make_good_struct(p):
    hashmap = {}
    index = 1
    for key, val in p.items():
        record_id = key.split(" ")
        record_id[0] = record_id[0] + " "
        record = {record_id[0]: record_id[1]}
        for k, v in val.items():
            record[k] = v
        hashmap[index] = record
        index += 1
    return hashmap


# this function finds the recordID
def find_id(record):
    for key, val in record.items():
        if "recordID" in key:
            return val


# this function finds the record's decade from the hashmap
def find_decade_in_hashmap(record_id, d):
    for val in d.values():
        if val["recordID: "] == record_id:
            return val["decade: "]


# this functions added to the parsed hashmap of the xml the fields: Daphne's record, decade
def add_to_hashmap(p, d, to_add):
    title = "Daphne's_tag:"
    for key, val in p.items():
        record_id = find_id(val)
        new_tag = to_add[record_id]
        decade = find_decade_in_hashmap(record_id, d)
        val[title] = new_tag
        val["decade: "] = decade
        p[key] = val

    # to_save = json.dumps(p, ensure_ascii=False, indent=2)
    # with open('afterAdding.json', 'w', encoding='utf-16') as jsonFile:
    #     jsonFile.write(to_save)

    return p


# this function parses the tags from a given file
def parse_my_tag(my_tags):
    t = open(my_tags, "r", encoding="utf16")
    hashmap = {}
    for line in t:
        s1 = line.split("\t")
        if "tags" not in s1[0]:
            old = s1[0].replace("\"", "")
            hashmap[old] = s1[1].strip("\n")

    return hashmap


# this function creates the array of added tags
def add_my_tag(records, tags):
    hashmap = {}
    for key, value in records.items():
        record = key
        hashmap[record] = []
        for i in range(len(value)):
            my_tag = tags[value[i]]
            if my_tag not in hashmap[record]:
                hashmap[record].append(my_tag)
    return hashmap


# this function parses the records from the input file
def parse_records(input_file):
    f = open(input_file, "r", encoding="utf8")
    hashmap = {}
    record = 0
    for line in f:
        tags = []
        s = line.split(",")
        for i in range(len(s)):
            r = s[i].split(":")
            if "recordID" in r[0]:
                if r[1] is not None:
                    if "\"" in r[1]:
                        first = r[1].index("\"")
                        first += 1
                        last = r[1].index("\"", first)
                        temp = r[1]
                        record = temp[first:last]
            elif "tag" in r[0]:
                if "\"" in r[1]:
                    temp = r[1].split("}")
                    first = temp[0].index("\"")
                    if first > -1:
                        first += 1
                        last = temp[0].rfind("\"")
                        t = temp[0][first:last]
                        if len(t) > 0:
                            c = t[0]
                            if "\u0590" <= c <= "\u05EA":
                                tags.append(t)

        keys = hashmap.keys()
        if record not in keys:
            hashmap[record] = tags
        else:
            temp = hashmap.get(record)
            for i in range(len(tags)):
                temp.append(tags[i])
            hashmap[record] = temp

    return hashmap


if __name__ == '__main__':
    main()
