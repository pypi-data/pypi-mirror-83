import requests
import re
from bs4 import BeautifulSoup
from lxml import etree

class url2(object):
    """
    """
    def __init__(self, url, headers={'User-Agent':'Mozolla/5.0'}, encode=False, init=False, verify=True, cdx=True, form_data=None):
        self.url = url
        self.headers = headers
        self.encode = encode
        self.init = init
        self.verify = verify
        self.cdx = cdx
        self.form_data = form_data
    
    @property
    def html(self):
        """
        url2html
        """
        if self.form_data == None:
            r = requests.get(self.url, headers=self.headers, verify=self.verify, allow_redirects=self.cdx)
            if self.init == False:
                if self.encode == False:
                    r.encoding = r.apparent_encoding
                else:
                    r.encoding = r.apparent_encoding
                    r.encoding = 'utf-8'
                result = r.text
        else:
            def headers_handle(headers):
                '''
                对请求头加引号
                '''
                if headers[0] == '\n':
                    headers = headers[1:]
                pattern = '^(.*?):[\s]*(.*?)$'

                dict_str = ''
                dict_str += '{'
                for line in headers.splitlines():
                    dict_str += re.sub(pattern,'\'\\1\':\'\\2\',',line)
                dict_str += '}'
                
                dict_ = eval(dict_str)
                return dict_

            form_data = headers_handle(self.form_data)
            
            result = requests.post(self.url,data=form_data, headers=self.headers, verify=self.verify, allow_redirects=self.cdx).text
            
        return result

    @property
    def soup(self):
        """
        url2soup
        """
        html_ = self.html
        soup = BeautifulSoup(html_)
        return soup

    def html2xpath(html_):
        pass
    
    @property
    def xpath(self):
        """
        url2xpath
        """
        html = self.html
        return etree.HTML(html).xpath
