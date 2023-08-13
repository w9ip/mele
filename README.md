# mele

## Когда вычисляются наборы запросов QuerySet
Создание набора запросов QuerySet, их фильтрация, исключение некоторых наборов данных никак не затрагивает саму БД (т. е. никакой запрос не будет произведен к БД).

БД затрагивается только в следующих случаях:
- При первом их прокручивании в цикле.
- При слайсинге, например Post.objects.all()[:3]
- При их кешировании или консервации в поток байтов.
- При вызове на них функции repr(), len(), list().
- При их проверке в операциях bool(), or, and или if.

## Примечание метода exclude()
Определенные результаты можно исключать из набора запросов QuerySet, используя метод exclude(), Например, все посты, опубликованные в 2022 году, заголовки которых не начинаются со слова Why (Почему),можно получить следующим образом:
```py
>>> Post.objects.filter(publish__year=2022).exclude(title__startswith='Why')
```

##
