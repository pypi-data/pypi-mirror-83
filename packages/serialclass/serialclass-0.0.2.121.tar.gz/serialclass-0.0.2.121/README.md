# serialclass
A base class to get serialized representations of any Python class

[![gavanaken](https://circleci.com/gh/circleci/circleci-docs.svg?style=shield)](https://circleci.com/gh/gavanaken/serialclass)

## Install
```
pip install serialclass
```

## Usage
```
from serialclass import SerialClass


class InnerClass(SerialClass):

    def __init__(self, id_key):
        self.id_key = id_key


class Outerclass(SerialClass):

    def __init__(self):
        self._attribute = 'attribute'
        self._list = ['a', 'list']
        self._dict = {1: InnerClass('a'), 2: InnerClass('b')}


outclass = Outerclass()
```
```
outclass.serialize()  # dict

>>>> {'Outerclass': {'_attribute': 'attribute', '_dict': {1: {'InnerClass': {'id_key': 'a'}}, 2: {'InnerClass': {'id_key': 'b'}}}, '_list': ['a', 'list']}}'
```
```
outclass.serialize(depth=1)  # do not recurse

>>>> {'Outerclass': {'_attribute': 'attribute', '_dict': {1: <__main__.InnerClass object at 0x000001DC95C800C8>, 2: <__main__.InnerClass object at 0x000001DC95C801C8>}, '_list': ['a', 'list']}}
```
```
outclass.stringify()  # json string

>>>> {"Outerclass": {"_attribute": "attribute", "_dict": {"1": {"InnerClass": {"id_key": "a"}}, "2": {"InnerClass": {"id_key": "b"}}}, "_list": ["a", "list"]}}
```
```
outclass.pstringify(indent=2)  # json string with indent (default=4)

>>>> {
    "Outerclass": {
        "_attribute": "attribute",
        "_dict": {
            "1": {
                "InnerClass": {
                    "id_key": "a"
                }
            },
            "2": {
                "InnerClass": {
                    "id_key": "b"
                }
            }
        },
        "_list": [
            "a",
            "list"
        ]
    }
}
```
```
outclass.pstringify(indent=2, ignore_protected=True))  # ignore _ - prefaced attributes
>>>> {
    "Outerclass": {}
}
```
