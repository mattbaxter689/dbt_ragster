with cte as (
    select *
    from {{ source("public", "post_data") }}
)

select * from cte