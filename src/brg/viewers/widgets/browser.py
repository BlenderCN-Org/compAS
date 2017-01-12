"""Implementation of a browser widget."""

import sys
import os

try:
    from PySide.QtCore import QUrl
    from PySide.QtWebKit import QWebView
    from PySide.QtWebKit import QWebSettings

except ImportError:

    class QWebView(object):
        pass


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


class Browser(QWebView):
    pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from PySide.QtGui import QApplication

    app = QApplication(sys.argv)

    html_file = '/Users/vanmelet/bitbucket/brg_framework/src/brg/viewers/widgets/threejs/examples/webgl_geometry_nurbs.html'

    with open(html_file, 'r') as fp:
        html = fp.read()

    baseurl = QUrl().fromLocalFile(os.path.dirname(html_file))
    print baseurl

    browser = Browser()

    settings = browser.settings()
    settings.setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls, True)

    browser.load(html_file)
    # browser.setHtml(html, baseurl)

    browser.show()

    sys.exit(app.exec_())
