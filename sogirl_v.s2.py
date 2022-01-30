#coding: utf8
#title: AVSoGirl 사이트 추가 - 수정
#author: Kurt Bestor (이후 수정됨)
#discription: 12022-01-30 수정

import clf2
from utils import *
import json

@Downloader.register
class Downloader_sogirl(Downloader):
    type = 'sogirl'
    URLS = ['.sogirl.so']
    single = True

    def read(self):
        html = self.get_page()

        soup = Soup(html)
        title = soup.find('meta', {'property': 'og:title'})['content'].strip()

        playlist = soup.find('div', class_='fp-playlist-external')

        try:
            srcs = []
            for a in playlist.findAll('a'):
                data = a.get('data-item')
                if not data:
                    continue
                data = json.loads(data)
                for src in data['sources']:
                    if src.get('fv_title'): # Ad
                        continue
                    srcs.append(src['src'])

            url_video = srcs[0]
            self.urls.append(url_video)
            self.filenames[url_video] = '{}{}'.format(clean_title(title), get_ext(url_video))
            self.referer = self.url

            self.title = title
        except:
            self.print_('No data found')

    @try_n(16)
    def get_page(self):
        html = clf2.solve(self.url)

        if '502: Bad gateway' in html['html']:
            self.print_(f'Cloudflare Bad Gateway Error Occured')
            raise Exception('bad gateway')

        return html['html']

log('sogirl script loaded')