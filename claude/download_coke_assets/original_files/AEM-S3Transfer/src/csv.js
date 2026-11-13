const fs = require("fs");
const { parse } = require("csv-parse");

function readCSV(filePath) {
  return new Promise((resolve, reject) => {
    const rows = [];
    fs.createReadStream(filePath)
      .pipe(
        parse({
          columns: true,
          trim: true,
          skip_empty_lines: true
        })
      )
      .on("data", (r) => rows.push(r))
      .on("end", () => resolve(rows))
      .on("error", reject);
  });
}

function findColumnCI(row, expectedName) {
  const keys = Object.keys(row);
  const expected = String(expectedName).trim().toLowerCase();
  return keys.find((k) => String(k).trim().toLowerCase() === expected) || null;
}

function findAuthorLinkColumn(row) {
  return findColumnCI(row, "AUTHOR LINK");
}

function findDamPathColumn(row) {
  return (
    findColumnCI(row, "DAM_PATH") ||
    findColumnCI(row, "CONTENT_PATH") ||
    findColumnCI(row, "AEM_PATH")
  );
}

module.exports = { readCSV, findAuthorLinkColumn, findDamPathColumn };
