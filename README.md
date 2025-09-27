# 🍳 T2000's Cooking Recipes Collection

歡迎來到我的料理食譜收藏！這是一個以 **MkDocs Material** 打造的個人食譜網站，收錄了我日常整理的各式料理與烘焙食譜。  
我會盡量在每道食譜中附上參考 YouTube 影片，方便跟著做。  

🌐 **網站瀏覽**: [T2000's Cooking Recipes Collection](https://t2000chris.github.io/cooking-recipes/)

---

## 📂 食譜分類
目前已經整理好的食譜分為以下幾個類別：

- 🥐 **Bakery**：麵包、蛋糕、甜品與各種烘焙食譜  
- 🥢 **Hong Kong Cuisine**：港式小菜、家常菜、醬料與小食  
- 🍣 **Japanese Cuisine**：日式料理與經典菜餚  
- 🥘 **Korean Cuisine**：韓式料理、泡菜、拌菜與湯品  
- 🥩 **Western Cuisine**：歐美菜式、牛扒、焗烤與醬汁  

每個資料夾底下的食譜以 **Markdown 檔案** 存放，並搭配封面圖片與標籤（tags）來方便搜尋。  

---

## 🔎 如何搜尋與導覽
- 左側的 **樹狀目錄** 可展開不同分類，直接點選食譜即可瀏覽  
- 每份食譜都標有 **標籤 (tags)**，例如 `bakery`, `main`, `beef`, `soup`，方便快速搜尋  
- 你也可以直接使用右上角的搜尋功能輸入食材、料理名稱（支援中英文）  

---

## 🛠️ 專案架構
```bash
cooking-recipes/
│
├── docs/                # 食譜文件 (Markdown)
│   ├── bakery/          # 烘焙食譜
│   ├── hongkong/        # 港式料理
│   ├── japanese/        # 日式料理
│   ├── korean/          # 韓式料理
│   ├── western/         # 西式料理
│   └── tags.md          # 標籤說明
│
├── images/              # 食譜配圖
├── mkdocs.yml           # MkDocs 設定檔
└── README.md            # 本文件
