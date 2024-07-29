# WHYS - Django

## TASK / Problem
Zadání: 

Podívej se na json soubor test_data.json. Jsou tam data ve následujícím formátu:

```
[
  {
    "nazev modelu 1": {
      "sloupec 1": "data",
      "sloupec 2": ["pole", "dat"]
    }
  },
  {
    "nazev modelu 2": {
      "sloupec 1": "data",
    }
  },
  {
    "nazev modelu 1": {
      "sloupec 1": "data",
    }
  }
]
```


Tvým úkolem je vytvořit modely a API v djangu, které bude příjimat tento JSON formát dat, zparsuje jej a bude mít následující endpointy pro přístup k těmto datům. Piš to s předpokladem, že ten kód bude někdo číst, ujisti se, že špatný formát dat nezpůsobí v aplikaci chybu.

Endpointy:
[POST] /import - tento endpoint bude příjímat data a parsovat data
[GET] /detail/<nazev modelu>/ - seznam záznamů na základě názvu modelu
[GET] /detail/<nazev modelu>/<id> - všechna data ke konkrétnímu záznamu

* Nezapomeň vytvořit requirements.txt
* Nezapoměň vytvořit README, jak projekt spustit


## Solution
I created simple api with 4 endpoints using django and django rest frameworkk. 
The logic is implemented in api/whys, where you can find models, serializers, views and urls needed.

### POST /import

- This endpoint parses json payload data at once. It handles both create and update methods. 
It doesn't crash on invalid data, rather skip the invalid item and continue with parsing next data.
For your validation purposes, return arrays of successfully parsed and skipped model names.

### GET /detail/<model name>
- Returns array with all models with the given name and their information. 
- As you can see in serializers.py, some objects return direct values and some whole objects of linked data: 
    That means:
- EXAMPLE ATTRIBUTE OUTPUT WITH DIRECT VALUES
```
{
    "id": 1,
    "nazev_atributu": "Barva",
    "hodnota_atributu": "modrá"
}
```
- EXAMPLE ATTRIBUTE OUTPUT WITH LINKED OBJECTS
```
{
        "id": 1,
        "attributes": [
            {
                "id": 19,
                "nazev_atributu": "displej",
                "hodnota_atributu": "ano"
            },
            {
                "id": 4,
                "nazev_atributu": "Barva",
                "hodnota_atributu": "růžová"
            },
            {
                "id": 18,
                "nazev_atributu": "Povrch",
                "hodnota_atributu": "jemný"
            },
            {
                "id": 22,
                "nazev_atributu": "Skladem",
                "hodnota_atributu": "ne"
            }
        ],
        "images": [
            {
                "id": 1,
                "obrazek": "https://free-images.com/or/4929/fridge_t_png.jpg",
                "nazev": null
            },
            {
                "id": 2,
                "obrazek": "https://free-images.com/or/ccc6/faulty_fridge_lighting_led_0.jpg",
                "nazev": "plná lednice"
            }
        ],
        "nazev": "Whirlpool B TNF 5323 OX",
        "description": "Volně stojící kombinovaná lednička se šestým smyslem. Díky tomuto šestému smyslu FreshLock dokáže obnovit teplotu 5× rychleji",
        "cena": "21566.00",
        "mena": "CZK",
        "published_on": null,
        "is_published": false
    },
```

!!! IF THIS IS CONFUSING, I CAN EXPLAIN IT IN FURTHER CONVERSATION !!!

### GET /detail/<model name>/id

- Returns detailed info about given module name with given id
- Same principle as other get endpoint

### DELETE /delete-all

- Rather unsafe endpoint for deleting all the data
- Just for testing purposes
- I left it in the app since you might want to use it too 


## LOCAL SETUP 



## TESTING

App runs on python 11

It was tested with postman. Some endpoints to try out:
- http://127.0.0.1:8000/import/ (with json payload)
- http://127.0.0.1:8000/detail/product
- http://127.0.0.1:8000/detail/catalog/1
- http://127.0.0.1:8000/detail/attribute/5
- http://127.0.0.1:8000/delete-all/

