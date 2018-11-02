"""
Prepare data for practical exercises on text clustering
"""
import re
from os import listdir
import os
from collections import defaultdict
import pathlib
from nltk.tokenize import word_tokenize

max_number = 100

path_to_reuters_data = "./data/text_clustering/reuters21578"
output_dir = "./data/text_clustering/tem501"

pathlib.Path(output_dir).mkdir(exist_ok=True, parents=True)

filenames = listdir(path_to_reuters_data)
filenames = [f for f in filenames if re.search(r"\.sgm$", f)]

print("# Total files: {}".format(len(filenames)))

categories = {
    "acq", "coffee", "crude", "earn",  "grain",
    "interest", "money-fx", "ship", "trade", "sugar",
}


def get_topic(topics, categories):
    topics_ = [ topic for topic in topics if topic in categories ]
    if len(topics_) == 0 or len(topics_) == 2:
        return None
    return topics_[0]


def delete_files(folder):
    import shutil
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)


topic2doc = defaultdict(list)

for filename in filenames:
    filepath = os.path.join(path_to_reuters_data, filename)
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        has_topic = None
        topics = []
        doc_content = ""
        in_open_tag = False
        in_body_tag = False
        i = 0
        for line in f:
            i += 1
            line = line.strip()
            if line == "":
                continue
            m1 = re.search(r"^<REUTERS TOPICS=\"(.+?)\".+?>$", line)
            if m1:
                # print("line: {}".format(i))
                topic_attr = m1.group(1)
                if topic_attr == "NO":
                    has_topic = False
                else:
                    has_topic = True
                if in_open_tag:
                    print("ERROR: missing closing tag, line number: {}, line:{}, file: {}".format(i, line, filename))
                    in_open_tag = False
                    has_topic = None
                    doc_content = ""
                    topics = []
                in_open_tag = True
                continue

            if re.search(r"<TOPICS>.*</TOPICS>", line):
                rgx = re.compile(r"<D>(.+?)</D>")
                for m in rgx.finditer(line):
                    topic = m.group(1)
                    topics.append(topic)
                    continue
            import sys
            if re.search(r"</REUTERS>", line):
                topic = get_topic(topics, categories)
                if topic == "corn":
                    print("Found corn")
                    sys.exit()
                if not in_open_tag:
                    # print(in_open_tag)
                    print("ERROR: missing openning tag, line number: {}, line: {}, file: {}".format(i, line, filename))
                elif doc_content == "" or len(topics) == 0:
                    # print("IGNORE: empty doc content")
                    pass
                elif not has_topic:
                    # print("IGNORE: document w/o topic")
                    pass
                elif topic is None:
                    # print("IGNORE: document with topics that do not meet condition")
                    pass
                else:
                    # print(topic)
                    topic2doc[topic].append(doc_content)

                in_open_tag = False
                has_topic = None
                doc_content = ""
                in_open_tag = False
                topics = []
                continue

            m2 = re.search("<BODY>(.*)$", line)
            if m2:
                textline = m2.group(1)
                if in_body_tag:
                    print("ERROR: missing closing </BODY> tag")
                    doc_content = ""
                elif textline != "":
                    doc_content += textline + " "
                in_body_tag = True
                continue

            if re.search("</BODY></TEXT>", line):
                if not in_body_tag:
                    print("ERROR: missing openning <BODY> tag, line number: {}, line: {}, file: {}".format(i, line, filename))
                else:
                    in_body_tag = False
                continue

            if not re.search(r"^<.+?>", line) and line.lower() != "reuter" and in_body_tag:
                doc_content += line + " "
                continue

print(topic2doc.keys())
for topic in topic2doc.keys():
    print("{}: {}".format(topic, len(topic2doc[topic])))
    dir_path = os.path.join(output_dir, topic)
    pathlib.Path(dir_path).mkdir(exist_ok=True, parents=True)
    delete_files(dir_path)
    for i, doc in enumerate(topic2doc[topic], start=1):
        if i > max_number:
            break
        filepath = os.path.join(dir_path, "doc%s.txt" % i)
        doc_ = " ".join(word_tokenize(doc))
        with open(filepath, "w") as fo:
            fo.write(doc_)



















