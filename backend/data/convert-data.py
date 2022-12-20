import json
import logging

log_format = "%(asctime)s::%(levelname)s::%(filename)s::%(message)s"
logging.basicConfig(level='INFO', format=log_format)


with open('ingredients.json') as fileIngredients:
    result = []
    pushed_units = []
    json_data = json.load(fileIngredients)

    for index, ingredient in enumerate(json_data):
        if ingredient["measurement_unit"] in pushed_units:
            logging.info(f'skip {ingredient["measurement_unit"]}')
        else:
            pushed_units.append(ingredient["measurement_unit"])
            result.append(
                {
                    'model': 'recipes.measurementUnit',
                    'pk': index + 1,
                    'fields': {'name': ingredient["measurement_unit"]},
                }
            )
        result.append(
            {
                'model': 'recipes.ingredient',
                'pk': index + 1,
                'fields': {
                    'name': ingredient["name"],
                    'measurement_unit': ingredient["measurement_unit"],
                },
            }
        )

    with open('../foodgram/fixtures.json', 'w', encoding='utf-8') as fileResult:
        json.dump(result, fileResult, ensure_ascii=False, indent=4)
