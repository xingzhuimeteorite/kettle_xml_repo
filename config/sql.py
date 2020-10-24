insert_job_info = """
            INSERT INTO `dev_hermon`.`job_info_dev`
            ( 
             file_name
            , file_path_name
            , `job_name`
            , `job_path`
            , `job_create_time`
            , `job_update_time`
            ,  author
            , `job_entry`
            , `job_entry_type`
            , `job_entry_connection`
            , `job_entry_content`
            , `job_sql_complexity`
            ,  sql_size
            )
             values {};
            """
insert_trans_info = """
            INSERT INTO `dev_hermon`.`trans_info_dev`
            (  
             file_name
            , file_path_name
                , `trans_name`
                , `trans_path`
                , author
                , `trans_step`
                , `trans_step_type`
                , `trans_step_connection`
                , `trans_step_content`
                , trans_sql_complexity
                , sql_size
            )
             values {};
            """
