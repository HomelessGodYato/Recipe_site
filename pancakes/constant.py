
MODIFIABLE_FIELD_INGREDIENT_ID = "ingredient_id_{}"
MODIFIABLE_FIELD_INGREDIENT_TITLE = "ingredient_title_{}"
MODIFIABLE_FIELD_INGREDIENT_AMOUNT = "ingredient_amount_{}"
MODIFIABLE_FIELD_INGREDIENT_UNIT = "ingredient_unit_{}"
MODIFIABLE_FIELD_INGREDIENT_IS_REQUIRED = "ingredient_is_required_{}"
MODIFIABLE_FIELD_CATEGORY = "category_{}"
MODIFIABLE_FIELD_TAG = "tag_{}"

ID = "id"
AUTHOR = "author"
DATA_CREATE = "date_create"
STATUS = "status"
TITLE = "title"
UNIT = "unit"
IMAGE = "image"
AMOUNT = "amount"
IS_REQUIRED = "is_required"
COOKING_TIME = "cooking_time"
STAGE = "stage"
STAGES_LIST = "stages_list"
RECIPE = "recipe"
RECIPES_LIST = "recipes_list"
INGREDIENT = "ingredient"
DESCRIPTION = "description"
ORDER = "order"
TAG = "tag"
CATEGORY = "category"
RECIPE_ID = "recipe_id"
STAGE_ID = "stage_id"
INGREDIENT_ID = "ingredient_id"
IS_CHECKED = "is_checked"

TAGS_LIST = "tags_list"
INGREDIENTS_LIST = "ingredients_list"
CATEGORIES_LIST = "categories_list"
INGREDIENTS_EXTENDED_LIST = "ingredients_extended_list"
INGREDIENTS_EXTENDED_LIST_LENGTH = "ingredients_extended_list_length"

ERROR = "error"
ERROR_TOO_SHORT = "{} musi mieć przynajmniej {} znaki"
ERROR_TOO_LONG = "{} może mieć maksymalnie {} znaków"
ERROR_IS_LESS_THAN_ZERO = "{} musi być dodatnie"
ERROR_INVALID_ID = "Nie ma {} o id {}"
ERROR_AUTHOR = "Nie jesteś autorem przepisu o id {}"

ERROR_THERE_IS_NOT_CATEGORY = "Nie ma przepisów z kategorią o nazwie: '{}'"
ERROR_THERE_IS_NOT_TAG = "Nie ma przepisów z tagiem o nazwie: '{}'"
ERROR_THERE_IS_NOT_AUTHOR = "Nie ma przepisów od użytkownika o id: '{}'"
ERROR_THERE_IS_NOT_TITLE = "Nie ma przepisów z pasującym słowem: '{}'"

NUMBER_OF_CATEGORIES = "number_of_categories"
NUMBER_OF_TAGS = "number_of_tags"

NUMBER_OF_INGREDIENTS_MAX = "number_of_ingredients_max"
NUMBER_OF_INGREDIENTS_RANGE = "number_of_ingredients_range"
number_of_ingredients_max = 30
number_of_ingredients_range = range(0, number_of_ingredients_max)

DEFAULT_RECIPE_IMAGE_PATH = 'default/default.PNG'
DEFAULT_STAGE_IMAGE_PATH = 'default/default.PNG'

RECIPE_INGREDIENT_STATUS_DRAFT = "DRAFT"
RECIPE_INGREDIENT_STATUS_APPROVED = "APPROVED"
RECIPE_STATUS_DRAFT = "DRAFT"
RECIPE_STATUS_APPROVED = "APPROVED"

ACTION = "ACTION"
ACTION_CREATE = "ACTION_CREATE"
ACTION_UPDATE = "ACTION_UPDATE"
ACTION_DELETE = "ACTION_DELETE"

RECIPE_FORM_STATE = "RECIPE_FORM_STATE"
RECIPE_FORM_STATE_FIRST = "RECIPE_FORM_STATE_FIRST"
RECIPE_FORM_STATE_STAGE = "RECIPE_FORM_STATE_STAGE"
RECIPE_FORM_STATE_LAST_STAGE = "RECIPE_FORM_STATE_LAST_STAGE"
RECIPE_FORM_STATE_LAST = "RECIPE_FORM_STATE_LAST"

ACTION_SEARCH_ARTICLES = "ACTION_SEARCH_ARTICLES"
ACTION_CREATE_ARTICLE = "ACTION_CREATE_ARTICLE"
ACTION_CREATE_COMMENT = "ACTION_CREATE_COMMENT"
ACTION_CREATE_COMMENT_REPLY = "ACTION_CREATE_COMMENT_REPLY"
ACTION_TRY_TO_ADD_COMMENT = "ACTION_TRY_TO_ADD_COMMENT"
ACTION_TRY_TO_ADD_REPLY = "ACTION_TRY_TO_ADD_REPLY"
ACTION_ACCEPT_CHANGES = "ACTION_ACCEPT_CHANGES"
ACTION_REJECT_CHANGES = "ACTION_REJECT_CHANGES"
ACTION_DELETE_ARTICLE = "ACTION_DELETE_ARTICLE"
ACTION_DELETE_COMMENT = "ACTION_DELETE_COMMENT"

NO_RESULTS = "no_results"
NO_RESULTS_INFO = 'Brak wyników dla frazy "{}".'
PAGES_COUNT = "pages_count"
NEXT_PAGE_NUMBER = "next_page_number"
PREV_PAGE_NUMBER = "prev_page_number"
NOT_SEARCHING = "not_searching"

ARTICLE = "article"
ARTICLES = "articles"
MY_ARTICLES = "my_articles"
COMMENTS = "comments"
SUB_COMMENTS = "sub_comments"
SUB_COMMENTS_COUNT = "sub_comments_count"
IMAGES = "images"
DATE_CREATE = "date_create"
IS_CREATOR = "is_creator"
IS_USER_AUTHENTICATED = "is_user_authenticated"

SEARCH_FORM = "search_form"
ARTICLE_FORM = "article_form"
COMMENT_FORM = "comment_form"
IMAGE_FORM = "image_form"
EDIT_IMAGES_FORM = "edit_images_form"
EDIT_FORM = "edit_form"