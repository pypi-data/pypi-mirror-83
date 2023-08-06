import logging
from os.path import join, abspath, dirname
import argparse


def main(args=None):
    # START args
    parser = argparse.ArgumentParser()
    parser.add_argument("api_home", help="The web address (URL) stating point (home) of the API")
    parser.add_argument("-r", "--requirements", help="Perform the Requirements tests", action="store_true")
    parser.add_argument("-as", "--abstracttests", help="Perform the Abstract Tests tests", action="store_true")
    # parser.add_argument("-c", "--recommendations", help="Perform the Recommendation tests", action="store_true")
    parser.add_argument("-a", "--alltests", help="Perform all tests", action="store_true")
    parser.add_argument("-l", "--log", help="How to log", choices=["screen", "file", "both"], default="screen")
    args = parser.parse_args()

    # END args

    # START logging
    if args.log == "file":
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s:\t%(levelname)-8s\t%(message)s",
            datefmt="%Y-%m-%d %H:%M",
            filename=join(abspath(dirname(__file__)), "testclient.log"),
            filemode="w"
        )
    elif args.log == "both":
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s:\t%(levelname)-8s\t%(message)s",
            datefmt="%Y-%m-%d %H:%M",
            filename=join(abspath(dirname(__file__)), "testclient.log"),
            filemode="w"
        )
        # set screen logging for levels > INFO
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter('%(asctime)s:\t%(levelname)-8s\t%(message)s'))
        logging.getLogger().addHandler(console)
    else:
        # set screen logging for levels > INFO
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s:\t%(levelname)-8s\t%(message)s",
        )
        console = logging.StreamHandler()
        logging.getLogger(__name__).addHandler(console)

    logging.info("OGC API LD Test Client started")
    logging.info("API Home is {}".format(args.api_home))
    # END logging

    results = []
    # START requirements tests
    if args.requirements or args.alltests:
        from tests.requirements_tests import main as req_main

        results.extend(req_main(args.api_home))
    # END requirements tests

    # # START abstract tests tests
    # if args.abstracttests or args.alltests:
    #     from tests.abstract_tests import *
    # # END abstract tests tests
    #
    # # START core tests
    # results = []
    # print("Testing core Requirements")
    # for i, test in enumerate(REQUIREMENTS["core"]):
    #     # parts = []
    #     # for k, v in test["parts"].items():
    #     #     parts.append("{}: {}".format(k, v))
    #     #
    #     # logging.info("Testing {} {}".format(test["name"], test["id"]))
    #     # for part in parts:
    #     #     logging.info("\t\t" + part)
    #
    #     print("Requirement {}".format(i))
    #
    #     test_function = "req_{}_test".format(str(i+1).zfill(2))
    #
    #     o = globals()[test_function](args.api_home)
    #     results.append({
    #         "id": test["id"],
    #         "outcome": o
    #     })
    #     logging.info("\t\t{}".format("PASS" if o[0] else "FAIL"))
    #
    #     if not o[0]:
    #         logging.info("Ending due to test failure")
    #         break
    # # END core tests
    #
    # logging.info("Aggregated results")
    # for res in results:
    #     logging.info("{}: {}".format(res["id"], res["outcome"]))

    for result in results:
        if result[1] == "FAIL":
            logging.info("Test for Requirement {}, {}.\nMessages:\n\t\t{}".format(
                result[0],
                result[1],
                "\n\t\t".join(result[2])))
        else:
            logging.info("Test for Requirement {}, {}".format(result[0], result[1]))


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])

    print("\n\ntesting complete")
