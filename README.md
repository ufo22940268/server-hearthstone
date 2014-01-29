#Hearthstone app server

负责为[android hearthstone app](https://github.com/ufo22940268/android-hearthstone.git)提供数据。同事负责去网络上抓取最新的套牌数据。

## 服务器运行方式

* `make env`
* `./manage server`


## 抓取数据

* `./manage.py import_data`
* `./manage.py import_cards_decks`
