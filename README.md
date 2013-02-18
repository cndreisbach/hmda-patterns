HMDA Patterns
=============

"HMDA Patterns" is inspired by Jim Campen's [Changing Patterns][], an
annual report prepared for the Massachusetts Community & Banking
Council about mortgage lending practices in the Greater Boston area.

The data in "Changing Patterns" is used by non-profit and community
organizing groups in Boston. We feel that this information would be
useful for groups in urban areas all over the United States. "HMDA
Patterns" allows you to create a report for any Metropolitan
Statistical Area (MSA) in the United States.

Our aspirational goal is to replicate all of the charts available in
"Changing Patterns" and provide tables of the data used in those
charts. We are, obviously, not there yet, and invite you to
contribute.

[Changing Patterns]: http://mcbc.info/reports/mortgage

## HMDA

"HMDA" refers to the [Home Mortgage Disclosure Act][hmda], a law that
requires financial institutions to maintain and annually disclose data
about home purchases, home purchase pre-approvals, home improvement,
and refinance applications. This data is made public and is available
from the US Government at the [FFIEC HMDA Products][hmda-products]
site.

[hmda]: http://en.wikipedia.org/wiki/Home_Mortgage_Disclosure_Act
[hmda-products]: http://www.ffiec.gov/hmda/hmdaproducts.htm

## Usage

```sh
python ./manage.py runserver [--config config]
```

`config` should be the path to a Flask configuration file.

## Tools Used

This project is a sister project to [hmda-tools][], a set of Python
libraries used to load HMDA and HMDA-related data.

### Back end
* [Flask][]
* [SQLAlchemy][]

### Front end
* [Zurb Foundation][zurb]
* [Chosen][]
* [Sugar.js][]
* [d3.js][]
* [xCharts][]

[hmda-tools]: https://github.com/crnixon/hmda-tools
[Flask]: http://flask.pocoo.org/
[SQLAlchemy]: http://www.sqlalchemy.org/
[zurb]: http://foundation.zurb.com/
[Raphael.js]: http://raphaeljs.com/
[gRaphael]: http://g.raphaeljs.com/
[Chosen]: http://harvesthq.github.com/chosen/
[Sugar.js]: http://sugarjs.com/
[d3.js]: http://d3js.org/
[xCharts]: http://tenxer.github.com/xcharts/

## Contributors

"HMDA Patterns" was created by Clinton Dreisbach, Marc Esher, and
Virginia Czosek.

