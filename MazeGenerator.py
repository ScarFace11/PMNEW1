# Генерация на сайте https://keesiemeijer.github.io/maze-generator/#generate
# Wall thickness: 2
# Maze entries: none
# Bias: none, но пожеланию можно сделать горизонтальный или вертикальный
# Remove maze walls: 300
from PIL import Image
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
def GetMazeFromParcing():
    #Нерабочая версия № 2
    """
    # Инициализация веб-драйвера
    driver = webdriver.Chrome()  # Укажите путь к драйверу вашего браузера

    # URL страницы с генератором лабиринтов
    url = "https://keesiemeijer.github.io/maze-generator/#generate"

    # Открытие страницы в браузере
    driver.get(url)

    # Нахождение и ввод значений в соответствующие элементы
    wall_thickness_input = driver.find_element_by_id('wall-size')
    wall_thickness_input.clear()
    wall_thickness_input.send_keys('2')

    columns_input = driver.find_element_by_id('width')
    columns_input.clear()
    columns_input.send_keys('8')

    rows_input = driver.find_element_by_id('height')
    rows_input.clear()
    rows_input.send_keys('8')

    # Выбор нужной опции в select
    entry_select = driver.find_element_by_id('entry')
    entry_select.find_elements_by_tag_name('option')[1].click()  # Выбор второй опции

    remove_walls_input = driver.find_element_by_id('remove_walls')
    remove_walls_input.clear()
    remove_walls_input.send_keys('300')

    # Нажатие кнопки генерации лабиринта
    generate_button = driver.find_element_by_id('generate')
    generate_button.click()

    # Пауза для завершения генерации (может потребоваться подождать, чтобы лабиринт полностью сгенерировался)
    time.sleep(5)

    # Закрытие браузера
    driver.quit()
    """
    # Нерабочая версия № 1
    """
    Value_Wall_thickness = 2
    Value_Columns = 8
    Value_Rows = 8
    Value_Remove_maze_walls = 300
    url = "https://keesiemeijer.github.io/maze-generator/#generate"
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        form_data = {}


        input_Wall_thickness = soup.find('input', {'id': 'wall-size'})
        input_Wall_thickness['value'] = Value_Wall_thickness
        form_data['wall-size'] = input_Wall_thickness

        input_Columns = soup.find('input', {'id': 'width'})
        input_Columns['value'] = Value_Columns
        form_data['width'] = input_Columns

        input_Rows = soup.find('input', {'id': 'height'})
        input_Rows['value'] = Value_Rows
        form_data['height'] = Value_Rows

        input_Maze_entries = soup.find('select', {'id': 'entry'})
        # Находим все опции внутри select
        options = input_Maze_entries.find_all('option')
        
        # Проходим по опциям и выбираем нужную
        for option in options:
            option.attrs.pop('selected', None)
            if option.get('value') == "":
                option['selected'] = 'selected'

        input_Remove_maze_walls = soup.find('input', {'id': 'remove_walls'})
        input_Remove_maze_walls['value'] = Value_Remove_maze_walls
        form_data['remove_walls'] = Value_Remove_maze_walls
        response_post = requests.post(url, data=form_data)
        if response_post.status_code == 200:
            print("Данные успешно отправлены!")
        else:
            print("Ошибка при отправке данных:", response_post.status_code)
    else:
        print("Произошла ошибка:", response.status_code)
    """
#GetMazeFromParcing()
def convert_image_to_binary(image_path, wall_thickness, scale_factor):
    image = Image.open(image_path)
    image = image.convert("L")  # Преобразование в оттенки серого
    pixels = image.load()
    width, height = image.size

    scaled_width = width // scale_factor
    scaled_height = height // scale_factor

    binary_data = []

    for y in range(0, scaled_height):
        row_data = []
        for x in range(0, scaled_width):
            pixel = pixels[x * scale_factor, y * scale_factor]
            if pixel == 0 or (x < wall_thickness or x >= scaled_width - wall_thickness or y < wall_thickness or y >= scaled_height - wall_thickness):
                row_data.append(1)  # Черный цвет или граница стенки
            else:
                row_data.append(0)  # Белый цвет
        binary_data.append(row_data)

    return binary_data

def GetMazeFromImage():
    maze_name = 'MazeClassicmini1'
    image_path = f"Sprite/{maze_name}.png"
    wall_thickness = 1
    scale_factor = 2
    binary_data = convert_image_to_binary(image_path, wall_thickness, scale_factor)
    maze = binary_data

    print(f"{maze_name} = [")
    for row in maze:
        print(f"{row},")
    print(']')

GetMazeFromImage()