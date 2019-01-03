# pydeck: Easily build remark slide decks  

## Overview  
pydeck is a python package that makes it easy to create 
[remark](https://github.com/gnab/remark) slide decks. remark is a flexible,
markdown-driven slideshow tool that makes beautiful presentations. The cool
thing is that you really only need to know markdown syntax to get started.
It is also highly custimizable if you know a bit of HTML and CSS.  

The pydeck package simplifies the creation of remark slide decks by taking
care of the boilerplate html for you. It also provides the ability to live
preview your slides upon saving the markdown file or its CSS dependencies.  

## Installation
pydeck is not yet on PyPI, but it can still be installed with pip.
Note that pydeck is only available for Python 3.5+.

``` python
pip3 install git+git://github.com/wfondrie/pydeck
```

## Known Issues  

- Slide_Deck.serve() has problems with local paths to media if they are
outside of the root directory.  
- Printing using Google Chrome's print to pdf feature is works only for
aspect ratios of 16:9. [DeckTape](https://github.com/astefanutti/decktape) 
may be a more reliable option.  




