//mi segundo push

//IMPORT LIBRERIAS
const puppeteer = require('puppeteer');
const fs = require('fs');
const csv = require('csv-parser');

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
const OUTPUT_DIR = './data';

// Crear carpeta de salida si no existe
if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR);

// Leer CSV y devolver array de folios
async function leerCSV(filePath) {
    return new Promise((resolve, reject) => {
        const folios = [];
        fs.createReadStream(filePath)
            .pipe(csv())
            .on('data', (row) => {
                if (row.Folio) folios.push(row.Folio);
            })
            .on('end', () => resolve(folios))
            .on('error', (err) => reject(err));
    });
}

(async () => {
    const folios = await leerCSV('sr_clean2.csv');
    const resultados = [];

    const browser = await puppeteer.launch({
        headless: false, // cambiar a true cuando esté validado
        defaultViewport: null,
        args: ['--start-maximized']
    });

    for (const folio of folios) {
        const page = await browser.newPage(); // Abrir nueva pestaña por folio
        try {
            // Ir a la página de búsqueda
            await page.goto('https://web.bcpa.net/BcpaClient/#/Record-Search', { waitUntil: 'networkidle2' });

            // Esperar input y escribir folio
            await page.waitForSelector('#txtField', { visible: true });
            await page.click('#txtField', { clickCount: 3 }); // limpiar input
            await page.type('#txtField', folio);

            // Clic en buscar
            await page.waitForSelector('#searchButton', { visible: true });
            await page.evaluate(() => document.querySelector('#searchButton').click());

            // Esperar que cargue la página de detalles
            await page.waitForSelector("#hideRecInfoTab", { visible: true });
            await delay(2000);

            // Extraer los datos
            const data = await page.evaluate(() => {
                const eff_yr = document.querySelector("#effectiveAgeId")?.innerText || '';
                const yr_built = document.querySelector("#actualAgeId")?.innerText || '';
                const dpty_app = document.querySelector("#deputyAppraiserNameId")?.innerText || '';
                const unit_beds_baths = document.querySelector("#unitsBedsBathsId")?.innerText || '';
                const property_use = document.querySelector("#useCodeId")?.innerText || '';
                const mkt_value = document.querySelector("#justCurrentYearId")?.innerText || '';
                const house_size = document.querySelector("#improvementAssessment")?.innerText || '';
                return { eff_yr, yr_built, dpty_app, unit_beds_baths, property_use, mkt_value, house_size };
            });

            resultados.push({ folio, ...data });
            console.log(`Datos extraídos correctamente para folio: ${folio}`);

        } catch (err) {
            console.error(`Error procesando folio ${folio}:`, err.message);
        }

        await page.close(); // cerrar la pestaña antes de pasar al siguiente folio
    }

    await browser.close();

    // Guardar resultados en JSON
    const jsonPath = `${OUTPUT_DIR}/resultados.json`;
    fs.writeFileSync(jsonPath, JSON.stringify(resultados, null, 2));
    console.log(`Datos guardados en ${jsonPath}`);
})();
