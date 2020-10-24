-- DDL
/*
表实际意义 存储job的步骤信息
job_detail

job_info

父job名称

job名称  
job路径  
job创建时间 
job修改时间

job步骤
job步骤类型
步骤连接
步骤内容

 who字段
 
transinfo

转换名称
转换步骤
转换类型 
转换连接
转换内容
who字段
job     job_name job_path 
*/

drop table if exists dev_hermon.job_info ;
drop table if exists dev_hermon.trans_info ;
drop table if exists dev_hermon.job_detail;


create table dev_hermon.job_info 
(
`id` int NOT NULL AUTO_INCREMENT comment 'id',
`parent_job_name` char(50)  comment '父job名称',
`job_name` char(50) not null comment 'job名称',
`job_path` char(50) not null comment 'job路径',
`job_create_time` datetime  comment 'job创建时间',
`job_update_time` datetime  comment 'job更新时间',
`job_entry` char(50) not null comment 'job步骤',
`job_entry_type` char(50) not null comment 'job步骤类型',
`job_entry_connection` char(50) not null comment 'job路径',
`job_entry_content` text not null comment 'job路径',
`job_sql_complexity` int  comment 'sql复杂度',
`sql_size` char(50) comment 'sql文件大小',
`create_time` datetime  DEFAULT '1111-11-11 11:11:11' COMMENT '创建时间',
`update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  COMMENT '更新时间',
 PRIMARY KEY (`id`)
)
ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='job信息';

create table dev_hermon.trans_info 
(
`id` int NOT NULL AUTO_INCREMENT comment 'id',
`job_name` char(50) not null comment 'job_name',
`trans_name` char(50) not null comment 'trans_name',
`trans_path` char(50) not null comment 'trans路径',
`trans_step` char(50) not null comment 'trans步骤',
`trans_step_type` char(50) not null comment 'trans步骤类型',
`trans_step_connection` char(50) not null comment 'trans步骤连接',
`trans_step_content` text not null comment 'trans步骤内容',
`trans_sql_complexity` int  comment 'sql复杂度',
`sql_size` char(50) comment 'sql文件大小',
`create_time` datetime  DEFAULT '1111-11-11 11:11:11' COMMENT '创建时间',
`update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  COMMENT '更新时间',
 PRIMARY KEY (`id`)
)
ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='trans信息';


create table dev_hermon.job_detail
(
`id` int NOT NULL AUTO_INCREMENT comment 'id',
`parent_job_name` char(50)  comment '父job名称',
`job_name` char(50) not null comment 'job名称',
`job_path` char(50) not null comment 'job路径',
`job_create_time` char(50) not null comment 'job创建时间',
`job_update_time` char(50) not null comment 'job更新时间',
`job_entry` char(50) not null comment 'job步骤',
`job_entry_type` char(50) not null comment 'job步骤类型',
`job_entry_connection` char(50) not null comment 'job路径',
`job_entry_content` char(50) not null comment 'job路径',
`trans_name` char(50) not null comment 'trans_name',
`trans_path` char(50) not null comment 'trans路径',
`trans_step` char(50) not null comment 'trans步骤',
`trans_step_type` char(50) not null comment 'trans步骤类型',
`trans_step_connection` char(50) not null comment 'trans步骤连接',
`trans_step_content` text not null comment 'trans步骤内容',
`job_sql_complexity` int  comment 'sql复杂度',
`create_time` datetime  DEFAULT '1111-11-11 11:11:11' COMMENT '创建时间',
`update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  COMMENT '更新时间',
 PRIMARY KEY (`id`)

)
ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='job明细';

