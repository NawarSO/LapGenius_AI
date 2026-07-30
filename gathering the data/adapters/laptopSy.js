const axios = require('axios');

const {
    extractBrand,
    cleanHTML,
    extract,
    extractInline
} = require('./../utils/transformhelper.js');

async function fetchData(){
    try{
        const response = await axios.get(process.env.laptopSy, {
            params:{
                per_page:100,
                category:'apple,available,business,gaming,laptop,new,openbox'
            }
        })
        const data = response.data;
        const filtered = data.filter(item => {
            const categories = item.categories.map(c => c.slug.toLowerCase());
            return !categories.includes("pc");
          });
        return filtered;
    }catch(error){
        console.error('error fetch data from laptop.sy', error.message);
        return [];
    }
}


/////////////////////////////////////////////////////
  
    function transform(item){
    try{
      const text = cleanHTML(item.description);
  
      const lines = text
        .split("\n")
        .map(l => l.trim())
        .filter(Boolean);
  
      const cpu = extract(lines, "المعالج");
  
      const ram = extractInline(lines, "الرام");
  
      const hard = extractInline(lines, "الهارد");
  
      const gpu = extract(lines, "كرت الشاشة") || extract(lines, "كرتين شاشة") || extract(lines, "كرت شاشة") ;
  
      return {
        brand: extractBrand(item.name),
        model: item.name,
        cpu,
        ram,
        hard,
        gpu,
        new: item.categories?.some(c => c.slug.toLowerCase() === "new") || false,
        price: parseFloat(item.prices?.price) || null,
        source: "laptopSy",
      };
  
    }catch(error){
      console.error("Transform error:", error.message);
      return null;
    }
  }



module.exports = {fetchData, transform};