シンプルなTodo管理APIです。panorama-fastapiと同様のオニオンアーキテクチャを採用しています。

## 機能

- ユーザー認証（JWT）
- Todo CRUD操作
- RESTful API設計
- 自動API仕様書生成

## API エンドポイント

### 認証
- `POST /api/v1/auth/signup` - ユーザー登録
- `POST /api/v1/auth/login` - ログイン
- `GET /api/v1/auth/me` - 現在のユーザー情報

### Todo管理
- `GET /api/v1/todos` - Todo一覧取得
- `GET /api/v1/todos/{todo_id}` - 特定Todo取得
- `POST /api/v1/todos` - Todo作成
- `PUT /api/v1/todos/{todo_id}` - Todo更新
- `DELETE /api/v1/todos/{todo_id}` - Todo削除

## セットアップ

### 1. リポジトリをクローン

```bash
git clone <repository-url>
cd sample-fastapi
```

### 2. 環境変数を設定

```bash
cp .env.example .env
# .envファイルを編集して適切な値を設定
```

### 3. Docker Composeで起動

```bash
# ビルドして起動
docker-compose up --build

# バックグラウンドで起動
docker-compose up -d

# 停止
docker-compose down
```

# うまく立ち上がらなかったら。。。
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### 4. ローカル開発（仮想環境）

```bash
# 仮想環境作成
python -m venv venv

# 仮想環境有効化（Windows）
venv\Scripts\activate

# 仮想環境有効化（Mac/Linux）
source venv/bin/activate

# 依存関係インストール
pip install -r requirements.txt

# PostgreSQLを別途起動後、アプリケーション起動
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API仕様書

起動後、以下のURLでAPI仕様書を確認できます：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 使用例

### 1. ユーザー登録

```bash
curl -X POST "http://localhost:8000/api/v1/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "Test User",
    "password": "password123"
  }'
```

### 2. ログイン

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

レスポンス例：
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Todo作成

```bash
curl -X POST "http://localhost:8000/api/v1/todos" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, bread, eggs",
    "completed": false
  }'
```

### 4. Todo一覧取得

```bash
curl -X GET "http://localhost:8000/api/v1/todos" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5. Todo更新

```bash
curl -X PUT "http://localhost:8000/api/v1/todos/TODO_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, bread, eggs, cheese",
    "completed": true
  }'
```

### 6. Todo削除

```bash
curl -X DELETE "http://localhost:8000/api/v1/todos/TODO_ID" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## プロジェクト構造

```
sample-fastapi/
├── app/
│   ├── main.py                 # エントリーポイント
│   ├── api/                    # API層
│   │   ├── dependencies/       # 依存関係
│   │   └── routes/            # エンドポイント
│   ├── core/                  # コア設定
│   ├── domain/               # ドメイン層
│   │   ├── models/           # SQLAlchemyモデル
│   │   └── schemas/          # Pydanticスキーマ
│   ├── services/             # ビジネスロジック
│   └── utils/               # ユーティリティ
├── requirements.txt
├── Dockerfile
├── docker-compose.yaml
└── README.md
```

## 開発

### テストの実行

```bash
# テストコードを追加後
pytest
```

### コードフォーマット

```bash
# Black（コードフォーマッター）
black app/

# isort（インポート順序）
isort app/

# flake8（リンター）
flake8 app/
```

## 環境変数

| 変数名 | 説明 | デフォルト値 |
|--------|------|-------------|
| DATABASE_URL | PostgreSQL接続URL | - |
| SECRET_KEY | JWT署名用秘密鍵 | - |
| ALGORITHM | JWT署名アルゴリズム | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | トークン有効期限（分） | 60 |

## Flutter連携例

```dart
class TodoApi {
  static const String baseUrl = 'http://localhost:8000/api/v1';
  static String? _token;

  static Future<void> login(String email, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'email': email, 'password': password}),
    );
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      _token = data['access_token'];
    }
  }

  static Future<List<Todo>> getTodos() async {
    final response = await http.get(
      Uri.parse('$baseUrl/todos'),
      headers: {
        'Authorization': 'Bearer $_token',
        'Content-Type': 'application/json',
      },
    );
    
    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((json) => Todo.fromJson(json)).toList();
    }
    
    throw Exception('Failed to load todos');
  }
}
```

## トラブルシューティング

### コンテナが起動しない場合

#### 1. ログ確認
```bash
# アプリケーションログ確認
docker-compose logs app

# データベースログ確認
docker-compose logs db

# 全体ログ確認
docker-compose logs
```

#### 2. 完全リセット
```bash
# 全てのコンテナ・ボリューム削除
docker-compose down -v
docker system prune -f

# 再ビルド
docker-compose build --no-cache
docker-compose up
```

#### 3. 個別確認
```bash
# データベースのみ起動
docker-compose up db

# 別ターミナルでアプリのみ起動
docker-compose up app
```

### よくあるエラーと解決方法

#### エラー: "ModuleNotFoundError"
```bash
# 依存関係の再インストール
docker-compose build --no-cache
```

#### エラー: "Connection refused"
```bash
# データベース接続確認
docker-compose exec db psql -U postgres -d sample_db -c "SELECT 1;"
```

#### エラー: "Port already in use"
```bash
# ポート使用状況確認
lsof -i :8000

# docker-compose.yamlのポートを変更
# ports: "8001:8000"
```

### API動作確認

#### 1. ブラウザ確認
- http://localhost:8000/docs - Swagger UI
- http://localhost:8000/health - ヘルスチェック
- http://localhost:8000/ - メイン

#### 2. コマンドライン確認
```bash
# ヘルスチェック
curl http://localhost:8000/health

# ユーザー登録テスト
curl -X POST "http://localhost:8000/api/v1/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "Test User",
    "password": "password123"
  }'
```

### 開発時の注意点

#### Docker Composeの警告解消
```bash
# docker-compose.yamlの最初の行を削除
# version: '3.8' ← この行を削除
```

#### 環境変数確認
```bash
# 現在の環境変数確認
docker-compose exec app env | grep DATABASE_URL
docker-compose exec app env | grep SECRET_KEY
```

#### データベース直接接続
```bash
# PostgreSQLに直接接続
docker-compose exec db psql -U postgres -d sample_db

# テーブル一覧確認
\dt

# 終了
\q
```

### パフォーマンス改善

#### 1. 開発時のホットリロード確認
- `app/` フォルダ内のファイル変更で自動リロード
- ログで "Reloading..." メッセージを確認

#### 2. データベース最適化
```bash
# 不要なデータ削除
docker-compose exec db psql -U postgres -d sample_db -c "VACUUM;"
```

#### 3. Docker最適化
```bash
# 不要なイメージ削除
docker image prune -f

# キャッシュクリア
docker builder prune -f
```

### 本番環境への準備

#### 1. 環境変数の変更
```bash
# 強力なSECRET_KEY生成
openssl rand -hex 32

# .env.production ファイル作成
cp .env.example .env.production
# SECRET_KEYを変更
# ACCESS_TOKEN_EXPIRE_MINUTES=15 (短縮)
```

#### 2. セキュリティチェック
```bash
# 開発用の危険な設定確認
grep -r "password" .
grep -r "localhost" .
grep -r "allow_origins.*\*" .
```

## ライセンス

MIT License
# sample-fastapi
