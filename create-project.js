import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();

const token = process.env.CLICKUP_API_TOKEN;
const spaceId = "901810925356"; // Burak Ozdelice's Workspace -> Team Space ID
const listName = "Floor Plan Visuals Mobile App Design";

if (!token) {
  console.error("Hata: CLICKUP_API_TOKEN eksik.");
  process.exit(1);
}

const client = axios.create({
  baseURL: "https://api.clickup.com/api/v2",
  headers: {
    "Authorization": token,
    "Content-Type": "application/json"
  }
});

async function main() {
  try {
    console.log(`ClickUp'ta yeni proje/liste oluşturuluyor: "${listName}"...`);
    const response = await client.post(`/space/${spaceId}/list`, {
      name: listName
    });
    console.log(`\n✓ Proje başarıyla oluşturuldu!`);
    console.log(`📋 Proje Adı: ${response.data.name}`);
    console.log(`🆔 Liste (Proje) ID: ${response.data.id}`);
  } catch (error) {
    const errorDetails = error.response ? JSON.stringify(error.response.data) : error.message;
    console.error("Proje oluşturulurken hata:", errorDetails);
  }
}

main();
