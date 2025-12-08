// Script de scraping para Tamarac usando Puppeteer y Chrome real


const puppeteer = require('puppeteer-core'); // usar puppeteer-core para conectarse a Chrome existente
const fs = require('fs');
const readline = require('readline');
const { exec } = require('child_process');
const path = require('path');

// --- Ruta a Chrome en Windows ---
const chromePath = `"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"`;
// --- Carpeta temporal para perfil ---
const userDataDir = `"${path.join(__dirname, 'chrome-temp-debug')}"`;
// --- Puerto de remote debugging ---
const debugPort = 9222;

// Abrir Chrome con Remote Debugging
exec(`${chromePath} --remote-debugging-port=${debugPort} --user-data-dir=${userDataDir} --new-window`, (err) => {
  if (err) {
    console.error('Error al abrir Chrome:', err);
  }
});

(async () => {
  // Esperar un poco para que Chrome inicie
  await new Promise(r => setTimeout(r, 3000));

  // Conectar Puppeteer a tu Chrome real
  const browser = await puppeteer.connect({
    browserURL: `http://127.0.0.1:${debugPort}`, // puerto de remote debugging
  });

  const pages = await browser.pages();
  const page = pages[0]; // usar la primera pestaña abierta

  page.on('dialog', async dialog => { 
      console.log('Alerta detectada:', dialog.message());
      await dialog.dismiss(); 
  });

  // Ir a la página de permisos
  await page.goto('https://e-gov.tamarac.org/Click2GovBP/selectpermit.html', { waitUntil: 'networkidle2' });

  // --- 1. Seleccionar opción 4 del dropdown principal ---
  await page.waitForSelector('#searchMethod');
  await page.evaluate(() => {
    const select = document.querySelector('#searchMethod');
    select.selectedIndex = 3;
    select.dispatchEvent(new Event('change', { bubbles: true }));
  });

  // --- 2. Escribir en el input ---
  await page.waitForSelector('#searchName');
  await page.click('#searchName');
  await page.type('#searchName', 'roof');

  console.log("Formulario listo. Haz click manualmente en el botón de submit...");

  // --- Preparar readline para input manual ---
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  let allData = [];

  while (true) {
    // --- Esperar que aparezca la tabla ---
    await page.waitForSelector('#DataTables_Table_0 tbody tr', { timeout: 0 });
    console.log("Tabla de resultados detectada.");

    // --- Seleccionar opción de filas por página ---
    await page.waitForSelector('#DataTables_Table_0_length select');
    await page.select('#DataTables_Table_0_length select', '25'); // o '50', '100'
    // esperar a que la tabla se refresque
    await new Promise(resolve => setTimeout(resolve, 1000));

    // --- Iterar filas ---
    const rowsData = await page.$$eval('#DataTables_Table_0 tbody tr', rows => {
      return rows.map(row => {
        const cells = row.querySelectorAll('td');
        const obj = {};
        cells.forEach((cell, index) => {
          obj[`column_${index+1}`] = cell.innerText.trim();
        });
        return obj;
      });
    });

    allData = allData.concat(rowsData);
    console.log(`Se agregaron ${rowsData.length} filas. Total acumulado: ${allData.length}`);

    // --- Esperar input del usuario ---
    const answer = await new Promise(resolve => {
      rl.question('Cuando quieras continuar a otra pestaña escribe ENTER, o "OK" para terminar: ', resolve);
    });

    if (answer.trim().toUpperCase() === 'OK') break;

    console.log("Esperando que cambies de pestaña y hagas submit manual...");
  }

  rl.close();

  // --- Guardar JSON final ---
  fs.writeFileSync('resultadosTamarac.json', JSON.stringify(allData, null, 2));
  console.log('Todos los datos guardados en resultados.json');

})();
