# no-more-query-string
Remove *unneccessary* query-string from the URL given. Especially fbclid.

## Changelog
+ [CHANGELOG](https://github.com/EltonChou/no-more-query-string/blob/main/CHANGELOG.md)
## Installation
```sh
pip install no-more-query-string
```

## Usage
```py
from no_more_qs import NoMoreQS

nmq = NoMoreQS()
url = "https://www.youtube.com/watch?v=h-RHH79hzHI&feature=emb_logo&ab_channel=Ceia"

NoMoreQS.clean(url)
# 'https://www.youtube.com/watch?v=h-RHH79hzHI'
```
## Parameters
***fbclid* will be cleaned from all domains**
```py
# default
NoMoreQS(include_flds=[], exclude_flds=[], strict=True)
```
### include_flds ( `List[str] | Tuple[str]`=[] )

first-level domains list which are allowed to clean query string.
```py
include_flds = ('youtube.com', 'google.com')

url = "https://www.youtube.com/watch?v=h-RHH79hzHI&feature=emb_logo&ab_channel=Ceia&fbclid=IwAR2NasdasdasdadasdfP58isTW-c3U"

NoMoreQS(include_flds=include_flds).clean(url)
# 'https://www.youtube.com/watch?v=h-RHH79hzHI'
```
### exclude_flds ( `List[str] | Tuple[str]`=[] )

first-level domains which are disallowed to clean query string.
```py
exclude_flds = ('youtube.com', 'google.com')

url = "https://www.youtube.com/watch?v=h-RHH79hzHI&feature=emb_logo&ab_channel=Ceia&fbclid=IwAR2NasdasdasdadasdfP58isTW-c3U"

NoMoreQS(exclude_flds=exclude_flds).clean(url)
# 'https://www.youtube.com/watch?v=h-RHH79hzHI&feature=emb_logo&ab_channel=Ceia'

```
### strict ( bool=True )
if the domain is not in `include_flds` or `exclude_flds`
+ True(default): Remove all unneccessary query string.
+ False: Only remove `fbclid` from query string.
```py
url = "https://www.youtube.com/watch?v=h-RHH79hzHI&feature=emb_logo&ab_channel=Ceia&fbclid=IwAR2NasdasdasdadasdfP58isTW-c3U"

NoMoreQS(strict=True).clean(url)
# 'https://www.youtube.com/watch?v=h-RHH79hzHI'

NoMoreQS(strict=False).clean(url)
# 'https://www.youtube.com/watch?v=h-RHH79hzHI&feature=emb_logo&ab_channel=Ceia'
```
## Method parameters
```py
NoMoreQS().clean(url, allow_og_url=False)
```
### allow_og_url (bool=False)
if can't find `canonical url`, will return `og url`
