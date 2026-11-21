"""!
@file constants.py
@brief Every constant of the nutrition scraper, defined in one place.
"""

## Address of the site that is scraped.
BASE_URL: str = "https://www.nutritionvalue.org"

## Path of the robots exclusion file on the site. It is read before any page is fetched.
ROBOTS_PATH: str = "/robots.txt"

## Address of the project, shown in the User-Agent so the site can see who is asking.
PROJECT_URL: str = "https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/093-assignment-custom-web-scraper"

## Name the scraper uses towards the site, in robots.txt checks and in the User-Agent header.
USER_AGENT_NAME: str = "NutritionScraperStudy"

## The User-Agent header sent with every request.
USER_AGENT: str = f"{USER_AGENT_NAME}/1.0 (+{PROJECT_URL})"

## Seconds to wait between two requests. The site asks for 1 second in robots.txt; twice that is used.
REQUEST_DELAY_SECONDS: float = 2.0

## Seconds to wait for one response before the request counts as failed.
REQUEST_TIMEOUT_SECONDS: float = 20.0

## How many times a failed request is repeated before the page is skipped.
MAX_RETRIES: int = 2

## Seconds to wait before a repeated request, multiplied by the number of the attempt.
RETRY_BACKOFF_SECONDS: float = 5.0

## Query string that makes a food page show the values per 100 g, so foods can be compared.
PORTION_QUERY: str = "size=100%20g"

## Ranking pages to read: a label and the path on the site. Each is a food category sorted by one nutrient.
RANKING_PAGES: tuple[tuple[str, str], ...] = (
    ("protein in fish and shellfish", "/foods_by_Protein_content_in_Finfish_and_Shellfish_Products.html"),
    ("protein in poultry", "/foods_by_Protein_content_in_Poultry_Products.html"),
    ("protein in legumes", "/foods_by_Protein_content_in_Legumes_and_Legume_Products.html"),
    ("protein in dairy and eggs", "/foods_by_Protein_content_in_Dairy_and_Egg_Products.html"),
    ("fibre in vegetables", "/foods_by_Fiber_content_in_Vegetables_and_Vegetable_Products.html"),
    ("fibre in legumes", "/foods_by_Fiber_content_in_Legumes_and_Legume_Products.html"),
    ("lowest calories in vegetables", "/foods_by_Calories_content_lowest_in_Vegetables_and_Vegetable_Products.html"),
    ("lowest calories in fruits", "/foods_by_Calories_content_lowest_in_Fruits_and_Fruit_Juices.html"),
)

## How many foods are taken from the top of each ranking page.
DEFAULT_FOODS_PER_RANKING: int = 10

## Protein per 100 g, in grams, from which a food counts as high in protein.
HIGH_PROTEIN_GRAMS: float = 20.0

## Fibre per 100 g, in grams, from which a food counts as high in fibre.
HIGH_FIBRE_GRAMS: float = 6.0

## Calories per 100 g, in kcal, up to which a food counts as low in calories.
LOW_CALORIE_KCAL: float = 60.0

## Sodium per 100 g, in milligrams, above which a food is left out.
MAX_SODIUM_MG: float = 400.0

## Tags a food can get.
TAG_HIGH_PROTEIN: str = "high-protein"
TAG_HIGH_FIBRE: str = "high-fibre"
TAG_LOW_CALORIE: str = "low-calorie"

## HTTP status codes after which a request is worth repeating: too many requests and temporary server errors.
RETRY_STATUS_CODES: tuple[int, ...] = (429, 500, 502, 503, 504)

## Character set used to read a page when the server does not name one.
DEFAULT_CHARSET: str = "utf-8"

## Nutrient rows of a food page. The key is the name the page uses; the value is the Food field and the unit of
## that field. A value the page gives in another unit is converted.
NUTRIENT_ROWS: dict[str, tuple[str, str]] = {
    "Protein": ("protein_g", "g"),
    "Carbohydrate": ("carbohydrate_g", "g"),
    "Fiber": ("fibre_g", "g"),
    "Sugars": ("sugars_g", "g"),
    "Fat": ("fat_g", "g"),
    "Saturated fatty acids": ("saturated_fat_g", "g"),
    "Sodium": ("sodium_mg", "mg"),
    "Potassium": ("potassium_mg", "mg"),
    "Calcium": ("calcium_mg", "mg"),
    "Iron": ("iron_mg", "mg"),
    "Vitamin C": ("vitamin_c_mg", "mg"),
}

## How many of a unit make one gram, so a value can be converted to the unit of its Food field.
UNIT_PER_GRAM: dict[str, float] = {"g": 1.0, "mg": 1_000.0, "mcg": 1_000_000.0}

## Where the CSV is written unless the user chooses another file.
DEFAULT_OUTPUT_PATH: str = "data/wellness_foods.csv"

## Columns of the CSV, in order. Each is a field of the Food value object.
CSV_COLUMNS: tuple[str, ...] = (
    "name",
    "category",
    "tags",
    "calories_kcal",
    "protein_g",
    "carbohydrate_g",
    "fibre_g",
    "sugars_g",
    "fat_g",
    "saturated_fat_g",
    "sodium_mg",
    "potassium_mg",
    "calcium_mg",
    "iron_mg",
    "vitamin_c_mg",
    "source_url",
)

## Name of the program shown in help and in the log.
APP_TITLE: str = "Nutrition Wellness Scraper"
