truncate table job_info;
truncate table trans_info;

-- 添加数据到正式表
 insert into dev_hermon.job_info select * from dev_hermon.job_info_dev;
 insert into dev_hermon.trans_info select * from dev_hermon.trans_info_dev;


-- 当前目录替换为绝对路径
update job_info

set job_entry_connection = job_path
where job_entry_connection in ('${Internal.Entry.Current.Directory}','${Internal.Entry.Current.Directory}_hc');
update job_info  
set job_entry_connection = '/arnon/arnon_2copt_cache_goods_category_analyze' 
where  job_entry_connection = 'arnon/arnon_2copt_cache_goods_category_analyze';
update job_info  
set job_entry_connection = '/tiberias/tiberias_zzh_kf_chat_response_daily'
where job_entry_connection in ('/tiberias/Trans_temp_service_zzh_kf_chat_response_daily','/tiberias/Trans_tiberias_service_zzh_kf_chat_response_daily');

--  拼接job明细结果表
drop table job_detail;
create table job_detail as select
	a.job_name,
	a.job_path,
	a.job_create_time,
	a.job_update_time,
	a.job_entry_content,
	case a.job_entry_type
	when 'TRANS' then concat(	a.job_entry,' ',a.job_entry_content) 
	else a.job_entry
	end as job_entry
,
case a.job_entry_type
	when 'TRANS' then a.job_entry_type
	when 'JOB'  then null
	end as  job_entry_type
,
	case a.job_entry_type
	when 'TRANS' then b.trans_step_connection
	when 'JOB'  then null
	else  a.job_entry_connection
	end as database_connection
	,b.trans_step
	,case a.job_entry_type
	when 'TRANS' then b.trans_step_content
	else a.job_entry_content
	end as step_content
	,case a.job_entry_type
	when 'TRANS' then b.trans_sql_complexity
	else  a.job_sql_complexity
	end as sql_complexity
	,case a.job_entry_type
	when 'TRANS' then b.sql_size
	else  a.sql_size
	end as sql_size
from
	job_info a
left join trans_info b 
on a.job_entry_type = 'TRANS'
and  a.job_entry_content = b.file_name 
and  a.job_entry_connection = b.file_path_name
order by a.job_name;
-- 拼接job hop表

insert  into  job_detail  

 select
	a.job_name,
	a.job_path,
	a.job_create_time,
	a.job_update_time,
	a.job_entry_content,
	case a.job_entry_type
	when 'TRANS' then concat(	a.job_entry,' ',a.job_entry_content) 
	else a.job_entry
	end as job_entry
,
a.job_entry_type
,
	case a.job_entry_type
	when 'TRANS' then b.trans_step_connection
	when 'JOB'  then null
	else  a.job_entry_connection
	end as database_connection
	,b.trans_step
	,case a.job_entry_type
	when 'TRANS' then b.trans_step_content
	else a.job_entry_content
	end as step_content
	,case a.job_entry_type
	when 'TRANS' then b.trans_sql_complexity
	else  a.job_sql_complexity
	end as sql_complexity
	,case a.job_entry_type
	when 'TRANS' then b.sql_size
	else  a.sql_size
	end as sql_size
from
	job_info a
right join(
select  job_name,job_path,job_entry_content
from job_detail
where sql_complexity is null 
and job_name in (
'Job_tiberias_shop_activity_subsist_v1.ktr'
,'Job_tiberias_2copt_shop_transactions_hourly_hc'

)
) c  on c.job_path = a.job_path and a.job_name = c.job_name and a.job_entry_content = c.job_entry_content
left join trans_info b 
on a.job_entry_type = 'TRANS'
and  a.job_entry_content = b.trans_name  
and  a.job_entry_connection = b.trans_path
;

delete from job_detail 
where job_name in (
'Job_tiberias_shop_activity_subsist_v1.ktr'
,'Job_tiberias_2copt_shop_transactions_hourly_hc'

)and sql_complexity is null ;

INSERT INTO job_detail ( `job_name`, `job_path`, `job_create_time`, `job_update_time`, `job_entry_content`, `job_entry`, `job_entry_type`, `database_connection`, `trans_step`, `step_content`, `sql_complexity`, `sql_size` )

select file_name,file_path_name,null,null,null,null,trans_step_type,trans_step_connection,trans_step,trans_step_content,trans_sql_complexity,sql_size from  
trans_info 
where file_name not in 
(
select 
job_entry_content
from 

job_info 
where job_entry_type = 'TRANS')
and trans_name not in 
(
select 
job_entry_content
from 

job_info 
where job_entry_type = 'TRANS');

	
drop table job_hop;
create table job_hop as 
select distinct
job_name,
job_entry_content as chlid_step,
job_path,
job_entry_connection as child_path 
from
	job_info 
where
	job_entry_type IN ( 'JOB', 'TRANS' ) 
order by
	job_name;


