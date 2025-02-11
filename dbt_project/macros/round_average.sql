{% macro round_average(column_name, places=2) %}
    round(AVG({{ column_name }}), {{ places }})
{% endmacro %}