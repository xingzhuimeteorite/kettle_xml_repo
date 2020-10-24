import re

# 元组内元素 建议为小写
# keywords = ('join','group\s*by','order\s*by','distinct','max[(]','min[(]','over','insert')
# keywords = ('join','group\s*by','order\s*by','distinct','max[(]','min[(]','over [(]parition by.*？[)]','insert ')
keywords = ('join ','group\s*by','order\s*by','distinct','max[(]','min[(]','over\s*[(]partition by.*[)]','insert ')



class SqlAnalysis():
    global keywords
    len = 0
    def __init__(self,sqls):
        self.complexity = 0
        self.sql = []
        self.sourcesql = sqls
        self.sqls = sqls
        if sqls == None:
            self.sql = []
        else :
             self.sqls = re.sub('-- .*', '', sqls)
             #多行模式 flags=re.DOTALL
             if re.findall('.*?;',self.sqls, flags=re.DOTALL) == []:
                 self.sql.append(self.sqls)
             else :
                 self.sql =  re.findall('.*?;',self.sqls, flags=re.DOTALL)
        self.complexities = [0]
    def getComplexity(self,s):
        self.complexity = 0
        for keyword in keywords:
            # 忽略大小写进行匹配
            list = re.findall(keyword, s, re.IGNORECASE)
            if list != []:
                self.complexity += len(list)
            else:
                self.complexity += 0
        return self.complexity
    def getMaxComplexity(self):

        for s in self.sql:
            self.complexities.append(self.getComplexity(s))

        return max(self.complexities)

    def getSqlSize(self):
        if self.sqls == None:
            return '0'
        else :
            self.len = len(self.sourcesql.encode('utf-8'))
            # self.size = str(int(self.len) * 8 / 1024) + 'k' + '  utf-8'
            self.size = int(self.len)
            return self.size

if __name__ == '__main__':
    sql = '''
    
SELECT   
t.p_segment_year
,t.p_segment_code
,t.cate_name as  cate_name
,t.goods_brand as  goods_brand
,t.regions_name as regions_name
,t.one_level_addr as  one_level_addr
,t.two_level_addr as  two_level_addr
,t.city_level as  city_level
,t.three_level_addr as three_level_addr
-- ,cast(sum(t.goods_amount) as decimal(20,2))  as sale_amount
,cast(t_ytd.month_amount as decimal(20,2))  as sale_amount

,cast(t_ytd.ytd_month_amount  as decimal(20,2)) as  ytd_sale_amount
,cast(tt.shop_num as int) as shop_cnt
,cast(tt_order.order_num  as int)as order_cnt
,cast(t_last.month_amount as decimal(20,2))   as last_sale_amount
,cast(tt_last.shop_num  as int)  as  last_shop_cnt
,cast(tt_order_last.order_num  as int)  as  last_order_cnt
,now() as create_time
,now() as update_time
FROM  arnon_dwd_b2xtl_order_detail_manual  t
left join (
select count(1) as shop_num,a.p_segment_year,a.p_segment_code,a.cate_name,a.goods_brand,a.regions_name,a.one_level_addr,a.two_level_addr,a.city_level,a.three_level_addr from (
select distinct
a.p_segment_year,a.p_segment_code,a.cate_name,a.goods_brand,a.regions_name,a.one_level_addr,a.two_level_addr,a.city_level,a.three_level_addr
,a.shop_code
from 
arnon_dwd_b2xtl_order_detail_manual a 

where a.goods_amount>0
and a.if_delete = 0
order by a.cate_name,a.goods_brand
) a 
 group  by a.p_segment_year,a.p_segment_code,a.cate_name,a.goods_brand,a.regions_name,a.one_level_addr,a.two_level_addr,a.city_level,a.three_level_addr
 
) tt on 
tt.p_segment_year = t.p_segment_year
and tt.p_segment_code = t.p_segment_code
and tt.cate_name = t.cate_name
and tt.goods_brand = t.goods_brand
and tt.regions_name = t.regions_name
and tt.one_level_addr = t.one_level_addr
and tt.two_level_addr = t.two_level_addr
and tt.city_level = t.city_level
and tt.three_level_addr = t.three_level_addr
left join (
select count(1) as shop_num,a.p_segment_year,a.p_segment_code,a.cate_name,a.goods_brand,a.regions_name,a.one_level_addr,a.two_level_addr,a.city_level,a.three_level_addr from (
select distinct
a.p_segment_year,a.p_segment_code,a.cate_name,a.goods_brand,a.regions_name,a.one_level_addr,a.two_level_addr,a.city_level,a.three_level_addr
,a.shop_code
from 
arnon_dwd_b2xtl_order_detail_manual a 

where a.goods_amount>0
and a.if_delete = 0 
order by a.cate_name,a.goods_brand
) a 
 group  by a.p_segment_year,a.p_segment_code,a.cate_name,a.goods_brand,a.regions_name,a.one_level_addr,a.two_level_addr,a.city_level,a.three_level_addr
 
) tt_last on 
tt_last.p_segment_year = (t.p_segment_year-1)
and tt_last.p_segment_code = t.p_segment_code
and tt_last.cate_name = t.cate_name
and tt_last.goods_brand = t.goods_brand
and tt_last.regions_name = t.regions_name
and tt_last.one_level_addr = t.one_level_addr
and tt_last.two_level_addr = t.two_level_addr
and tt_last.city_level = t.city_level
and tt_last.three_level_addr = t.three_level_addr
left join (
select distinct
t.p_segment_year,t.p_segment_code,t.cate_name,t.goods_brand,t.regions_name,t.one_level_addr,t.two_level_addr,t.city_level,t.three_level_addr,
sum( t.goods_amount ) over (
	partition by t.p_segment_year,t.p_segment_code,
	t.cate_name,
	t.goods_brand,
	t.regions_name,
	t.one_level_addr,
	t.two_level_addr,
	t.city_level,
	t.three_level_addr 
	) as month_amount ,
sum(t.goods_amount)  over (partition by t.p_segment_year,t.cate_name,t.goods_brand,t.regions_name,t.one_level_addr,t.two_level_addr,t.city_level,t.three_level_addr order by t.p_segment_code) as ytd_month_amount
from arnon_dwd_b2xtl_order_detail_manual t 
where t.if_delete = 0
-- group by t.p_segment_year,t.p_segment_code,t.cate_name,t.goods_brand,t.regions_name,t.one_level_addr,t.two_level_addr,t.city_level,t.three_level_addr
) t_ytd on 
    t_ytd.p_segment_year = t.p_segment_year
and t_ytd.p_segment_code = t.p_segment_code
and t_ytd.cate_name = t.cate_name
and t_ytd.goods_brand = t.goods_brand
and t_ytd.regions_name = t.regions_name
and t_ytd.one_level_addr = t.one_level_addr
and t_ytd.two_level_addr = t.two_level_addr
and t_ytd.city_level = t.city_level
and t_ytd.three_level_addr = t.three_level_addr
left join (
select 
t.p_segment_year,t.p_segment_code,t.cate_name,t.goods_brand,t.regions_name,t.one_level_addr,t.two_level_addr,t.city_level,t.three_level_addr,
sum(t.goods_amount)  as  month_amount
from arnon_dwd_b2xtl_order_detail_manual t 
where t.if_delete = 0
group by t.p_segment_year,t.p_segment_code,t.cate_name,t.goods_brand,t.regions_name,t.one_level_addr,t.two_level_addr,t.city_level,t.three_level_addr 
) t_last on 
    t_last.p_segment_year = (t.p_segment_year-1)
and t_last.p_segment_code = t.p_segment_code
and t_last.cate_name = t.cate_name
and t_last.goods_brand = t.goods_brand
and t_last.regions_name = t.regions_name
and t_last.one_level_addr = t.one_level_addr
and t_last.two_level_addr = t.two_level_addr
and t_last.city_level = t.city_level
and t_last.three_level_addr = t.three_level_addr
left join (
select count(1) as order_num,a.p_segment_year,a.p_segment_code,a.cate_name,a.goods_brand,a.regions_name,a.one_level_addr,a.two_level_addr,a.city_level,a.three_level_addr from (
select distinct
a.p_segment_year,a.p_segment_code,a.cate_name,a.goods_brand,a.regions_name,a.one_level_addr,a.two_level_addr,a.city_level,a.three_level_addr
,a.order_no
from 
arnon_dwd_b2xtl_order_detail_manual a
where a.if_delete = 0
order by a.cate_name,a.goods_brand
) a 
 group  by a.p_segment_year,a.p_segment_code,a.cate_name,a.goods_brand,a.regions_name,a.one_level_addr,a.two_level_addr,a.city_level,a.three_level_addr
 
) tt_order  on 
tt_order.p_segment_year = t.p_segment_year
and tt_order.p_segment_code = t.p_segment_code
and tt_order.cate_name = t.cate_name
and tt_order.goods_brand = t.goods_brand
and tt_order.regions_name = t.regions_name
and tt_order.one_level_addr = t.one_level_addr
and tt_order.two_level_addr = t.two_level_addr
and tt_order.city_level = t.city_level
and tt_order.three_level_addr = t.three_level_addr
left join (
select count(1) as order_num,a.p_segment_year,a.p_segment_code,a.cate_name,a.goods_brand,a.regions_name,a.one_level_addr,a.two_level_addr,a.city_level,a.three_level_addr from (
select distinct
a.p_segment_year,a.p_segment_code,a.cate_name,a.goods_brand,a.regions_name,a.one_level_addr,a.two_level_addr,a.city_level,a.three_level_addr
,a.order_no
from 
arnon_dwd_b2xtl_order_detail_manual a 
where a.if_delete = 0
order by a.cate_name,a.goods_brand
) a 
 group  by a.p_segment_year,a.p_segment_code,a.cate_name,a.goods_brand,a.regions_name,a.one_level_addr,a.two_level_addr,a.city_level,a.three_level_addr
 
) tt_order_last  on 
tt_order_last.p_segment_year = (t.p_segment_year-1)
and tt_order_last.p_segment_code = t.p_segment_code
and tt_order_last.cate_name = t.cate_name
and tt_order_last.goods_brand = t.goods_brand
and tt_order_last.regions_name = t.regions_name
and tt_order_last.one_level_addr = t.one_level_addr
and tt_order_last.two_level_addr = t.two_level_addr
and tt_order.city_level = t.city_level
and tt_order.three_level_addr = t.three_level_addr
where t.if_delete = 0
group by t.p_segment_year,t.p_segment_code,t.cate_name,t.goods_brand,t.regions_name,t.one_level_addr,t.two_level_addr,t.city_level,t.three_level_addr;

    '''
    sql1 = re.sub('--.*','', sql)
    # print(sql1)
    sql1 =re.findall('.*;', sql1, flags=re.DOTALL)
    print(sql1)

    num = SqlAnalysis(sql)
    print(num.sql)
    print(num.getMaxComplexity())
    print(num.getSqlSize())
    print(num.complexities)
