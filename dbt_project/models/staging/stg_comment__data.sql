with cte as (
    select *
    from {{ source("public", "comment_data") }}
)

select * from cte