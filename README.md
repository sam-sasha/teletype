Как запустить

Вариант запуска без кода
```
export TELETYPE_TOKEN="TOKEN"
export TELETYPE_DIALOG_ID="DIALOG_ID"
python app.py
```
Откройте файл docker-compose.yml и обязательно замените ВАШ_TOKEN_СЮДА на ваш реальный токен от Teletype (строка 10).
Откройте терминал в папке с этими файлами и выполните команду:
bash
```
docker-compose up -d --build
```
Дождитесь сборки (потребуется скачать образ Python, это займет минуту при первом запуске).

Как проверить, что всё работает
На этом же сервере выполните в терминале:
```
curl -X POST http://localhost:5050/alert \
-H "Content-Type: application/json" \
-d '{"status":"firing","title":"Тестовый алерт из Docker","alerts":[{"labels":{"alertname":"TestAlert","instance":"srv-01"}}]}'
```
