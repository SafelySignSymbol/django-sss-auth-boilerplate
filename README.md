# django sss auth boilerplate

## Install

```
$ pip install sss-auth
```

## Django側での設定
Djangoプロジェクトの ```INSTALLED_APPS```や```AUTHENTICATION_BACKENDS```に追加します

```
INSTALLED_APPS = (
    ...
    'sssauth.apps.sssAuthConfig',
    ...
)
AUTHENTICATION_BACKENDS = [
'django.contrib.auth.backends.ModelBackend',
'sssauth.backend.Web3Backend'
]
```

settings.pyにsssauthで使用される設定を追加します
```
SERVER_SECRET = '**************'
PUB = "************"
OWNER = "********"
NETWORK_TYPE = 152 # mainnet: 104, testnet: 152
EXPIRATION_DATE = 60 * 1 * 1 * 1000
```

ユーザーモデルの設定を行います
```
# Using CustomUser
AUTH_USER_MODEL = 'sssauth.MyUser'
```
URLパターンにsssauthのURLを追加します
```
urlpatterns = [
    path(r'^', include('sssauth.urls', namespace='sssauth')),
]
```

ログイン時の挙動を記述してURLに追加します
```
from sssauth.forms import LoginForm, SignupForm
urlpatterns = [
    path('signup/', CreateView.as_view(
        template_name='accounts/signup.html',
        form_class=SignupForm,
        success_url='/',
    ), name='signup'),
    path('login/', LoginView.as_view(
        redirect_authenticated_user=True,
        template_name='accounts/login.html',
    ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
```
## Setting
sss-authではサーバトークンの作成、復号に秘密鍵を使用します。秘密鍵はサーバ以外の用途で使用しないようにしてください。
|  項目名  |  用途  | 値|
| ---- | ---- |---- |
|  SERVER_SECRET  |  サーバが使用する秘密鍵  | String(64)|
|  PUB  | サーバが使用する公開鍵  |String(64)|
|  OWNER  |  サーバのSymbolアドレス(ハイフン無し)  |String(39)|
|  NETWORK_TYPE  |  ネットワークタイプ  |Int(メインネット:104, テストネット:152)|
|EXPIRATION_DATE|サーバが受け入れる暗号化メッセージの有効期限|Int(ミリ秒）|

設定例
```
SERVER_SECRET = '0000000000000000000000000000000000000000000000000000000000000000'
PUB = "3B6A27BCCEB6A42D62A3A8D02A6F0D73653215771DE243A63AC048A18B59DA29"
OWNER = "TCHBDENCLKEBILBPWP3JPB2XNY64OE7PYHHE32I"
NETWORK_TYPE = 152
EXPIRATION_DATE = 60 * 1 * 1 * 1000
```

## Documentation
その他の設定等や構成例についてはこちらをご覧ください
https://docs.sss-symbol.com/
