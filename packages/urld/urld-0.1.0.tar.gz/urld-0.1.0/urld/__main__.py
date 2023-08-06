import argparse
from typing import Iterator, Any, Optional
import logging
import sys
from urllib.parse import urlparse, ParseResult, parse_qs
import os

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Descompose URL in parts.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
        "$ echo 'https://domain.com/index.html?a=b' | urlp\n"
        "https domain.com /index.html a=b\n"
        "\n"
        "$ echo 'https://domain.com/index.html?a=b' | urlp -f protocol host\n"
        "https domain.com\n"
        "\n"
        "$ echo 'https://domain.com/index.html?foo=bar' | urlp -p foo\n"
        "bar"
    )

    parser.add_argument(
        "url",
        help="Url to search in wayback machine. It can include wildcards.",
        nargs="*",
    )

    field_choices = [
        "scheme", "protocol", "proto",
        "netloc",
        "host", "hostname", "domain",
        "port",
        "path",
        "query",
        "fragment",
        "username", "user",
        "password", "pass",
        "extension", "ext"
    ]
    parser.add_argument(
        "-f", "--fields",
        help="Parts to show of URL. The options are: %s." % field_choices,
        metavar="FIELD",
        nargs="+",
        choices=field_choices,
    )

    parser.add_argument(
        "-p", "--params",
        help="Params of URL to show.",
        nargs="+",
    )

    parser.add_argument(
        "-v",
        help="Verbose",
        dest="verbosity",
        action="count",
        default=0,
    )

    args = parser.parse_args()

    if not args.params:
        args.params = []

    if not args.fields:
        if args.params:
            args.fields = []
        else:
            args.fields = ["scheme", "netloc", "path", "query", "fragment"]

    for i, f in enumerate(args.fields):
        if f == "protocol":
            args.fields[i] = "scheme"

        elif f == "host":
            args.fields[i] = "hostname"

    return args


def main():
    args = parse_args()
    init_log(args.verbosity)

    logger.debug("URL parts: %s", args.fields)
    logger.debug("URL Params: %s", args.params)

    for url in read_text_targets(args.url):
        logger.info("URL: %s", url)
        url_p = urlparse(url)

        fields = [get_url_field(url_p, field) for field in args.fields]
        params = [
            " ".join(get_url_param(url_p, param))
            for param in args.params
        ]

        fields.extend(params)

        line = " ".join(fields)
        if line.strip() != "":
            print(*fields)


def init_log(verbosity=0, log_file=None):

    if verbosity == 1:
        level = logging.INFO
    elif verbosity > 1:
        level = logging.DEBUG
    else:
        level = logging.WARN

    logging.basicConfig(
        level=level,
        filename=log_file,
        format="%(levelname)s:%(name)s:%(message)s"
    )


def get_url_field(url_p: ParseResult, field: str) -> str:
    if field in ["scheme", "protocol", "proto"]:
        return url_p.scheme
    elif field in ["hostname", "host", "domain"]:
        return url_p.hostname or ''
    elif field == "port":
        return str(url_p.port) or ''
    elif field == "netloc":
        return url_p.netloc
    elif field == "path":
        return url_p.path
    elif field == "fragment":
        return url_p.fragment
    elif field == "query":
        return url_p.query
    elif field in ["username", "user"]:
        return url_p.username or ''
    elif field in ["password", "pass"]:
        return url_p.password or ''
    elif field in ["extension", "ext"]:
        return os.path.splitext(url_p.path)[1]

    raise KeyError(field)


def get_url_param(url_p: ParseResult, param: str) -> [str]:
    return parse_qs(url_p.query).get(param, [])


def read_text_targets(targets: Any) -> Iterator[str]:
    yield from read_text_lines(read_targets(targets))


def read_targets(targets: Optional[Any]) -> Iterator[str]:
    """Function to process the program ouput that allows to read an array
    of strings or lines of a file in a standard way. In case nothing is
    provided, input will be taken from stdin.
    """
    if not targets:
        yield from sys.stdin

    for target in targets:
        try:
            with open(target) as fi:
                yield from fi
        except FileNotFoundError:
            yield target


def read_text_lines(fd: Iterator[str]) -> Iterator[str]:
    """To read lines from a file and skip empty lines or those commented
    (starting by #)
    """
    for line in fd:
        line = line.strip()
        if line == "":
            continue
        if line.startswith("#"):
            continue

        yield line


if __name__ == '__main__':
    main()
