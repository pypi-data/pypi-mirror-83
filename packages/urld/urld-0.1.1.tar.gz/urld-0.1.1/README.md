# urld

URL descomposer to extract parts of url. It accepts urls by stdin and displays
the parts in stdout.

## Installation

From pypi:
```
pip install urld
```



## Usage

By default, it splits the urls in their different parts:
```shell
$ echo "https://www.gitlab.com/Zer1t0?test=a#hey" | urld
https www.gitlab.com /Zer1t0 test=a hey
```

But can also specify the parts you would like to retrieve:
```shell
$ echo "https://www.gitlab.com/index.html" | urld -f host
www.gitlab.com

$ echo "https://www.gitlab.com/index.html" | urld -f protocol path
https /index.html

$ echo "https://www.gitlab.com/index.html" | urld -f extension
.html


$ echo "https://www.gitlab.com/?foo=bar" | urld -p foo
bar
```
