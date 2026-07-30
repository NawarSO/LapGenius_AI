const {saveCSV,
    saveJson} = require("./utils/savers");

async function runAdapter(adapter){
  try{  
    const rowData = await adapter.fetchData();
    const transformedData = rowData.map(item => adapter.transform(item)).filter(Boolean);
    
    const cleanedData = transformedData.filter(item => {
        const price = Number(item.price);
      
        if (!Number.isFinite(price)) return false;
        if (price <= 0) return false;
        if (price > 100000) return false; 
      
        return true;
      });
       
      if (!cleanedData.length) {
        throw new Error("No valid data after filtering");
      }
    const source = cleanedData[0].source;
    saveJson(`./data/row/${source}.json`, rowData);
    saveJson(`./data/processed/${source}.json`, cleanedData);
    saveCSV(`./data/final/${source}.csv`, cleanedData) 
 
    return cleanedData;

    }catch(error){
        console.error('An error had been happen while fetching the data', error.message);
    }
}

module.exports = {runAdapter};



