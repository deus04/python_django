# Практическая работа 14

## Цель практической работы
Научиться применять Django REST framework для получения (в том числе фильтрации и поиска), создания, обновления, удаления сущностей в Django-приложении.

### Что нужно сделать
Воспользуйтесь кодовой базой из пройденных модулей или файлами из репозитория с практической работой.
1. Установите Django REST framework.
2. Подключите Django REST framework в настройках проекта:
   - добавьте rest_framework в INSTALLED_APPS; 
   - укажите словарь REST_FRAMEWORK, добавьте туда стандартные настройки для пагинации (DEFAULT_PAGINATION_CLASS, PAGE_SIZE).
3. Создайте сериализатор для модели (на основе ModelSerializer):
   - Product, 
   - Order.
4. Создайте ViewSet для моделей (на основе ModelViewSet):
   - Product,
   - Order.
5. Через DefaultRouter подключите созданные ViewSet к urls в приложении ShopApp:
   - подключите ViewSet для Product к routers,
   - подключите ViewSet для Order к routers,
   - подключите ссылки из routers к urlpatterns.
6. Установите django-filters.
7. Обновите настройки проекта:
   - установите приложение django_filters (добавив в список INSTALLED_APPS); 
   - укажите стандартный бэкенд для фильтрации DEFAULT_FILTER_BACKENDS.
8. Добавьте правила фильтрации на ViewSet для Product:
   - правила поиска через SearchFilter (фильтр и поля, по которым можно фильтровать); 
   - правила сортировки через OrderingFilter (фильтр и поля, по которым можно сортировать).
9. Добавьте правила фильтрации на ViewSet для Order:
   - правила фильтрации через DjangoFilterBackend (фильтр и поля, по которым можно фильтровать);
   - правила сортировки через OrderingFilter (фильтр и поля, по которым можно сортировать).


### Что оценивается
- В настройках проекта settings.py: 
   - указаны настройки в REST_FRAMEWORK:
      - DEFAULT_PAGINATION_CLASS; 
      - PAGE_SIZE;
      - DEFAULT_FILTER_BACKENDS.
   - установлены приложения:
      - rest_framework;
      - django_filters.
   - Созданы сериализаторы на основе ModelSerializer для моделей:
      - Product,
      - Order.
   - Созданы ViewSet на основе ModelViewSet для моделей:
      - Product,
      - Order.
   - На ViewSet добавлены правила фильтрации:
      - для Product:
         - правила поиска через SearchFilter;
         - правила сортировки через OrderingFilter;
      - для Order:
         - правила фильтрации через DjangoFilterBackend;
         - правила сортировки через OrderingFilter.


### Как отправить работу на проверку
Сдайте практическую работу через Skillbox GitLab. В поле для сдачи практической работы напишите «Сделано» и прикрепите ссылку на репозиторий.
