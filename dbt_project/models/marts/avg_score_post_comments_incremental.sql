{{
    config(
        materialized="incremental"
    )
}}

with cte as (

    select * from {{ ref("stg_comment__data") }}

),
final as (

    select 
        distinct post_id, 
        created_utc::date, 
        {{ round_average('score') }} as avg
    from cte

    {% if is_incremental() %}
        where created_utc::date >= (select coalesce(max(created_utc::date), '1900-01-01') from {{ this }} )
    {% endif %}
    
    group by post_id, created_utc::date

)

select * from final