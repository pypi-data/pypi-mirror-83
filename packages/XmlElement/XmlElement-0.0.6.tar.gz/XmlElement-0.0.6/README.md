# XmlElement

A simpler XML writer.

## Installation

`pip install XmlElement`

## Test

```
>>> from XmlElement import XmlElement as X
>>> xml = X.from_string('<test><x/></test>')
>>> xml
XmlElement(test)
```

## Usage

```python
import XmlElement from XmlElement

xml = XmlElement('RootElement', s=[ # root element without attributes
    X('Child1', {'name': 'child1'}, [ # sub element with an attribute
        X('Child2', t='Example Value') # sub-sub element with text value
    ])
])

print(xml)
```



