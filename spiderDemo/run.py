from scrapy import cmdline

name = 'demo'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())