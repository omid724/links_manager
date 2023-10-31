# In the name of God
# Omid

import os
import re
import csv
import json
import logging
import urllib.parse
from configparser import ConfigParser

import requests
import pandas as pd


def config_finder_constructor(path):
    config_file = path
    config1 = ConfigParser()

    config1.read(config_file)

    return config1


config = config_finder_constructor("adjust.conf")


def make_requierd_dir(path, folder):
    requierd_dir = os.path.join(path, folder)
    if not os.path.isdir(requierd_dir):
        os.mkdir(requierd_dir)


make_requierd_dir("", config["Logging"]["log_dir"])


def logger_constructor(name_of_module):
    logger1 = logging.getLogger(name_of_module)
    logger1.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")

    log_file_path = os.path.join(
        config["Logging"]["log_dir"], config["Logging"]["log_file"]
    )
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger1.addHandler(file_handler)

    return logger1


logger = logger_constructor(__name__)


def find_is_standard_url(url):
    pure_d = find_domain(url)
    return find_is_standard_pure_domain(pure_d)


def remove_last_forward_slash(url):
    if url[-1] == "/":
        url = url[:-1]
    return url


def add_record_csv_file(information):
    with open("archive/neat_links.csv", mode="a") as urls_info_file:
        fieldnames = ["address", "title", "group", "tags", "stars"]
        url_info_writer = csv.DictWriter(urls_info_file, fieldnames=fieldnames)

        url_info_writer.writerow(information)


def contain_random_string(s):
    c = len(re.findall(r"\d[a-zA-Z]", s))
    c += len(re.findall(r"[a-zA-Z]\d", s))
    result = True if c > 3 else False
    return result


def get_all_exist_record():
    with open("archive/neat_links.csv", mode="r") as csv_file:
        urls_info = csv.DictReader(csv_file, delimiter=",")
        urls_info = list(urls_info)

    return urls_info


def bookmark_url(url):
    title = titleBug5(url)
    print("Computer find this title:", title)
    answer = input("Do you accept this? [Y]es or [N]o: ")
    if not (answer == "y" or answer == "Y"):
        title = input("Please enter a title: ")
    with open("name_of_groups.json", "r") as f:
        text = f.read()
        print(text)
        groups = json.loads(text)

    group_number = input("Which group is this link: ")
    group = groups[group_number]
    print("Please enter tags split them with 'ENTER' -empty for break:\n")
    tags = []
    while True:
        tag = input()
        if tag != "":
            tags.append(tag)
        else:
            break

    tags_str = ""
    c = 0
    for tag in tags:
        tags_str += "_t_" + tag
        c += 1

    stars = input("How many stars do you give the link? [between 0-5]: ")
    stars = int(stars)

    info = {
        "address": url + " ",
        "title": title,
        "group": group,
        "tags": tags_str,
        "stars": stars,
    }

    add_record_csv_file(info)


def get_files_name_in_links_folder():
    input_links_path = config["Application"]["input_dir"]
    filenames_in_links_folder = os.listdir(input_links_path)

    return filenames_in_links_folder


def clear():
    """Clear the screen"""
    logger.info("Screen cleaned")
    os.system("cls" if os.name == "nt" else "clear")


def add_to_deactivate_list(url):
    with open("deactive_urls.txt", "a") as f:
        f.write(url + "\n")


def links_detector(file_path):
    """pass the function a file name,
    then you can have your all link in that file"""

    with open(file_path, "r", encoding="utf-8") as file5:
        total_file = file5.read()

    # https://gist.github.com/gruber/8891611
    regex_variable = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""

    links = re.findall(regex_variable, total_file)

    return links


def links_detector_from_scv(file_path):
    logger.info("a csv file now scaning")

    df = pd.read_csv(file_path)
    l = []
    d = df.to_dict()

    for item in d:
        column1 = d[item]
        for key in column1:
            filed = column1[key]
            if isinstance(filed, str):
                l.append(filed)

    total_file = "\n".join(l)

    # https://gist.github.com/gruber/8891611
    regex_variable = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""

    links = re.findall(regex_variable, total_file)

    return links


def get_all_urls_from_input_links_folder():
    all_url_exist_in_links_folder = []
    file_names = get_files_name_in_links_folder()
    input_links_path = os.path.relpath(config["Application"]["input_dir"])

    # TODO - if our file is csv file should have another approach
    for file_name in file_names:
        if len(file_name) >= 5 and file_name[-4:] == ".csv":
            all_url_exist_in_links_folder += links_detector_from_scv(
                os.path.join(input_links_path, file_name)
            )
        else:
            all_url_exist_in_links_folder += links_detector(
                os.path.join(input_links_path, file_name)
            )

    # Also add previous find links if exist file
    first_table_find_urls = os.path.join(
        config["Application"]["input_dir"], config["Application"]["first_table"]
    )
    if os.path.isfile(first_table_find_urls):
        df = pd.read_csv(first_table_find_urls, index_col="Unnamed: 0")
        all_url_exist_in_links_folder += list(df.iloc[:, 0])

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

    if url[-1] == "/":
        url_p = url[:-1]
        l2.append(url_p)
        append_other_write(url_p)
    else:
        url_p = url + "/"
        l2.append(url_p)
        append_other_write(url_p)

    return l2


def get_url_is_done(url):
    known_urls = []
    for item in ["neat_links.csv", "deactive_urls.txt"]:
        known_urls += links_detector(item)

    url_is_done = False
    for url_p in get_other_shape(url):
        if url_p in known_urls:
            url_is_done = True
            break
    return url_is_done


def url_homework(url):
    clear()
    if not len(re.findall(r"/", url)):
        url = url + "/"
    print(url)
    answer = input("Do you may need this link? [Y]es or [N]o? ")
    if answer == "y" or answer == "Y":
        answer = input("Do you want to open the link? [Y]es or [N]o? ")
        if answer == "y" or answer == "Y":
            # webbrowser.open(url, new=0, autoraise=True)
            os.system(f"firefox --safe-mode --new-tab {url}")
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
        root_url = re.findall(r"^.+?\..+?/", url)[0]
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
    if len(re.findall(r"[^a-zA-Z0-9.-]", x)):
        result = False
    else:
        result = (
            False
            if x[0] == "."
            or x[-1] == "."
            or x.find("..") >= 0
            or x[0] == "-"
            or x[-1] == "-"
            or x.find("--") >= 0
            or len(x) == 0
            or x.find(".") < 0
            else True
        )
    return result


def split_protocol_part_of_url(url):
    splited_with_double_qute_url = url.split(":")
    number_of_parts = len(splited_with_double_qute_url)
    assert number_of_parts <= 2, f"Not a normal link passed. url: {url}"

    protocol_part = splited_with_double_qute_url[0] if number_of_parts == 2 else ""
    url_without_protocol = (
        splited_with_double_qute_url[1] if number_of_parts == 2 else url
    )
    url_without_protocol = (
        url_without_protocol[2:]
        if "//" == url_without_protocol[:2]
        else url_without_protocol
    )

    return protocol_part, url_without_protocol


def find_domain(url):
    url = url.lower()
    # input shape: https://tarh.ir/golha/ ---> output shape: https://tarh.ir/
    res_url = re.findall(r"^.+?\..+?/", url)
    res_url = res_url[0] if len(res_url) else url

    return res_url


def find_pure_url(url):
    url = url.lower()
    # input shape: https://tarh.ir/golha/ ---> output shape: tarh.ir
    res_url = re.findall(r"^.+?\..+?/", url)
    res_url = res_url[0] if len(res_url) else url
    protocol_part, res_url = split_protocol_part_of_url(res_url)

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
    domain = find_domain(url)
    domain_place = url_copy.find(domain)
    if domain_place >= 0:
        tail_place = domain_place + len(domain)
        res_url = url[:tail_place].lower() + url[tail_place:]

    return res_url


def make_first_table():
    output = config["Application"]["first_table"]
    output = os.path.join(config["Application"]["output_dir"], output)
    urls = get_all_urls_from_input_links_folder()

    df = pd.DataFrame()
    df["URL"] = urls

    df["URL"] = df["URL"].apply(make_lower_case_protocol_and_domain_part)
    df["URL"] = df["URL"].apply(remove_last_forward_slash)

    filt = df.duplicated()
    df.drop(index=df[filt].index, inplace=True)

    df.insert(loc=1, column="protocol_part", value="NA")
    df.insert(loc=2, column="URL_without_protocol_part", value="NA")
    for index, row in df.iterrows():
        try:
            protocol_part, url_without_protocol_part = split_protocol_part_of_url(
                row["URL"]
            )
        except Exception as e:
            logger.error(f"Error: {str(e)}\nURL: {row['URL']}")
        else:
            df.loc[index, "protocol_part"] = protocol_part
            df.loc[index, "URL_without_protocol_part"] = url_without_protocol_part

    df.sort_values(by="URL_without_protocol_part", ascending=True, inplace=True)
    df.reset_index(inplace=True)
    df.drop(columns="index", inplace=True)

    df.to_csv(output)

    return df


def make_domains_table():
    source_table = config["Application"]["first_table"]
    source_table = os.path.join(config["Application"]["output_dir"], source_table)
    output_table = config["Application"]["domains_table"]
    output_table = os.path.join(config["Application"]["output_dir"], output_table)

    if os.path.isfile(source_table):
        df = pd.read_csv(source_table, index_col="Unnamed: 0")
        # just use main column ("URL" column)
        df = pd.DataFrame(df.iloc[:, 0])

        df.insert(loc=1, column="protocol_part", value="NA")
        df.insert(loc=2, column="URL_without_protocol_part", value="NA")

        df["URL"] = df["URL"].apply(find_domain)

        for index, row in df.iterrows():
            protocol_part, pure_domain = split_protocol_part_of_url(row["URL"])
            df.loc[index, "protocol_part"] = protocol_part
            df.loc[index, "URL_without_protocol_part"] = pure_domain

        df["URL"] = df["URL"].apply(remove_last_forward_slash)
        df["URL_without_protocol_part"] = df["URL_without_protocol_part"].apply(
            remove_last_forward_slash
        )

        filt = df.duplicated()
        df.drop(index=df[filt].index, inplace=True)

        filt = df["URL_without_protocol_part"].apply(find_is_standard_pure_domain)
        df.drop(index=df[~filt].index, inplace=True)

        filt = df["URL_without_protocol_part"].apply(contain_random_string)
        df.drop(index=df[filt].index, inplace=True)

        filt = df["URL_without_protocol_part"].apply(lambda x: len(x) > 60)
        df.drop(index=df[filt].index, inplace=True)

        df.sort_values(by="URL_without_protocol_part", ascending=True, inplace=True)
        df.reset_index(inplace=True)
        df.drop(columns="index", inplace=True)

        df.to_csv(output_table)

        return df


def make_all_links_table(df_first, df_domains):
    # Arguments are two pandas dataframe that should bind to each other - df_first and df_domains

    output = config["Application"]["all_urls_table"]
    output = os.path.join(config["Application"]["output_dir"], output)

    df = pd.concat([df_first, df_domains])

    df.reset_index(inplace=True)
    df.drop(columns="index", inplace=True)

    filt = df.duplicated()
    df.drop(index=df[filt].index, inplace=True)
    df.sort_values(by="URL_without_protocol_part", ascending=True, inplace=True)

    df.reset_index(inplace=True)
    df.drop(columns="index", inplace=True)

    df.to_csv(output)


def ask_clint_yes_or_no(question):
    answer = ""
    while not ((answer in "yn") and (len(answer) == 1)):
        answer = input(question).lower()

    answer = True if answer == "y" else False

    return answer


def delete_first_table():
    first_table = config["Application"]["first_table"]
    first_table_path = os.path.join(config["Application"]["output_dir"], first_table)

    if os.path.isfile(first_table_path):
        ans = ask_clint_yes_or_no(
            "Are you sure to delete first table -previously find links? "
        )
        if ans:
            os.remove(first_table_path)
        print("First table file deleted")

    else:
        print("First table file doesn't exist")


# TODO --- make it complete
def find_urls_all_need_context(link):
    """pass the function a link to find its title for you"""

    headers = {}
    data = {}

    # headers = {

    #    "Host": "www.dideo.ir",
    #    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    #    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    #    "Accept-Language": "en-US,en;q=0.5",
    #    "Accept-Encoding": "gzip, deflate, br",
    #    "Referer": "https://www.dideo.ir/ch/yt/UC_Oao2FYkLAUlUVkBfze4jg/mining-massive-datasets",
    #    "Upgrade-Insecure-Requests": "1",
    #    "Connection": "keep-alive",
    #    "Cookie": "ch=eyJpdiI6Ikt4TWhFWGFSQ3RtUEFpTHp4UUZPRFE9PSIsInZhbHVlIjoiRlRtUWYwQmQ3emtIbzA3WXQ4eVVJUT09IiwibWFjIjoiMGI0ZWY4MjdkZDFjZWZlMDA0MmUyNTAyOWNiYWM2MGQyMGJkYTM0NjU1NmE2OWRjNDZjYWU4ZTc3NjIxNDI1ZSJ9; hm=eyJpdiI6Ilo4aGpcLzNYYWg1c2ZvbFVJQjZXbnh3PT0iLCJ2YWx1ZSI6IjU2a1VQNzA4Y0hCRHYzWHNpcEM4dWc9PSIsIm1hYyI6IjRkZTMzNmMzZTMyODQ4NGI2MDhjYmU2NjYyMmQ5NDZiMWQwM2U5YzdmMzNkNzNlNDY0ZjQ5NmVmZTE3YWI5YzEifQ%3D%3D; _hjid=01ceff05-ab8e-471a-b556-8b10cd74caa9; _ga=GA1.2.1301730268.1622740778; can-ide=1; _ga_WNXH6FY3JQ=GS1.1.1622740885.1.0.1622740889.0; re-au=0; XSRF-TOKEN=eyJpdiI6IjNvckc5XC9BaHZmTXBxV3hOaWljazJ3PT0iLCJ2YWx1ZSI6Imc5R0NXN1NEb2NIY0xvSkhDNTdxblV4SjRuTWhDZ01NYnlPc0dzZHZJa25HeWdFeFIyTjNCMUFTYko3bXVqSkIiLCJtYWMiOiI4MzJhZjgwYTRhNDc5MzA3YThkMjBhZGU5NzNhNjkxNTZlZWI2NzlhMzYyNDkyZmQ5ODdjMDk2MGQ0N2YyNGU2In0%3D; kraken_session=eyJpdiI6Ijl0S1RXTUlTdG84d3J2UHEyOWFwZnc9PSIsInZhbHVlIjoiN3hEZ3VVNlJMNDZTY0xlK2dYNm9CSHU5RkFpNmRLR3BZXC8rTzVTQmIrWUsrY20zcUF0amhQelNrWXNOYkJnajUiLCJtYWMiOiI0MzFjNmU5Zjk1OWJiYzJkYmJiYmRmNzRiZDVhYTRkNGYzODhjMjJlMmY3M2Q5NWY2NTA2MTI1ZjJhZGVlMmVkIn0%3D; vQnnFCkmZZHEodWa0yAOIu6jaf9fwfTMNLeSEFQ4=eyJpdiI6ImxZTUxPYklBU3ZJWHNLcVFsSFZjd1E9PSIsInZhbHVlIjoiaStzeWZ4K1BBKytZT3Arb1ZEam51V0VTVGs5S1wvN1ZzZkxySUZ3OVV2N09Eb2NsRDVtRUZ6b2FlSTU1RFF6RzBkMkNqOXFzNlFSR3BUMzhKRTRrYzE2QmV6QmwzUmpvREMyWkpSQ2NLbEJwWktuQ3hheCtlaXAzWGw1NDBBUDFtZUg1SlNjRVwveGFlbzBhVXRTTEFycXJ6eGNrVktiblJ0eDI1c1hYNG1YdVVmTlJvbWoxWktRMDY5U3pRVjhyenNIbk1HWlFPZXkrTHJtR2lKZE5hZHcyc1pLU214dUxlampnaUdpUm9cL1Nxem1xTUs2VmI2RW9qSk05czVPdXpvdFppSUkyc0RJa2ZRQnljXC9YdmhldEhzaHlwMEltUlc3UEZ6ZlBzM1ZDbzVNQm9XRFQ2dXBaNXNRdGlGQ3hFZEtcL0hVUTk4WGl2b3hDb3RUTlQyZG1adW03d1Q5WHZiTlNkNmN2bUtKUER2Ylh1cExYYjZLa2tSVHZ1Q2JNTllsYStOZG54OGc2ME1Ub1dOQmxhTnpDWjdNVU5RWURNanZyNHpvNU5mbHdUbkhmRXEwaGFUM1JLTDFVcnpST0NPNncrQ2xUR1pDSDFuQXBuaXVBaGVhUit0VTRiMmU0eXg0V1BJOUNQeWVTNHNWVWg2c2p0QTF0OFdDT0k5MWNOV283ZG9JY3c4a1h6T2xoaVY3ajlMQ1VyQXR0U3RwVFwvMUoxd051SHJwbXJYS2RrPSIsIm1hYyI6IjFkOTc2MzFkMDc0NGUyYzkzODliMmQ1YTlhMzkzN2QzZjljYTk4NTY0NTE0YjZkMTkxOWIzMDAxNmFjNzA0MDAifQ%3D%3D; _hjTLDTest=1; _hjAbsoluteSessionInProgress=1; _gid=GA1.2.752561178.1624001582; XSRF-TOKEN=eyJpdiI6Imk0NndVTEhVSUk4N2M1VjVnNW5BdlE9PSIsInZhbHVlIjoiMDBGNXk3d0JxWnpVNElBYVBNcDlyeU12dFBxK2c0bjh2Zk5RRjVhUitIY1ZMR2psQThEcnVvUTZiTGJJT1NUc1VvWElEQVFZT2M5S3YwckFZQytiNWc9PSIsIm1hYyI6ImU4NGMyNWE5YjQyNmJhYjZlZDQ2NTMyZmQxMGRlN2Q0NTdmODE4YTdhODJhMmEzYzZkNGU0ZGQ2Yjk3ZjdhMjgifQ%3D%3D; client-id=eyJpdiI6ImVZdzVtZ1hrRmhQeGRQRUFSZUE1dUE9PSIsInZhbHVlIjoiaG9EMXhaS3VNYU9Pc1dHdVlHSTBnQT09IiwibWFjIjoiNjEzZWU1MmQ1YzAyZDdiMDE0YWMzNzY5YzllNTE5NzJkNTNlZDRiZDQ1MzUwZWE0NjJmNDhiZGYyNWM3NDZhNCJ9; _gat_UA-82218710-1=1"
    #    }
    try:
        total_page = requests.get(link, headers=headers, timeout=7)

    except requests.exceptions.MissingSchema as e:
        logger.info(f"Couldn't find title for the link {link}\nthe error was {str(e)}")
        total_text = ""

    except requests.exceptions.ConnectionError as e:
        logger.info(f"Couldn't find title for the link {link}\nthe error was {str(e)}")
        total_text = ""

    else:
        total_text = total_page.text

    total_page = re.sub(r"\n", "", total_text)

    title = re.findall(r"title>(.+?)</title", total_page)
    try:
        title = title[0].strip()
    except IndexError:
        print("Title didn't find.")
        title = "---"
        # answer = input('Do you want try find title from url if it has unicode? [Y/N]? ')
        answer = "y"
        if answer == "y" or answer == "Y":
            title = urllib.parse.unquote(link, encoding="utf-8", errors="replace")

    return title
