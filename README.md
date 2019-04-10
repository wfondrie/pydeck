# pydeck: Easily build remark.js slide decks  

## Overview  
pydeck is a python package that makes it easy to create 
[remark.js](https://github.com/gnab/remark) slide decks. remark.js is a
flexible, markdown-driven slideshow tool that makes beautiful presentations. The
cool thing is that you really only need to know markdown syntax to get started.
It is also highly custimizable if you know a bit of HTML and CSS.  

The pydeck package simplifies the creation of remark.js slide decks by taking care
of the boilerplate HTML for you. It also provides the ability to live preview
your slides upon saving the markdown file or its CSS dependencies.  

## Installation
pydeck not yet on PyPI, but it can still be installed with pip.
Note that pydeck is only available for Python 3.5+.

``` bash
pip3 install git+git://github.com/wfondrie/pydeck
```

## Getting Started  
The pydeck package takes a markdown file and outputs an HTML file with all of
the boilerplate code added to make it a valid remark.js slide deck. To begin,
all you need is a simple markdown file, which we'll call `example.md`:  

```md
class: center, middle

# My Cool Presentation

---

# A Second Slide  
With some cool content.

```

While pydeck can be used as a normal Python package, the easiest way to build
simple slide decks is from the command line.  Assuming `example.md` is
in your working directory, running the following will produce `example.html`:

```bash
pydeck example.md
```
Now you can open `example.html` in a browser and view your first slide show!

## Slide Formatting  
The [remark.js wiki](https://github.com/gnab/remark/wiki) contains
detailed documentation on how to format slides and operate the resulting slide
show. The pydeck package simplifies things mentioned in the wiki. For example,
pydeck handles the boilerplate HTML and also enables the use
of LaTeX math by default (using MathJax). 

Great presentations can be made using the default CSS and plain markdown.
However, you can customize your presentations in almost every way with knowledge
of HTML and CSS. 

## Configuration  
Configuration options can be added by including a YAML header in the markdown
file. This is where you can specify custom CSS files to use for styling and
modify specific remark.js settings. For example, a markdown file with a YAML
header specifying the default options would look like this:  

```md
---
title: pydeck
css: ["default-fonts", "default"]
self_contained: True
mathjax: True
remarkjs: "https://remarkjs.com/downloads/remark-latest.min.js"
remark_config:
    ratio: "16:9"
    navigation:
        scroll: True
        touch: True
        click: false
    countIncrementalSlides: True
    highlighting:
        highlightLanguage: "-"
---

# My Cool Presentation

---
# A Second Slide  
With some content.
```

Detailed documentation on these options is still a work in progress.


## Known Issues  
- Printing using Google Chrome's print to pdf feature is works only for
aspect ratios of 16:9 using the default CSS. 
[DeckTape](https://github.com/astefanutti/decktape) may be a more reliable 
option.  




