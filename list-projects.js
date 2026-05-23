import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();

const token = process.env.CLICKUP_API_TOKEN;

if (!token) {
  console.error("Error: CLICKUP_API_TOKEN is missing in process environment.");
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
    console.log("ClickUp API bağlantısı kuruluyor...");
    const teamRes = await client.get("/team");
    const teams = teamRes.data.teams;
    
    if (!teams || teams.length === 0) {
      console.log("Herhangi bir Workspace (Çalışma Alanı) bulunamadı.");
      return;
    }
    
    for (const team of teams) {
      console.log(`\n🏢 Çalışma Alanı (Workspace): ${team.name} (ID: ${team.id})`);
      
      // Fetch Spaces
      const spaceRes = await client.get(`/team/${team.id}/space`);
      const spaces = spaceRes.data.spaces;
      
      if (!spaces || spaces.length === 0) {
        console.log("  Bu çalışma alanında herhangi bir Alan (Space) bulunamadı.");
        continue;
      }
      
      for (const space of spaces) {
        console.log(`  🚀 Alan (Space): ${space.name} (ID: ${space.id})`);
        
        // Fetch Folders in Space
        const folderRes = await client.get(`/space/${space.id}/folder`);
        const folders = folderRes.data.folders;
        
        for (const folder of folders) {
          console.log(`    📁 Klasör (Folder): ${folder.name} (ID: ${folder.id})`);
          
          // Fetch Lists in Folder
          const listRes = await client.get(`/folder/${folder.id}/list`);
          const lists = listRes.data.lists;
          for (const list of lists) {
            console.log(`      📝 Liste (List): ${list.name} (ID: ${list.id})`);
          }
        }
        
        // Fetch Folderless Lists in Space
        const listRes = await client.get(`/space/${space.id}/list`);
        const lists = listRes.data.lists;
        if (lists && lists.length > 0) {
          console.log(`    📁 Klasörsüz Listeler:`);
          for (const list of lists) {
            console.log(`      📝 Liste (List): ${list.name} (ID: ${list.id})`);
          }
        }
      }
    }
  } catch (error) {
    const errorDetails = error.response ? JSON.stringify(error.response.data) : error.message;
    console.error("Projeleri çekerken hata oluştu:", errorDetails);
  }
}

main();
