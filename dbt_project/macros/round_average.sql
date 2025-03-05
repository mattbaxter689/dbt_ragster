{% macro round_average(column_name, places=2) %}
    round(CAST(AVG({{ column_name }}) as numeric), {{ places }})
{% endmacro %}