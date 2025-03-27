from include.datasets import DATASET_COCKTAIL
from airflow.exceptions import AirflowFailException


def _get_cocktail(ti=None):
    import requests
    from airflow.models import Variable

    # Variable.set('_my_variable_4', 200)
    api = Variable.get("api")
    response = requests.get(api)
    with open(DATASET_COCKTAIL.uri, "wb") as f:
        f.write(response.content)
    ti.xcom_push(key="cocktail", value=len(response.content))

def _check_size(ti=None):
    size = ti.xcom_pull(key="cocktail", task_ids="get_cocktail")
    print(size)
    if size <= 0:
        raise AirflowFailException("This is a test")


def _validate_cocktail_fields():
    """Validate that the cocktail JSON data has the expected structure."""
    import json

    required_fields = {
        'drinks': [
                      'idDrink', 'strDrink', 'strDrinkAlternate', 'strTags', 'strVideo',
                      'strCategory', 'strIBA', 'strAlcoholic', 'strGlass', 'strInstructions',
                      'strInstructionsES', 'strInstructionsDE', 'strInstructionsFR',
                      'strInstructionsIT', 'strInstructionsZH-HANS', 'strInstructionsZH-HANT',
                      'strDrinkThumb'
                  ] + [f'strIngredient{i}' for i in range(1, 16)]
                  + [f'strMeasure{i}' for i in range(1, 16)]
                  + ['strImageSource', 'strImageAttribution', 'strCreativeCommonsConfirmed', 'dateModified']
    }

    with open(DATASET_COCKTAIL.uri, 'r') as f:
        data = json.load(f)

    if not isinstance(data, dict) or 'drinks' not in data:
        raise ValueError("JSON must have a 'drinks' array")

    if not isinstance(data['drinks'], list) or not data['drinks']:
        raise ValueError("'drinks' must be a non-empty array")

    drink = data['drinks'][0]
    missing_fields = [field for field in required_fields['drinks']
                      if field not in drink]

    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")