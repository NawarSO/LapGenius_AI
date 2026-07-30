const {extractSpec} = require("../utils/transformhelper.js");
const axios = require('axios');

async function fetchData() {
    try{
        const response = await axios.get(process.env.afandySpahy_API, {
            params:{
                "page":1,
                "per_page":100,
                "category":"brand-new-laptops,used-laptop"
            }
        })
        return response.data;
    }catch(error){
        console.error('An error had been happened while fetching Data from Alafandy & sbahi ...', error.message);
    }
};

function transform(item){
    try{
        const cpuS = [
            extractSpec(item, "المعالج") || extractSpec(item, "فئة المعالج"),
            extractSpec(item, "جيل المعالج") || extractSpec(item, "توصيف المعالج")
          ]
          .filter(Boolean)
          .join(" ");
        
          const hardS = [ extractSpec(item, "سعة التخزين"),extractSpec(item, "نوع التخزين")
          ]
          .filter(Boolean).join(" ")
          || extractSpec(item, "التخزين الداخلي")
          || null;

        const status = extractSpec(item, "حالة الجهاز")?.trim() || "";
        return{
            brand:extractSpec(item, "الماركة"),
            model:extractSpec(item, "الموديل") , 
            cpu:cpuS ,   
            ram: extractSpec(item, "سعة و نوع الذاكرة") || extractSpec(item, "الذاكرة"), // الذاكرة
            hard:hardS,
            gpu: extractSpec(item, "كرت الشاشة"),
            new: status === "جديد", 
            price: parseFloat(item.prices.price)/100 || null,
            source: "afandyAndSpahi"
        }
    }catch(error){
        console.error('An error had been happened while tranfoming the data...', error.message);
        return null;
    }
}




module.exports = {fetchData, transform};