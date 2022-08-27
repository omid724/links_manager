# In the name of God
# Omid

import csv
import json
import logging
import os
import re
import subprocess
from configparser import ConfigParser

import pandas as pd
# import webbrowser

from title_finder import titleBug5


protocol_part_of_an_url = ['https://www.', 'https://', 'http://www.', 'http://', "www."]


def config_finder_constructor(path):
    config_file = path
    config1 = ConfigParser()

    config1.read(config_file)

    return config1


config = config_finder_constructor('adjust.conf')


def logger_constructor(name_of_module):
    logger1 = logging.getLogger(name_of_module)
    logger1.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

    file_handler = logging.FileHandler(config['Logging']['log_file'])
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger1.addHandler(file_handler)

    return logger1


logger = logger_constructor(__name__)


def find_is_standard_url(url):
    pure_d = find_pure_url(url)
    return find_is_standard_pure_domain(pure_d)


def remove_last_forward_slash(url):
    if url[-1] == "/":
        url = url[:-1]
    return url


def add_record_csv_file(information):
    with open("archive/neat_links.csv", mode="a") as urls_info_file:
        fieldnames = ['address', 'title', 'group', 'tags', 'stars']
        url_info_writer = csv.DictWriter(urls_info_file, fieldnames=fieldnames)

        url_info_writer.writerow(information)


def contain_random_string(s):
    c = len(re.findall(r'\d[a-zA-Z]', s))
    c += len(re.findall(r'[a-zA-Z]\d', s))
    result = True if c > 3 else False
    return result


def get_all_exist_record():
    with open("archive/neat_links.csv", mode="r") as csv_file:
        urls_info = csv.DictReader(csv_file, delimiter=',')
        urls_info = list(urls_info)

    return urls_info


def bookmark_url(url):

    title = titleBug5(url)
    print("Computer find this title:", title)
    answer = input("Do you accept this? [Y]es or [N]o: ")
    if not (answer == "y" or answer == "Y"):
        title = input("Please enter a title: ")
    with open('name_of_groups.json', 'r') as f:
        text = f.read()
        print(text)
        groups = json.loads(text)

    group_number = input("Which group is this link: ")
    group = groups[group_number]
    print("Please enter tags split them with 'ENTER' -empty for break:\n")
    tags = []
    while True:
        tag = input()
        if tag != '':
            tags.append(tag)
        else:
            break
            
    tags_str = ''
    c = 0
    for tag in tags:
            
        tags_str += "_t_" + tag
        c += 1

    stars = input("How many stars do you give the link? [between 0-5]: ")
    stars = int(stars)

    info = {
        'address': url + " ",
        'title': title,
        'group': group,
        'tags': tags_str,
        'stars': stars
    }

    add_record_csv_file(info)


def get_files_name_in_links_folder():
    input_links_path = config["Application"]["input_links_path"]
    p1 = subprocess.run(['ls', input_links_path], capture_output=True, text=True, check=True)
    filenames_in_links_folder = p1.stdout
    filenames_in_links_folder = filenames_in_links_folder.split(sep='\n')
    return filenames_in_links_folder[:-1]


def clear():
    """ Clear the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def add_to_deactivate_list(url):
    with open('deactive_urls.txt', 'a') as f:
        f.write(url + "\n")


def links_detector(file_path):
    """pass the function a file name,
    then you can have your all link in that file"""

    with open(file_path, 'r') as file5:
        total_file = file5.read()

    # https://gist.github.com/gruber/8891611
    regex_variable = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""

    links = re.findall(regex_variable, total_file)

    return links


def get_all_urls_from_input_links_folder():
    all_url_exist_in_links_folder = []
    file_names = get_files_name_in_links_folder()

    for file_name in file_names:
        all_url_exist_in_links_folder += links_detector('Data/busy_files_links/' + file_name)

    # Also add previous find links if exist file
    first_table_find_urls = config["Application"]["first_table"]
    if os.path.isfile(first_table_find_urls):
        all_url_exist_in_links_folder += links_detector(first_table_find_urls)

    # Remove duplicates in list
    all_url_exist_in_links_folder = list(set(all_url_exist_in_links_folder))

    return all_url_exist_in_links_folder


def get_other_shape(url):
    l1 = protocol_part_of_an_url
    l2 = [url]

    def append_other_write(u):
        for this in l1:
            if this in u:
                l2.append(u.replace(this, ""))
            else:
                l2.append(this + url)

    append_other_write(url)

    if url[-1] == '/':
        url_p = (url[:-1])
        l2.append(url_p)
        append_other_write(url_p)
    else:
        url_p = (url + '/')
        l2.append(url_p)
        append_other_write(url_p)

    return l2


def get_url_is_done(url):
    known_urls = []
    for item in ['neat_links.csv', 'deactive_urls.txt']:
        known_urls += links_detector(item)

    url_is_done = False
    for url_p in get_other_shape(url):
        if url_p in known_urls:
            url_is_done = True
            break
    return url_is_done


def url_homework(url):
    clear()
    if not len(re.findall(r'/', url)):
        url = url + "/"
    print(url)
    answer = input("Do you may need this link? [Y]es or [N]o? ")
    if answer == "y" or answer == "Y":
        answer = input("Do you want to open the link? [Y]es or [N]o? ")
        if answer == "y" or answer == "Y":
            # webbrowser.open(url, new=0, autoraise=True)
            os.system(f'firefox --safe-mode --new-tab {url}')
        answer = input("Do you want to bookmark this? [Y]es or [N]o? ")
        if answer == "y" or answer == "Y":
            print("***bookmark***")
            bookmark_url(url)
        else:
            print("***Add to deactivate list***")
            add_to_deactivate_list(url)

    else:
        print("***Add to deactivate list***")
        add_to_deactivate_list(url)


def link_lib_bug():
    urls = get_all_urls_from_input_links_folder()

    for url in urls:
        root_url = re.findall(r'^.+?\..+?/', url)[0]
        is_root = url == root_url

        url_is_done = get_url_is_done(url)

        if not url_is_done:
            url_homework(url)
            answer = input("Continue? [Y]es or [N]o? ")
            if not (answer == "y" or answer == "Y"):
                break

        if not is_root and not get_url_is_done(root_url):
            url_homework(root_url)
            answer = input("Continue? [Y]es or [N]o? ")
            if not (answer == "y" or answer == "Y"):
                break


def find_is_standard_pure_domain(x):
    if len(re.findall(r'[^a-zA-Z0-9.-]', x)):
        result = False
    else:
        result = False if x[0] == "." or x[-1] == "." or x.find("..") >= 0 or \
                          x[0] == "-" or x[-1] == "-" or x.find("--") >= 0 or \
                          len(x) == 0 or x.find(".") < 0 else True
    return result


def remove_protocol_part_of_url(url):
    url_copy, res_url = url.lower(), url
    for item in protocol_part_of_an_url:
        if url_copy.find(item) == 0:
            res_url = url[len(item):]
            break

    protocol_part = url.split(res_url)[0]

    return protocol_part, res_url


def find_pure_url(url):
    url = url.lower()
    # input shape: https://tarh.ir/golha/ ---> output shape: tarh.ir
    res_url = re.findall(r'^.+?\..+?/', url)
    res_url = res_url[0] if len(res_url) else url
    protocol_part, res_url = remove_protocol_part_of_url(res_url)

    return protocol_part, res_url


def interface():
    clear()

    with open("interface_menu.txt", "r") as f:
        interface_menu = f.readlines()

    for item in interface_menu:
        print(item, end="")

    select = int(input("Enter a number: "))

    return select


def make_lower_case_protocol_and_domain_part(url):
    url_copy, res_url = url.lower(), url
    domain = find_pure_url(url)
    domain_place = url_copy.find(domain)
    if domain_place >= 0:
        tail_place = domain_place + len(domain)
        res_url = url[:tail_place].lower() + url[tail_place:]

    return res_url


def make_first_table():
    output = config["Application"]["first_table"]
    urls = get_all_urls_from_input_links_folder()

    df = pd.DataFrame()
    df["URL"] = urls

    df["URL"] = df["URL"].apply(make_lower_case_protocol_and_domain_part)
    # df["URL"] = df["URL"].apply(remove_protocol_part_of_url)
    df["URL"] = df["URL"].apply(remove_last_forward_slash)
    df["URL"] = df["URL"].apply(lambda x: find_is_standard_url(remove_protocol_part_of_url(find_pure_url(x))))

    filt = df.duplicated()
    df.drop(index=df[filt].index, inplace=True)

    df.sort_values(by="URL", ascending=True, inplace=True)
    df.reset_index(inplace=True)
    df.drop(columns="index", inplace=True)

    df.to_csv(output)

    return df


# TODO change the name of this func to "make main domain address table"
def make_pure_url_table():
    output = config["Application"]["pure_domain_table"]

    source_table = config["Application"]["first_table"]
    if os.path.isfile(source_table):
        df = pd.read_csv(source_table, index_col="Unnamed: 0")
        # TODO - iterrate on urls and make two columns for save both protocol part and pure domain
        df["URL"] = df["URL"].apply(find_pure_url)

        filt = df.duplicated()
        df.drop(index=df[filt].index, inplace=True)

        filt = df["URL"].apply(find_is_standard_pure_domain)
        df.drop(index=df[~filt].index, inplace=True)

        filt = df["URL"].apply(contain_random_string)
        df.drop(index=df[filt].index, inplace=True)

        filt = df["URL"].apply(lambda x: len(x) > 60)
        df.drop(index=df[filt].index, inplace=True)

        df.sort_values(by="URL", ascending=True, inplace=True)
        df.reset_index(inplace=True)
        df.drop(columns="index", inplace=True)

        df.to_csv(output)

        return df


def find_urls_title():
    pass


def ask_clint_yes_or_no(question):
    answer = ""
    while not ((answer in "yn") and (len(answer) == 1)):
        answer = input(question).lower()

    answer = True if answer == "y" else False

    return answer


def delete_first_table():
    first_table = config["Application"]["first_table"]

    if os.path.isfile(first_table):
        ans = ask_clint_yes_or_no("Are you sure to delete first table -previously find links? ")
        if ans:
            os.remove(first_table)
        print("First table file deleted")

    else:
        print("First table file doesn't exist")
