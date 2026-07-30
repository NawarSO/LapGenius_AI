const fs = require('fs');
const {Parser} = require('json2csv');

function saveJson(filepath, data){
    fs.writeFileSync(filepath, JSON.stringify(data, null, 2), 'utf-8');
}

function saveCSV(filepath, data){
    const parser = new Parser();
    const csv = parser.parse(data);
    fs.writeFileSync(filepath, csv, 'utf-8');
}

module.exports = {saveJson, saveCSV};
