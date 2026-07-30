const axios = require('axios');
const {extractModel, extractSpec} = require('./../utils/transformhelper');

async function fetchData() {
  try{  
    let x = await axios.get(process.env.newLaptop_API,{
      params:{
        per_page:1,
        category:'laptop'
      }
    });
    const numOfProducts = x.headers['x-wp-total'];
    const numOfPages = Math.ceil((numOfProducts/100));
    let responses = [];

    for(let i = 1; i<= numOfPages; i++){
      const requests = await axios.get(process.env.newLaptop_API, {
        params:{
          per_page:100,
          page:i,
          category: "laptop"
        }
      })
      responses.push(...requests.data);
    }

    return responses; // data
  }catch(error){
      console.error('An error had been happen fetchind data from new-laptop.net')
      return [];
    }
}

function transform(item){
  return{
    brand:extractSpec(item,"الشركة المصنعة" ) ,
    model: extractModel(item.name) , 
    cpu: extractSpec(item,  "المعالج"),
    ram: extractSpec(item,  "ذاكرة"),
    hard: extractSpec(item,"سعة التخزين"),
    gpu: extractSpec(item,"كرت الشاشة"),
    new: Boolean(1),
    price: item.prices.price || null,
    source: "new-laptop",
};
}

module.exports = {fetchData, transform};