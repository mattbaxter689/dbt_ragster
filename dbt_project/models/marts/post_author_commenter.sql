with post_data as (

    select * from {{ ref('stg_post__data') }}

), comment_data as (

    select * from {{ ref('stg_comment__data') }}

), final as (

    select p.id,
        c.comment_id,
        p.author as post_author,
        c.author as comment_author,
        p.locked as post_locked,
        p.score as post_score,
        p.num_comments as num_post_comments,
        p.upvote_ratio as post_upvote_ratio,
        c.score as comment_score
    from post_data p
    left join comment_data c ON p.author = c.author

)

select * from final