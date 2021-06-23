
-- shopping list for all recipes (without supply/usage taken into account)

SELECT
  COALESCE(section.name, 'other') AS section,
  item.name,  
  SUM(ingr.amount),
  unit.code

FROM recipes_recipe r

JOIN recipes_ingredient ingr ON ingr.recipe_id = r.id
JOIN recipes_item       item ON item.id = ingr.item_id
JOIN recipes_unit       unit ON unit.id = ingr.units_id

LEFT JOIN recipes_section section ON section.id = item.section_id

GROUP BY
  item.name, section, unit.code

ORDER BY
  section, item.name
