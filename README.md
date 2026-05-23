# ClickUp MCP Server Entegrasyonu

[English](#english) | [Türkçe](#türkçe)

---

## Türkçe

ClickUp, yapay zeka asistanlarının (örneğin Claude Desktop, Cursor vb.) çalışma alanınızla güvenli bir şekilde etkileşime girmesini sağlamak için **Resmi ve Hosted bir MCP Sunucusu** sunmaktadır. Bu resmi sunucu kişisel API anahtarları (tokens) yerine **OAuth 2.1** tabanlı kullanıcı girişi (User Login) kullanır.

Ayrıca dilerseniz tamamen yerel çalışan ve kişisel API token ile çalışan kendi özel sunucumuzu da kullanabilirsiniz.

---

### Yöntem 1: Resmi ClickUp MCP Sunucusu (Önerilen - Şifresiz/Login ile)

Bu yöntem en güvenli ve resmi yoldur. Herhangi bir API anahtarı (token) oluşturmanıza gerek kalmadan doğrudan ClickUp kullanıcı girişinizle (OAuth) çalışır.

#### Claude Desktop İçin Kurulum Adımları:

1.  **Yapılandırma Dosyasını Açın:**
    *   **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json` dosyasını bir metin editörü ile açın.
    *   **Windows:** `%APPDATA%\Claude\claude_desktop_config.json` dosyasını açın.

2.  **Aşağıdaki Yapılandırmayı Ekleyin:**
    `mcpServers` bloğunun içerisine aşağıdaki resmi entegrasyonu ekleyin:

    ```json
    {
      "mcpServers": {
        "clickup-official": {
          "command": "npx",
          "args": ["-y", "mcp-remote", "https://mcp.clickup.com/mcp"]
        }
      }
    }
    ```

3.  **Claude Uygulamasını Yeniden Başlatın:**
    Claude Desktop uygulamasını tamamen kapatıp yeniden başlatın.

4.  **Giriş Yapın (OAuth Flow):**
    Claude uygulamasında ClickUp ile ilgili bir soru sorduğunuzda (örn: *"ClickUp alanlarımı göster"*), sistem sizi otomatik olarak ClickUp giriş ekranına yönlendirecektir. Giriş yapıp yetki verdikten sonra entegrasyon tamamlanmış olacaktır.

---

### Yöntem 2: Özel Yerel ClickUp MCP Sunucusu (API Token ile)

Eğer yerel olarak kendi kodunuzu koşturmak ve statik bir Kişisel API Token'ı ile yetkilendirme yapmak isterseniz, bu dizinde hazırladığımız özel sunucuyu kullanabilirsiniz.

#### 1. ClickUp API Token Edinme
1. ClickUp **Settings > Apps** sekmesine gidin.
2. **Personal API Token** başlığı altından yeni bir token oluşturun (Örn: `pk_123456_...`).

#### 2. Sunucuyu Derleme
```bash
npm install
npm run build
```

#### 3. Claude Desktop Yapılandırması:
Yapılandırma dosyanıza aşağıdaki bloğu ekleyin:

```json
{
  "mcpServers": {
    "clickup-local": {
      "command": "node",
      "args": ["/Users/nostromo/Desktop/Antigravity/_Projects/Click-up/dist/index.js"],
      "env": {
        "CLICKUP_API_TOKEN": "SİZİN_KİŞİSEL_API_TOKENİNİZ"
      }
    }
  }
}
```

---

## English

ClickUp offers an **Official Hosted MCP Server** which utilizes secure **OAuth 2.1 User Login** instead of static personal API tokens. 

Alternatively, you can run the custom offline-ready local MCP server built in this workspace using your Personal API Token.

---

### Method 1: Official ClickUp MCP Server (Recommended - OAuth User Login)

This is the most secure and official method. It connects to ClickUp's hosted MCP endpoint and prompts you to log in via browser when accessed.

#### Claude Desktop Setup:

1.  **Open Configuration File:**
    *   **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
    *   **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

2.  **Add Configuration:**
    Insert the following official config inside the `mcpServers` object:

    ```json
    {
      "mcpServers": {
        "clickup-official": {
          "command": "npx",
          "args": ["-y", "mcp-remote", "https://mcp.clickup.com/mcp"]
        }
      }
    }
    ```

3.  **Restart Claude Desktop:**
    Completely close and relaunch Claude.

4.  **Login & Authorize:**
    The first time you ask Claude to perform a ClickUp task, a browser login prompt will appear. Log in and click authorize to establish the connection.

---

### Method 2: Custom Local ClickUp MCP Server (API Token)

If you prefer to run a local self-hosted server using a static ClickUp Personal API Token:

#### 1. Generate Personal API Token
Go to ClickUp **Settings > Apps** and click **Generate Personal API Token** (starts with `pk_...`).

#### 2. Build the Server
```bash
npm install
npm run build
```

#### 3. Claude Desktop Configuration:
Add this block under `mcpServers`:

```json
{
  "mcpServers": {
    "clickup-local": {
      "command": "node",
      "args": ["/Users/nostromo/Desktop/Antigravity/_Projects/Click-up/dist/index.js"],
      "env": {
        "CLICKUP_API_TOKEN": "YOUR_PERSONAL_API_TOKEN"
      }
    }
  }
}
```
