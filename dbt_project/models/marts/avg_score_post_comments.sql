with cte as (

    select * from {{ ref("stg_comment__data") }}

),
final as (

    select 
        distinct post_id, 
        created_utc::date, 
        {{ round_average('score') }} as avg_score
    from comment_data
    group by post_id, created_utc::date

)

select * from final