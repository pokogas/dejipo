# デジポ


#何が出来るの？
ポイントを作れたり作ったポイントで取引が出来ます！
イベントとかで使用したい場合は招待制にするなどして使えます！

# デプロイ
 
```bash
docker-compose -f docker-compose.yml -f prod.yml build
```
```bash
docker-compose -f docker-compose.yml -f prod.yml up
```
#使用した技術
- フロントエンド
   - nuxt.js
   - Vuetify.js

- バックエンド
   - Django-rest-framework

- データベース
   - PostgreSQL

- その他
   - nginx
   - Docker
   

#雑談
元々Djangoのみで開発をしていたのですが、SPAなどSSRの開発に興味を持ちリファレンスなど読みまくりながら作った為最初と最後ではコードの書き方が全然違うところは許してください。
