# aiohglib

The aiohglib is an asynchronous variant of [hglib](https://www.mercurial-scm.org/wiki/PythonHglib), which is library with a fast, convenient interface to Mercurial. It uses Mercurial's command server for communication with hg.

The code itself takes advantage of asyncio library and async/await syntax.

Another difference against standard hglib is suport for timezones and changesets details like p1, p2 and extras.

## Basic usage

```python
import asyncio
import aiohglib

async def main():
    async with aiohglib.open(path) as client:
        log = await client.log(revrange="tip")
        print(log)

# Depending on your Python version you need to run one of those:

# Python 3.7 or newer
asyncio.run(main())

# Python 3.6
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()

# Python 3.6 on Windows
loop = asyncio.ProactorEventLoop()
loop.run_until_complete(main())
loop.close()
```

## Dependencies ##

* Python 3.6
* [pytz](https://pypi.org/project/pytz/)
* [chardet](https://pypi.org/project/chardet/) (optional)

## Changelog ##

### 1.4 ###

* Fixed await syntax in client.py
* Fixed redundant \_\_bool\_\_ in util.py
* Optional detection of encoding for changeset's author and description via chardet module
* Optional safe\_template is now *not* used by default


## Licence ##

MIT

## Contact ##

Michal Šiška <michal.515k4@gmail.com>
