
  
  
  
  create or replace view `dbt_pipeline1`.`staging`.`stg_smoke_test`
  
  as (
    select 1 as id, 'scaffold_ok' as status
  )
