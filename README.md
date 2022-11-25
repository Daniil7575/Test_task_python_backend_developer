# Тестовое задание
1) Cклонируйте репозиторий в удобную папку (желательно, чтобы в пути не было кириллицы)
```
git clone https://github.com/Daniil7575/Test_task_python_backend_developer.git
```

2) Перейдите в папку ***stripe_project*** и соберите, а затем запустите контейнер
```
sudo docker compose build
sudo docker compose up
```

3) По желанию создайте суперпользователя на сервере для взаимодействия с админ-панелью.
```
sudo docker compose exec web python3 manage.py createsuperuser
```

4) Зайдите на веб интерфейс по адресу - `http://0.0.0.0:8000/item/`

Эндпоинты:

`item/` - каталог товаров

`item/{item_id}/` - страница с подробным описанием товара

`buy/{item_id}/` - формирование stripeCheckoutSession

`{order_id}/success/` - страница после успешной оплаты заказа

`{order_id}/cancel/` - отмена заказа (с сохранением корзины)

`add-to-cart/{item_id}/` - добавление продукта в корзину

`create/` - создание заказа в модели Order и перенаправление на формирование stripeCheckoutSession

`clear-cart/` - очистка корзины

`asd` - asd
