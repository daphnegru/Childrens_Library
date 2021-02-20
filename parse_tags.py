import os
import sys


def main():
    input_file = os.path.abspath(os.path.realpath(sys.argv[1]))
    parse_tags(input_file)


# this function parses the tags from the input file
def parse_tags(input_file):
    f = open(input_file, "r", encoding="utf8")
    hashmap = {}
    index = 0
    for line in f:
        tags = []
        s = line.split(",")
        for i in range(len(s)):
            r = s[i].split(":")
            if "tag" in r[0]:
                if "\"" in r[1]:
                    first = r[1].index("\"")
                    if first > -1:
                        first += 1
                        last = r[1].rfind("\"")
                        t = r[1][first:last]
                        if len(t) > 0:
                            c = t[0]
                            if "\u0590" <= c <= "\u05EA":
                                t.replace("\"", "")
                                tags.append(t)

        for i in range(len(tags)):
            if tags[i] not in hashmap.values():
                hashmap[index] = tags[i]
                index += 1

    with open('hebTags.csv', 'w', encoding='utf-16') as csvFile:
        for key in hashmap.keys():
            csvFile.write("%s\n" % (hashmap[key]))


if __name__ == '__main__':
    main()
