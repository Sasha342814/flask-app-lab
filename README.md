# Лабораторна «Побудова зв'язків. Практика» (Flask + SQLAlchemy 2.0)

## Запуск

```
cd lab8
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python build_lab.py          # міграції (п.1-4, 9) + тестові дані
python lab_demo.py           # п.7 і п.10 (пости користувачів, теги поста / пости тегу)
python run.py                # веб-застосунок: http://127.0.0.1:5000
```

## Відповідність пунктам завдання

| Пункт | Де |
|---|---|
| 1-2 User + міграція | `stages/models_1_user.py`, міграція "Add User" |
| 3-4 Post.user_id + двосторонній зв'язок | `stages/models_2_relation.py`, міграція "Replace author with user relationship" |
| 5-6 користувачі, автори постів | `seed.py` |
| 7 пости user id=2 і id=1 | `python lab_demo.py` (`user.posts`) |
| 8 список авторів у формі | `app/posts/forms.py` (`author_id`), `routes.py` (`add_post`) |
| 9 Many-to-many Post-Tag | `app/models.py` (`post_tags`, `Tag`) |
| 10 append(), теги поста / пости тегу | `python lab_demo.py` |
| 11 SelectMultipleField тегів | `forms.py` (`tags`), `routes.py` |
| 12 стилізований вивід тегів | `app/templates/post_detail.html` (`.tag-link`) |
| 13 оптимізація запитів | `python measure.py plain` / `python measure.py optimized` |

## Скріни для звіту (пункти 7-13)

1. **п.7, 10** - вивід `python lab_demo.py`.
2. **п.8** - сторінка http://127.0.0.1:5000/add_post з розкритим списком Author.
3. **п.11** - та сама форма з виділеними кількома тегами; потім сторінка створеного поста.
4. **п.12** - сторінка поста (`/post/1`) зі стилізованими тегами.
5. **п.13** - два окремі запуски (окремі процеси = нові ORM-сесії):
   ```
   python measure.py plain
   python measure.py optimized
   ```
   Скрін коду, SQL-журналу та підсумку "Кількість SELECT". Занесіть числа в таблицю:

   | Варіант запиту | Кількість дописів | Кількість SELECT |
   |---|---|---|
   | Без .options() | (з виводу plain) | (з виводу plain) |
   | Із joinedload() та selectinload() | (з виводу optimized) | (з виводу optimized) |

   Орієнтир для 5 дописів, 2 авторів: без options приблизно 8 SELECT (1 на дописи + 2 на авторів, бо
   автор вантажиться один раз завдяки identity map + 5 на теги), з options - 2 SELECT.
   Записуйте те, що покаже ваш запуск.

## Перенесення у ваш існуючий проєкт

Скопіюйте з `app/models.py` класи `User`, `Tag`, `post_tags` і поля `user_id`, `user`, `tags` у вашу модель
`Post`, з `app/posts/forms.py` поля `author_id`, `tags`, а з `routes.py` код заповнення `choices`
та збереження. Далі зробіть `flask db migrate` та `flask db upgrade`.
