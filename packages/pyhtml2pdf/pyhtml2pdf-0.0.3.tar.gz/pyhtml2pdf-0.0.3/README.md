# pyhtml2pdf
Simple python wrapper to convert HTML to PDF with headless Chrome via selenium.

## Install
```
pip install pyhtml2pdf
```

## Dependencies

 - Selenium Chrome Webdriver [https://chromedriver.chromium.org/downloads] (If Chrome is installed on the machine you won't need to install the chrome driver)
 - Ghostscript [https://www.ghostscript.com/download.html]

## Example

### **Convert to PDF**

**Use with website url**

```
from pyhtml2pdf import converter

converter.convert('https://pypi.org', 'sample.pdf')
```

**Use with html file from local machine**

```
import os
from pyhtml2pdf import converter

path = os.path.abspath('index.html')
converter.convert(f'file:///{path}', 'sample.pdf')
```

**Some JS objects may have animations or take a some time to render. You can set a time out in order to help render those objects. You can set timeout in seconds**

```
converter.convert(source, target, timeout=2)
```

**Compress the converted PDF**

Some PDFs may be oversized. So there is a built in PDF compression feature.

The power of the compression,
 - 0: default
 - 1: prepress
 - 2: printer
 - 3: ebook
 - 4: screen

```
converter.convert(source, target, compress=True, power=0)
```

### **Compress PDF**

**Use it to compress a PDF file from local machine**

```
import os
from pyhtml2pdf import compressor

compressor.compress('sample.pdf', 'compressed_sample.pdf')
```

Inspired the works from,

 - https://github.com/maxvst/python-selenium-chrome-html-to-pdf-converter.git
 - https://github.com/theeko74/pdfc