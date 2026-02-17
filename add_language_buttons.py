import os

# Путь к твоему HTML файлу
html_file = "templates/index.html"

# Проверяем, существует ли файл
if not os.path.exists(html_file):
    print(f"Файл {html_file} не найден!")
    exit()

# Читаем исходный HTML
with open(html_file, "r", encoding="utf-8") as f:
    content = f.read()

# Код для вставки формы выбора языков и кнопки
language_block = """
<form method="POST" class="space-y-4">
    <textarea name="text" placeholder="Введите текст" required
              class="w-full p-3 border rounded-md dark:bg-gray-700 dark:border-gray-600"></textarea>

    <div class="flex justify-between gap-2">
        <div class="flex-1">
            <label>С языка:</label>
            <select name="from_lang" class="w-full p-2 border rounded-md dark:bg-gray-700 dark:border-gray-600">
                <option value="ru">Русский</option>
                <option value="en">Английский</option>
                <option value="fr">Французский</option>
                <option value="de">Немецкий</option>
            </select>
        </div>
        <div class="flex-1">
            <label>На язык:</label>
            <select name="to_lang" class="w-full p-2 border rounded-md dark:bg-gray-700 dark:border-gray-600">
                <option value="en">Английский</option>
                <option value="ru">Русский</option>
                <option value="fr">Французский</option>
                <option value="de">Немецкий</option>
            </select>
        </div>
    </div>

    <div class="flex justify-between gap-2">
        <button type="submit" class="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md">
            Перевести
        </button>
        <button type="button" onclick="swapLanguages()" 
                class="flex-1 bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded-md">
            🔄 Поменять языки
        </button>
    </div>
</form>

<script>
function swapLanguages() {
    const fromLangSelect = document.querySelector('select[name="from_lang"]');
    const toLangSelect = document.querySelector('select[name="to_lang"]');
    
    const temp = fromLangSelect.value;
    fromLangSelect.value = toLangSelect.value;
    toLangSelect.value = temp;
}
</script>
"""

# Вставляем блок перед закрывающим тегом </body>
if "</body>" in content:
    content = content.replace("</body>", language_block + "\n</body>")
else:
    content += language_block  # если </body> нет, просто добавляем в конец

# Записываем обратно
with open(html_file, "w", encoding="utf-8") as f:
    f.write(content)

print("Блок выбора языков и кнопка смены языков успешно добавлены в HTML!")
