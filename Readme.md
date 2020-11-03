##Аппаратное обеспечение:
 - Raspberry Pi c usb адаптером RS-232 или RS-485 (в зависимости от версии ОМ-310)
 - [ОМ-310](https://novatek-electro.com/docs/doc_om-310.pdf)
 - Опционально: [реле](https://www.chipdip.ru/product/rdc1-1rta-relay-elektronnye-vojska?utm_source=google&utm_medium=cpc&position_type={position_type}|k50id|pla-293946777986|cid|11128065280|aid|464684997822|gid|105934773021&utm_campaign=G_tovarnieobjavlenija&utm_content=text1_ga&utm_term=) 
 
 Файл конфигурации располагается в каталоге /etc/om310, по умолчанию используется 80 порт для веб сервера и GPIO 17 для управление реле
 
##Функции
 - мониторинг качества питания через json, доступна конфигурация для Home Assistant (/opt/om310/extra/home_assistant)
 - внешние управление реле отключения неприоритетной нагрузкой (в этом случае не используется реле ОМ-310)
 
 ##TODO:
 - Исользовать modbus (включена в стандартный репозиторий) библитеку вместо minimalmodbus
 - Авторизация по токенам
 - Конфигурирование ОМ-310 через интерефейс HA и\или через веб интерфейс приложения
 - Изучение возможожности использование реле ОМ-310 вне зависимости от внутренних настроек ОМ-310
 - Изучение возможности плавной регулеровки мощности электрокотлов
 - Настроить CI для сборки deb пакета
 
 ##Назначение:
 - Мониторинг качества ввода напряжения
 - Отключение неприоритетной нагрузки при превышении пороговых значений (к примеру электрокотла при дефеците подведенной мощности)
 
  