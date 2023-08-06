#!/usr/bin/python
#coding=utf-8
import io
from simplified_scrapy.core.regex_helper import *
from simplified_scrapy.core.request_helper import extractHtml, _getResponseStr
from simplified_scrapy.extracter import ExtractModel
from simplified_scrapy.core.utils import absoluteUrl, getFileContent, isExistsFile
from simplified_scrapy.core.regex_dic import RegexDict
from simplified_scrapy.core.listex import List


class SimplifiedDoc(RegexDict):
    def __init__(self,
                 html=None,
                 start=None,
                 end=None,
                 before=None,
                 edit=True):
        self._fileName = None
        self._fileParas = {}
        self._fileEncoding = None
        self._editFlag = edit
        self['html'] = None
        self.last = None
        if (not html): return
        html = _getResponseStr(html)
        sec = getSection(html, start, end, before)
        if (sec): html = html[sec[0]:sec[1]]
        html = preDealHtml(html)
        self['html'] = html

    def loadHtml(self, html, start=None, end=None, before=None):
        if (not html): return
        html = _getResponseStr(html)
        sec = getSection(html, start, end, before)
        if (sec): html = html[sec[0]:sec[1]]
        html = preDealHtml(html)
        self['html'] = html

    def loadFile(self, fileName, lineByline=False, encoding='utf-8', **other):
        if not lineByline:
            html = getFileContent(fileName, encoding=encoding, **other)
            html = _getResponseStr(html)
            html = preDealHtml(html)
            self['html'] = html
        else:
            self._fileName = fileName
            self._fileParas = other
            self._fileEncoding = encoding
            self._editFlag = False

    def getIterable(self,
                    tag=None,
                    start=None,
                    end=None,
                    first=None,
                    last=None):
        if not self._fileName:
            print('warning: file name is empty.\nPlease call the method loadFile first, self.loadFile(fileName, lineByline=True, ...')
            return
        if not isExistsFile(self._fileName):
            print('warning: file {} is not exists.'.format(self._fileName))
            return
        with io.open(self._fileName,
                     "r",
                     encoding=self._fileEncoding,
                     **self._fileParas) as file:
            line = file.readline()

            start = False
            block = ''
            while line != '':
                if first and line.find(first) < 0:
                    continue
                elif first:
                    first = False

                if not first and last and line.find(last) >= 0:
                    break

                if not start:
                    start = self._getStart(line, tag, start, end)
                if start:
                    block = block + line
                    i = self._getEnd(line, tag, start, end)
                    if i >= 0:
                        doc = SimplifiedDoc(block)
                        if tag:
                            yield doc.getElement(tag)
                        else:
                            yield doc
                        block = ''
                        start = False

                line = file.readline()

    def traverse(self,
                 event,
                 tag=None,
                 start=None,
                 end=None,
                 first=None,
                 last=None):
        for d in self.getIterable(tag, start, end, first, last):
            flag = event(d)
            if flag == False:
                break

    def _getStart(self, line, tag, start, end):
        if line.strip() == '': return False
        if start and end:
            return line.find(start) >= 0
        else:
            i = line.find('<' + tag)
            if i < 0:
                return False
            tmp = line[i + len(tag) + 1]
            if tmp == '>' or tmp.strip() == '':
                return True
            return False

    def _getEnd(self, line, tag, start, end):
        if line.strip() == '': return False
        if start and end:
            return line.find(end) >= 0
        else:
            return line.find('</' + tag + '>')

    def removeElement(self,
                      tag,
                      attr='class',
                      value=None,
                      html=None,
                      start=None,
                      end=None,
                      before=None):
        if html: html = preDealHtml(html)
        if (not html): html = self.html
        if (not html and self.last): html = self.last.html
        self['html'] = removeElement(tag, attr, value, html, start, end,
                                     before)
        return self['html']

    def removeElements(self,
                       tag,
                       attr='class',
                       value=None,
                       html=None,
                       start=None,
                       end=None,
                       before=None):
        if html: html = preDealHtml(html)
        if (not html): html = self.html
        if (not html and self.last): html = self.last.html
        while True:
            tmp = removeElement(tag, attr, value, html, start, end, before)
            if tmp != html:
                html = tmp
            else:
                break
        self['html'] = html
        return self['html']

    def getSection(self, html=None, start=None, end=None, before=None):
        return self._getSection(html, start, end, before)[0]

    def _getSection(self, html=None, start=None, end=None, before=None):
        if html: html = preDealHtml(html)
        if (not html): html = self.html
        if (not html and self.last): html = self.last.html
        s, e = getSection(html, start, end, before)
        l = 0
        if before: l = len(before)
        elif start: l = len(start)
        el = 0
        if end: el = len(end)
        if s < 0:
            s = 0
            l = 0
        if e < 0:
            e = len(html)
            el = 0
        return (html[s + l:e], s, e + el)

    def removeHtml(self, html, separator='', tags=None):
        return removeHtml(html, separator, tags)

    def trimHtml(self, html):
        return trimHtml(html)

    def absoluteUrl(self, baseUrl, url):
        return absoluteUrl(baseUrl, url)

    def getObjByModel(self, html, url=None, models=[{"Type": 3}], title=None):
        if (not isinstance(models, dict) and not isinstance(models, list)):
            models = json.loads(models)
        if (isinstance(models, dict)):
            models = [models]
        return extractHtml(url, html, models, None, title)
