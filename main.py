# In the name of God
# Omid


from pack import config_finder_constructor, make_requierd_dir
from pack import interface
from pack import logger_constructor
from pack import make_first_table
from pack import make_domains_table
from pack import make_all_links_table
from pack import delete_first_table


logger = logger_constructor(__name__)
config = config_finder_constructor('adjust.conf')


def main():
    make_requierd_dir("", config["Application"]["main_data_dir"])
    make_requierd_dir("", config["Application"]["input_dir"])
    make_requierd_dir("", config["Application"]["output_dir"])
    logger.info("--- START POINT ---")
    
    select = interface()

    if select == 1:
        df_first = make_first_table()
        df_domains = make_domains_table()
        make_all_links_table(df_first, df_domains)

    elif select == 2:
        delete_first_table()
    elif select == 6:
        print("Bye!!!")


if __name__ == "__main__":
    main()
