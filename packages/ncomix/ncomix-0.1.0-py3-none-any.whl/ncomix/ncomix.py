"""
#Future dev:
proxies and ip rotation
use proxy without headers HTTP_X_FORWARDED_FOR or HTTP_VIA
User-agent spoofing and rotation -> DONE
back-off time for requests -> DONE
Reducing the crawling rate -> STOPPED by unnecessary
multiprocessing to download images -> STOPPED by ethics
make and use a parsing method with css selectors
store and access links to categories and tags
"""


from __future__ import annotations

import csv
import json
import random
import sys
import time
from io import BytesIO
from PIL import Image
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum, unique
from pathlib import Path
from typing import Iterator, List, Tuple
from urllib.parse import urljoin, urlparse
from urllib.request import getproxies

import faker.providers.user_agent
import requests
from faker import Faker
from requests import HTTPError, Session
from requests.adapters import HTTPAdapter
from requests.models import Response
from bs4 import BeautifulSoup as bs
from urllib3.util.retry import Retry

try:
    assert sys.version_info.major == 3
    assert sys.version_info.minor >= 7
except AssertionError:
    raise RuntimeError("ncomix requires Python 3.7+")

def perf(func,*args,**kwargs):
	def new_func(*args,**kwargs):
		t1=time.time()
		result = func(*args,**kwargs)
		t2=time.time()
		print(f'function {func.__name__}:{func} executed in {t2-t1} seconds')
		return result
	return new_func

class RequestHandler:
	fake = Faker()
	_timeout = (3.05, 6.05)
	_total = 5
	_status_forcelist = [413, 429, 500, 502, 503, 504]
	_backoff_factor = 1

	def get(self, url, *args,**kwargs):
		session = Session()

		session.headers.update({"User-Agent" : self.fake.chrome(version_from=80, version_to=86, build_from=4100, build_to=4200)})

		assert_status_hook = lambda response, *args, **kwargs: response.raise_for_status()
		session.hooks['response'] = [assert_status_hook]

		retry_strategy = Retry(total=self._total, status_forcelist=self._status_forcelist, backoff_factor=self._backoff_factor)
		session.mount("https://", HTTPAdapter(max_retries = retry_strategy))

		response = session.get(url, timeout = self._timeout,*args,**kwargs)
		return response

class ncomix:
	"""
	Central class that bundles together all properties and methods related to single comic.
	under work : is_valid_name(),is_valid_url()
	"""
	HOME = 'https://www.porncomix.one/'
	_URL1 = 'https://www.porncomix.one/link/'
	_URL2 = 'https://www.porncomix.one/gallery/'
	_URL3 = 'https://www.porncomix.one/comic-link/'

	def __init__(self, url: str=None, name: str=None):
		if url and name:
			raise ValueError("Too many arguments. Only one of name or url must be given")
		elif not(url or name):
			raise ValueError("Insufficient arguments")
		if name:
			if not ncomix.is_valid_name(name):
				raise ValueError("Invalid name")
			self.name = name
			self.url = urljoin(ncomix._URL,name)
		else:
			url = url.rstrip('/')
			if not ncomix.is_valid_url(url):
				raise ValueError("Invalid url")
			self.name = url.split('/')[-1]
			self.url = url

		#setting other constants
		self.handler = RequestHandler()
		self.response = self.get(url)


	@staticmethod
	def is_valid_name(name: str) -> bool:
		banned_chars = ['/','\\',':','https','.','_']
		for char in banned_chars:
			if char in name:
				return False
		return True

	@staticmethod
	def is_valid_url(name: str) -> bool:
		#s_url = url.split('/')
		#if not(url.startswith(ncomix._URL) and len(s_url)==5):
		#	return False
		return True

	def get(self,url: str) -> dict:
		"""
		works on:
		"https://www.porncomix.one/link/lemonfont-pearl-necklace/522877"
		"https://www.porncomix.one/gallery/black-pharaoh-joker-the-inner-joke"
		"https://www.porncomix.one/gallery/my-bad-bunny-wanton-widow-2"
		"https://www.porncomix.one/gallery/psmike-locker-room-story"

		doesn't work on:
		"https://www.porncomix.one/gallery/big-boobs-grow-4" #Error in pages
		"""

		response = self.handler.get(url)
		assert(response.ok)

		short_url = response.headers['link'].split()[2].rstrip(';').rstrip('>').lstrip('<')
		soup = bs(response.content,'html.parser')
		category = soup.find(id='content').find('article').find('p',{'class':'post-meta entry-meta'}).find('span',{'class':'post-category'}).text.strip()
		tags = {t.text:t['href'] for t in soup.find(id='content').find('article').find('p',{'class':'post-meta entry-meta'}).find('span',{'class':'post-tag'}).find_all('a')}
		author = {a.text:a['href'] for a in soup.find(id='content').find('article').find('span',{'class':'post-author'}).find_all('a')}
		title = soup.find(id='content').find('article').find('h1',{'class':'post-title entry-title'}).text
		pages = [{'url':fig.find('a')['href'],'width':int(fig.find('img')['width']),'height':int(fig.find('img')['height'])} for fig in soup.find(id='content').find('article').find('div',{'class':'post-content'}).find('div',{'id':'dgwt-jg-2'}).find_all('figure')]
		num_pages = len(pages)
		res = {'num_pages':num_pages,'short_url':short_url,'category':category,'title':title,'author':author,'pages':pages,'tags':tags}

		return res

	@property
	def num_pages(self) -> int:
		return self.response['num_pages']

	@property
	def title(self) -> str:
		return self.response['title']

	@property
	def short_url(self) -> str:
		return self.response['short_url']

	@property
	def id(self) -> str:
		return urlparse(self.short_url).query[2:]

	@property
	def category(self) -> str: #note: implement category class
		return self.response['category']

	@property
	def tags(self) -> dict: #note: implement tag class
		return self.response['tags']

	@property
	def pages(self) -> dict:
		return self.response['pages']

	@property #note: implement author class
	def author(self) -> str:
		return self.response['author']

	@property
	def page_urls(self) -> List: #outs list coz list is faster to iterate over
		return [page['url'] for page in self.response['pages']]

	@property
	def filename(self) -> str: #currently for windows only, barely
		banned_chars = r'/\:*?"<>|'
		banned_names = ('CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9')
		filename = ''.join(c for c in self.title if c not in banned_chars)
		filename = filename.strip('.').strip() #weak
		if filename in banned_names:
			print('Warning: Invalid filename, returned "default_filename" as filename')
			return 'default_filename'
		return filename

	def __repr__(self):
		return f'<ncomix.ncomix object at {id(self)}> id={self.id}, title={self.title}, url={self.short_url}, pages={self.num_pages}'

	def get_images(self):
		images_raw = [self.handler.get(page['url']).content for page in self.pages]
		return images_raw

	@perf
	def download(self,dest: Path = Path.cwd(), delay: int=0) -> None:
		dest = dest.joinpath(self.filename)
		dest.mkdir(parents=True, exist_ok=True)

		print('downloading...')
		load_percent = 0
		num_pages = self.num_pages
		for i,img_url in enumerate(self.page_urls):
			response = self.handler.get(img_url, stream=True)
			filename = dest.joinpath(img_url[img_url.rfind('/')+1:])
			with open(filename, mode='wb') as f:
				for chunk in response.iter_content(1024):
					f.write(chunk)

			if load_percent != (i/num_pages)//0.01:
				load_percent = (i/num_pages)//0.01
				print(f'{load_percent:2} %', end='\r')
			time.sleep(delay)

	@perf
	def download_pdf(self,dest: Path = Path.cwd(), delay: int=0) -> None:
		dest.mkdir(parents=True, exist_ok=True)
		dest = dest.joinpath(self.filename+'.pdf')
		images = []

		print('downloading pdf...')
		load_percent = 0
		num_pages = self.num_pages
		for i,img_url in enumerate(self.page_urls):
			response = self.handler.get(img_url, stream=True)
			images.append(Image.open(BytesIO(response.content)))
			if load_percent != (i/num_pages)//0.01:
				load_percent = (i/num_pages)//0.01
				print(f'{load_percent:2} %', end='\r')
			time.sleep(delay)
		images[0].save(dest,save_all=True, append_images=images[1:])



		






