with cte as (

    select * from {{ ref("stg_post__data") }}

),
final as (
    select 
        distinct id as post_id,
        created_utc::date,
        {{ round_average('score') }} as avg_post_score
    from cte
    group by id, created_utc::date

)

select * from final