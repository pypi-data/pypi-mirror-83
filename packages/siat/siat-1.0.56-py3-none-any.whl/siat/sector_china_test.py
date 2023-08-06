# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 23:41:54 2020

@author: Peter
"""
#数据网址：http://finance.sina.com.cn/stock/sl/#qmxindustry_1

import akshare as ak

# 板块行情
stock_industry_sina_df = ak.stock_sector_spot(indicator="新浪行业")

stock_industry_star_df = ak.stock_sector_spot(indicator="启明星行业")

stock_industry_concept_df = ak.stock_sector_spot(indicator="概念")

stock_industry_region_df = ak.stock_sector_spot(indicator="地域")

stock_industry_industry_df = ak.stock_sector_spot(indicator="行业")
hangye_list=list(set(list(stock_industry_industry_df['label'])))
hangye_list.sort()

#板块详情：nmc-流通市值？mktcap-总市值？
#"行业"
stock_sector_zl01_df = ak.stock_sector_detail(sector="hangye_ZL01")
len(stock_sector_zl01_df)

stock_sector_zc27_df = ak.stock_sector_detail(sector="hangye_ZC27")

#"概念"
stock_sector_kc50_df = ak.stock_sector_detail(sector="gn_kc50")

#"地域"
stock_sector_440000_df = ak.stock_sector_detail(sector="diyu_440000")

#"新浪行业"
stock_sector_dlhy_df = ak.stock_sector_detail(sector="new_dlhy")

#"启明星行业"：无详情



import os; os.chdir("S:/siat")
from siat.sector_china import *


