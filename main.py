# In the name of God
# Omid

from pack import config_finder_constructor
from pack import interface
from pack import logger_constructor
from pack import store_all_links
from pack import make_pure_url_table
from pack import delete_first_table

logger = logger_constructor(__name__)
config = config_finder_constructor('adjust.conf')


def main():
    select = interface()

    if select == 1:
        store_all_links()
        make_pure_url_table()
    elif select == 2:
        delete_first_table()


if __name__ == "__main__":
    main()
