with cte as (

    select * from {{ ref('stg_post__data') }}

),
final as (

    select distinct created_utc::date,
        {{ round_average('upvote_ratio') }} as avg_upvote_ratio
    from cte
    group by created_utc::date

)

select * from final