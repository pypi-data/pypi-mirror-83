# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mithrandir']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['lint = scripts:lint', 'test = scripts:test']}

setup_kwargs = {
    'name': 'mithrandir',
    'version': '1.1.0',
    'description': '',
    'long_description': '# Mithrandir\n\nfree-form monad & other crazy implementations\n\n### Features\n- async/await\n- operator-overloading\n\n### Examples\nOn sync-mode:\n```python\nlist_of_ten = list(range(10))\n\ndata = (\n    Monad([])\n    | Op.CONCAT(*list_of_ten)\n    | Op.MAP(lambda x: x * 2)\n    | Op.CONCAT(*list(range(0, 200, 3)))\n    | Op.MAP(lambda x: [{"val": x}])\n    | Op.FILTER(lambda x: x[0]["val"] % 2 == 0)\n    | Op.FOLD(lambda v, x: [*v, str(x[0]["val"])], [])\n    | Op.MAP(list)\n    | Op.FLATTEN()\n    | Op.DISTINCT(key=lambda x: x[0])\n    | Op.MAP(int)\n    | Op.SORT()\n    | Sig.RESOLVE\n)\n\nassert data == [0, 2, 4, 6, 8, 10, 30, 54, 72, 90]\n```\n\nOn `async`, simply add `await` before everything\n```python\nasync def inc_by_2(n: int):\n    return n + 2\n\nasync def only_gt_10(n: int):\n    return n > 10\n\nasync def to_int(n: str):\n    return int(n)\n\ndef convert_to_map(final: Dict[str, int], val: int):\n    final.update({f"{val}__key": val})\n    return final\n\nasync def convert_map_to_array(d: List[Dict]):\n    return d[0].values()\n\ndef only_less_than_30(n: int):\n    return n < 30\n\nasync_monad = await (\n    Monad(list(range(20)))\n    | Op.MAP(inc_by_2)\n    | Op.FILTER(only_gt_10)\n    | Op.MAP(str)\n    | Op.FILTER(lambda x: "2" in x)\n    | Op.SORT(reverse=True)\n    | Op.MAP(to_int)\n    | Op.CONCAT(*list(range(50, 100, 3)))\n    | Op.FOLD(convert_to_map, dict())\n    | Op.BIND(convert_map_to_array)\n    | Op.DISTINCT()\n    | Op.FILTER(only_less_than_30)\n    | Sig.RESOLVE\n)\n\nassert async_monad.unwrap() == [21, 20, 12]\n```\n\n### Usage\n- Refer `tests`\n\n\n### Coverage\n```\nCoverage report: 98%\n-------\nTotal\t86\t2\t0\t98%\nmithrandir/__init__.py\t1\t0\t0\t100%\nmithrandir/monad.py\t85\t2\t0        98%\n-------\ncoverage.py v5.3, created at 2020-10-20 15:25 +0700\n```\n',
    'author': 'vutr',
    'author_email': 'me@vutr.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
