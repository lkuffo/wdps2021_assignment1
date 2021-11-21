#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import os
import gzip
import re
import urllib
import requests
from io import BytesIO
from warcio.archiveiterator import ArchiveIterator
from bs4 import BeautifulSoup
from selectolax.parser import HTMLParser
#from lxml.html import fromstring
from pyquery import PyQuery
#from polyglot.text import Text,Detector
from dragnet import extract_content

def isurl(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return True if re.match(regex,url) else False

def get_html_warc(warcfile):
    '''
    读取CommonCrawl的warc\wet文件，返回html,

    Args:
        pathfile：CommonCrawl的warc、wet格式文件或url字符串,warc,wet文件为gzip压缩格式
    Returns:
        A string of html
    '''
    #判断参数是否为url
    if isurl(warcfile):
        resp = requests.get(warcfile, stream=True)
        f=resp.raw
    else:
        f = gzip.open(warcfile,'rb')
    for record in ArchiveIterator(f):
        #page_id = record.rec_headers.get_header('WARC-Record-ID')
        #print(page_id)
        page_id = record.rec_headers.get_header('WARC-TREC-ID')
        print(page_id)
        if record.rec_type == 'warcinfo':
            warcinfo=record.raw_stream.read()
        #get warc file content\
        elif record.rec_type == 'response':
            content_type=record.http_headers.get_header('Content-Type')
            if content_type and content_type[:9] == 'text/html':
                # get html charset
                strlist=content_type.replace(' ', '').lower().split(';')
                if len(strlist)>1:
                    if strlist[1][:8]=='charset=':
                        charset=strlist[1][8:]
                    else:
                        charset=strlist[1]
                else: #no charset
                    charset='utf-8'
                payload = record.content_stream().read().decode(encoding=charset,errors= 'ignore')
                yield [payload, page_id]
            elif content_type and content_type[:19] == 'application/rss+xml':
                #process xml type
                xml=record.content_stream().read()
            elif content_type == 'application/pdf' :
                #process pdf type
                pdf=record.content_stream().read()
            else:
                #other type
                pass 
        #get wet file content         
        elif record.rec_type == 'conversion':
            payload=record.content_stream().read().decode(encoding=charset,errors= 'ignore')
            yield [payload, page_id]
    if not isurl(warcfile):
        f.close()

def get_warc_from_pathfile(pathfile):
    '''
    Input:warc.path.gz、wet.path.gz、wat.path.gz),返回不含网址带路径的warc、wet、wat文件

    Args:
        pathfile：CommonCrawl格式的路径文件或url字符串,warc,wet,wat的路径文件为gzip压缩格式
    Returns:
        A string of filename
    '''
    if isurl(pathfile):
        #resp = requests.get(url, stream=True)
        with urllib.request.urlopen(pathfile) as fp:
            buffer=BytesIO(fp.read())
            f=gzip.GzipFile(fileobj=buffer)            
            while True:
                line=f.readline()
                if line:
                        # decode转换utf-8显示，否则中文为乱码，而且需要去掉
                        # 最后一个\n
                    yield line.decode('utf-8')[:-1]
                else:
                    return
    else:      
        with gzip.open(pathfile, 'rb') as f:
            while True:
                line=f.readline()
                if line:
                        # decode转换utf-8显示，否则中文为乱码，而且需要去掉
                        # 最后一个\n
                    yield line.decode('utf-8')[:-1]
                else:
                    return
    

def text_extract(html_prase):
    try: 
        text = extract_content(html_phrase)
    except:
        soup= BeautifulSoup(html_prase,'lxml')
        body= soup.body
        if body is None:
            return None
        for tag in body.select('script'):
            tag.decompose()
        for tag in body.select('style'):
            tag.decompose()
        text = body.get_text(separator='')
    return text

def save_to_file(file_name,contents):
    file =open(file_name,'w+')
    file.write(contents)
    file.close()

def parse_warc(location):
    #html_prase = get_html_warc('data/sample.warc.gz')
    html_prase = get_html_warc(location)
    text = text_extract(html_prase)
    return text
