# HTCCCS - 花東青少年合唱音樂營選課系統

一個基於 Django 的選課系統 Web App，專為花東青少年合唱音樂營設計，支援學生線上選課、志工查詢與管理員後台管理。

## 目錄
- 專案概述
- 系統功能
- 安裝與部署
- 操作流程說明
- 技術棧
- 專案結構
- 資料模型
- 主要頁面
- 開發注意事項
- 常見問題
- 聯絡資訊

## 專案概述

本系統提供完整的選課流程管理，包含：
- **學生端**：線上選課、查詢選課結果
- **志工端**：查詢學員資料與選課結果
- **管理端**：課程管理、選課結果調整、資料匯入匯出、一鍵生成選課結果影印檔

### 系統功能

- 介面簡易明瞭，無程式基礎也可以輕鬆操作
- 國中部/高中部分流進行志願選填
- 雙階段選課機制（第一次/第二次選課）
- Excel 批量資料匯入/匯出
- 由演算法自動生成選課結果
- 依照特定需求手動調整選課結果
- 一鍵生成選課結果影印檔
- Docker 容器化

## 技術棧

- **後端框架**: Django 4.2.17
- **資料庫**: MySQL 8.0
- **Web 伺服器**: Nginx + Gunicorn
- **容器化**: Docker + Docker Compose
- **前端**: HTML/CSS/JavaScript (Vanilla JS)
- **數據處理**: Pandas, Openpyxl

## 安裝與部署

### PythonAnywhere 部署（推薦）

PythonAnywhere 是一個完全托管的 Python 環境，無需設置伺服器，適合快速部署。

#### 前置準備

1. **註冊 PythonAnywhere 帳戶**
   - 訪問 [pythonanywhere.com](https://www.pythonanywhere.com)
   - 選擇免費方案，如要部署

2. **在本地準備專案**
   - 確保所有代碼已推送至 GitHub（推薦做法）
   - 更新 `requirements.txt` 確保所有依賴正確

#### 步驟 1：設置 Web App

1. 登入 PythonAnywhere 帳戶
2. 點擊 **Web**  → **Add a new web app**
3. 選擇 **Manual configuration** → 選擇 **Python 3.10**（或相容版本）

#### 步驟 2：複製專案

在 PythonAnywhere **Bash 終端機**執行：

```bash
# 進入主目錄
cd ~

# 克隆專案
git clone <your-github-repo-url> HTCCCS

# 進入 Django 項目目錄
cd HTCCCS/django_project
```

#### 步驟 3：設置虛擬環境

```bash
# 進入主目錄
cd ~

# 建立虛擬環境（PythonAnywhere 推薦位置）
mkvirtualenv --python=/usr/bin/python3.10 htcccs_env

# 啟動虛擬環境
workon htcccs_env

# 安裝依賴
pip install -r ~/HTCCCS/django_project/requirements.txt

# 確保已安裝 gunicorn
pip install gunicorn
```

#### 步驟 4：配置 MySQL 資料庫

1. 在 PythonAnywhere **Databases** 選項卡中建立 MySQL 資料庫
   - 記下資料庫名稱、用戶名與密碼

2. 編輯 `django_project/settings.py`：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_username$database_name',  # PythonAnywhere 格式
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'your_username.mysql.pythonanywhere-services.com',
        'PORT': '3306',
    }
}
```

3. 推送設置變更至 GitHub 並在 PythonAnywhere 中拉取最新代碼：
```bash
cd ~/HTCCCS
git pull origin main
```

#### 步驟 5：執行數據庫遷移

```bash
cd ~/HTCCCS/django_project
workon htcccs_env
python manage.py migrate
python manage.py createsuperuser  # 建立管理員帳戶
python manage.py collectstatic --noinput  # 收集靜態檔案
```

#### 步驟 6：配置 WSGI 文件

PythonAnywhere 會自動生成 WSGI 文件。編輯 `/var/www/your_username_pythonanywhere_com_wsgi.py`：

```python
import os
import sys

# 添加專案路徑
path = '/home/your_username/HTCCCS/django_project'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'django_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

#### 步驟 7：配置 Web App 設定

1. 在 PythonAnywhere **Web** 選項卡中編輯 Web App：
   - **Virtualenv**: `/home/your_username/.virtualenvs/htcccs_env`
   - **WSGI configuration file**: `/var/www/your_username_pythonanywhere_com_wsgi.py`

2. 配置 **Static files**：
   ```
   URL: /static/
   Directory: /home/your_username/HTCCCS/django_project/staticfiles/
   ```

3. 點擊 **Reload** 重啟 Web App

#### 步驟 8：配置自訂域名（選用）

1. 在 PythonAnywhere **Web** 選項卡中修改域名設置
2. 在 Django `settings.py` 中更新 `ALLOWED_HOSTS`：
```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

3. 推送變更並重啟 Web App

#### 步驟 9：上傳資料

在 **Bash 終端機**執行：

```bash
cd ~/HTCCCS/django_project

# 建立資料庫目錄
mkdir -p media

# 上傳資料（例如學生基本資料、課程資料等）
# 可透過管理後台上傳或使用終端機命令
```

#### 步驟 10：測試與驗證

1. 訪問你的 PythonAnywhere 域名
2. 測試各功能：
   - 學生登入與選課
   - 管理員後台
   - 資料查詢

#### 常見問題排解

**問題 1：資料庫連線失敗**
- 確認資料庫名稱格式：`your_username$database_name`
- 確認用戶名與密碼正確
- 在 **Databases** 中檢查資料庫狀態

**問題 2：靜態檔案 404**
```bash
cd ~/HTCCCS/django_project
workon htcccs_env
python manage.py collectstatic --noinput
```
然後在 PythonAnywhere Web 選項卡重啟 App

**問題 3：匯入錯誤或模塊缺失**
```bash
workon htcccs_env
pip list  # 檢查已安裝的包
pip install --upgrade <package-name>  # 升級特定包
```

**問題 4：查看錯誤日誌**
- 在 PythonAnywhere **Web** 選項卡中查看 **Error log** 和 **Access log**

#### 定期維護

1. **每天檢查日誌**：在 Web 選項卡檢查錯誤日誌
2. **定期備份資料庫**：
```bash
cd ~/backups
mysqldump -h your_username.mysql.pythonanywhere-services.com \
  -u your_username -p your_username\$database_name > backup_$(date +%Y%m%d).sql
```

3. **更新代碼**：
```bash
cd ~/HTCCCS
git pull origin main
python manage.py migrate  # 如有新遷移
python manage.py collectstatic --noinput
# 重啟 Web App
```

## 操作流程說明

1. 請參考 `DBzip.zip` 中的 Excel 檔案格式將志工、學生基本資料填入
2. 請將志工大頭貼以「志工 Camp Name」作為檔名存進 `pfp` 資料夾
3. 將基本資料的 `DBzip` 壓縮
4. 進入**主頁**後點選`選課組`，以密碼`HTCCcs2025`登入，進入`修改資料`頁面，在`上傳資料壓縮檔`欄位選取檔案，並點選`上傳檔案`。若上傳失敗，請依照置頂提示修改 Excel 檔案。
5. 登出後，進入**學員頁面**確認是否能正常登入，志工課程、大頭貼是否也已經一併完整匯入。
6. 在`選課組`的`跑志願與結果`頁面中可以確認還有哪些學員還沒選課。確認皆已完成選課之後點選第一/二次選課標題旁「箭頭向下」的按鈕進行志願分發，稍待約30秒直到「志願分發完成」出現。
7. 志願分發完成之後點選下方的`下載點名總表`取得點名表的 Excel檔；`下載選課結果`則會彈出另一個視窗，按下`Crtl+P`（Ｍac:`Command+P`），並在`顯示更多設定`下拉選單中勾取`顯示背景圖形`。點選`列印`之後就會存成pdf檔，或是直接在有連線的印表機進行列印。
9. 志工頁面以密碼`htcccs_v`登入，選取國/高中部、小隊就可以查看選課結果。 

## 專案結構

```
django_project/
├── django_app/              # 主應用程式
│   ├── models.py           # 資料模型（Student, Course, Selection等）
│   ├── views.py            # 視圖邏輯（1400+ 行）
│   ├── urls.py             # URL 路由
│   ├── auth_utils.py       # 學生認證工具
│   └── migrations/         # 資料庫遷移檔案
├── templates/              # HTML 模板
│   ├── stdLogin.html       # 學生登入
│   ├── select_form.html    # 選課表單
│   ├── dashboard.html      # 管理員後台
│   └── ...
├── static/                 # 靜態資源
│   ├── style.css
│   ├── select_form.js      # 選課表單邏輯
│   └── double_check.js     # 確認頁面邏輯
├── backups/                # 資料庫備份
├── docker-compose.yml      # Docker 編排配置
├── Dockerfile              # Docker 映像檔配置
├── nginx.conf              # Nginx 配置
└── requirements.txt        # Python 依賴
```

## 資料模型

### 核心模型

- **Student**: 學員資料（學號、姓名、小隊、聲部、國/高中）
- **Course**: 一般課程
- **SpecialCourse**: 國中部/高中部專屬課程
- **Section**: 節次（時段）
- **Selection**: 學生選課志願
- **SelectionResult**: 選課結果（使用 Generic Foreign Key）
- **Volunteer**: 志工資料
- **AdminSetting**: 系統設定

## 使用者角色與權限

系統定義三種角色權限：

1. **學生 (Student)** - `is_student`
   - 登入方式：學號 + 姓名
   - 功能：選課、查詢選課結果

2. **志工 (Volunteer)** - `is_volunteer`
   - 登入方式：營隊姓名 + 密碼
   - 功能：查詢小隊與課程選課結果

3. **管理員/選課組 (Admin/CS)** - `is_cs`, `is_admin`
   - 登入方式：帳號 + 密碼
   - 功能：完整系統管理

## 主要頁面

### 學生端
- `/stdLogin` - 學生登入
- `/std_index` - 選課導覽頁
- `/select_form/<form_stage>` - 選課表單（1 或 2）
- `/select_form/confirm` - 確認選課結果
- `/success` - 送出成功頁面

### 志工端
- `/Volunteer_Login` - 志工登入
- `/volunteer_dashboard` - 志工儀表板
- `/team_results_lookup/` - 小隊選課結果查詢
- `/course_results_lookup/` - 課程選課結果查詢

### 管理端
- `/csLogin` - 管理員登入
- `/dashboard` - 管理員儀表板
- `/dashboard/updateData` - 課程與學生資料更新
- `/dashboard/result` - 選課結果管理
- `/dashboard/result/print_results_table` - 列印選課結果
- `/dashboard/result/generate_xlsx` - 產生 Excel 點名表
- `/upload_zip` - 批量上傳資料（ZIP 壓縮檔）
- `/upload_result_change` - 上傳選課結果調整檔案

## 開發注意事項

### 資料庫備份
系統會定期備份資料庫至 `backups/` 目錄：
```bash
docker exec mysql_container mysqldump -u test_user -p test_db > backup.sql
```

### 靜態檔案
- 開發環境: `STATICFILES_DIRS = [BASE_DIR / 'static']`
- 生產環境: `STATIC_ROOT = BASE_DIR / 'staticfiles'`
- 收集靜態檔案: `python manage.py collectstatic`

### 生產部署設定
編輯 `settings.py`:
```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'your-ip']
SECRET_KEY = 'your-secret-key'  # 請更換為安全的密鑰
```

## 常見問題

### ImportError: Couldn't import Django（無法導入 Django）

**錯誤訊息**: `ImportError: Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?`

**原因**: 虛擬環境未激活或 Django 未安裝在當前 Python 環境中

**解決方案**:

1. **創建虛擬環境**（如果尚未創建）:
```bash
cd django_project
python3 -m venv venv
```

2. **激活虛擬環境**:
```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. **安裝依賴**:
```bash
pip install -r requirements.txt
```

4. **確認 Django 已安裝**:
```bash
python -c "import django; print(django.get_version())"
# 應該輸出: 4.2.17
```

5. **啟動伺服器**:
```bash
python manage.py runserver
```

**注意**: 每次開啟新的終端視窗時，都需要重新激活虛擬環境（步驟 2）

### MySQL 連線超時或系統檢查卡住

**症狀**: 執行 `python manage.py runserver` 時，系統檢查卡在 "Performing system checks..." 不動

**原因**: MySQL 資料庫未運行或無法連線

**解決方案**:

**選項 1 - 使用 Docker 啟動 MySQL**:
```bash
cd django_project
docker-compose up -d mysql
# 等待 MySQL 啟動（約 10-20 秒）
python manage.py runserver
```

**選項 2 - 本地安裝 MySQL**:
```bash
# macOS
brew install mysql
brew services start mysql

# 創建資料庫
mysql -u root -p
CREATE DATABASE htcccs CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# 執行遷移
python manage.py migrate
```

**選項 3 - 暫時使用 SQLite（開發測試用）**:

編輯 `django_project/settings.py`，暫時將資料庫改為 SQLite:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

然後執行:
```bash
python manage.py migrate
python manage.py runserver
```

### Docker 容器無法啟動
- 檢查 3307 端口是否被佔用
- 確認 MySQL 健康檢查通過: `docker-compose logs mysql`

### 靜態檔案 404
```bash
python manage.py collectstatic --noinput
docker-compose restart nginx
```

### 資料庫連線失敗
- 確認 `settings.py` 中的資料庫配置
- 檢查 MySQL 容器狀態: `docker ps`
- 查看錯誤日誌: `docker-compose logs web`

### 權限錯誤 (Permission Denied)
```bash
# 確保 manage.py 有執行權限
chmod +x manage.py

# 或使用 python 明確調用
python manage.py runserver
```

## 聯絡資訊

如有問題或建議，請寄信至 wildiam356@gmail.com。

---

**最後更新**: 2026年2月
